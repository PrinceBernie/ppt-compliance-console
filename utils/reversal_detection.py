"""
Reversal detection and allocation dump cleaning utilities
"""
import pandas as pd
import re
import difflib
import config
from typing import Tuple, List, Dict


def detect_reversals(allocation_df: pd.DataFrame, batch_col: str = 'Batch number') -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Detect reversed transactions based on batch number pattern (ends with /1).
    
    Args:
        allocation_df: Allocation dump DataFrame
        batch_col: Name of the batch number column
        
    Returns:
        Tuple of (original_transactions, reversed_transactions)
    """
    df = allocation_df.copy()
    
    # Identify reversed transactions (batch number ends with /1)
    df['IS_REVERSAL'] = df[batch_col].astype(str).str.endswith('/1')
    
    reversed_txns = df[df['IS_REVERSAL']].copy()
    
    # Find original transactions by removing /1 from reversed batch numbers
    original_batch_numbers = []
    for batch in reversed_txns[batch_col]:
        if pd.notna(batch):
            original_batch = str(batch).replace('/1', '')
            original_batch_numbers.append(original_batch)
    
    # Find original transactions
    original_txns = df[df[batch_col].astype(str).isin(original_batch_numbers)].copy()
    
    return original_txns, reversed_txns


def remove_reversals(allocation_df: pd.DataFrame, batch_col: str = 'Batch number') -> Tuple[pd.DataFrame, int, int]:
    """
    Remove both original and reversed transactions from allocation dump.
    
    Args:
        allocation_df: Allocation dump DataFrame
        batch_col: Name of the batch number column
        
    Returns:
        Tuple of (cleaned_df, num_originals_removed, num_reversals_removed)
    """
    original_txns, reversed_txns = detect_reversals(allocation_df, batch_col)
    
    # Get indices to remove
    indices_to_remove = set(original_txns.index.tolist() + reversed_txns.index.tolist())
    
    # Remove both original and reversed transactions
    cleaned_df = allocation_df.drop(index=list(indices_to_remove))
    
    num_originals = len(original_txns)
    num_reversals = len(reversed_txns)
    
    return cleaned_df, num_originals, num_reversals


def remove_withdrawals(allocation_df: pd.DataFrame, reference_col: str = 'Reference') -> Tuple[pd.DataFrame, int]:
    """
    Remove all records with 'withdrawal' in the Reference column.
    
    Args:
        allocation_df: Allocation dump DataFrame
        reference_col: Name of the reference column
        
    Returns:
        Tuple of (cleaned_df, num_withdrawals_removed)
    """
    df = allocation_df.copy()
    
    # Case-insensitive search for 'withdrawal'
    withdrawal_mask = df[reference_col].astype(str).str.lower().str.contains('withdrawal', na=False)
    
    num_withdrawals = withdrawal_mask.sum()
    
    # Remove withdrawal records
    cleaned_df = df[~withdrawal_mask]
    
    return cleaned_df, num_withdrawals


def clean_reference_field(allocation_df: pd.DataFrame, reference_col: str = 'Reference') -> pd.DataFrame:
    """
    Clean reference field by removing 'Payment for ' prefix.
    
    Args:
        allocation_df: Allocation dump DataFrame
        reference_col: Name of the reference column
        
    Returns:
        DataFrame with cleaned reference column
    """
    df = allocation_df.copy()
    
    # Remove 'Payment for ', 'Contribution for', etc. (case-insensitive)
    # Handles: payment for, payments for, contribution for, contributions for
    df[reference_col + '_CLEAN'] = df[reference_col].astype(str).str.replace(
        r'(?:payment|contribution)s?\s+for\s+',
        '',
        case=False,
        regex=True
    ).str.strip()

    # Apply spelling correction to the cleaned reference
    # We apply this to the cleaned column to avoid expensive operations on full text
    df[reference_col + '_CLEAN'] = df[reference_col + '_CLEAN'].apply(lambda x: correct_month_spelling(x))
    
    return df


def clean_allocation_dump(
    allocation_df: pd.DataFrame,
    batch_col: str = 'Batch number',
    reference_col: str = 'Reference'
) -> Tuple[pd.DataFrame, Dict]:
    """
    Complete cleaning pipeline for allocation dump:
    1. Remove withdrawals
    2. Remove reversals (both original and reversed)
    3. Clean reference field
    
    Args:
        allocation_df: Raw allocation dump DataFrame
        batch_col: Name of the batch number column
        reference_col: Name of the reference column
        
    Returns:
        Tuple of (cleaned_df, cleaning_stats)
    """
    stats = {}
    
    # Step 1: Remove withdrawals
    df_no_withdrawals, num_withdrawals = remove_withdrawals(allocation_df, reference_col)
    stats['withdrawals_removed'] = num_withdrawals
    
    # Step 2: Remove reversals
    df_no_reversals, num_originals, num_reversals = remove_reversals(df_no_withdrawals, batch_col)
    stats['original_transactions_removed'] = num_originals
    stats['reversed_transactions_removed'] = num_reversals
    
    # Step 3: Clean reference field
    df_cleaned = clean_reference_field(df_no_reversals, reference_col)
    
    stats['total_records_input'] = len(allocation_df)
    stats['total_records_output'] = len(df_cleaned)
    stats['total_records_removed'] = len(allocation_df) - len(df_cleaned)
    
    return df_cleaned, stats


def correct_month_spelling(text: str, month_list: List[str] = None) -> str:
    """
    Correct misspelled month names in text using fuzzy matching.
    
    Args:
        text: Input text string
        month_list: List of correct month names
        
    Returns:
        Text with corrected month names
    """
    if month_list is None:
        month_list = config.MONTH_NAMES
        
    if pd.isna(text) or text == '':
        return text
        
    text_str = str(text)
    words = text_str.split()
    corrected_words = []
    
    for word in words:
        # Check if match found
        matches = difflib.get_close_matches(word.title(), month_list, n=1, cutoff=0.7)
        if matches:
            corrected_words.append(matches[0])
        else:
            corrected_words.append(word)
            
    return ' '.join(corrected_words)
