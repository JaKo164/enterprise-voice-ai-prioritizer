import io

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Enterprise Voice AI Prioritizer", layout="wide")

# ------------------------------
# Configuration
# ------------------------------
SCORE_COLUMNS = [
    "business_value",
    "implementation_effort",
    "data_readiness",
    "integration_complexity",
    "compliance_risk",
    "executive_sponsorship",
    "time_to_value",
]

FRIENDLY_LABELS = {
    "business_value": "Business Value",
    "implementation_effort": "Implementation Effort",
    "data_readiness": "Data Readiness",
    "integration_complexity": "Integration Complexity",
    "compliance_risk": "Compliance/Risk",
    "executive_sponsorship": "Executive Sponsorship",
    "time_to_value": "Time to Value",
}

# Weights sum to 1.0
WEIGHTS = {
    "business_value": 0.25,
    "implementation_effort": 0.15,
    "data_readiness": 0.15,
    "integration_complexity": 0.10,
    "compliance_risk": 0.10,
    "executive_sponsorship": 0.15,
    "time_to_value": 0.10,
}


# ------------------------------
# Helpers
# ------------------------------
def normalize_inverse(series: pd.Series) -> pd.Series:
    """
    Convert a 1-5 score where lower is better into a 1-5 positive score.
    Example: 1 -> 5, 5 -> 1
    """
    return 6 - series


def compute_scores(df: pd.DataFrame) -> pd.DataFrame:
    """Compute weighted priority and categorization fields."""
    clean = df.copy()

    # Ensure numeric and clamp to the scoring range
    for col in SCORE_COLUMNS:
        clean[col] = pd.to_numeric(clean[col], errors="coerce").fillna(3).clip(1, 5)

    # Invert negative dimensions so all normalized dimensions follow:
    # higher = better for prioritization
    normalized = pd.DataFrame(index=clean.index)
    normalized["business_value"] = clean["business_value"]
    normalized["implementation_effort"] = normalize_inverse(clean["implementation_effort"])
    normalized["data_readiness"] = clean["data_readiness"]
    normalized["integration_complexity"] = normalize_inverse(clean["integration_complexity"])
    normalized["compliance_risk"] = normalize_inverse(clean["compliance_risk"])
    normalized["executive_sponsorship"] = clean["executive_sponsorship"]
    normalized["time_to_value"] = normalize_inverse(clean["time_to_value"])

    clean["weighted_priority_score"] = (
        sum(normalized[c] * WEIGHTS[c] for c in SCORE_COLUMNS).round(2)
    )

    # A simple quick-win lens:
    # feasibility = easy effort, low complexity, lower risk, fast time-to-value, and data readiness
    clean["feasibility_score"] = (
        (
            normalized["implementation_effort"]
            + normalized["integration_complexity"]
            + normalized["compliance_risk"]
            + normalized["time_to_value"]
            + normalized["data_readiness"]
        )
        / 5
    ).round(2)

    # Strategic potential lens = value + sponsorship + readiness
    clean["strategic_potential"] = (
        (
            normalized["business_value"]
            + normalized["executive_sponsorship"]
            + normalized["data_readiness"]
        )
        / 3
    ).round(2)

    median_feasibility = clean["feasibility_score"].median()
    median_strategic = clean["strategic_potential"].median()

    def classify(row: pd.Series) -> str:
        if row["feasibility_score"] >= median_feasibility and row["strategic_potential"] >= median_strategic:
            return "Quick Win + Strategic"
        if row["feasibility_score"] >= median_feasibility:
            return "Quick Win"
        if row["strategic_potential"] >= median_strategic:
            return "Strategic Bet"
        return "Longer-Term Candidate"

    clean["portfolio_view"] = clean.apply(classify, axis=1)
    clean = clean.sort_values("weighted_priority_score", ascending=False).reset_index(drop=True)
    clean["rank"] = clean.index + 1

    return clean


# ------------------------------
# UI
# ------------------------------
st.title("Enterprise Voice AI Use-Case Prioritizer")
st.caption(
    "A lightweight decision-support tool for AI business owners and deployment strategists "
    "to compare voice/conversational AI opportunities."
)

st.markdown("### 1) Load and edit use cases")
st.write(
    "Score each use case from **1 (low)** to **5 (high)** for each dimension. "
    "For **effort, complexity, risk, and time to value**, lower raw scores are better and are automatically inverted in prioritization."
)

uploaded_file = st.file_uploader("Optional: upload a CSV to replace the sample", type=["csv"])

if uploaded_file is not None:
    input_df = pd.read_csv(uploaded_file)
else:
    input_df = pd.read_csv("sample_usecases.csv")

required_columns = ["use_case", *SCORE_COLUMNS]
missing_columns = [c for c in required_columns if c not in input_df.columns]

if missing_columns:
    st.error(
        "Your data is missing required columns: "
        + ", ".join(missing_columns)
        + ". Please follow the sample CSV format."
    )
    st.stop()

editable_df = st.data_editor(
    input_df[required_columns],
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True,
)

scored_df = compute_scores(editable_df)

st.markdown("### 2) Ranked use cases")
ranked_cols = [
    "rank",
    "use_case",
    "weighted_priority_score",
    "feasibility_score",
    "strategic_potential",
    "portfolio_view",
]
st.dataframe(scored_df[ranked_cols], use_container_width=True, hide_index=True)

st.markdown("### 3) Quick-win vs Strategic-bet view")
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(
    scored_df["feasibility_score"],
    scored_df["strategic_potential"],
)

for _, row in scored_df.iterrows():
    ax.annotate(
        row["use_case"],
        (row["feasibility_score"], row["strategic_potential"]),
        fontsize=8,
        alpha=0.85,
    )

ax.set_xlabel("Feasibility (higher means easier/faster/safer)")
ax.set_ylabel("Strategic Potential (higher means bigger strategic upside)")
ax.set_title("Use-Case Portfolio Map")
ax.grid(alpha=0.3)
st.pyplot(fig)

st.markdown("### 4) Download results")
csv_buffer = io.StringIO()
scored_df.to_csv(csv_buffer, index=False)
st.download_button(
    label="Download prioritized use cases as CSV",
    data=csv_buffer.getvalue(),
    file_name="prioritized_usecases.csv",
    mime="text/csv",
)

with st.expander("Scoring logic (short explanation)", expanded=True):
    st.markdown(
        """
- **Weighted Priority Score** combines all dimensions on a normalized 1–5 scale.
- Higher score means a better candidate for near-term enterprise investment.
- Dimensions where *lower is better* (effort, complexity, risk, time to value) are inverted automatically.
- **Quick-win vs strategic-bet** is shown on a 2D map:
  - **Feasibility** = how easy/safe/fast to deliver.
  - **Strategic Potential** = value + sponsorship + readiness.
        """
    )

st.info(
    "Tip: Use this in discovery workshops to align business, IT, and operations stakeholders on a transparent prioritization method."
)
