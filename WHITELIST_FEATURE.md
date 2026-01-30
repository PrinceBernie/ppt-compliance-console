# PPT Compliance Console - Whitelist Feature

## Overview
The PPT Compliance Console now supports an optional **Whitelist** feature to handle members whose names vary between the schedule and the system. This eliminates false mismatches caused by name variations.

## What's New

### 1. Cached Member Dump
- The system member dump (`Members.xlsx`) is now **loaded from the local project folder** instead of being uploaded every time
- Location: `D:\APPS\ppt_compliance_console\files\Members.xlsx`
- This file is **cached** for performance and only needs to be updated when the member database changes
- **No need to upload this file anymore** - it's automatically loaded on each run

### 2. Optional Whitelist Upload
- You can now upload an **optional whitelist file** containing pre-approved name mappings
- The whitelist helps match members whose names are spelled differently in the schedule vs. the system
- **When to use**: If you notice consistent mismatches for certain members due to name variations

## Whitelist File Format

The whitelist file must be an Excel (.xlsx) or CSV file with the following columns:

| Column Name | Description | Example |
|------------|-------------|---------|
| **Current Employer** | Current employer name | ABC Company |
| **Member Name [Schedule]** | Name as it appears in the schedule | John Doe Smith |
| **Member Name [System]** | Name as it appears in the system | Smith John Doe |
| **Scheme Number** | Member's scheme number | SCH12345 |
| **Previous Employer** | Previous employer (if applicable) | XYZ Corp |
| **SSNIT Number** | SSNIT number | C123456789 |
| **Ghana Card** | Ghana Card number | GHA-123456789-0 |
| **Contact** | Contact number | 0241234567 |

### Sample Template
A sample whitelist template is available at:
```
D:\APPS\ppt_compliance_console\files\Whitelist_Template.csv
```

## How It Works

### Matching Priority (in order)
1. **Whitelist Match** (if whitelist is uploaded)
   - Checks if the member has a pre-approved name mapping
   - Uses exact matching for employer and schedule name
   - Maps to the system name from the whitelist
   
2. **Tier 1: Contact & Name Match**
   - Matches by phone number with fuzzy name verification
   - Threshold: 70% similarity
   
3. **Tier 2: ID Number Match**
   - Bidirectional matching using SSNIT and Ghana Card numbers
   - Threshold: 70% similarity
   
4. **Tier 3: Name & Employer Match**
   - Matches by name within the same employer group
   - Threshold: 90% similarity (higher for accuracy)

## Usage Instructions

### Step 1: Ensure Member Dump is in Place
1. Make sure `Members.xlsx` is in the `files` folder
2. The application will automatically load it when you run Check Registration

### Step 2: Upload Suspense Data
1. Navigate to **Check Registration** module
2. Upload your suspense data file (required)

### Step 3: Upload Whitelist (Optional)
1. If you have known name variations, prepare a whitelist file
2. Use the template as a guide
3. Upload the whitelist file in the second column
4. The system will validate the file format

### Step 4: Run Matching
1. Select the scheme type
2. Click "Run Registration Check"
3. The system will:
   - First check the whitelist for matches
   - Then fall back to the three-tier fuzzy matching
   - Display statistics showing whitelist matches separately

## Match Statistics

After processing, you'll see:
- **Whitelist Matches**: Members matched via the whitelist
- **Tier 1 Matches**: Contact & Name matches
- **Tier 2 Matches**: ID Number matches
- **Tier 3 Matches**: Name & Employer matches
- **No Matches**: Records that couldn't be matched

## Benefits

✅ **Efficiency**: No need to upload the large member dump file every time  
✅ **Accuracy**: Whitelist ensures known name variations are matched correctly  
✅ **Performance**: Cached member dump loads faster  
✅ **Flexibility**: Whitelist is optional - use it only when needed  
✅ **Transparency**: Clear statistics show which matches came from the whitelist  

## Troubleshooting

### Member Dump Not Found
**Error**: "Member dump file not found"  
**Solution**: Ensure `Members.xlsx` is placed in `D:\APPS\ppt_compliance_console\files\`

### Whitelist Validation Failed
**Error**: "Whitelist file is missing required columns"  
**Solution**: Check that your whitelist file has all 8 required columns (see format above)

### No Whitelist Matches
**Issue**: Whitelist uploaded but no matches found  
**Possible Causes**:
- Name/employer spelling doesn't match exactly
- Check for extra spaces or special characters
- Verify the employer name matches between schedule and whitelist

## Technical Details

### Files Modified
- `utils/file_loader.py` - New utility for loading cached files
- `utils/matching.py` - Added whitelist matching logic
- `modules/check_registration.py` - Updated to use cached member dump and whitelist
- `config.py` - Added whitelist match status

### Caching
The member dump is cached using Streamlit's `@st.cache_data` decorator, which means:
- First load reads from disk
- Subsequent loads use cached data (instant)
- Cache clears when the file is modified or the app restarts

---

**Last Updated**: 2026-01-30  
**Version**: 2.0
