# Quick Reference: Whitelist Feature

## What Changed?

### ✅ Member Dump Upload - REMOVED
- **Before**: Had to upload Members.xlsx every time
- **Now**: Automatically loaded from `files/Members.xlsx`
- **Benefit**: Faster, more efficient, no repeated uploads

### ✅ Whitelist Upload - NEW (Optional)
- **Purpose**: Handle members with name variations between schedule and system
- **When to use**: When fuzzy matching fails due to different name spellings
- **Location**: Upload in the Check Registration module (right column)

## Whitelist File Columns (Required)

```
1. Current Employer
2. Member Name [Schedule]    ← Name in the suspense/schedule file
3. Member Name [System]       ← Name in the member dump
4. Scheme Number
5. Previous Employer
6. SSNIT Number
7. Ghana Card
8. Contact
```

## Example Whitelist Entry

| Current Employer | Member Name [Schedule] | Member Name [System] | Scheme Number |
|-----------------|------------------------|---------------------|---------------|
| ABC Company | John Doe Smith | Smith John Doe | SCH12345 |

This tells the system: "When you see 'John Doe Smith' from 'ABC Company' in the schedule, match it to 'Smith John Doe' in the system."

## Matching Order (Priority)

1. **Whitelist** ← Checked first (if uploaded)
2. **Contact & Name** (70% threshold)
3. **ID Numbers** (70% threshold)  
4. **Name & Employer** (90% threshold)

## Quick Start

1. Ensure `Members.xlsx` is in `files/` folder ✓
2. Upload suspense data (required)
3. Upload whitelist (optional - only if needed)
4. Select scheme and run

## Template Location

Sample whitelist template:
```
D:\APPS\ppt_compliance_console\files\Whitelist_Template.csv
```

## Tips

💡 **Whitelist is optional** - only use it when you have known name mismatches  
💡 **Exact matching** - Employer and schedule name must match exactly  
💡 **Case insensitive** - System normalizes text automatically  
💡 **Statistics** - Whitelist matches shown separately in results  

---
For detailed documentation, see: `WHITELIST_FEATURE.md`
