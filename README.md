# enterprise-voice-ai-prioritizer

A lightweight Streamlit app for enterprise teams to prioritize voice AI and conversational AI opportunities using a transparent, workshop-friendly scoring model.

## Problem this tool solves

Enterprise teams often have many promising AI ideas, but struggle to decide what to build first. Discussions can become subjective, with business, IT, and compliance stakeholders using different criteria.

This tool creates a shared prioritization framework so teams can quickly compare use cases and align on where to invest.

## Target user

- AI business owner
- AI deployment strategist
- Digital transformation lead
- Product or operations leaders running AI discovery workshops

## Example enterprise use cases

- Multilingual customer support voice agent
- Appointment booking assistant
- Sales call summarization
- Training content voice localization
- Internal knowledge voice assistant
- Proactive service follow-up calls

(Additional examples are included in `sample_usecases.csv`.)

## How scoring works

Each use case is scored from 1 to 5 on:

- Business value
- Implementation effort
- Data readiness
- Integration complexity
- Compliance/risk
- Executive sponsorship
- Time to value

The app then:

1. Applies weighted scoring to calculate a **weighted priority score**.
2. Normalizes dimensions where lower is better (effort, complexity, risk, time to value).
3. Produces a **quick-win vs strategic-bet** view using feasibility and strategic potential indicators.

See full details in [`scoring_logic.md`](scoring_logic.md).

## Why this is useful in AI discovery/prioritization workshops

- Creates a common language across business, IT, and risk stakeholders
- Makes trade-offs explicit instead of implicit
- Helps distinguish fast pilots from longer-horizon strategic bets
- Produces a ranked list that can feed roadmap and investment decisions

## Setup instructions

### 1) Create and activate an environment (Python 3.11)

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Run the app

```bash
streamlit run app.py
```

The app opens in your browser and loads `sample_usecases.csv` by default.

## Screenshot

> Add a screenshot of the running app here after launching locally.

![App screenshot placeholder](docs/screenshot-placeholder.png)


## Troubleshooting: new files do not appear on GitHub

If you created files locally but cannot see them in your GitHub repository:

1. Confirm the files are tracked in git:
   ```bash
   git ls-files
   ```
2. Confirm you are on the expected branch:
   ```bash
   git branch --show-current
   ```
3. Ensure you committed changes:
   ```bash
   git log --oneline -n 5
   ```
4. Add your GitHub remote (if missing) and push:
   ```bash
   git remote add origin <your-repo-url>
   git push -u origin <your-branch>
   ```

In this environment, files are committed locally on branch `work`. They will only appear in GitHub after pushing to a configured remote.
