# 📈 Trend Agent

Turn any business description into a 7-day content plan built from **real,
live Google Trends data** — no AI, no paid APIs, no mock data. Just real
trends scraped on demand.

> Input: `"lash tech in Manchester"` → Output: real trending topics + a
> Monday–Sunday content plan + best posting times.

---

## 🧰 Tech Stack

| Technology | Role |
|---|---|
| **Python 3.10+** | Language |
| **Flask** | Web server / REST endpoint |
| **flask-cors** | CORS enabled for all origins (frontend can call it directly) |
| **pytrends** | Scrapes live Google Trends (related queries + topics) |
| **pandas** | Parses the trend data returned by pytrends |

---

## 🚀 Quick Start

```powershell
# 1. Install dependencies
py -3.10 -m pip install -r requirements.txt

# 2. Run the server
py -3.10 app.py
```

That's it. The server is now live at **http://localhost:5000**.

> **Why `py -3.10` and not `python`?** This project is tested on Python
> 3.10. If your `python` command points at a different interpreter (e.g. an
> MSYS2 / Microsoft Store Python), `python app.py` will fail with
> `ModuleNotFoundError: No module named 'flask'` because the packages were
> installed for a *different* Python. Using `py -3.10` guarantees the same
> interpreter for install **and** run. On macOS/Linux, use `python3` for
> both commands instead.

> **Tip:** check it's alive by opening <http://localhost:5000/> in a browser —
> you should see `{"status": "ok", "endpoint": "POST /generate"}`.

---

## 📡 API

### `POST /generate`

**Request**

```json
{ "business": "lash tech in Manchester" }
```

**Try it with curl**

```bash
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d "{\"business\": \"lash tech in Manchester\"}"
```

**Response** (real example from a live run)

```json
{
  "trending": [
    "maybelline lash stiletto ultimate length mascara",
    "clinique chubby lash fattening mascara",
    "billion dollar beauty forever lash mascara",
    "maybelline great lash waterproof mascara",
    "lancome lash idole curl goddess mascara"
  ],
  "contentPlan": [
    {
      "day": "Monday",
      "hook": "maybelline lash stiletto ultimate length is trending now",
      "idea": "Show how your lash tech ties into 'maybelline lash stiletto ultimate length mascara' - film a quick before/after or tip your clients can use today."
    }
  ],
  "bestTimes": ["7am-9am", "12pm-1pm", "7pm-9pm"]
}
```

`contentPlan` always returns **7 entries, Monday → Sunday**. Every `hook`
and `idea` is built from a real scraped trend; hooks are kept under 10 words.

**Errors**

| Status | When |
|---|---|
| `400` | `business` field missing or empty |
| `502` | Google Trends returned no data (usually rate-limiting — retry shortly) |

---

## ⚙️ How It Works

1. **Extract keywords** — the business string is cleaned, stopwords and
   filler are removed, and the resulting phrase + key words become search
   terms (max 5 — pytrends' per-payload limit).
2. **Scrape Google Trends** — `pytrends` pulls `related_queries` (rising +
   top) and `related_topics` for each keyword, de-duplicated and ranked.
   Requests are paced (1s) to stay under Google's rate limit.
3. **Build the response** — scraped trends populate `trending`, and each
   day's hook/idea is templated from a real trend + the detected business
   type. No AI, no external APIs anywhere in the pipeline.

---

## 🩹 Troubleshooting

| Symptom | Cause & Fix |
|---|---|
| `502` "try again shortly" | Google Trends is rate-limiting (HTTP 429). Wait ~30–60s and retry — it's Google throttling, not a bug. |
| Request takes a few seconds | Expected. Each call scrapes multiple keywords with deliberate 1s pacing to avoid bans. |
| `Port 5000 in use` | Another app holds port 5000. Edit the last line of `app.py` (`port=5000`) to a free port. |
| Frontend can't reach it | CORS is already open for all origins — make sure you're calling `http://localhost:5000/generate` with method `POST` and `Content-Type: application/json`. |
