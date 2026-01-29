# PPT Compliance Console

A Streamlit-based application for reconciling legacy suspense contributions with the core application database to prevent double registration and crediting of member contributions.

## 🎯 Purpose

Suspense data is static and doesn't update with real-time system changes. This application ensures that:
- Members who were registered after their contributions were placed in suspense are identified
- Members who have already been credited are flagged to prevent double crediting
- Data integrity is maintained throughout the reconciliation process

## 🚀 Quick Start

### Installation

1. **Clone or download this repository**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## 📋 Data Requirements

### Suspense Data
Required columns:
- `EMPLOYER` - Employer/company name
- `MEMBER NAME` - Full name of member
- `SCHEME NUMBER` - Will be populated by the app
- `SSNIT NUMBER` - Social Security number
- `GH. CARD NUMBER` - Ghana Card number
- `CONTACT` - Phone/mobile number
- `CONTRIBUTION MONTH` - Month of contribution (e.g., "January 2026")
- `5% CONTRIBUTION` - Contribution amount
- `SCHEME` - Scheme type

### Member Dump (System Data)
Required columns:
- `First name` - Member's first name
- `[Middle name]` - Member's middle name (optional data)
- `[Last name]` - Member's last name (optional data)
- `Member number` - Unique member identifier
- `[Scheme number]` - Member's scheme number
- `Mobile` - Contact number
- `S s n i t` - SSNIT number
- `Id number` - Ghana Card or other ID
- `[Scheme name]` - Name of the scheme
- `Group name` - Employer/group name

### Allocation Dump
Required columns:
- `Batch number` - Transaction batch number
- `Product type` - Scheme type
- `[Scheme number]` - Member's scheme number
- `Reference` - Transaction reference (e.g., "Payment for January 2026")
- `[Contribution]` - Contribution amount
- `[Withdrawal]` - Withdrawal amount

*Note: Columns in [brackets] may contain empty values but must exist in the file*

## 🔄 Workflow

### Step 1: Check Registration

**Purpose:** Identify which suspense members are already registered in the system

1. Navigate to **Check Registration** in the sidebar
2. Upload your suspense data file (Excel or CSV)
3. Upload the member dump from your core system
4. Select the scheme type to filter by
5. Click **Run Registration Check**
6. Review the match statistics
7. Download the results

**Matching Logic:**
- **Tier 1:** Contact number match with 70% name similarity
- **Tier 2:** Bidirectional ID matching (SSNIT ↔ Ghana Card) with 70% name similarity
- **Tier 3:** Name match within same employer with 80% similarity

### Step 2: Check Credits

**Purpose:** Verify if members have already been credited for their contributions

1. Navigate to **Check Credits** in the sidebar
2. Upload the processed suspense data from Step 1
3. Upload the contribution allocation dump
4. Select the scheme type
5. Click **Run Credit Check**
6. Review the credit statistics and risky records
7. Download the final report

**Processing:**
- Removes withdrawal transactions
- Detects and removes reversals (batch numbers ending with `/1`)
- Matches scheme number + contribution month pairs
- Flags already credited members

## 🎨 Features

### Intelligent Matching
- Three-tier fallback logic for maximum accuracy
- Fuzzy name matching to handle typos and variations
- Bidirectional ID matching to handle data entry inconsistencies
- Employer-scoped matching to prevent false positives

### Data Cleaning
- Automatic normalization of contacts and IDs
- Reversal detection and removal
- Withdrawal filtering
- Reference field cleaning

### Analytics & Reporting
- Real-time match statistics
- Credit status breakdown
- Risk assessment
- Downloadable Excel reports with timestamps

### Performance Optimization
- Cached member dump for large datasets
- Progress tracking for long-running operations
- Efficient pandas operations

## 📊 Understanding Results

### Registration Check Output

The processed suspense file will include:
- `SCHEME NUMBER` - Populated for matched members
- `MATCHED NAME` - Name from system dump
- `MATCH STATUS` - Type of match (Tier 1/2/3 or No Match)
- `MATCH SIMILARITY` - Similarity score (0-1)

### Credit Check Output

The final report will include:
- `CREDIT STATUS` - One of:
  - `Already Credited` - ⚠️ Risk of double crediting
  - `Not Credited` - ✅ Safe to credit
  - `Not Registered` - Needs registration first
- `ALLOCATION REFERENCE` - Matching transaction reference
- `ALLOCATION BATCH` - Batch number of matching transaction

## ⚠️ Important Notes

### Reversal Detection
Reversed transactions are identified by batch numbers ending with `/1`:
- Original: `PPTY5CH3134729`
- Reversed: `PPTY5CH3134729/1`

Both the original and reversed transactions are removed to prevent false matches.

### Scheme Filtering
Always filter by scheme type as schemes are mutually exclusive. This ensures:
- Accurate matching within the correct scheme
- No cross-scheme false positives
- Proper data segregation

### Data Quality
The accuracy of matching depends on data quality:
- Clean, consistent contact numbers improve Tier 1 matching
- Accurate ID numbers improve Tier 2 matching
- Consistent employer names improve Tier 3 matching

## 🛠️ Troubleshooting

### File Upload Issues
- Ensure files are in Excel (.xlsx, .xls) or CSV format
- Check that all required columns are present
- Verify column names match exactly (case-sensitive)

### No Matches Found
- Verify scheme filter is correct
- Check data quality (missing contacts, IDs, names)
- Review employer name consistency
- Consider data normalization issues

### Performance Issues
- Large member dumps are cached automatically
- First run may be slow, subsequent runs will be faster
- Consider filtering data before upload if possible

### Memory Issues
- Close other applications
- Process schemes separately
- Consider splitting large files

## 📁 Project Structure

```
ppt_compliance_console_gemini/
├── app.py                          # Main application
├── config.py                       # Configuration and constants
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── components/
│   ├── sidebar.py                  # Navigation sidebar
│   └── file_uploader.py           # File upload component
├── modules/
│   ├── home.py                     # Home page
│   ├── check_registration.py      # Registration check module
│   ├── check_credits.py           # Credit check module
│   └── analytics.py               # Analytics dashboard
└── utils/
    ├── data_cleaning.py           # Data normalization utilities
    ├── matching.py                # Fuzzy matching logic
    └── reversal_detection.py     # Reversal detection utilities
```

## 🔐 Data Privacy

- All data processing happens locally on your machine
- No data is sent to external servers
- Files are processed in memory and not permanently stored
- Clear browser cache to remove session data

## 📝 Version History

### v1.0 (Current)
- Initial release
- Two-step reconciliation workflow
- Three-tier matching logic
- Reversal detection
- Analytics dashboard

## 💡 Tips for Best Results

1. **Clean your data first:** Remove obvious duplicates and fix formatting issues
2. **Use consistent naming:** Ensure employer names match between files
3. **Verify IDs:** Check that SSNIT and Ghana Card numbers are accurate
4. **Review statistics:** Pay attention to match rates and adjust if needed
5. **Download results:** Always download and review results before taking action
6. **Process by scheme:** Handle one scheme at a time for better accuracy

## 🆘 Support

For issues or questions:
1. Check the **Quick Guide** in the sidebar
2. Review the expandable sections on the Home page
3. Examine match statistics for insights
4. Review this README for detailed information

## 📄 License

Internal use only - PPT Compliance Console

---

**Built with ❤️ using Streamlit**
