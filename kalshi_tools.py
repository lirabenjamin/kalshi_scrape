from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, Any, Tuple
import pandas as pd
import re
from edsl import QuestionFreeText, Survey, Model
# ------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------
DATA_PATH = Path("data") / "kalshi_filtered.csv"
DEFAULT_PANEL = pd.read_csv(DATA_PATH)
DEFAULT_PANEL['resolution_criteria'] = DEFAULT_PANEL['rules_primary'].fillna('') + ' ' + DEFAULT_PANEL['rules_secondary'].fillna('')
DEFAULT_PANEL['resolution_criteria'] = DEFAULT_PANEL['resolution_criteria'].str.strip()

sbr_nrc = '''You are an expert superforecaster, familiar with the work of Philip Tetlock.

Event title: {event_title}
Title: {title}
Subtitle: {subtitle}
Possible outcomes: Yes (1) or No (0)
Resolution criteria: {rules}
Scheduled close date: {expiration_time}
(Note: The question may resolve before this date.)

Instructions:
Please provide a single best estimate of the base rate for the event occurring.

Output your answer as a valid JSON object with exactly the following fields:
- "reasoning": A brief explanation of how the base rate estimate was derived.
- "base_rate": A single numeric value between 0 and 1, inclusive.

Your final output must be a JSON object and must include no other text outside of the JSON.
'''

