import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


def detect_chart_type(df: pd.DataFrame) -> str:
    if df.empty or df.shape[1] < 2:
        return None

    x_col, y_col = df.columns[0], df.columns[1]

    
    if pd.api.types.is_datetime64_any_dtype(df[x_col]):
        return "line"

    if any(k in x_col.lower() for k in ["date", "time", "month", "year", "timestamp"]):
        return "line"


    if df[x_col].nunique() <= 6:
        return "pie"

    
    if df[x_col].nunique() <= 12:
        return "bar"


    return "bar"



def plot_chart(df: pd.DataFrame, chart_type: str):
    """Generate matplotlib chart with improved formatting."""
    if df.empty or df.shape[1] < 2:
        return None

    x_col, y_col = df.columns[0], df.columns[1]
    fig, ax = plt.subplots(figsize=(7, 4))

    if chart_type == "bar":
        ax.bar(df[x_col], df[y_col])
        ax.set_xticklabels(df[x_col], rotation=45, ha='right')

    elif chart_type == "line":
        ax.plot(df[x_col], df[y_col], marker="o")
        ax.set_xticklabels(df[x_col], rotation=45, ha='right')

    elif chart_type == "pie":
        wedges, texts, autotexts = ax.pie(
            df[y_col],
            labels=df[x_col],
            autopct="%1.1f%%",
            startangle=90,
            pctdistance=0.8,
            labeldistance=1.1,
            wedgeprops=dict(edgecolor='white')
        )

        
        for text in texts:
            text.set_fontsize(10)
        for autotext in autotexts:
            autotext.set_fontsize(9)

        ax.axis('equal')  

    ax.set_title(f"{chart_type.capitalize()} Chart of {x_col} vs {y_col}")
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
