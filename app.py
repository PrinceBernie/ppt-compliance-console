"""
PPT Compliance Console - Main Application
Legacy Suspense Clearing & Reconciliation System
"""
import streamlit as st
from components.sidebar import render_sidebar
from modules.home import run_home
from modules.check_registration import run_check_registration
from modules.check_credits import run_check_credits
from modules.analytics import run_analytics
import config


# Page configuration
st.set_page_config(**config.PAGE_CONFIG)

# Custom CSS for modern, elevated UI with brand colors
st.markdown("""
<style>
    /* Import Google Fonts: Inter and Manrope */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
    
    /* Global Styles - Default to Inter */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main content styling - minimal padding */
    .main .block-container {
        padding-top: 0.75rem !important;
        padding-bottom: 0.75rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 95% !important;
    }
    
    /* Aggressive vertical spacing reduction */
    .element-container {
        margin-bottom: 0.25rem !important;
    }
    
    /* Reduce spacing between sections */
    [data-testid="stVerticalBlock"] > [data-testid="element-container"] {
        margin-bottom: 0.4rem !important;
    }
    
    /* Streamlit default background override */
    .stApp {
        background: #000000 !important;
    }
    
    /* Headers - minimal margins */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Manrope', -apple-system, BlinkMacSystemFont, sans-serif !important;
        line-height: 1.2 !important;
    }

    h1 {
        color: #d32027 !important;
        font-weight: 800 !important;
        margin-top: 0.25rem !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: -0.5px;
    }
    
    h2 {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        margin-top: 0.5rem !important;
        margin-bottom: 0.35rem !important;
    }
    
    h3 {
        color: #969696 !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        margin-top: 0.4rem !important;
        margin-bottom: 0.3rem !important;
    }
    
    /* Paragraph - minimal margins */
    p, .stMarkdown, span, div {
        color: #FFFFFF !important;
    }
    
    p {
        margin-bottom: 0.25rem !important;
        line-height: 1.5 !important;
    }
    
    /* Reduce horizontal rule spacing */
    hr {
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Reduce sidebar padding */
    [data-testid="stSidebar"] {
        padding-top: 1rem !important;
    }
    
    [data-testid="stSidebar"] .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0.5rem !important;
    }
    
    
    
    /* Modern Card Styling - Black cards with red accent borders */
    .stApp > div > div {
        background: #000000;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 16px rgba(211, 32, 39, 0.3), 0 2px 8px rgba(211, 32, 39, 0.2);
        margin-bottom: 1rem;
        border: 1px solid rgba(211, 32, 39, 0.3);
    }
    
    /* Additional card containers */
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
        background: transparent;
    }
    
    /* Column containers - black with red borders */
    [data-testid="column"] {
        background: #000000;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 16px rgba(211, 32, 39, 0.3), 0 2px 8px rgba(211, 32, 39, 0.2);
        border: 1px solid rgba(211, 32, 39, 0.3);
    }
    
    /* Ensure all text in columns is white */
    [data-testid="column"] p,
    [data-testid="column"] span,
    [data-testid="column"] div,
    [data-testid="column"] label {
        color: #FFFFFF !important;
    }
    
    /* Metric Cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #d32027 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #FFFFFF !important;
        font-weight: 500;
        font-size: 0.875rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    [data-testid="stMetricDelta"] {
        font-weight: 600;
        color: #FFFFFF !important;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #d32027 0%, #a01a1f 100%);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 12px rgba(211, 32, 39, 0.25);
        letter-spacing: 0.3px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(211, 32, 39, 0.35);
        background: linear-gradient(135deg, #e63946 0%, #d32027 100%);
    }
    
    .stButton > button:active {
        transform: translateY(0px);
    }
    
    /* File Uploader Styling - Dark theme */
    [data-testid="stFileUploader"] {
        border: 2px dashed #d32027;
        border-radius: 16px;
        padding: 2rem;
        background: rgba(211, 32, 39, 0.1);
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #e63946;
        background: rgba(211, 32, 39, 0.15);
        box-shadow: 0 4px 12px rgba(211, 32, 39, 0.3);
    }
    
    [data-testid="stFileUploader"] label,
    [data-testid="stFileUploader"] span,
    [data-testid="stFileUploader"] p {
        color: #FFFFFF !important;
    }
    
    /* Dataframe Styling - Dark theme */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(211, 32, 39, 0.3);
        box-shadow: 0 2px 8px rgba(211, 32, 39, 0.2);
    }
    
    /* Dataframe headers and cells */
    [data-testid="stDataFrame"] table {
        background: #1a1a1a !important;
        color: #FFFFFF !important;
    }
    
    [data-testid="stDataFrame"] th {
        background: #d32027 !important;
        color: #FFFFFF !important;
        font-weight: 600;
    }
    
    [data-testid="stDataFrame"] td {
        background: #1a1a1a !important;
        color: #FFFFFF !important;
        border-color: rgba(211, 32, 39, 0.2) !important;
    }
    
    [data-testid="stDataFrame"] tr:hover td {
        background: #2a2a2a !important;
    }
    
    /* Expander Styling - Dark theme */
    .streamlit-expanderHeader {
        font-weight: 600;
        background: rgba(211, 32, 39, 0.1);
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid rgba(211, 32, 39, 0.3);
        transition: all 0.3s ease;
        color: #FFFFFF !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(211, 32, 39, 0.2);
        border-color: #d32027;
    }
    
    .streamlit-expanderContent {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 0 0 12px 12px;
        padding: 1rem;
    }
    
    /* Progress Bar Styling */
    .stProgress > div > div {
        background: linear-gradient(90deg, #d32027 0%, #e63946 100%);
        border-radius: 8px;
    }
    
    .stProgress > div {
        background-color: #F5F5F5;
        border-radius: 8px;
    }
    
    /* Alert Boxes with Dark Theme */
    .stSuccess {
        background: rgba(40, 167, 69, 0.15);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        border-left: 4px solid #28a745;
        box-shadow: 0 2px 8px rgba(40, 167, 69, 0.2);
        color: #FFFFFF !important;
    }
    
    .stSuccess p, .stSuccess span, .stSuccess div {
        color: #FFFFFF !important;
    }
    
    .stError {
        background: rgba(211, 32, 39, 0.15);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        border-left: 4px solid #d32027;
        box-shadow: 0 2px 8px rgba(211, 32, 39, 0.2);
        color: #FFFFFF !important;
    }
    
    .stError p, .stError span, .stError div {
        color: #FFFFFF !important;
    }
    
    .stWarning {
        background: rgba(245, 158, 11, 0.15);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        border-left: 4px solid #f59e0b;
        box-shadow: 0 2px 8px rgba(245, 158, 11, 0.2);
        color: #FFFFFF !important;
    }
    
    .stWarning p, .stWarning span, .stWarning div {
        color: #FFFFFF !important;
    }
    
    .stInfo {
        background: rgba(211, 32, 39, 0.15);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        border-left: 4px solid #d32027;
        box-shadow: 0 2px 8px rgba(211, 32, 39, 0.2);
        color: #FFFFFF !important;
    }
    
    .stInfo p, .stInfo span, .stInfo div {
        color: #FFFFFF !important;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #d32027 0%, #a01a1f 100%);
        box-shadow: 4px 0 12px rgba(0, 0, 0, 0.1);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Select Box Styling - Dark theme */
    .stSelectbox > div > div {
        border-radius: 12px;
        border: 2px solid rgba(211, 32, 39, 0.3);
        background: #1a1a1a;
        transition: all 0.3s ease;
        color: #FFFFFF !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #d32027;
        box-shadow: 0 2px 8px rgba(211, 32, 39, 0.3);
    }
    
    .stSelectbox label {
        color: #FFFFFF !important;
        font-weight: 500;
    }
    
    .stSelectbox input,
    .stSelectbox select,
    .stSelectbox div[role="button"] {
        color: #FFFFFF !important;
        background: #1a1a1a !important;
    }
    
    /* Text Input Styling - Dark theme */
    .stTextInput > div > div > input {
        background: #1a1a1a;
        color: #FFFFFF !important;
        border: 2px solid rgba(211, 32, 39, 0.3);
        border-radius: 12px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #d32027;
        box-shadow: 0 0 0 2px rgba(211, 32, 39, 0.2);
    }
    
    .stTextInput label {
        color: #FFFFFF !important;
    }
    
    /* Download Button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #4A4A4A 0%, #2d2d2d 100%);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(74, 74, 74, 0.25);
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(74, 74, 74, 0.35);
        background: linear-gradient(135deg, #5a5a5a 0%, #4A4A4A 100%);
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px 12px 0 0;
        padding: 0.75rem 1.5rem;
        background: #F5F5F5;
        color: #969696;
        font-weight: 600;
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #d32027 0%, #a01a1f 100%);
        color: white !important;
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #F5F5F5 50%, transparent 100%);
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #d32027 !important;
    }
    
    /* Caption Text */
    .caption {
        color: #969696;
        font-size: 0.875rem;
    }
    
    /* Code Blocks */
    code {
        background: #F5F5F5;
        padding: 0.25rem 0.5rem;
        border-radius: 6px;
        color: #d32027;
        font-weight: 500;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #F5F5F5;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #969696;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #d32027;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """
    Main application entry point.
    """
    # Render sidebar and get selected page
    selected_page = render_sidebar()
    
    # Route to appropriate page
    if selected_page == "Home":
        run_home()
    elif selected_page == "Check Registration":
        run_check_registration()
    elif selected_page == "Check Credits":
        run_check_credits()
    elif selected_page == "Analytics":
        run_analytics()
    else:
        st.error("Page not found")


if __name__ == "__main__":
    main()
