"""
Check Credits Module - RUN 2
Checks if members have already been credited for their contributions
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from utils.reversal_detection import clean_allocation_dump
from utils.data_cleaning import normalize_text
from components.file_uploader import upload_file, display_dataframe_preview, download_button
import config


def run_check_credits():
    """
    Main function for Check Credits module.
    """
    st.title("💰 Check Credits")
    st.markdown("Verify if members have already been credited for their contributions.")
    
    st.markdown("---")
    
    # File uploads
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 Processed Suspense Data")
        suspense_df = upload_file(
            label="Upload Processed Suspense Data",
            key="suspense_upload_credits",
            help_text="Upload the suspense data from Registration Check (with scheme numbers populated)",
            required_columns=[
                config.SUSPENSE_COLUMNS['member_name'],
                config.SUSPENSE_COLUMNS['scheme_number'],
                config.SUSPENSE_COLUMNS['contribution_month']
            ]
        )
        
        if suspense_df is not None:
            # Check if scheme numbers are populated
            empty_scheme_count = suspense_df[config.SUSPENSE_COLUMNS['scheme_number']].isna().sum()
            if empty_scheme_count == len(suspense_df):
                st.warning("⚠️ No scheme numbers found. Please run Registration Check first.")
            elif empty_scheme_count > 0:
                st.info(f"ℹ️ {empty_scheme_count} records without scheme numbers will be marked as 'Not Registered'")
    
    with col2:
        st.subheader("💳 Allocation Dump")
        allocation_df = upload_file(
            label="Upload Contribution Allocation Dump",
            key="allocation_dump_upload",
            help_text="Excel or CSV file with contribution allocation data",
            required_columns=[
                config.ALLOCATION_DUMP_COLUMNS['batch_number'],
                config.ALLOCATION_DUMP_COLUMNS['product_type'],
                config.ALLOCATION_DUMP_COLUMNS['scheme_number'],
                config.ALLOCATION_DUMP_COLUMNS['reference']
            ]
        )
    
    # Check if both files are uploaded
    if suspense_df is None or allocation_df is None:
        st.info("👆 Please upload both files to continue")
        return
    
    st.markdown("---")
    
    # Scheme filter
    st.subheader("🔍 Filter Settings")
    product_type_col = config.ALLOCATION_DUMP_COLUMNS['product_type']
    available_schemes = sorted(allocation_df[product_type_col].dropna().unique().tolist())
    
    if not available_schemes:
        st.error("❌ No schemes found in allocation dump")
        return
    
    selected_scheme = st.selectbox(
        "Select Scheme Type",
        options=available_schemes,
        help="Filter allocation dump by scheme type for matching"
    )
    
    st.markdown("---")
    
    # Run credit check
    if st.button("🚀 Run Credit Check", type="primary", use_container_width=True):
        with st.spinner("Processing... Cleaning allocation dump and checking credits."):
            
            # Step 1: Clean allocation dump
            st.info("🧹 Step 1: Cleaning allocation dump...")
            
            cleaned_allocation, cleaning_stats = clean_allocation_dump(
                allocation_df,
                config.ALLOCATION_DUMP_COLUMNS['batch_number'],
                config.ALLOCATION_DUMP_COLUMNS['reference']
            )
            
            # Display cleaning statistics
            with st.expander("📋 Allocation Dump Cleaning Statistics", expanded=True):
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Input Records", f"{cleaning_stats['total_records_input']:,}")
                with col2:
                    st.metric("Withdrawals Removed", cleaning_stats['withdrawals_removed'])
                with col3:
                    st.metric("Reversals Removed", 
                             cleaning_stats['original_transactions_removed'] + cleaning_stats['reversed_transactions_removed'])
                with col4:
                    st.metric("Output Records", f"{cleaning_stats['total_records_output']:,}")
            
            # Step 2: Filter by scheme
            st.info(f"🔍 Step 2: Filtering allocation dump by scheme: {selected_scheme}")
            
            scheme_filtered = cleaned_allocation[
                cleaned_allocation[product_type_col] == selected_scheme
            ].copy()
            
            st.success(f"✅ {len(scheme_filtered):,} allocation records for {selected_scheme}")
            
            # Step 3: Match contributions
            st.info("🔄 Step 3: Matching contributions...")
            
            # Initialize result columns
            suspense_df['CREDIT STATUS'] = 'Not Checked'
            suspense_df['ALLOCATION REFERENCE'] = ''
            suspense_df['ALLOCATION BATCH'] = ''
            
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            already_credited = 0
            not_credited = 0
            not_registered = 0
            
            total_records = len(suspense_df)
            
            for idx, row in suspense_df.iterrows():
                # Update progress
                progress = (idx + 1) / total_records
                progress_bar.progress(progress)
                status_text.text(f"Processing record {idx + 1} of {total_records:,}...")
                
                # Check if member is registered (has scheme number)
                scheme_number = row.get(config.SUSPENSE_COLUMNS['scheme_number'])
                
                if pd.isna(scheme_number) or str(scheme_number).strip() == '':
                    suspense_df.at[idx, 'CREDIT STATUS'] = 'Not Registered'
                    suspense_df.at[idx, 'ALLOCATION REFERENCE'] = 'N/A - No Scheme Number'
                    not_registered += 1
                    continue
                
                # Get contribution month
                contribution_month = row.get(config.SUSPENSE_COLUMNS['contribution_month'])
                
                if pd.isna(contribution_month):
                    suspense_df.at[idx, 'CREDIT STATUS'] = 'Missing Contribution Month'
                    not_credited += 1
                    continue
                
                # Normalize contribution month for matching
                contribution_month_clean = normalize_text(str(contribution_month))
                
                # Search for matching allocation
                matching_allocations = scheme_filtered[
                    (scheme_filtered[config.ALLOCATION_DUMP_COLUMNS['scheme_number']].astype(str) == str(scheme_number)) &
                    (scheme_filtered['Reference_CLEAN'].str.lower().str.contains(contribution_month_clean, na=False))
                ]
                
                if not matching_allocations.empty:
                    # Found a match - member has been credited
                    match = matching_allocations.iloc[0]
                    suspense_df.at[idx, 'CREDIT STATUS'] = 'Already Credited'
                    suspense_df.at[idx, 'ALLOCATION REFERENCE'] = match.get(config.ALLOCATION_DUMP_COLUMNS['reference'], '')
                    suspense_df.at[idx, 'ALLOCATION BATCH'] = match.get(config.ALLOCATION_DUMP_COLUMNS['batch_number'], '')
                    already_credited += 1
                else:
                    # No match found - member has not been credited
                    suspense_df.at[idx, 'CREDIT STATUS'] = 'Not Credited'
                    suspense_df.at[idx, 'ALLOCATION REFERENCE'] = 'No matching allocation found'
                    not_credited += 1
            
            progress_bar.empty()
            status_text.empty()
            
            # Display results
            st.success("✅ Credit check completed!")
            
            st.markdown("---")
            st.subheader("📊 Credit Check Statistics")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Already Credited", already_credited, 
                         help="Members who have already been credited for this contribution month")
            with col2:
                st.metric("Not Credited", not_credited, 
                         help="Members who have NOT been credited yet")
            with col3:
                st.metric("Not Registered", not_registered, 
                         help="Members without scheme numbers (not found in registration check)")
            
            # Calculate percentages
            if total_records > 0:
                credited_pct = (already_credited / total_records * 100)
                not_credited_pct = (not_credited / total_records * 100)
                
                st.info(f"""
                📈 **Summary:**
                - {credited_pct:.1f}% already credited (⚠️ risk of double crediting)
                - {not_credited_pct:.1f}% safe to credit
                - {not_registered:.0f} members need registration first
                """)
            
            # Preview results
            st.markdown("---")
            display_dataframe_preview(suspense_df, "Results Preview", max_rows=20)
            
            # Highlight risky records
            risky_records = suspense_df[suspense_df['CREDIT STATUS'] == 'Already Credited']
            if not risky_records.empty:
                st.warning(f"⚠️ **IMPORTANT:** {len(risky_records):,} records are already credited. Review these carefully to avoid double crediting!")
                
                with st.expander("🔍 View Already Credited Records"):
                    st.dataframe(risky_records, use_container_width=True)
            
            # Download button
            st.markdown("---")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"suspense_credit_check_{selected_scheme}_{timestamp}.xlsx"
            
            download_button(suspense_df, filename, "📥 Download Credit Check Results")
            
            # Store in session state
            st.session_state['credit_results'] = suspense_df
