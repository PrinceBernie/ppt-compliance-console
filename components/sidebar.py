"""
Sidebar navigation component
"""
import streamlit as st
from streamlit_option_menu import option_menu


def render_sidebar():
    """
    Render the sidebar navigation menu with brand colors.
    
    Returns:
        Selected menu item
    """
    with st.sidebar:
        st.markdown("# 📊 PPT Compliance Console")
        st.markdown("---")
        
        selected = option_menu(
            menu_title=None,
            options=["Home", "Check Registration", "Check Credits", "Analytics"],
            icons=["house-fill", "person-check-fill", "cash-coin", "bar-chart-fill"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#ffffff", "font-size": "20px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "5px",
                    "padding": "12px 16px",
                    "border-radius": "12px",
                    "color": "#ffffff",
                    "background-color": "rgba(255, 255, 255, 0.1)",
                    "--hover-color": "rgba(255, 255, 255, 0.2)",
                    "transition": "all 0.3s ease",
                },
                "nav-link-selected": {
                    "background": "linear-gradient(135deg, rgba(255, 255, 255, 0.25) 0%, rgba(255, 255, 255, 0.15) 100%)",
                    "color": "#ffffff",
                    "font-weight": "600",
                    "box-shadow": "0 4px 12px rgba(0, 0, 0, 0.2)",
                },
            }
        )
        
        st.markdown("---")
        st.markdown("### 📖 Quick Guide")
        st.markdown("""
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
        """)
        
        st.markdown("---")
        st.caption("PPT Compliance Console v1.0")
        
    return selected
