"""
Sidebar navigation component
"""
import streamlit as st
from streamlit_option_menu import option_menu
from utils.icons import get_icon
import config


def render_sidebar():
    """
    Render the sidebar navigation menu with modern design.
    
    Returns:
        Selected menu item
    """
    with st.sidebar:
        # Title
        st.markdown("""
            <div style="margin-bottom:16px; padding:0 8px;">
                <h2 style="margin:0; padding:0; font-size:1.3rem; color:#ffffff; font-weight:700; letter-spacing:-0.3px;">
                    Compliance Console
                </h2>
            </div>
        """, unsafe_allow_html=True)
        
        selected = option_menu(
            menu_title=None,
            options=["Home", "Check Registration", "Check Credits", "Analytics"],
            icons=["house", "person-check", "credit-card", "bar-chart"],
            menu_icon=None,
            default_index=0,
            styles={
                "container": {
                    "padding": "0!important", 
                    "background-color": "transparent"
                },
                "icon": {
                    "color": "#ffffff", 
                    "font-size": "18px",
                    "margin-right": "12px"
                },
                "nav-link": {
                    "font-size": "15px",
                    "text-align": "left",
                    "margin": "4px 0",
                    "padding": "12px 16px",
                    "padding-left": "16px",
                    "border-radius": "8px",
                    "color": "#ffffff",
                    "background-color": "transparent",
                    "transition": "all 0.2s ease",
                    "font-weight": "500",
                    "border-left": "3px solid transparent",
                },
                "nav-link-selected": {
                    "background": "rgba(255, 255, 255, 0.1)",
                    "color": "#ffffff !important",
                    "font-weight": "600",
                    "border-left": "3px solid #ffffff",
                    "padding-left": "16px",
                    "transform": "translateX(2px)",
                    "box-shadow": "0 2px 8px rgba(0, 0, 0, 0.15)",
                },
            }
        )
        
        # Add comprehensive CSS for styling
        st.markdown("""
            <style>
            /* Remove black background from menu containers - comprehensive approach */
            [data-testid="stSidebar"] nav,
            [data-testid="stSidebar"] nav > div,
            [data-testid="stSidebar"] [class*="container"],
            [data-testid="stSidebar"] [class*="nav"],
            [data-testid="stSidebar"] [style*="background"],
            [data-testid="stSidebar"] div[data-baseweb],
            [data-testid="stSidebar"] ul,
            [data-testid="stSidebar"] .css-1544g2n,
            [data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > div {
                background: transparent !important;
                background-color: transparent !important;
            }
            
            /* Wildcard approach for any black backgrounds */
            [data-testid="stSidebar"] div[style*="background-color: rgb(0, 0, 0)"],
            [data-testid="stSidebar"] div[style*="background: black"],
            [data-testid="stSidebar"] div[style*="background:#000"] {
                background: transparent !important;
                background-color: transparent !important;
            }
            
            /* Keep ALL icons white */
            [data-testid="stSidebar"] .nav-link *,
            [data-testid="stSidebar"] .nav-link-selected *,
            [data-testid="stSidebar"] a *,
            [data-testid="stSidebar"] button * {
                color: #ffffff !important;
            }
            
            /* Specifically target Bootstrap icons */
            [data-testid="stSidebar"] i::before,
            [data-testid="stSidebar"] i {
                color: #ffffff !important;
            }
            
            /* Target SVG icons */
            [data-testid="stSidebar"] svg {
                color: #ffffff !important;
                stroke: #ffffff !important;
            }
            
            /* Enhance selected state with additional visual cues */
            [data-testid="stSidebar"] .nav-link-selected,
            [data-testid="stSidebar"] a[aria-selected="true"],
            [data-testid="stSidebar"] button[aria-selected="true"] {
                position: relative;
            }
            
            /* Hover effect for non-selected items */
            [data-testid="stSidebar"] .nav-link:not(.nav-link-selected):hover,
            [data-testid="stSidebar"] a:not([aria-selected="true"]):hover,
            [data-testid="stSidebar"] button:not([aria-selected="true"]):hover {
                background-color: rgba(255, 255, 255, 0.08) !important;
                transform: translateX(2px);
            }
            </style>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown(f"""
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px; padding:0 8px;">
                {get_icon('book-open', color='#ffffff', size=18)}
                <h3 style="margin:0; padding:0; font-size:0.95rem; color:#ffffff; font-weight:600;">Quick Guide</h3>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="font-size:0.85rem; line-height:1.5; padding:0 8px;">
        
        **Step 1:** Check Registration
        - Upload suspense data
        - Upload member dump
        - Run matching process
        - Download results
        
        **Step 2:** Check Credits
        - Upload processed suspense
        - Upload allocation dump
        - Run credit check
        - Download final report
        
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.caption("PPT Compliance Console v1.1")
        
    return selected
