"""Gradio frontend for the Stock Picker Crew — deploy to Hugging Face Spaces."""

import json
import os
import sys
import warnings
from datetime import datetime
from pathlib import Path

import gradio as gr
from dotenv import load_dotenv

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

from stock_picker.crew import StockPicker  # noqa: E402

load_dotenv(ROOT / ".env")

SECTORS = [
    "Technology",
    "Healthcare",
    "Energy",
    "Finance",
    "Consumer",
    "Industrials",
    "Real Estate",
]


def _read_text(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def _read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"raw": path.read_text(encoding="utf-8")}


def _check_api_keys() -> str | None:
    google_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    serper_key = os.getenv("SERPER_API_KEY")

    if not google_key:
        return "Missing `GOOGLE_API_KEY` or `GEMINI_API_KEY`. Add it in Settings → Secrets on Hugging Face."
    if not serper_key:
        return "Missing `SERPER_API_KEY`. Get a free key at https://serper.dev and add it as a Space secret."
    return None


def run_stock_picker(sector: str) -> tuple[str, dict, dict, str]:
    error = _check_api_keys()
    if error:
        return f"### Configuration error\n\n{error}", {}, {}, error

    os.makedirs(ROOT / "output", exist_ok=True)
    os.makedirs(ROOT / "memory", exist_ok=True)

    inputs = {
        "sector": sector,
        "current_date": str(datetime.now()),
    }

    try:
        result = StockPicker().crew().kickoff(inputs=inputs)
        decision = _read_text(ROOT / "output" / "decision.md") or result.raw
        trending = _read_json(ROOT / "output" / "trending_companies.json")
        research = _read_json(ROOT / "output" / "research_report.json")
        status = f"Completed analysis for **{sector}** at {datetime.now():%Y-%m-%d %H:%M}."
        return decision, trending, research, status
    except Exception as exc:
        message = f"### Run failed\n\n`{exc}`"
        return message, {}, {}, str(exc)


def build_ui() -> gr.Blocks:
    with gr.Blocks(title="Stock Picker Crew") as demo:
        gr.Markdown(
            """
            # Stock Picker Crew
            Multi-agent AI crew that finds trending companies, researches them, and picks the best investment.

            **Note:** A full run takes several minutes and uses Gemini + Serper API credits.
            """
        )

        with gr.Row():
            sector = gr.Dropdown(SECTORS, value="Technology", label="Sector")
            run_btn = gr.Button("Run Stock Picker", variant="primary")

        status = gr.Textbox(label="Status", interactive=False)
        decision = gr.Markdown(label="Final decision")

        with gr.Accordion("Trending companies (JSON)", open=False):
            trending = gr.JSON(label="Trending companies")

        with gr.Accordion("Research report (JSON)", open=False):
            research = gr.JSON(label="Research report")

        run_btn.click(
            fn=run_stock_picker,
            inputs=[sector],
            outputs=[decision, trending, research, status],
        )

       

    return demo


if __name__ == "__main__":
    demo = build_ui()
    demo.launch(theme=gr.themes.Soft())
