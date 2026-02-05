"""
Data cleaning and normalization utilities
"""
import re
import pandas as pd
from typing import Optional


def clean_contact(contact: Optional[str]) -> str:
    """
    Remove all non-alphanumeric characters from contact numbers.
    Also replaces '0' values with empty string (placeholder data).
    
    Args:
        contact: Raw contact number string
        
    Returns:
        Cleaned contact number with only alphanumeric characters, or empty string
    """
    if pd.isna(contact) or contact is None:
        return ""
    
    # Convert to string and remove all non-alphanumeric characters
    cleaned = re.sub(r'[^A-Za-z0-9]', '', str(contact))
    cleaned = cleaned.strip()
    
    # Replace '0' with empty string (placeholder/invalid data)
    if cleaned == '0':
        return ""
    
    return cleaned


def clean_id(id_value: Optional[str]) -> str:
    """
    Remove all non-alphanumeric characters from ID numbers (SSNIT, Ghana Card).
    Also replaces '0' values with empty string (placeholder data).
    
    Args:
        id_value: Raw ID number string
        
    Returns:
        Cleaned ID number with only alphanumeric characters, or empty string
    """
    if pd.isna(id_value) or id_value is None:
        return ""
    
    # Convert to string and remove all non-alphanumeric characters
    cleaned = re.sub(r'[^A-Za-z0-9]', '', str(id_value))
    cleaned = cleaned.strip().upper()
    
    # Replace '0' with empty string (placeholder/invalid data)
    if cleaned == '0':
        return ""
    
    return cleaned


def concat_name(row: pd.Series, first_col: str, middle_col: str, last_col: str) -> str:
    """
    Concatenate first, middle, and last name columns into a single full name.
    
    Args:
        row: DataFrame row
        first_col: Column name for first name
        middle_col: Column name for middle name
        last_col: Column name for last name
        
    Returns:
        Full name as a single string
    """
    parts = []
    
    # Add first name
    if first_col in row.index and not pd.isna(row[first_col]):
        parts.append(str(row[first_col]).strip())
    
    # Add middle name
    if middle_col in row.index and not pd.isna(row[middle_col]):
        parts.append(str(row[middle_col]).strip())
    
    # Add last name
    if last_col in row.index and not pd.isna(row[last_col]):
        parts.append(str(row[last_col]).strip())
    
    return ' '.join(parts)


def normalize_text(text: Optional[str]) -> str:
    """
    Normalize text for matching: lowercase, strip whitespace, remove extra spaces.
    
    Args:
        text: Raw text string
        
    Returns:
        Normalized text
    """
    if pd.isna(text) or text is None:
        return ""
    
    # Convert to string, lowercase, strip, and remove extra spaces
    normalized = str(text).lower().strip()
    normalized = re.sub(r'\s+', ' ', normalized)
    return normalized


def normalize_name(name: Optional[str]) -> str:
    """
    Normalize name for matching: lowercase, strip, remove extra spaces, and SORT alphabetically.
    Sorting improves matching by handling different name orderings.
    
    Example:
        "John Ashley Miles" -> "ashley john miles"
        "Miles John Ashley" -> "ashley john miles"
    
    Args:
        name: Raw name string
        
    Returns:
        Normalized and sorted name
    """
    if pd.isna(name) or name is None:
        return ""
    
    # Convert to string, lowercase, strip
    normalized = str(name).lower().strip()
    
    # Remove extra spaces
    normalized = re.sub(r'\s+', ' ', normalized)
    
    # Split into parts and sort alphabetically
    name_parts = normalized.split()
    name_parts.sort()
    
    # Join back together
    return ' '.join(name_parts)


def clean_dataframe_columns(df: pd.DataFrame, column_mapping: dict) -> pd.DataFrame:
    """
    Clean and normalize all relevant columns in a DataFrame.
    
    Args:
        df: Input DataFrame
        column_mapping: Dictionary mapping column purposes to column names
        
    Returns:
        DataFrame with cleaned columns
    """
    df_clean = df.copy()
    
    # Clean contact columns
    if 'contact' in column_mapping and column_mapping['contact'] in df_clean.columns:
        df_clean[column_mapping['contact'] + '_CLEAN'] = df_clean[column_mapping['contact']].apply(clean_contact)
    
    if 'mobile' in column_mapping and column_mapping['mobile'] in df_clean.columns:
        df_clean[column_mapping['mobile'] + '_CLEAN'] = df_clean[column_mapping['mobile']].apply(clean_contact)
    
    # Clean ID columns
    if 'ssnit_number' in column_mapping and column_mapping['ssnit_number'] in df_clean.columns:
        df_clean[column_mapping['ssnit_number'] + '_CLEAN'] = df_clean[column_mapping['ssnit_number']].apply(clean_id)
    
    if 'gh_card_number' in column_mapping and column_mapping['gh_card_number'] in df_clean.columns:
        df_clean[column_mapping['gh_card_number'] + '_CLEAN'] = df_clean[column_mapping['gh_card_number']].apply(clean_id)
    
    if 'ssnit' in column_mapping and column_mapping['ssnit'] in df_clean.columns:
        df_clean[column_mapping['ssnit'] + '_CLEAN'] = df_clean[column_mapping['ssnit']].apply(clean_id)
    
    if 'id_number' in column_mapping and column_mapping['id_number'] in df_clean.columns:
        df_clean[column_mapping['id_number'] + '_CLEAN'] = df_clean[column_mapping['id_number']].apply(clean_id)
    
    return df_clean


def parse_date(value: Optional[str]) -> Optional[pd.Timestamp]:
    """
    Parse date from various formats, handling 'Jan 25' as Jan 2025.
    Returns: A pandas Timestamp normalized to the 1st of the month, or None.
    """
    if pd.isna(value) or str(value).strip() == '':
        return None
        
    s = str(value).strip()
    
    # Handle "Jan 25" or "Jan-25" (Month YY)
    # Regex for 3+ letters, space/dash, 2 digits
    match = re.match(r'^([A-Za-z]{3,})[\s-]?(\d{2})$', s)
    if match:
        month_str, year_str = match.groups()
        try:
            # Assume 20xx for now as this is current suspense data
            return pd.to_datetime(f"{month_str} 20{year_str}").replace(day=1)
        except:
            pass
            
    # Try standard pandas parsing
    try:
        dt = pd.to_datetime(s, errors='coerce')
        if pd.notna(dt):
            # If the year is very small (e.g. 0025), it might be valid in some contexts but not here
            # But pd.to_datetime often fails on year 25 out of bounds, so we catch exception usually.
            # However, if it parsed "Jan 25" as Jan 25th current year, we might want to be careful.
            # But the user said "Jan 25" = "01/01/2025".
            
            # If input was "Jan 25" and pd.to_datetime returns Jan 25th 2026 (current year),
            # that is WRONG for the user's intent (Jan 2025).
            # The regex above should catch "Jan 25" first.
            
            return dt.replace(day=1)
    except:
        pass
        
    return None

