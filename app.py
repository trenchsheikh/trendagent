"""
Trend Agent - Flask server

Single endpoint:  POST /generate
Body:             { "business": "lash tech in Manchester" }

Pipeline:
  1. Extract keywords from the business description.
  2. Scrape Google Trends (via pytrends) for related topics + queries.
  3. Build the response purely from the scraped data - no AI, no APIs.
"""

import re
import time

from flask import Flask, request, jsonify
from flask_cors import CORS
from pytrends.request import TrendReq

app = Flask(__name__)
CORS(app)

# Words that carry no business meaning - dropped during keyword extraction.
STOPWORDS = {
    "a", "an", "the", "in", "on", "at", "of", "for", "to", "and", "or",
    "with", "near", "based", "my", "our", "your", "is", "are", "i", "we",
    "business", "company", "shop", "store", "service", "services",
}

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday",
        "Friday", "Saturday", "Sunday"]

BEST_TIMES = ["7am-9am", "12pm-1pm", "7pm-9pm"]


def extract_keywords(business):
    """Turn a free-text business description into a few search keywords.

    "lash tech in Manchester" -> ["lash tech in Manchester", "lash", "tech"]
    The full phrase (minus stopwords) is kept first because it usually
    matches a real niche on Google Trends; individual words act as
    broader fallbacks when the niche has too little search volume.
    """
    cleaned = re.sub(r"[^a-zA-Z0-9\s]", " ", business).lower()
    words = [w for w in cleaned.split() if w and w not in STOPWORDS]

    keywords = []
    phrase = " ".join(words).strip()
    if phrase:
        keywords.append(phrase)

    for w in words:
        if len(w) > 2 and w not in keywords:
            keywords.append(w)

    # pytrends accepts at most 5 terms per payload.
    return keywords[:5] or [business.strip().lower()]


def business_type(keywords):
    """Short human label for the business, e.g. 'lash tech'."""
    label = keywords[0] if keywords else "business"
    # Keep it to the first few words so templated copy stays tight.
    return " ".join(label.split()[:3])


def scrape_trends(keywords):
    """Scrape related topics + queries from Google Trends.

    Returns a de-duplicated, ranked list of trend strings. Google Trends
    is unauthenticated and rate-limited, so each keyword is tried in turn
    and failures are skipped rather than fatal.
    """
    pytrends = TrendReq(hl="en-US", tz=0)
    trends = []
    seen = set()

    def add(value):
        if not value:
            return
        v = str(value).strip()
        key = v.lower()
        if v and key not in seen and len(v) > 1:
            seen.add(key)
            trends.append(v)

    for kw in keywords:
        try:
            pytrends.build_payload([kw], timeframe="today 3-m")
        except Exception:
            time.sleep(1)
            continue

        # Related queries: people actively searching alongside this term.
        try:
            related_q = pytrends.related_queries()
            data = related_q.get(kw) or {}
            for bucket in ("rising", "top"):
                df = data.get(bucket)
                if df is not None and not df.empty:
                    for q in df["query"].tolist():
                        add(q)
        except Exception:
            pass

        # Related topics: broader themes around this term.
        try:
            related_t = pytrends.related_topics()
            data = related_t.get(kw) or {}
            for bucket in ("rising", "top"):
                df = data.get(bucket)
                if df is not None and not df.empty:
                    col = "topic_title" if "topic_title" in df else df.columns[0]
                    for t in df[col].tolist():
                        add(t)
        except Exception:
            pass

        # Be gentle with Google Trends to avoid 429s.
        time.sleep(1)

    return trends


def mock_trends(keywords, biz_type):
    """Keyword-driven fallback trends.

    Built from the *same* extracted keywords/business type the scraper
    uses, so the shape mirrors real Google Trends output. Used when the
    live scrape returns nothing (rate-limited) or when the caller asks
    for mock data explicitly.
    """
    base = biz_type
    primary = keywords[1] if len(keywords) > 1 else base.split()[0]
    return [
        f"best {base} near me",
        f"{base} prices 2026",
        f"{primary} trends tiktok",
        f"how to choose a {base}",
        f"{primary} before and after",
    ]


def build_content_plan(trends, biz_type):
    """7-day plan (Mon-Sun) where every hook + idea is built from a trend."""
    plan = []
    for i, day in enumerate(DAYS):
        trend = trends[i % len(trends)]
        # Trim the trend itself (not the whole hook) so the hook never
        # truncates mid-phrase. Cap at 6 words, then add a short suffix
        # that keeps the total punchy and under 10 words.
        short_trend = " ".join(trend.split()[:6])
        hook = f"{short_trend} is trending now"

        idea = (
            f"Show how your {biz_type} ties into '{trend}' - "
            f"film a quick before/after or tip your clients can use today."
        )
        plan.append({"day": day, "hook": hook, "idea": idea})
    return plan


@app.route("/generate", methods=["POST"])
def generate():
    body = request.get_json(silent=True) or {}
    business = (body.get("business") or "").strip()
    if not business:
        return jsonify({"error": "Missing 'business' in request body"}), 400

    keywords = extract_keywords(business)
    biz_type = business_type(keywords)

    # `"mock": true` in the body skips the (slow, rate-limited) scrape
    # entirely - handy for frontend dev. Otherwise scrape live and fall
    # back to mock only if Google returns nothing.
    force_mock = bool(body.get("mock"))
    if force_mock:
        trends, source = mock_trends(keywords, biz_type), "mock"
    else:
        trends = scrape_trends(keywords)
        if trends:
            source = "live"
        else:
            trends, source = mock_trends(keywords, biz_type), "mock"

    return jsonify({
        "trending": trends[:5],
        "contentPlan": build_content_plan(trends, biz_type),
        "bestTimes": BEST_TIMES,
        "source": source,
    })


@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "ok", "endpoint": "POST /generate"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
