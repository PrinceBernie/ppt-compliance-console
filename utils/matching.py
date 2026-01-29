"""
Fuzzy matching utilities for member reconciliation
"""
import pandas as pd
from rapidfuzz import fuzz
from typing import Optional, Tuple, Dict
from utils.data_cleaning import normalize_text, clean_contact, clean_id, normalize_name


def fuzzy_match_name(name1: str, name2: str, threshold: float = 0.7) -> Tuple[bool, float]:
    """
    Perform fuzzy matching between two names with alphabetical sorting.
    Names are sorted alphabetically to handle different orderings.
    
    Example:
        "John Ashley Miles" vs "Miles John Ashley" -> High similarity
    
    Args:
        name1: First name to compare
        name2: Second name to compare
        threshold: Minimum similarity score (0-1) to consider a match
        
    Returns:
        Tuple of (is_match, similarity_score)
    """
    if not name1 or not name2:
        return False, 0.0
    
    # Normalize both names (includes alphabetical sorting)
    norm_name1 = normalize_name(name1)
    norm_name2 = normalize_name(name2)
    
    # Calculate similarity using token sort ratio (handles word order differences)
    similarity = fuzz.token_sort_ratio(norm_name1, norm_name2) / 100.0
    
    is_match = similarity >= threshold
    return is_match, similarity


def match_by_contact(
    suspense_row: pd.Series,
    member_df: pd.DataFrame,
    suspense_contact_col: str,
    suspense_name_col: str,
    member_contact_col: str,
    member_name_col: str,
    threshold: float = 0.7
) -> Optional[Dict]:
    """
    Tier 1: Match by contact number with fuzzy name verification.
    
    Args:
        suspense_row: Row from suspense DataFrame
        member_df: Member dump DataFrame
        suspense_contact_col: Contact column name in suspense data
        suspense_name_col: Name column name in suspense data
        member_contact_col: Contact column name in member dump
        member_name_col: Name column name in member dump
        threshold: Fuzzy matching threshold
        
    Returns:
        Dictionary with match details or None if no match
    """
    suspense_contact = clean_contact(suspense_row.get(suspense_contact_col))
    suspense_name = suspense_row.get(suspense_name_col, "")
    
    if not suspense_contact:
        return None
    
    # Find members with matching contact
    member_df_clean = member_df.copy()
    member_df_clean['CONTACT_CLEAN'] = member_df_clean[member_contact_col].apply(clean_contact)
    
    matching_contacts = member_df_clean[member_df_clean['CONTACT_CLEAN'] == suspense_contact]
    
    if matching_contacts.empty:
        return None
    
    # Verify with fuzzy name matching
    for idx, member_row in matching_contacts.iterrows():
        member_name = member_row.get(member_name_col, "")
        is_match, similarity = fuzzy_match_name(suspense_name, member_name, threshold)
        
        if is_match:
            return {
                'match_type': 'tier1',
                'matched_row': member_row,
                'similarity': similarity,
                'match_field': 'Contact & Name'
            }
    
    return None


def match_by_id(
    suspense_row: pd.Series,
    member_df: pd.DataFrame,
    suspense_ssnit_col: str,
    suspense_gh_card_col: str,
    suspense_name_col: str,
    member_ssnit_col: str,
    member_id_col: str,
    member_name_col: str,
    threshold: float = 0.7
) -> Optional[Dict]:
    """
    Tier 2: Bidirectional ID matching (SSNIT <-> Ghana Card) with fuzzy name verification.
    
    Args:
        suspense_row: Row from suspense DataFrame
        member_df: Member dump DataFrame
        suspense_ssnit_col: SSNIT column in suspense data
        suspense_gh_card_col: Ghana Card column in suspense data
        suspense_name_col: Name column in suspense data
        member_ssnit_col: SSNIT column in member dump
        member_id_col: ID number column in member dump
        member_name_col: Name column in member dump
        threshold: Fuzzy matching threshold
        
    Returns:
        Dictionary with match details or None if no match
    """
    suspense_ssnit = clean_id(suspense_row.get(suspense_ssnit_col))
    suspense_gh_card = clean_id(suspense_row.get(suspense_gh_card_col))
    suspense_name = suspense_row.get(suspense_name_col, "")
    
    if not suspense_ssnit and not suspense_gh_card:
        return None
    
    # Clean member dump IDs
    member_df_clean = member_df.copy()
    member_df_clean['SSNIT_CLEAN'] = member_df_clean[member_ssnit_col].apply(clean_id)
    member_df_clean['ID_CLEAN'] = member_df_clean[member_id_col].apply(clean_id)
    
    # Bidirectional matching
    matches = pd.DataFrame()
    
    # Match 1: Suspense SSNIT -> Member SSNIT
    if suspense_ssnit:
        match1 = member_df_clean[member_df_clean['SSNIT_CLEAN'] == suspense_ssnit]
        matches = pd.concat([matches, match1])
    
    # Match 2: Suspense SSNIT -> Member ID
    if suspense_ssnit:
        match2 = member_df_clean[member_df_clean['ID_CLEAN'] == suspense_ssnit]
        matches = pd.concat([matches, match2])
    
    # Match 3: Suspense Ghana Card -> Member SSNIT
    if suspense_gh_card:
        match3 = member_df_clean[member_df_clean['SSNIT_CLEAN'] == suspense_gh_card]
        matches = pd.concat([matches, match3])
    
    # Match 4: Suspense Ghana Card -> Member ID
    if suspense_gh_card:
        match4 = member_df_clean[member_df_clean['ID_CLEAN'] == suspense_gh_card]
        matches = pd.concat([matches, match4])
    
    matches = matches.drop_duplicates()
    
    if matches.empty:
        return None
    
    # Verify with fuzzy name matching
    for idx, member_row in matches.iterrows():
        member_name = member_row.get(member_name_col, "")
        is_match, similarity = fuzzy_match_name(suspense_name, member_name, threshold)
        
        if is_match:
            return {
                'match_type': 'tier2',
                'matched_row': member_row,
                'similarity': similarity,
                'match_field': 'ID Number'
            }
    
    return None


