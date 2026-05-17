# Trend Agent

**Your niche. This week’s Google searches. A full content plan — in seconds.**

Trend Agent is for creators, shop owners, and side hustlers who are tired of staring at a blank caption box. Tell it what you do — *“lash tech in Manchester”*, *“mobile barber in Atlanta”*, *“vegan bakery Portland”* — and it pulls **real, live** topics from Google Trends, then maps them onto **Monday through Sunday** with hooks, post ideas, and when to publish.

No monthly fee. No ChatGPT bill. No fake “trending” placeholders. When Google cooperates, every hook is tied to something people are actually searching for right now. When Google throttles requests, you still get a usable plan built from your own words — the app never leaves you on a dead screen.

---

## What lands in your lap

| You get | Why it matters |
|---|---|
| **Trending topics** | Real search phrases in your space — not guesses |
| **7-day content plan** | One hook + one concrete post idea per day |
| **Best posting windows** | Morning, lunch, and evening slots to aim for |

Open **index.html** in your browser, describe your business, hit generate. Keep the small Python server running in the background (takes two minutes to set up once) and you’re live.

---

## Under the hood (the stack, in human terms)

This project is deliberately small and honest: a browser UI, a lightweight API, and a direct line to Google Trends. Nothing exotic — just tools that do one job well.

| Technology | What it does here |
|---|---|
| **Python 3.10** | Runs the whole backend — keyword cleanup, trend fetching, plan building |
| **Flask** | Powers the web server and the `/generate` endpoint your browser talks to |
| **flask-cors** | Lets the frontend call the API from your machine without browser security headaches |
| **pytrends** | Talks to Google Trends and brings back related queries and topics |
| **pandas** | Sorts and shapes the raw trend data into clean lists |
| **HTML, CSS & JavaScript** | The dark, single-page UI in **index.html** — no React build step, no npm install |

**Philosophy:** scrape real data, template smart copy, ship fast. No LLM in the loop means no API keys, no hallucinated trends, and no surprise invoices.

---

## What you need before you start

1. **A laptop or desktop** — Windows, Mac, or Linux  
2. **Python 3.10** — grab it from [python.org](https://www.python.org/downloads/). On Windows, check **“Add python.exe to PATH”** during install if you see it  
3. **Wi‑Fi** — live lookups need the internet; everything else runs locally on your machine  

You do **not** need a Google Cloud account, OpenAI key, or credit card.

---

## Get running in four steps

### 1. Open the project folder

Clone or download this repo from GitHub, then open the folder. You should see **app.py**, **index.html**, and **requirements.txt** sitting together.

### 2. Install dependencies (one time)

Open a terminal inside that folder:

- **Windows:** right-click the folder → **Open in Terminal**, or open PowerShell and `cd` into the folder  
- **Mac:** right-click → **New Terminal at Folder**, or `cd` into the folder from Terminal  

Run:

`py -3.10 -m pip install -r requirements.txt`

On Mac/Linux, if that fails, try:

`python3 -m pip install -r requirements.txt`

That pulls in Flask, pytrends, pandas, and the rest. Wait until it finishes — you only do this once per machine.

### 3. Start the server

From the same folder:

`py -3.10 app.py`

(Mac/Linux: `python3 app.py` if needed.)

**Leave this window open.** When you see that the app is listening on port **5000**, the backend is ready. Quick sanity check: visit **http://localhost:5000/** in a browser — a short “status ok” message means Flask is humming.

### 4. Open the app and generate

Double-click **index.html** (or drag it into Chrome, Edge, Firefox, or Safari). Type your business with a bit of location and niche detail, submit, and give it a few seconds — the first live scrape is always the slowest.

---

## Tips that actually help

- **Be specific.** “Coffee shop Shoreditch” beats “coffee” every time.  
- **Keep the terminal open** while you use the site — closing it kills Flask.  
- **Seeing “mock” instead of “live”?** Google rate-limited you. Wait 30–60 seconds and try again; your plan is still usable in the meantime.  
- **First request feels slow?** Normal. The app paces requests so Google doesn’t ban the IP.  

---

## When something breaks

| What you see | What to try |
|---|---|
| “Module not found” / Flask missing | Re-run the install step with the **same** Python you use to start **app.py** (`py -3.10` on Windows). |
| Page can’t connect | Confirm **app.py** is still running in the terminal. |
| Port 5000 already in use | Close other dev tools, or change the port at the bottom of **app.py**. |
| Results feel generic | Google throttled the scrape — wait a minute and regenerate. |
| `python` won’t run on Windows | Stick with `py -3.10` for **both** install and run so Windows uses one interpreter. |

---

## The pipeline (60-second version)

1. **You** describe the business in plain English.  
2. **Python** strips noise words and builds a handful of search terms.  
3. **pytrends** hits Google Trends for related queries and topics.  
4. **pandas** ranks and deduplicates what comes back.  
5. **Flask** serves a JSON plan — trends, seven days of hooks/ideas, posting times.  
6. **The browser** renders it in a clean weekly layout.

Templates turn trend text into captions — not an AI model. That’s the trade-off: predictable, free, and grounded in real search behavior.

---

## Project files

| File | Role |
|---|---|
| **app.py** | Flask server + trend logic |
| **index.html** | Frontend you open in the browser |
| **requirements.txt** | Python packages to install |
| **README.md** | You are here |

---

Built for people who post for a living — powered by Python, Flask, and whatever the internet is searching for today.