mbr_nrc = '''
You are an expert superforecaster, familiar with the work of Philip Tetlock.

Event title: {event_title}
Title: {title}
Subtitle: {subtitle}
Possible outcomes: Yes (1) or No (0)
Resolution criteria: {rules}
Scheduled close date: {expiration_time}
(Note: The question may resolve before this date.)

Instructions:
Please provide multiple strong candidate estimates of the base rate for the event occurring.

Output your answer as a valid JSON object with exactly the following fields:
- "reasoning": A brief explanation of how the base rate estimates were derived.
- "base_rates": An array of numeric values between 0 and 1, inclusive.

Your final output must be a JSON object and must include no other text outside of the JSON.
'''
cbr_nrc = '''
You are an expert superforecaster, familiar with the work of Philip Tetlock.

Event title: {event_title}
Title: {title}
Subtitle: {subtitle}
Possible outcomes: Yes (1) or No (0)
Resolution criteria: {rules}
Scheduled close date: {expiration_time}
(Note: The question may resolve before this date.)

Instructions:
1. Please provide multiple strong candidate estimates of the base rate for the event occurring.
2. Compare and evaluate the different base rate estimates, and select the one you judge to be most appropriate and useful for this forecasting task.

Output your answer as a valid JSON object with exactly the following fields:
- "reasoning": A brief explanation of how the base rate estimates were derived and evaluated.
- "base_rates": An array of numeric values between 0 and 1, inclusive.
- "selected_base_rate": A single numeric value between 0 and 1, inclusive.

Your final output must be a JSON object and must include no other text outside of the JSON.
'''
sbr_src  = '''You are an expert superforecaster, familiar with the work of Philip Tetlock.

Event title: {event_title}
Title: {title}
Subtitle: {subtitle}
Possible outcomes: Yes (1) or No (0)
Resolution criteria: {rules}
Scheduled close date: {expiration_time}
(Note: The question may resolve before this date.)

Instructions:
1. Identify a single best reference class that would be most appropriate for generating base rates for this question.
2. For this reference class, please provide a single best estimate of the base rate for the event within this reference class.

Output your answer as a valid JSON object with exactly the following fields:
- "reasoning": A brief explanation of how the reference class and the base rate estimate were derived.
- "reference_class": A clear and concise description of the chosen reference class.
- "base_rate": A single numeric value between 0 and 1, inclusive.

Your final output must be a JSON object and must include no other text outside of the JSON.
'''
mbr_src = '''
You are an expert superforecaster, familiar with the work of Philip Tetlock.

Event title: {event_title}
Title: {title}
Subtitle: {subtitle}
Possible outcomes: Yes (1) or No (0)
Resolution criteria: {rules}
Scheduled close date: {expiration_time}
(Note: The question may resolve before this date.)

Instructions:
1. Identify a single best reference class that would be most appropriate for generating base rates for this question.
2. For this reference class, please provide multiple strong candidate estimates of the base rate for the event within this reference class.

Output your answer as a valid JSON object with exactly the following fields:
- "reasoning": A brief explanation of how the reference class and the base rate estimates were derived.
- "reference_class": A clear and concise description of the chosen reference class.
- "base_rates": An array of numeric values between 0 and 1, inclusive.

Your final output must be a JSON object and must include no other text outside of the JSON.
'''
cbr_src = '''You are an expert superforecaster, familiar with the work of Philip Tetlock.

Event title: {event_title}
Title: {title}
Subtitle: {subtitle}
Possible outcomes: Yes (1) or No (0)
Resolution criteria: {rules}
Scheduled close date: {expiration_time}
(Note: The question may resolve before this date.)

Instructions:
1. Identify a single best reference class that would be most appropriate for generating base rates for this question.
2. For this reference class, please provide multiple strong candidate estimates of the base rate for the event within this reference class.
3. Compare and evaluate the different base rate estimates, and select the one you judge to be most appropriate and useful for this forecasting task.


Output your answer as a valid JSON object with exactly the following fields:
- "reasoning": A brief explanation of how the reference class and the base rate estimates were derived and evaluated.
- "reference_class": A clear and concise description of the chosen reference class.
- "base_rates": An array of numeric values between 0 and 1, inclusive.
- "selected_base_rate": A single numeric value between 0 and 1, inclusive.

Your final output must be a JSON object and must include no other text outside of the JSON.
'''
sbr_mrc = '''You are an expert superforecaster, familiar with the work of Philip Tetlock.

Event title: {event_title}
Title: {title}
Subtitle: {subtitle}
Possible outcomes: Yes (1) or No (0)
Resolution criteria: {rules}
Scheduled close date: {expiration_time}
(Note: The question may resolve before this date.)

Instructions:
1. Identify multiple strong candidate reference classes that would be appropriate for generating base rates for this question.
2. For each of these reference classes, please provide a single best estimate of the base rate for the event within this reference class.
3. Compare and evaluate the different base rate estimates, and select the one you judge to be most appropriate and useful for this forecasting task.

Output your answer as a valid JSON object with exactly the following fields:
- "reasoning": A brief explanation of how the reference classes and the base rate estimates were derived and evaluated.
- "reference_classes": An array of strings, where each string is a clear and concise description of a reference class.
- "base_rates": An array of numeric values between 0 and 1, inclusive. Each base rate estimate should correspond to a reference class.
- "selected_base_rate": A single numeric value between 0 and 1, inclusive.

Your final output must be a JSON object and must include no other text outside of the JSON.
'''
mbr_mrc = '''You are an expert superforecaster, familiar with the work of Philip Tetlock.

Event title: {event_title}
Title: {title}
Subtitle: {subtitle}
Possible outcomes: Yes (1) or No (0)
Resolution criteria: {rules}
Scheduled close date: {expiration_time}
(Note: The question may resolve before this date.)

Instructions:
1. Identify multiple strong candidate reference classes that would be appropriate for generating base rates for this question.
2. For each of these reference classes, please provide multiple strong candidate estimates of the base rate for the event within this reference class.

Output your answer as a valid JSON object with exactly the following fields:
- "reasoning": A brief explanation of how the reference classes and the base rate estimates were derived.

- "reference_classes": An array of strings, where each string is a clear and concise description of a reference class.
- "base_rates": A 2-dimensional array of numeric values between 0 and 1, inclusive. Each sub-array should correspond to a reference class and contain its base rate estimates.
'''
cbr_mrc = '''You are an expert superforecaster, familiar with the work of Philip Tetlock.

Event title: {event_title}
Title: {title}
Subtitle: {subtitle}
Possible outcomes: Yes (1) or No (0)
Resolution criteria: {rules}
Scheduled close date: {expiration_time}
(Note: The question may resolve before this date.)

Instructions:
1. Identify multiple strong candidate reference classes that would be appropriate for generating base rates for this question.
2. For each of these reference classes, please provide multiple strong candidate estimates of the base rate for the event within this reference class.
3. Compare and evaluate the different base rate estimates, and select the one you judge to be most appropriate and useful for this forecasting task.

Output your answer as a valid JSON object with exactly the following fields:
- "reasoning": A brief explanation of how the reference classes and the base rate estimates were derived and evaluated.
- "reference_classes": An array of strings, where each string is a clear and concise description of a reference class.
- "base_rates": A 2-dimensional array of numeric values between 0 and 1, inclusive. Each sub-array should correspond to a reference class and contain its base rate estimates.
- "selected_base_rate": A single numeric value between 0 and 1, inclusive.

Your final output must be a JSON object and must include no other text outside of the JSON.
'''