def match_by_name_employer(
    suspense_row: pd.Series,
    member_df: pd.DataFrame,
    suspense_name_col: str,
    suspense_employer_col: str,
    member_name_col: str,
    member_employer_col: str,
    threshold: float = 0.8
) -> Optional[Dict]:
    """
    Tier 3: Match by name within the same employer group.
    
    Args:
        suspense_row: Row from suspense DataFrame
        member_df: Member dump DataFrame
        suspense_name_col: Name column in suspense data
        suspense_employer_col: Employer column in suspense data
        member_name_col: Name column in member dump
        member_employer_col: Employer/Group column in member dump
        threshold: Fuzzy matching threshold (higher for this tier)
        
    Returns:
        Dictionary with match details or None if no match
    """
    suspense_name = suspense_row.get(suspense_name_col, "")
    suspense_employer = normalize_text(suspense_row.get(suspense_employer_col, ""))
    
    if not suspense_name or not suspense_employer:
        return None
    
    # Filter member dump to same employer
    member_df_clean = member_df.copy()
    member_df_clean['EMPLOYER_CLEAN'] = member_df_clean[member_employer_col].apply(normalize_text)
    
    same_employer = member_df_clean[member_df_clean['EMPLOYER_CLEAN'] == suspense_employer]
    
    if same_employer.empty:
        return None
    
    # Find best name match within employer
    best_match = None
    best_similarity = 0.0
    
    for idx, member_row in same_employer.iterrows():
        member_name = member_row.get(member_name_col, "")
        is_match, similarity = fuzzy_match_name(suspense_name, member_name, threshold)
        
        if is_match and similarity > best_similarity:
            best_similarity = similarity
            best_match = member_row
    
    if best_match is not None:
        return {
            'match_type': 'tier3',
            'matched_row': best_match,
            'similarity': best_similarity,
            'match_field': 'Name & Employer'
        }
    
    return None


def find_member_match(
    suspense_row: pd.Series,
    member_df: pd.DataFrame,
    config: Dict
) -> Optional[Dict]:
    """
    Orchestrate three-tier fallback matching logic.
    
    Args:
        suspense_row: Row from suspense DataFrame
        member_df: Member dump DataFrame
        config: Configuration dictionary with column mappings and thresholds
        
    Returns:
        Dictionary with match details or None if no match found
    """
    # Tier 1: Contact matching
    tier1_match = match_by_contact(
        suspense_row,
        member_df,
        config['suspense_contact_col'],
        config['suspense_name_col'],
        config['member_contact_col'],
        config['member_name_col'],
        config['threshold_contact']
    )
    
    if tier1_match:
        return tier1_match
    
    # Tier 2: ID matching
    tier2_match = match_by_id(
        suspense_row,
        member_df,
        config['suspense_ssnit_col'],
        config['suspense_gh_card_col'],
        config['suspense_name_col'],
        config['member_ssnit_col'],
        config['member_id_col'],
        config['member_name_col'],
        config['threshold_id']
    )
    
    if tier2_match:
        return tier2_match
    
    # Tier 3: Name + Employer matching
    tier3_match = match_by_name_employer(
        suspense_row,
        member_df,
        config['suspense_name_col'],
        config['suspense_employer_col'],
        config['member_name_col'],
        config['member_employer_col'],
        config['threshold_name_employer']
    )
    
    return tier3_match
