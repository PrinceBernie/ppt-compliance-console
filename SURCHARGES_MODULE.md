# Surcharges Module Documentation

## Overview

The **Surcharges Module** has been integrated into the PPT Compliance Console to calculate surcharges for defaulters (members who have missed contributions). This module provides two calculation methods to accommodate different scenarios.

## Features

### 1. **File Upload**
- Accepts Excel (.xlsx, .xls) or CSV files
- Flexible column mapping to work with various file formats
- Auto-detection of contribution and months columns

### 2. **Two Calculation Methods**

#### A. Same Monthly Contributions (OPS Method)
- **Use Case**: When member's contribution amount is consistent each month
- **Formula**: Compounds the running balance month-by-month
- **Example**: 
  - Monthly Contribution: ₦5,000
  - Months in Default: 3
  - Calculation:
    - Month 1: ₦5,150 (5,000 × 1.03)
    - Month 2: ₦10,454.50 ((5,150 + 5,000) × 1.03)
    - Month 3: ₦15,918.14 ((10,454.50 + 5,000) × 1.03)
    - Surcharge: ₦918.14

#### B. Different Monthly Contributions
- **Use Case**: When each contribution period may have different amounts
- **Formula**: Calculates each contribution independently
- **Example**:
  - Contribution Amount: ₦5,000
  - Months in Default: 3
  - Calculation:
    - Month 1: ₦5,150 (5,000 × 1.03)
    - Month 2: ₦5,304.50 (5,150 × 1.03)
    - Month 3: ₦5,463.64 (5,304.50 × 1.03)
    - Surcharge: ₦463.64

### 3. **Comprehensive Statistics**
- Total records processed
- Success/failure counts
- Financial summary:
  - Total original contributions
  - Total surcharges
  - Total amount due
  - Average surcharge percentage

### 4. **Error Handling**
- Validates data types
- Handles missing values
- Shows detailed error messages
- Provides failed records report

### 5. **Export Functionality**
- Downloads results as Excel file
- Includes all original columns plus:
  - Amount Due
  - Surcharge
  - Calculation Status

## Usage Instructions

### Step 1: Navigate to Surcharges
1. Open the PPT Compliance Console
2. Click on **"Surcharges"** in the sidebar navigation

### Step 2: Upload Defaulters Data
1. Click the file upload area
2. Select your Excel or CSV file containing defaulters data
3. The file should contain:
   - **Required**: Contribution Amount column
   - **Required**: Number of Months column
   - **Optional**: Member Name, Scheme Number, Employer, etc.

### Step 3: Configure Column Mapping
1. Select the column containing **Contribution Amounts**
   - Auto-detection will try to find it for you
2. Select the column containing **Number of Months**
   - Auto-detection will try to find it for you

### Step 4: Choose Calculation Method
- Select **"Same Monthly Contributions (OPS Method)"** if:
  - Members have consistent monthly contributions
  - You want the total compound balance
  
- Select **"Different Monthly Contributions"** if:
  - Each contribution may be different
  - You want independent calculations

### Step 5: Calculate
1. Click **"🚀 Calculate Surcharges"**
2. Wait for processing to complete
3. Review the statistics and results

### Step 6: Download Results
1. Click **"📥 Download Surcharge Report"**
2. File will be named: `surcharge_calculation_[method]_[timestamp].xlsx`

## Expected File Format

Your uploaded file should contain these columns (names can vary):

| Column Name Example | Description | Required |
|---------------------|-------------|----------|
| Member Name | Name of the member | No |
| Scheme Number | Member's registration number | No |
| Employer | Employer name | No |
| Contribution Amount Defaulted / Contribution Amount | Amount owed | **Yes** |
| Number of Months Run / Number of Months | Months outstanding | **Yes** |

### Sample Data Structure

```
Member Name    | Scheme Number | Employer   | Contribution Amount | Number of Months
---------------|---------------|------------|---------------------|------------------
John Doe       | SCH001        | Company A  | 5000.00            | 3
Jane Smith     | SCH002        | Company B  | 7500.00            | 6
Bob Johnson    | SCH003        | Company C  | 3200.00            | 12
```

## Understanding the Calculations

### Surcharge Rate
- Fixed at **3% per month** (0.03)
- Compounds monthly

### OPS Method (Same Contributions)
```
For each month i from 1 to N:
    A_due = (1 + 0.03) × (A + C)
    A = A_due

Where:
- C = Monthly contribution amount (constant)
- N = Number of months in default
- A = Running balance (starts at 0)

Final Surcharge = A_due - (C × N)
```

### Different Contributions Method
```
For each month i from 1 to M:
    A_due = (1 + 0.03) × A
    A = A_due

Where:
- C = Contribution amount for this period
- M = Months this contribution has been in default
- A = Starting amount (equals C)

Final Surcharge = A_due - C
```

## Output Columns

The downloaded file will contain all your original columns plus:

| New Column | Description |
|------------|-------------|
| Amount Due | Total amount the member owes (contribution + surcharge) |
| Surcharge | Calculated surcharge amount |
| Calculation Status | Success, Missing Data, Invalid Values, or specific error |

## Troubleshooting

### "Missing Data" Status
- Check that the contribution amount and months columns have values
- Ensure no blank cells in required columns

### "Invalid Values" Status
- Contribution amounts must be greater than 0
- Number of months must be greater than 0

### Column Not Found Error
- Verify column names in your file
- Use the column mapping selectors to choose the correct columns

### No Auto-Detection
- If columns aren't auto-detected, manually select them from the dropdowns
- The module looks for keywords: "contribution", "amount", "month", "number", "run"

## Technical Details

### Dependencies
- `pandas`: Data manipulation
- `streamlit`: UI framework
- Standard library: `datetime`

### Calculation Functions
- `calculate_ops_surcharge(contribution_amount, num_months)`: OPS method
- `calculate_different_surcharge(contribution_amount, num_months)`: Different contributions method

### Session State
- Results are stored in `st.session_state['surcharge_results']`
- Persists during the browser session

## Integration

The module is fully integrated into the PPT Compliance Console:

1. **Navigation**: Added to sidebar with calculator icon
2. **Route**: Accessible via `app.py` routing
3. **Components**: Uses shared file uploader and download components
4. **Styling**: Follows the app's modern dark theme with brand colors

## Future Enhancements (Potential)

- Variable surcharge rates
- Date-based calculations
- Batch processing for multiple companies
- Export to multiple formats (CSV, PDF)
- Historical surcharge tracking
- Payment plan calculator

## Support

For issues or questions:
1. Check that your file format matches the expected structure
2. Verify column names are mapped correctly
3. Review error messages in the Failed Records section
4. Ensure numeric data is in correct format (no currency symbols, commas allowed)

---

**Module Version**: 1.0  
**Last Updated**: February 2026  
**Compatible with**: PPT Compliance Console v1.1+
