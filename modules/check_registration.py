"""
Check Registration Module - RUN 1
Matches suspense data against member dump to populate scheme numbers
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from utils.data_cleaning import concat_name, normalize_text
from utils.matching import find_member_match
from components.file_uploader import upload_file, display_dataframe_preview, download_button
import config


@st.cache_data(show_spinner=False)
def load_and_prepare_member_dump(df: pd.DataFrame, scheme_filter: str) -> pd.DataFrame:
    """
    Load and prepare member dump with caching for performance.
    Includes ID normalization and name concatenation.
    
    Args:
        df: Raw member dump DataFrame
        scheme_filter: Selected scheme to filter by
        
    Returns:
        Prepared and filtered member dump
    """
    from utils.data_cleaning import clean_id
    
    # Filter by scheme
    scheme_col = config.MEMBER_DUMP_COLUMNS['scheme_name']
    df_filtered = df[df[scheme_col] == scheme_filter].copy()
    
    # Normalize SSNIT and ID number columns
    if config.MEMBER_DUMP_COLUMNS['ssnit'] in df_filtered.columns:
        df_filtered[config.MEMBER_DUMP_COLUMNS['ssnit']] = df_filtered[config.MEMBER_DUMP_COLUMNS['ssnit']].apply(clean_id)
    
    if config.MEMBER_DUMP_COLUMNS['id_number'] in df_filtered.columns:
        df_filtered[config.MEMBER_DUMP_COLUMNS['id_number']] = df_filtered[config.MEMBER_DUMP_COLUMNS['id_number']].apply(clean_id)
    
    # Concatenate name columns
    df_filtered['FULL_NAME'] = df_filtered.apply(
        lambda row: concat_name(
            row,
            config.MEMBER_DUMP_COLUMNS['first_name'],
            config.MEMBER_DUMP_COLUMNS['middle_name'],
            config.MEMBER_DUMP_COLUMNS['last_name']
        ),
        axis=1
    )
    
    return df_filtered


def run_check_registration():
    """
    Main function for Check Registration module.
    """
    st.title("✅ Check Registration")
    st.markdown("Match suspense data against member dump to identify registered members.")
    
    st.markdown("---")
    
    # File uploads
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 Suspense Data")
        suspense_df = upload_file(
            label="Upload Suspense Data",
            key="suspense_upload_reg",
            help_text="Excel or CSV file with suspense contribution data",
            required_columns=[
                config.SUSPENSE_COLUMNS['employer'],
                config.SUSPENSE_COLUMNS['member_name'],
                config.SUSPENSE_COLUMNS['contact'],
                config.SUSPENSE_COLUMNS['ssnit_number'],
                config.SUSPENSE_COLUMNS['gh_card_number']
            ]
        )
    
    with col2:
        st.subheader("👥 Member Dump")
        member_dump_df = upload_file(
            label="Upload Member Dump",
            key="member_dump_upload",
            help_text="Excel or CSV file with system member data (will be cached)",
            required_columns=[
                config.MEMBER_DUMP_COLUMNS['first_name'],
                config.MEMBER_DUMP_COLUMNS['scheme_name'],
                config.MEMBER_DUMP_COLUMNS['mobile'],
                config.MEMBER_DUMP_COLUMNS['ssnit'],
                config.MEMBER_DUMP_COLUMNS['id_number'],
                config.MEMBER_DUMP_COLUMNS['group_name']
            ]
        )
    
    # Check if both files are uploaded
    if suspense_df is None or member_dump_df is None:
        st.info("👆 Please upload both files to continue")
        return
    
    st.markdown("---")
    
    # Scheme filter
    st.subheader("🔍 Filter Settings")
    scheme_col = config.MEMBER_DUMP_COLUMNS['scheme_name']
    available_schemes = sorted(member_dump_df[scheme_col].dropna().unique().tolist())
    
    if not available_schemes:
        st.error("❌ No schemes found in member dump")
        return
    
    selected_scheme = st.selectbox(
        "Select Scheme Type",
        options=available_schemes,
        help="Filter member dump by scheme type for matching"
    )
    
    st.markdown("---")
    
    # Run matching
    if st.button("🚀 Run Registration Check", type="primary", use_container_width=True):
        with st.spinner("Processing... This may take a few minutes for large datasets."):
            
            # STEP 1: Clean and normalize suspense data
            st.info("🧹 Step 1: Cleaning and normalizing suspense data...")
            
            # Clear existing scheme numbers (ensure fresh start)
            if config.SUSPENSE_COLUMNS['scheme_number'] in suspense_df.columns:
                suspense_df[config.SUSPENSE_COLUMNS['scheme_number']] = ""
            
            # Normalize SSNIT and Ghana Card columns (remove special characters, keep only alphanumeric)
            from utils.data_cleaning import clean_id
            
            if config.SUSPENSE_COLUMNS['ssnit_number'] in suspense_df.columns:
                suspense_df[config.SUSPENSE_COLUMNS['ssnit_number']] = suspense_df[config.SUSPENSE_COLUMNS['ssnit_number']].apply(clean_id)
            
            if config.SUSPENSE_COLUMNS['gh_card_number'] in suspense_df.columns:
                suspense_df[config.SUSPENSE_COLUMNS['gh_card_number']] = suspense_df[config.SUSPENSE_COLUMNS['gh_card_number']].apply(clean_id)
            
            st.success("✅ Data cleaning completed")
            
            # STEP 2: Prepare member dump
            st.info(f"📊 Step 2: Preparing member dump for scheme: {selected_scheme}")
            
            # Prepare member dump
            member_df_prepared = load_and_prepare_member_dump(member_dump_df, selected_scheme)
            
            st.success(f"✅ Matching against {len(member_df_prepared):,} members in scheme: {selected_scheme}")
            
            # Initialize result columns
            suspense_df['SCHEME NUMBER'] = ""
            suspense_df['MATCHED NAME'] = ""
            suspense_df['MATCH STATUS'] = config.MATCH_STATUS['no_match']
            suspense_df['MATCH SIMILARITY'] = 0.0
            
            # Matching configuration
            matching_config = {
                'suspense_contact_col': config.SUSPENSE_COLUMNS['contact'],
                'suspense_name_col': config.SUSPENSE_COLUMNS['member_name'],
                'suspense_ssnit_col': config.SUSPENSE_COLUMNS['ssnit_number'],
                'suspense_gh_card_col': config.SUSPENSE_COLUMNS['gh_card_number'],
                'suspense_employer_col': config.SUSPENSE_COLUMNS['employer'],
                'member_contact_col': config.MEMBER_DUMP_COLUMNS['mobile'],
                'member_name_col': 'FULL_NAME',
                'member_ssnit_col': config.MEMBER_DUMP_COLUMNS['ssnit'],
                'member_id_col': config.MEMBER_DUMP_COLUMNS['id_number'],
                'member_employer_col': config.MEMBER_DUMP_COLUMNS['group_name'],
                'threshold_contact': config.FUZZY_THRESHOLD_CONTACT_ID,
                'threshold_id': config.FUZZY_THRESHOLD_CONTACT_ID,
                'threshold_name_employer': config.FUZZY_THRESHOLD_NAME_EMPLOYER
            }
            
            # STEP 3: Run matching process
            st.info("🔄 Step 3: Running three-tier matching process...")
            
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            tier1_matches = 0
            tier2_matches = 0
            tier3_matches = 0
            no_matches = 0
            
            # Process each suspense record
            total_records = len(suspense_df)
            for idx, row in suspense_df.iterrows():
                # Update progress
                progress = (idx + 1) / total_records
                progress_bar.progress(progress)
                status_text.text(f"Processing record {idx + 1} of {total_records:,}...")
                
                # Find match
                match_result = find_member_match(row, member_df_prepared, matching_config)
                
                if match_result:
                    matched_row = match_result['matched_row']
                    match_type = match_result['match_type']
                    
                    # Populate scheme number
                    scheme_number = matched_row.get(config.MEMBER_DUMP_COLUMNS['scheme_number'], '')
                    suspense_df.at[idx, 'SCHEME NUMBER'] = scheme_number
                    
                    # Populate matched name
                    suspense_df.at[idx, 'MATCHED NAME'] = matched_row.get('FULL_NAME', '')
                    
                    # Set match status
                    if match_type == 'tier1':
                        suspense_df.at[idx, 'MATCH STATUS'] = config.MATCH_STATUS['tier1']
                        tier1_matches += 1
                    elif match_type == 'tier2':
                        suspense_df.at[idx, 'MATCH STATUS'] = config.MATCH_STATUS['tier2']
                        tier2_matches += 1
                    elif match_type == 'tier3':
                        suspense_df.at[idx, 'MATCH STATUS'] = config.MATCH_STATUS['tier3']
                        tier3_matches += 1
                    
                    # Set similarity score
                    suspense_df.at[idx, 'MATCH SIMILARITY'] = match_result['similarity']
                else:
                    no_matches += 1
            
            progress_bar.empty()
            status_text.empty()
            
            # Display results
            st.success("✅ Matching completed!")
            
            st.markdown("---")
            st.subheader("📊 Match Statistics")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Tier 1 Matches", tier1_matches, help="Contact & Name matches")
            with col2:
                st.metric("Tier 2 Matches", tier2_matches, help="ID Number matches")
            with col3:
                st.metric("Tier 3 Matches", tier3_matches, help="Name & Employer matches")
            with col4:
                st.metric("No Matches", no_matches, delta=f"-{no_matches/total_records*100:.1f}%")
            
            total_matches = tier1_matches + tier2_matches + tier3_matches
            match_rate = (total_matches / total_records * 100) if total_records > 0 else 0
            
            st.info(f"📈 Overall Match Rate: {match_rate:.1f}% ({total_matches:,} of {total_records:,} records)")
            
            # Preview results
            st.markdown("---")
            display_dataframe_preview(suspense_df, "Results Preview", max_rows=20)
            
            # Download button
            st.markdown("---")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"suspense_registration_check_{selected_scheme}_{timestamp}.xlsx"
            
            download_button(suspense_df, filename, "📥 Download Registration Check Results")
            
            # Store in session state for next module
            st.session_state['registration_results'] = suspense_df
            st.session_state['selected_scheme'] = selected_scheme