# The giant prompt strings must exist in the global namespace
# (import or define them before importing this helper).
TEMPLATES: Dict[str, str] = {
    "sbr_nrc": sbr_nrc,
    "mbr_nrc": mbr_nrc,
    "cbr_nrc": cbr_nrc,
    "sbr_src": sbr_src,
    "mbr_src": mbr_src,
    "cbr_src": cbr_src,
    "sbr_mrc": sbr_mrc,
    "mbr_mrc": mbr_mrc,
    "cbr_mrc": cbr_mrc,
}


# ════════════════════════════════════════════════════════════════
# Helper functions
# ════════════════════════════════════════════════════════════════

def _resolve_args(arg1, arg2) -> Tuple[str, pd.DataFrame]:
    """Accept (ticker, df) OR (df, ticker) and normalise."""
    if isinstance(arg1, str):
        ticker = arg1
        df = arg2 if isinstance(arg2, pd.DataFrame) else DEFAULT_PANEL
    elif isinstance(arg1, pd.DataFrame):
        if not isinstance(arg2, str):
            raise TypeError("Expected ticker as the second argument.")
        ticker, df = arg2, arg1
    else:
        raise TypeError("First arg must be ticker str or pandas DataFrame.")
    return ticker, df


def _row_for_ticker(ticker: str, df: pd.DataFrame) -> pd.Series:
    filtered = df.loc[df["ticker"] == ticker]
    if filtered.empty:
        raise ValueError(f"Ticker '{ticker}' not found (rows: {len(df)}).")
    return filtered.iloc[0]

def _strip_markdown_fence(raw: str) -> str:
    """Remove ```json / ``` fences if present and trim whitespace."""
    clean = raw.strip()
    if clean.startswith("```"):
        # Remove opening fence with optional language tag
        clean = re.sub(r"^```[^\n]*\n", "", clean)
        # Remove closing fence (last ``` on its own line)
        clean = re.sub(r"\n```\s*$", "", clean)
    return clean.strip()


def _safe_json_loads(raw: str) -> Dict[str, Any]:
    """Parse JSON safely, handling markdown‑fenced blocks and errors."""
    if not isinstance(raw, str) or not raw.strip():
        return {"error": "empty_response"}

    cleaned = _strip_markdown_fence(raw)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {"error": "json_parse_error", "raw": cleaned[:150]}

def _run_single_template(row: pd.Series, template_name: str, model_name: str) -> Dict[str, Any]:
    tpl = TEMPLATES[template_name]
    prompt_text = tpl.format(
        event_title=row.get("event_title", ""),
        title=row.get("title", ""),
        subtitle=row.get("subtitle", ""),
        rules=row["resolution_criteria"],
        expiration_time=row["expiration_time"],
    )
    survey = Survey([QuestionFreeText(question_name=template_name, question_text=prompt_text)])
    results = survey.by(Model(model_name)).run()
    answer_str = results.to_pandas(remove_prefix=True).loc[0, template_name]
    answer_dict = _safe_json_loads(answer_str)
    return {f"{template_name}__{k}": v for k, v in answer_dict.items()}

# ════════════════════════════════════════════════════════════════
# Public API
# ════════════════════════════════════════════════════════════════

def get_edsl_table(arg1, arg2=None, *, model_name: str = "gpt-4o") -> pd.DataFrame:
    ticker, df = _resolve_args(arg1, arg2)
    row = _row_for_ticker(ticker, df)
    record: Dict[str, Any] = {"ticker": ticker, "model": model_name}
    for name in TEMPLATES:
        record.update(_run_single_template(row, name, model_name))
    return pd.DataFrame([record])

row = _row_for_ticker("ARCTICICEMIN-24OCT01-T4.2", DEFAULT_PANEL)
_run_single_template(row, "sbr_mrc", 'gpt-4o')


def print_edsl_table(df: pd.DataFrame, max_col_width: int = 120) -> None:
    pd.set_option("display.max_colwidth", max_col_width)
    pd.set_option("display.max_columns", None)
    print(df.fillna("" if isinstance(df, pd.DataFrame) else df).to_string(index=False))
    pd.reset_option("display.max_colwidth")
    pd.reset_option("display.max_columns")

# ════════════════════════════════════════════════════════════════
# CLI test stub
# ════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    tbl = get_edsl_table("ARCTICICEMIN-24OCT01-T4.2")
    print_edsl_table(tbl)
