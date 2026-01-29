"""
Reusable file uploader component with validation
"""
import streamlit as st
import pandas as pd
from typing import Optional, List, Tuple


def upload_file(
    label: str,
    key: str,
    help_text: str = None,
    required_columns: List[str] = None,
    file_types: List[str] = None
) -> Optional[pd.DataFrame]:
    """
    File uploader component with validation.
    
    Args:
        label: Label for the file uploader
        key: Unique key for the uploader
        help_text: Help text to display
        required_columns: List of required column names
        file_types: List of allowed file extensions
        
    Returns:
        DataFrame if file is valid, None otherwise
    """
    if file_types is None:
        file_types = ['xlsx', 'xls', 'csv']
    
    uploaded_file = st.file_uploader(
        label,
        type=file_types,
        key=key,
        help=help_text
    )
    
    if uploaded_file is None:
        return None
    
    try:
        # Read file based on extension
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # Validate required columns
        if required_columns:
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                st.error(f"❌ Missing required columns: {', '.join(missing_columns)}")
                with st.expander("📋 Available columns in uploaded file"):
                    st.write(df.columns.tolist())
                return None
        
        # Display success message
        st.success(f"✅ File loaded successfully: {len(df):,} records")
        
        return df
        
    except Exception as e:
        st.error(f"❌ Error reading file: {str(e)}")
        return None


def display_dataframe_preview(df: pd.DataFrame, title: str = "Data Preview", max_rows: int = 10):
    """
    Display a preview of a DataFrame with statistics.
    
    Args:
        df: DataFrame to preview
        title: Title for the preview section
        max_rows: Maximum number of rows to display
    """
    st.subheader(title)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Records", f"{len(df):,}")
    with col2:
        st.metric("Total Columns", len(df.columns))
    with col3:
        st.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
    
    st.dataframe(df.head(max_rows), use_container_width=True)
    
    if len(df) > max_rows:
        st.caption(f"Showing first {max_rows} of {len(df):,} records")


def download_button(df: pd.DataFrame, filename: str, button_label: str = "📥 Download Results"):
    """
    Create a download button for a DataFrame.
    
    Args:
        df: DataFrame to download
        filename: Name for the downloaded file
        button_label: Label for the download button
    """
    # Convert to Excel
    from io import BytesIO
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Results')
    
    excel_data = output.getvalue()
    
    st.download_button(
        label=button_label,
        data=excel_data,
        file_name=filename,
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
