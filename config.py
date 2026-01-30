"""
Configuration file for Suspense Reconciliation Compliance Console
"""

# Application Settings
APP_TITLE = "PPT Compliance Console"
APP_ICON = "📊"
PAGE_CONFIG = {
    "page_title": "PPT Compliance Console",
    "page_icon": "📊",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# File Upload Settings
MAX_FILE_SIZE_MB = 100
ALLOWED_EXTENSIONS = ['.xlsx', '.xls', '.csv']

# Column Mappings
SUSPENSE_COLUMNS = {
    'employer': 'EMPLOYER',
    'member_name': 'MEMBER NAME',
    'scheme_number': 'SCHEME NUMBER',
    'ssnit_number': 'SSNIT NUMBER',
    'gh_card_number': 'GH. CARD NUMBER',
    'contact': 'CONTACT',
    'contribution_month': 'CONTRIBUTION MONTH',
    'contribution_amount': '5% CONTRIBUTION',
    'scheme': 'SCHEME'
}

MEMBER_DUMP_COLUMNS = {
    'first_name': 'First name',
    'middle_name': '[Middle name]',
    'last_name': '[Last name]',
    'member_number': 'Member number',
    'scheme_number': '[Scheme number]',
    'mobile': 'Mobile',
    'ssnit': 'S s n i t',
    'id_number': 'Id number',
    'scheme_name': '[Scheme name]',
    'group_name': 'Group name'
}

ALLOCATION_DUMP_COLUMNS = {
    'batch_number': 'Batch number',
    'mobile': 'Mobile',
    'product_type': 'Product type',
    'scheme_number': '[Scheme number]',
    'reference': 'Reference',
    'contribution': '[Contribution]',
    'withdrawal': '[Withdrawal]'
}

# Matching Thresholds
FUZZY_THRESHOLD_CONTACT_ID = 0.7  # 70% for contact and ID matching
FUZZY_THRESHOLD_NAME_EMPLOYER = 0.9  # 90% for name+employer matching

# Brand Colors
BRAND_RED = "#d32027"
BRAND_WHITE = "#000000"
BRAND_GREY = "#969696"
BRAND_LIGHT_GREY = "#F5F5F5"
BRAND_DARK_GREY = "#4A4A4A"

# Match Status Messages
MATCH_STATUS = {
    'whitelist': 'Matched - Whitelist',
    'tier1': 'Matched - Contact & Name',
    'tier2': 'Matched - ID Number',
    'tier3': 'Matched - Name & Employer',
    'no_match': 'No Match Found'
}

# UI Styling
SIDEBAR_STYLE = """
    <style>
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #d32027 0%, #a01a1f 100%);
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    </style>
"""

SUCCESS_COLOR = "#10b981"
WARNING_COLOR = "#f59e0b"
ERROR_COLOR = "#d32027"
INFO_COLOR = "#d32027"
