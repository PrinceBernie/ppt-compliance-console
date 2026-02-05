"""
Icon utility for PPT Compliance Console using HugeIcons style.
Provides helper functions to render inline SVGs.
"""
import streamlit as st

# HugeIcons SVG Definitions (Stroke based, 1.5px stroke width)
ICONS = {
    "home": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" class="{class_name}" width="{width}" height="{height}">
            <path d="M2.96967 10.9697L10.9697 2.96967C11.5555 2.38388 12.4445 2.38388 13.0303 2.96967L21.0303 10.9697C21.4658 11.4052 21.6 12.0674 21.3781 12.639C21.1561 13.2106 20.6139 13.5858 20 13.5858H19V20.5858C19 21.1381 18.5523 21.5858 18 21.5858H15V15.5858H9V21.5858H6C5.44772 21.5858 5 21.1381 5 20.5858V13.5858H4C3.38612 13.5858 2.84386 13.2106 2.62191 12.639C2.39996 12.0674 2.53416 11.4052 2.96967 10.9697Z" stroke="{color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
    """,
    "rocket": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" class="{class_name}" width="{width}" height="{height}">
            <path d="M12.9157 2.16436C12.5976 1.77607 12 1.9056 12 2.40822V10.5858H14.1776C14.6802 10.5858 14.8097 9.98818 14.4214 9.6701L12.9157 2.16436Z" stroke="{color}" stroke-width="1.5" stroke-linejoin="round"/>
            <path d="M11.0843 2.16436C11.4024 1.77607 12 1.9056 12 2.40822V10.5858H9.82236C9.31977 10.5858 9.19028 9.98818 9.57863 9.6701L11.0843 2.16436Z" stroke="{color}" stroke-width="1.5" stroke-linejoin="round"/>
            <path d="M16 17H8C6.34315 17 5 15.6569 5 14V13.5858C5 13.0335 5.44772 12.5858 6 12.5858H18C18.5523 12.5858 19 13.0335 19 13.5858V14C19 15.6569 17.6569 17 16 17Z" stroke="{color}" stroke-width="1.5"/>
            <path d="M16 17C16 19.2091 14.2091 21 12 21C9.79086 21 8 19.2091 8 17" stroke="{color}" stroke-width="1.5" stroke-linecap="round"/>
            <path d="M12 21V23" stroke="{color}" stroke-width="1.5" stroke-linecap="round"/>
            <path d="M5 13L2.25 15.75" stroke="{color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M19 13L21.75 15.75" stroke="{color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
    """,
    "search": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" class="{class_name}" width="{width}" height="{height}">
            <circle cx="11.5" cy="11.5" r="9.5" stroke="{color}" stroke-width="1.5"/>
            <path d="M18.5 18.5L22 22" stroke="{color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
    """,
    "file-check": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" class="{class_name}" width="{width}" height="{height}">
            <path d="M13 2H6C4.89543 2 4 2.89543 4 4V20C4 21.1046 4.89543 22 6 22H18C19.1046 22 20 21.1046 20 20V9L13 2Z" stroke="{color}" stroke-width="1.5" stroke-linejoin="round"/>
            <path d="M13 2V9H20" stroke="{color}" stroke-width="1.5" stroke-linejoin="round"/>
            <path d="M9 15L11 17L15 13" stroke="{color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
    """,
    "credit-card": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" class="{class_name}" width="{width}" height="{height}">
            <rect x="2" y="5" width="20" height="14" rx="3" stroke="{color}" stroke-width="1.5"/>
            <path d="M2 10H22" stroke="{color}" stroke-width="1.5"/>
            <path d="M7 15H9" stroke="{color}" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
    """,
    "check-circle": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" class="{class_name}" width="{width}" height="{height}">
            <circle cx="12" cy="12" r="10" stroke="{color}" stroke-width="1.5"/>
            <path d="M8.5 12.5L10.5 14.5L15.5 9.5" stroke="{color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
    """,
    "alert-circle": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" class="{class_name}" width="{width}" height="{height}">
            <circle cx="12" cy="12" r="10" stroke="{color}" stroke-width="1.5"/>
            <path d="M12 8V12" stroke="{color}" stroke-width="1.5" stroke-linecap="round"/>
            <path d="M12 16V16.01" stroke="{color}" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
    """,
    "book-open": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" class="{class_name}" width="{width}" height="{height}">
            <path d="M12 21V7" stroke="{color}" stroke-width="1.5" stroke-linecap="round"/>
            <path d="M4 19.5C4 18.6716 4.67157 18 5.5 18H12M4 19.5V5.5C4 4.67157 4.67157 4 5.5 4H12" stroke="{color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M20 19.5C20 18.6716 19.3284 18 18.5 18H12M20 19.5V5.5C20 4.67157 19.3284 4 18.5 4H12" stroke="{color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
    """,
    "workflow": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" class="{class_name}" width="{width}" height="{height}">
            <rect x="3" y="16" width="6" height="6" rx="2" stroke="{color}" stroke-width="1.5"/>
            <rect x="15" y="16" width="6" height="6" rx="2" stroke="{color}" stroke-width="1.5"/>
            <rect x="9" y="2" width="6" height="6" rx="2" stroke="{color}" stroke-width="1.5"/>
            <path d="M12 8V12" stroke="{color}" stroke-width="1.5"/>
            <path d="M12 12H6V16" stroke="{color}" stroke-width="1.5"/>
            <path d="M12 12H18V16" stroke="{color}" stroke-width="1.5"/>
        </svg>
    """,
    "settings": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" class="{class_name}" width="{width}" height="{height}">
            <path d="M12 15C13.6569 15 15 13.6569 15 12C15 10.3431 13.6569 9 12 9C10.3431 9 9 10.3431 9 12C9 13.6569 10.3431 15 12 15Z" stroke="{color}" stroke-width="1.5"/>
            <path d="M19.4 15.3464C20.2 15.7464 20.2 16.9464 19.4 17.3464L18.4 17.8464C17.6 18.2464 16.6 17.7464 16.4 16.8464C16.2 15.9464 15.2 15.3464 14.2 15.3464C13.2 15.3464 12.2 15.9464 12 16.8464C11.8 17.7464 10.8 18.2464 10 17.8464L9 17.3464C8.2 16.9464 8.2 15.7464 9 15.3464C9.8 14.9464 10.2 14.1464 10.2 13.1464C10.2 12.1464 9.8 11.3464 9 10.9464C8.2 10.5464 8.2 9.34641 9 8.94641L10 8.44641C10.8 8.04641 11.8 8.54641 12 9.44641C12.2 10.3464 13.2 10.9464 14.2 10.9464C15.2 10.9464 16.2 10.3464 16.4 9.44641C16.6 8.54641 17.6 8.04641 18.4 8.44641L19.4 8.94641C20.2 9.34641 20.2 10.5464 19.4 10.9464C18.6 11.3464 18.2 12.1464 18.2 13.1464C18.2 14.1464 18.6 14.9464 19.4 15.3464Z" stroke="{color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
    """,
    "help-circle": """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" class="{class_name}" width="{width}" height="{height}">
            <circle cx="12" cy="12" r="10" stroke="{color}" stroke-width="1.5"/>
            <path d="M9.09871 8.99995C9.09871 8.99995 9.46743 7.5 12 7.5C14.5326 7.5 14.9013 9 14.9013 9C14.9013 9 15.2536 11.1271 12.9868 12.3168C12.4419 12.6027 12.0528 13.1492 12.0528 13.764L12.0528 14.25" stroke="{color}" stroke-width="1.5" stroke-linecap="round"/>
            <path d="M12 17V17.01" stroke="{color}" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
    """
}

def get_icon(name: str, color: str = None, size: int = 24, class_name: str = "icon") -> str:
    """
    Get the SVG string for an icon with specified properties.
    
    Args:
        name: Name of the icon (must exist in ICONS)
        color: Stroke color (default None, inherits currentColor)
        size: Width and height of the icon
        class_name: CSS class for the SVG
        
    Returns:
        Formatted SVG string
    """
    if name not in ICONS:
        return f"<!-- Icon '{name}' not found -->"
        
    icon_svg = ICONS[name]
    
    return icon_svg.format(
        color=color if color else "currentColor",
        width=size,
        height=size,
        class_name=class_name
    ).strip()

def icon_html(name: str, label: str = "", color: str = None) -> str:
    """
    Return HTML for an icon followed by a label.
    Useful for st.markdown.
    """
    svg = get_icon(name, color=color, size=24)
    if label:
        return f'<div style="display:flex; align-items:center; gap:8px;">{svg} <span style="font-weight:600;">{label}</span></div>'
    return svg
