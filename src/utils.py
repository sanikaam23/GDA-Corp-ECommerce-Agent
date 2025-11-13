import matplotlib.pyplot as plt
import pandas as pd
import io
import base64
import streamlit as st
from typing import Optional, Tuple


def generate_plot_from_data(df: pd.DataFrame, title: str) -> Optional[io.BytesIO]:
    """
    Generates a simple horizontal bar plot from a DataFrame suitable for categorical data
    and returns it as a BytesIO object (in-memory image).

    This function assumes the input DataFrame (df) has been cleaned and returned 
    by the Text-to-SQL agent, typically having two columns:
    1. Label/Category (e.g., 'Category Name')
    2. Value (e.g., 'Total Sales')

    Args:
        df: DataFrame containing the data to plot (at least 2 columns).
        title: Title for the chart.

    Returns:
        A BytesIO object containing the PNG image data, or None if plotting fails.
    """
    if df.empty or len(df.columns) < 2:
        return None

    try:
      
        df.columns = ['Label', 'Value']
        
    
        df = df.sort_values('Value', ascending=False)
        
   
        plt.figure(figsize=(10, 6))
        
   
        plt.barh(df['Label'], df['Value'], color='teal')
        
        plt.title(title, fontsize=14, fontweight='bold')
        plt.xlabel(df.columns[1].replace('_', ' ').title(), fontsize=12)
        plt.ylabel(df.columns[0].replace('_', ' ').title(), fontsize=12)
        
     
        plt.grid(axis='x', linestyle='--', alpha=0.6)
        
        plt.tight_layout()
        
 
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close() 
        buf.seek(0)
        return buf
    
    except Exception as e:
        print(f"Error generating plot: {e}")
        return None


