"""
Home page for PPT Compliance Console
"""
import streamlit as st


def run_home():
    """
    Display the home page with instructions and overview.
    """
    st.title("🏠 Welcome to PPT Compliance Console")
    st.markdown("### Legacy Suspense Clearing & Reconciliation System")
    
    st.markdown("---")
    
    # Overview
    st.markdown("""
    ## 📋 Overview
    
    This application helps reconcile legacy suspense contributions with the core application database
    to prevent **double registration** and **double crediting** of member contributions.
    
    ### Why This Matters
    
    Suspense data is static and doesn't update with real-time system changes. A member whose contributions
    were held in suspense because they weren't registered might have been registered later and even credited.
    Without proper reconciliation, we risk:
    
    - ❌ Double registering members
    - ❌ Double crediting contributions
    - ❌ Data integrity issues
    - ❌ Compliance violations
    """)
    
    st.markdown("---")
    
    # Workflow
    st.markdown("## 🔄 Two-Step Workflow")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Step 1️⃣: Check Registration
        
        **Purpose:** Identify which suspense members are already registered in the system
        
        **What you need:**
        - 📄 Suspense data file
        - 👥 Member dump from core system
        
        **What it does:**
        - Matches members using 3-tier fallback logic:
          1. Contact number + name fuzzy match (70%)
          2. ID number bidirectional match (70%)
          3. Name + employer match (80%)
        - Populates scheme numbers for matched members
        - Generates downloadable results
        
        **Output:** Suspense data with scheme numbers populated
        """)
    
    with col2:
        st.markdown("""
        ### Step 2️⃣: Check Credits
        
        **Purpose:** Verify if members have already been credited
        
        **What you need:**
        - 📄 Processed suspense data (from Step 1)
        - 💳 Contribution allocation dump
        
        **What it does:**
        - Cleans allocation dump (removes withdrawals & reversals)
        - Matches scheme number + contribution month pairs
        - Identifies already credited vs. safe to credit
        - Highlights risky records
        
        **Output:** Final report showing credit status for each member
        """)
    
    st.markdown("---")
    
    # Key Features
    st.markdown("## ✨ Key Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🎯 Intelligent Matching**
        - Three-tier fallback logic
        - Fuzzy name matching
        - Bidirectional ID matching
        - Employer-scoped matching
        """)
    
    with col2:
        st.markdown("""
        **🧹 Data Cleaning**
        - Automatic reversal detection
        - Withdrawal filtering
        - Reference field normalization
        - Contact/ID cleaning
        """)
    
    with col3:
        st.markdown("""
        **📊 Rich Analytics**
        - Match statistics
        - Credit status breakdown
        - Risk identification
        - Downloadable reports
        """)
    
    st.markdown("---")
    
    # Getting Started
    st.markdown("## 🚀 Getting Started")
    
    st.info("""
    **Ready to begin?**
    
    1. Navigate to **Check Registration** in the sidebar
    2. Upload your suspense data and member dump
    3. Select the scheme type
    4. Run the registration check
    5. Download the results
    6. Proceed to **Check Credits** with the processed data
    """)
    
    st.markdown("---")
    
    # Data Requirements
    with st.expander("📋 Data Format Requirements"):
        st.markdown("""
        ### Suspense Data Required Columns:
        - EMPLOYER
        - MEMBER NAME
        - SCHEME NUMBER (will be populated)
        - SSNIT NUMBER
        - GH. CARD NUMBER
        - CONTACT
        - CONTRIBUTION MONTH
        - 5% CONTRIBUTION
        - SCHEME
        
        ### Member Dump Required Columns:
        - First name
        - [Middle name]
        - [Last name]
        - Member number
        - [Scheme number]
        - Mobile
        - S s n i t
        - Id number
        - [Scheme name]
        - Group name
        
        ### Allocation Dump Required Columns:
        - Batch number
        - Product type
        - [Scheme number]
        - Reference
        - [Contribution]
        - [Withdrawal]
        
        *Note: Columns in [brackets] may have optional data but must exist*
        """)
    
    with st.expander("⚙️ Matching Logic Details"):
        st.markdown("""
        ### Three-Tier Fallback Matching
        
        **Tier 1: Contact Number Match (70% name similarity)**
        - Matches suspense contact against member mobile
        - Verifies with fuzzy name matching
        - Most reliable when contact data is accurate
        
        **Tier 2: ID Number Match (70% name similarity)**
        - Bidirectional matching of SSNIT ↔ Ghana Card
        - Handles data entry inconsistencies
        - Checks all four combinations:
          - Suspense SSNIT → Member SSNIT
          - Suspense SSNIT → Member ID
          - Suspense Ghana Card → Member SSNIT
          - Suspense Ghana Card → Member ID
        
        **Tier 3: Name + Employer Match (80% similarity)**
        - Matches name within same employer group
        - Higher threshold for accuracy
        - Scoped to prevent cross-employer false matches
        
        ### Data Normalization
        - All contacts/IDs cleaned (alphanumeric only)
        - Names normalized (lowercase, trimmed)
        - Fuzzy matching handles typos and variations
        """)
    
    with st.expander("🔍 Reversal Detection Logic"):
        st.markdown("""
        ### How Reversals Are Detected
        
        Reversed transactions are identified by batch numbers ending with `/1`:
        
        **Example:**
        - Original: `PPTY5CH3134729`
        - Reversed: `PPTY5CH3134729/1`
        
        **Cleaning Process:**
        1. Identify all transactions with `/1` suffix
        2. Find their original transactions (without `/1`)
        3. Remove BOTH original and reversed transactions
        4. This prevents false positive credit matches
        
        ### Withdrawal Filtering
        - Any record with "withdrawal" in Reference field is removed
        - Case-insensitive search
        - Prevents matching against withdrawal transactions
        """)
    
    st.markdown("---")
    
    # Support
    st.markdown("## 💡 Need Help?")
    
    st.markdown("""
    - 📖 Check the **Quick Guide** in the sidebar
    - 🔍 Expand the sections above for detailed information
    - 📊 Review match statistics after each run
    - ⚠️ Pay attention to warning messages
    """)
    
    st.markdown("---")
    st.caption("PPT Compliance Console v1.0 | Built with Streamlit")
