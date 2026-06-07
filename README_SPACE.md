---
title: Stock Picker Crew
emoji: 📈
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 5.22.0
app_file: app.py
pinned: false
license: mit
---

# Stock Picker Crew

Multi-agent CrewAI app that finds trending companies in a sector, researches them, and recommends the best investment.

## Required secrets

Add these in your Space **Settings → Secrets**:

| Secret | Description |
|--------|-------------|
| `GOOGLE_API_KEY` | Google AI / Gemini API key |
| `SERPER_API_KEY` | Web search key from [serper.dev](https://serper.dev) |

Optional: `PUSHOVER_USER` and `PUSHOVER_TOKEN` for push notifications.

## Deploy steps

1. Create a new Space at [huggingface.co/new-space](https://huggingface.co/new-space) with **Gradio** SDK.
2. Upload this `stock_picker` folder (or push via git).
3. Copy this file's YAML frontmatter to the top of `README.md` in the Space repo.
4. Add the secrets above.
5. Wait for the build to finish, then open the Space.

## Local preview

```bash
cd stock_picker
uv sync
cp .env.example .env   # add your keys
uv run python app.py
```
