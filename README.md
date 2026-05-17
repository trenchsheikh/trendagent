# Trend Agent

Trend Agent helps you plan a week of social media content for your business. You describe what you do — for example, a lash technician in Manchester — and the app looks up what people are actually searching for on Google right now. It then suggests trending topics, a post idea for each day Monday through Sunday, and rough times of day when posting tends to work well.

There is no paid subscription, no ChatGPT, and no fake “example” trends. The ideas are built from live Google Trends data whenever Google allows the lookup. If Google is busy or rate-limits the request, the app still returns a sensible plan based on your business words so the page never breaks.

---

## What you get

- **Trending topics** — real search phrases related to your niche  
- **A 7-day content plan** — one hook and one concrete post idea per weekday  
- **Best posting windows** — simple time ranges (morning, lunch, evening) to aim for  

Open the **index.html** page in your browser, type your business, and click generate. Keep the small server running in the background (see below) so the page can fetch results.

---

## What you need first

1. **A computer** running Windows, Mac, or Linux  
2. **Python 3.10** — download the installer from [python.org](https://www.python.org/downloads/). On Windows, during install, tick **“Add python.exe to PATH”** if you see that option.  
3. **An internet connection** — the app talks to Google Trends when you generate a plan  

You do not need a Google account or API keys for this project.

---

## How to run it (step by step)

### 1. Get the project on your computer

If you cloned or downloaded this folder from GitHub, open it in File Explorer (Windows) or Finder (Mac). You should see files such as **app.py**, **index.html**, and **requirements.txt** in the same folder.

### 2. Install the extra Python packages (one time)

Open a terminal in that folder:

- **Windows:** right-click the folder → “Open in Terminal”, or open Command Prompt / PowerShell, then use `cd` to go to the project folder.  
- **Mac:** right-click the folder → New Terminal at Folder, or open Terminal and `cd` into the folder.

Run this command (copy it exactly):

`py -3.10 -m pip install -r requirements.txt`

On Mac or Linux, if `py -3.10` does not work, try:

`python3 -m pip install -r requirements.txt`

Wait until it finishes without errors. You only need to do this once, or again if you delete Python or move to a new machine.

### 3. Start the server

In the same terminal, from the project folder, run:

`py -3.10 app.py`

On Mac or Linux, use `python3 app.py` if needed.

Leave this window open. You should see a message that the app is listening on port 5000. That means the backend is ready.

To check: open a browser and go to **http://localhost:5000/** — you should see a short JSON message saying the service is OK. You can close that tab; the main app is the HTML page.

### 4. Open the app in your browser

Double-click **index.html** in the project folder, or drag it into Chrome, Edge, Firefox, or Safari.

Type a short description of your business (city and niche help), submit the form, and wait a few seconds. The first request can take a little longer while Google Trends is queried.

---

## Tips for everyday use

- **Describe your business clearly** — e.g. “coffee shop in Austin” or “mobile dog groomer Leeds” works better than a single vague word.  
- **Keep the terminal running** while you use the website. Closing the terminal stops the server.  
- **If results say they are not “live”** — Google sometimes limits how often trends can be fetched. Wait about a minute and try again, or retry later. The plan will still be usable.  
- **Slow first load** — live trend lookups take a few seconds on purpose so Google does not block the app.  

---

## If something goes wrong

| What you see | What to try |
|---|---|
| “Module not found” or Flask missing | Run the install step again with the same Python you use to start **app.py** (`py -3.10` on Windows). |
| Page says it cannot connect | Make sure **app.py** is still running in the terminal and you did not close that window. |
| Port 5000 already in use | Another program is using that port. Close other dev tools, or change the port number at the bottom of **app.py** and use the new address in the browser. |
| Plan looks generic, not “live” | Google rate-limited the lookup. Wait 30–60 seconds and generate again. |
| `python` does not work on Windows | Use `py -3.10` for both install and run so Windows picks the right Python version. |

---

## How it works (in plain terms)

1. You describe your business in plain English.  
2. The app pulls out useful words and searches Google Trends for related topics and queries.  
3. It turns those real search phrases into seven days of hooks and post ideas, plus suggested posting times.  

No AI model writes the copy — templates and the trend text itself shape what you see. That keeps the tool simple, free, and tied to what people are actually searching for.

---

## Files in this project

| File | Purpose |
|---|---|
| **app.py** | The small server that fetches trends and builds your plan |
| **index.html** | The page you open in the browser |
| **requirements.txt** | List of Python libraries to install once |
| **README.md** | This guide |
