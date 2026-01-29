"""
Analytics page for viewing reconciliation statistics
"""
import streamlit as st
import pandas as pd


def run_analytics():
    """
    Display analytics and statistics from reconciliation runs.
    """
    st.title("📊 Analytics Dashboard")
    st.markdown("View statistics and insights from your reconciliation runs.")
    
    st.markdown("---")
    
    # Check if we have results in session state
    has_reg_results = 'registration_results' in st.session_state
    has_credit_results = 'credit_results' in st.session_state
    
    if not has_reg_results and not has_credit_results:
        st.info("""
        📈 **No data available yet**
        
        Run the reconciliation processes to see analytics here:
        1. Complete **Check Registration** to see registration statistics
        2. Complete **Check Credits** to see credit statistics
        """)
        return
    
    # Registration Analytics
    if has_reg_results:
        st.subheader("✅ Registration Check Analytics")
        
        reg_df = st.session_state['registration_results']
        
        # Overall statistics
        col1, col2, col3, col4 = st.columns(4)
        
        total_records = len(reg_df)
        tier1_count = (reg_df['MATCH STATUS'] == 'Matched - Contact & Name').sum()
        tier2_count = (reg_df['MATCH STATUS'] == 'Matched - ID Number').sum()
        tier3_count = (reg_df['MATCH STATUS'] == 'Matched - Name & Employer').sum()
        no_match_count = (reg_df['MATCH STATUS'] == 'No Match Found').sum()
        
        with col1:
            st.metric("Total Records", f"{total_records:,}")
        with col2:
            st.metric("Total Matches", f"{tier1_count + tier2_count + tier3_count:,}")
        with col3:
            match_rate = ((tier1_count + tier2_count + tier3_count) / total_records * 100) if total_records > 0 else 0
            st.metric("Match Rate", f"{match_rate:.1f}%")
        with col4:
            st.metric("No Matches", f"{no_match_count:,}")
        
        # Match breakdown
        st.markdown("#### Match Type Breakdown")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Tier 1 (Contact)", tier1_count, help="Contact & Name matches")
        with col2:
            st.metric("Tier 2 (ID)", tier2_count, help="ID Number matches")
        with col3:
            st.metric("Tier 3 (Name+Employer)", tier3_count, help="Name & Employer matches")
        
        # Match status distribution
        st.markdown("#### Match Status Distribution")
        match_status_counts = reg_df['MATCH STATUS'].value_counts()
        st.bar_chart(match_status_counts)
        
        # Average similarity scores
        if 'MATCH SIMILARITY' in reg_df.columns:
            matched_records = reg_df[reg_df['MATCH STATUS'] != 'No Match Found']
            if not matched_records.empty:
                avg_similarity = matched_records['MATCH SIMILARITY'].mean()
                st.metric("Average Match Similarity", f"{avg_similarity:.1%}")
        
        st.markdown("---")
    
    # Credit Analytics
    if has_credit_results:
        st.subheader("💰 Credit Check Analytics")
        
        credit_df = st.session_state['credit_results']
        
        # Overall statistics
        col1, col2, col3, col4 = st.columns(4)
        
        total_records = len(credit_df)
        already_credited = (credit_df['CREDIT STATUS'] == 'Already Credited').sum()
        not_credited = (credit_df['CREDIT STATUS'] == 'Not Credited').sum()
        not_registered = (credit_df['CREDIT STATUS'] == 'Not Registered').sum()
        
        with col1:
            st.metric("Total Records", f"{total_records:,}")
        with col2:
            st.metric("Already Credited", f"{already_credited:,}", delta="⚠️ Risk", delta_color="inverse")
        with col3:
            st.metric("Not Credited", f"{not_credited:,}", delta="✅ Safe", delta_color="normal")
        with col4:
            st.metric("Not Registered", f"{not_registered:,}")
        
        # Risk assessment
        if total_records > 0:
            risk_pct = (already_credited / total_records * 100)
            safe_pct = (not_credited / total_records * 100)
            
            st.markdown("#### Risk Assessment")
            
            if risk_pct > 50:
                st.error(f"🚨 **HIGH RISK:** {risk_pct:.1f}% of records are already credited. Carefully review before processing!")
            elif risk_pct > 25:
                st.warning(f"⚠️ **MODERATE RISK:** {risk_pct:.1f}% of records are already credited. Review recommended.")
            else:
                st.success(f"✅ **LOW RISK:** Only {risk_pct:.1f}% of records are already credited.")
            
            st.info(f"📊 {safe_pct:.1f}% of records are safe to credit ({not_credited:,} members)")
        
        # Credit status distribution
        st.markdown("#### Credit Status Distribution")
        credit_status_counts = credit_df['CREDIT STATUS'].value_counts()
        st.bar_chart(credit_status_counts)
        
        st.markdown("---")
    
    # Combined insights
    if has_reg_results and has_credit_results:
        st.subheader("🔍 Combined Insights")
        
        reg_df = st.session_state['registration_results']
        credit_df = st.session_state['credit_results']
        
        # Funnel analysis
        st.markdown("#### Reconciliation Funnel")
        
        total_suspense = len(reg_df)
        total_registered = (reg_df['MATCH STATUS'] != 'No Match Found').sum()
        total_safe_to_credit = (credit_df['CREDIT STATUS'] == 'Not Credited').sum()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Starting Suspense Records", f"{total_suspense:,}")
        with col2:
            reg_rate = (total_registered / total_suspense * 100) if total_suspense > 0 else 0
            st.metric("Found Registered", f"{total_registered:,}", delta=f"{reg_rate:.1f}%")
        with col3:
            safe_rate = (total_safe_to_credit / total_suspense * 100) if total_suspense > 0 else 0
            st.metric("Safe to Credit", f"{total_safe_to_credit:,}", delta=f"{safe_rate:.1f}%")
        
        st.markdown("""
        **Interpretation:**
        - Records that are registered but not yet credited are safe to process
        - Records already credited should be excluded to prevent double crediting
        - Records not registered need manual registration first
        """)
