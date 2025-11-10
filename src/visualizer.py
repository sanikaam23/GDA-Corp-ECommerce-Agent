import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def detect_chart_type(df: pd.DataFrame) -> str:
    """Automatically detect suitable chart type."""
    if df.empty or df.shape[1] < 2:
        return None

    x_col, y_col = df.columns[0], df.columns[1]

    # Detect time-series
    if any(keyword in x_col.lower() for keyword in ["date", "month", "year"]):
        return "line"

    # Detect categorical
    if df[x_col].nunique() <= 10 and df[y_col].dtype in ["int64", "float64"]:
        return "bar"

    # For small number of categories
    if df[x_col].nunique() <= 6:
        return "pie"

    return "bar"


def plot_chart(df: pd.DataFrame, chart_type: str):
    """Generate matplotlib chart."""
    if df.empty or df.shape[1] < 2:
        return None

    x_col, y_col = df.columns[0], df.columns[1]
    fig, ax = plt.subplots(figsize=(7, 4))

    if chart_type == "bar":
        ax.bar(df[x_col], df[y_col])
    elif chart_type == "line":
        ax.plot(df[x_col], df[y_col], marker="o")
    elif chart_type == "pie":
        ax.pie(df[y_col], labels=df[x_col], autopct="%1.1f%%")

    ax.set_title(f"{chart_type.capitalize()} Chart of {x_col} vs {y_col}")
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


def visualize_dataframe(df: pd.DataFrame, show_chart: bool = True):
    """Display dataframe and visualization in Streamlit."""
    if df is None or df.empty:
        st.info("No structured data found for visualization.")
        return

    st.markdown("### 📊 Table View:")
    st.dataframe(df)

    if show_chart:
        st.markdown("### 📈 Visualization:")
        chart_type = detect_chart_type(df)
        if chart_type:
            fig = plot_chart(df, chart_type)
            if fig:
                st.pyplot(fig)
        else:
            st.info("Could not determine suitable chart type.")
    else:
        st.caption("Chart visualization hidden by user preference.")
