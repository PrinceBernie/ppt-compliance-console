"""
Home page for PPT Compliance Console
"""
import streamlit as st
import config
from utils.icons import get_icon, icon_html


def run_home():
    """
    Display the home page with simplified, categorized content.
    """
    # Title with icon
    st.markdown(f"""
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:24px;">
            {get_icon('home', color=config.BRAND_RED, size=32)}
            <h1 style="margin:0; padding:0; display:inline;">PPT Compliance Console</h1>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 1. Getting Started - Keep visible
    st.markdown(icon_html("rocket", "Quick Start", color=config.BRAND_RED), unsafe_allow_html=True)
    st.info("""
    1.  **Check Registration:** Upload suspense data & member dump to identify registered members.
    2.  **Check Credits:** Use the processed file & allocation dump to verify credit status.
    """)

    st.markdown("### 📚 Documentation & Reference")

    # 2. Workflow (Expandable)
    with st.expander("🔄 How it Works: Two-Step Workflow", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(icon_html("file-check", "Step 1: Check Registration", color=None), unsafe_allow_html=True)
            st.markdown("**Goal:** Identify suspense members already in the system.")
            st.markdown("- **Input:** Suspense Data + Member Dump")
            st.markdown("- **Logic:** Matches via Contact, ID Numbers, or Name+Employer.")
            st.markdown("- **Output:** Suspense data with populated Scheme Numbers.")
        
        with col2:
            st.markdown(icon_html("credit-card", "Step 2: Check Credits", color=None), unsafe_allow_html=True)
            st.markdown("**Goal:** Verify if contributions are already credited.") 
            st.markdown("- **Input:** Processed Suspense Data + Allocation Dump")
            st.markdown("- **Logic:** Matches Scheme Number + Contribution Month.")
            st.markdown("- **Output:** Final report flagging 'Already Credited' members.")

    # 3. Data Requirements (Expandable)
    with st.expander("📋 Data & File Requirements", expanded=False):
        st.markdown(icon_html("file-check", "Required Columns"), unsafe_allow_html=True) 
        col_req1, col_req2, col_req3 = st.columns(3)
        
        with col_req1:
            st.markdown("**Suspense Data**")
            st.code("""
EMPLOYER
MEMBER NAME
SCHEME NUMBER
SSNIT NUMBER
GH. CARD NUMBER
CONTACT
CONTRIBUTION MONTH
5% CONTRIBUTION
SCHEME
            """, language="text")
            
        with col_req2:
            st.markdown("**Member Dump**")
            st.code("""
First name
[Middle name]
[Last name]
Member number
[Scheme number]
Mobile
S s n i t
Id number
Group name
            """, language="text")
            
        with col_req3:
            st.markdown("**Allocation Dump**")
            st.code("""
Batch number
Product type
[Scheme number]
Reference
[Contribution]
[Withdrawal]
            """, language="text")
        st.caption("*Columns in [brackets] are optional but headers must exist.*")

    # 4. Technical Details (Expandable)
    with st.expander("⚙️ Matching & Cleaning Logic", expanded=False):
        st.markdown(icon_html("settings", "1. Registration Matching Tiers"), unsafe_allow_html=True)
        st.markdown("- **Tier 1:** Contact + Name Fuzzy (70%)")
        st.markdown("- **Tier 2:** SSNIT/Ghana Card Bidirectional Match (70% Name check)")
        st.markdown("- **Tier 3:** Name + Employer Match (80%)")
        
        st.divider()
        
        st.markdown(icon_html("check-circle", "2. Credit Check Logic"), unsafe_allow_html=True)
        st.markdown("- **Date Standardization:** 'Jan 25' matches 'January 2025'.")
        st.markdown("- **Reversals:** Transactions with batch numbers ending in `/1` are removed (along with original).")
        st.markdown("- **Withdrawals:** Rows with 'withdrawal' in Reference are ignored.")

    # 5. Support (Expandable)
    with st.expander("❓ Help & Support", expanded=False):
        st.markdown(icon_html("help-circle", "Additional Help", color=config.BRAND_RED), unsafe_allow_html=True)
        st.markdown("- 📖 See **Quick Guide** in the sidebar.")
        st.markdown("- ⚠️ Always verify 'Risk of Double Crediting' warnings.")

    
    st.markdown("---")
    st.caption("PPT Compliance Console v1.1 | Built with Streamlit")
