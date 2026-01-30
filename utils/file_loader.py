"""
Utility functions for loading cached files
"""
import pandas as pd
import streamlit as st
from pathlib import Path
import config


@st.cache_data(show_spinner=False)
def load_cached_member_dump() -> pd.DataFrame:
    """
    Load the cached member dump from the project files directory.
    
    Returns:
        DataFrame with member dump data
        
    Raises:
        FileNotFoundError: If the Members.xlsx file is not found
    """
    # Path to the cached member dump
    file_path = Path(__file__).parent.parent / "files" / "Members.xlsx"
    
    if not file_path.exists():
        raise FileNotFoundError(
            f"Member dump file not found at: {file_path}\n"
            f"Please ensure Members.xlsx is placed in the 'files' directory."
        )
    
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        raise Exception(f"Error reading cached member dump: {str(e)}")


def validate_whitelist_columns(df: pd.DataFrame) -> bool:
    """
    Validate that the whitelist file has all required columns.
    
    Args:
        df: Whitelist DataFrame to validate
        
    Returns:
        True if valid, False otherwise
    """
    required_columns = [
        'Current Employer',
        'Member Name [Schedule]',
        'Member Name [System]',
        'Scheme Number',
        'Previous Employer',
        'SSNIT Number',
        'Ghana Card',
        'Contact'
    ]
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        st.error(f"❌ Whitelist file is missing required columns: {', '.join(missing_columns)}")
        with st.expander("📋 Available columns in uploaded whitelist"):
            st.write(df.columns.tolist())
        return False
    
    return True
