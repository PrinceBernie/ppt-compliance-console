# Quick Start Guide

## 🚀 Running the Application

The application is now running! You should see:
```
Local URL: http://localhost:8501
Network URL: http://192.168.21.94:8501
```

Open your web browser and navigate to **http://localhost:8501**

## 📝 Step-by-Step Usage

### STEP 1: Check Registration

1. **Navigate** to "Check Registration" in the sidebar
2. **Upload Suspense Data:**
   - Click "Upload Suspense Data"
   - Select your Excel/CSV file with suspense contributions
   - Verify the file loads successfully (you'll see record count)

3. **Upload Member Dump:**
   - Click "Upload Member Dump"
   - Select your system member dump file
   - This file will be cached for performance

4. **Select Scheme:**
   - Choose the scheme type from the dropdown
   - This filters the member dump to only that scheme

5. **Run the Check:**
   - Click "🚀 Run Registration Check"
   - Watch the progress bar as it processes
   - Review the match statistics

6. **Download Results:**
   - Preview the results table
   - Click "📥 Download Registration Check Results"
   - Save the file for Step 2

### STEP 2: Check Credits

1. **Navigate** to "Check Credits" in the sidebar
2. **Upload Processed Suspense:**
   - Upload the file you downloaded from Step 1
   - Verify scheme numbers are populated

3. **Upload Allocation Dump:**
   - Upload your contribution allocation report
   - This contains all credited transactions

4. **Select Scheme:**
   - Choose the same scheme type as Step 1

5. **Run the Check:**
   - Click "🚀 Run Credit Check"
   - Review cleaning statistics (withdrawals, reversals removed)
   - Check credit match results

6. **Review Risky Records:**
   - Expand "View Already Credited Records"
   - These members should NOT be credited again

7. **Download Final Report:**
   - Click "📥 Download Credit Check Results"
   - Use this report for your final processing

### STEP 3: View Analytics

1. **Navigate** to "Analytics" in the sidebar
2. **Review Statistics:**
   - Registration match rates
   - Credit status breakdown
   - Risk assessment
   - Combined insights

## ⚠️ Important Reminders

### Data Quality Tips
- **Clean your data first:** Remove obvious duplicates
- **Consistent naming:** Ensure employer names match
- **Verify IDs:** Check SSNIT and Ghana Card accuracy
- **One scheme at a time:** Process each scheme separately

### Understanding Results

**Registration Check Output:**
- `SCHEME NUMBER` - Populated for matched members
- `MATCHED NAME` - Name from system dump
- `MATCH STATUS` - How the match was found:
  - "Matched - Contact & Name" (Tier 1)
  - "Matched - ID Number" (Tier 2)
  - "Matched - Name & Employer" (Tier 3)
  - "No Match Found"

**Credit Check Output:**
- `CREDIT STATUS`:
  - "Already Credited" ⚠️ - DO NOT credit again
  - "Not Credited" ✅ - Safe to credit
  - "Not Registered" - Register first

### Common Issues

**Problem:** No matches found
**Solution:** 
- Check scheme filter is correct
- Verify data quality (contacts, IDs, names)
- Review employer name consistency

**Problem:** File upload fails
**Solution:**
- Verify file format (Excel or CSV)
- Check column names match exactly
- Ensure all required columns exist

**Problem:** Too many "Already Credited"
**Solution:**
- This is expected! It's preventing double crediting
- Only process "Not Credited" members
- Review the risky records carefully

## 📊 Sample Data Format

### Suspense Data Columns (Required)
```
EMPLOYER | MEMBER NAME | SCHEME NUMBER | SSNIT NUMBER | GH. CARD NUMBER | CONTACT | CONTRIBUTION MONTH | 5% CONTRIBUTION | SCHEME
```

### Member Dump Columns (Required)
```
First name | [Middle name] | [Last name] | Member number | [Scheme number] | Mobile | S s n i t | Id number | [Scheme name] | Group name
```

### Allocation Dump Columns (Required)
```
Batch number | Product type | [Scheme number] | Reference | [Contribution] | [Withdrawal]
```

## 🎯 Best Practices

1. **Always download results** after each step
2. **Review statistics** before downloading
3. **Check risky records** in credit check
4. **Process one scheme at a time**
5. **Keep backups** of original files
6. **Document your process** for audit trail

## 💡 Tips for Success

- **First run:** Start with a small test dataset
- **Verify matches:** Spot-check a few matched records
- **Review no-matches:** Understand why they didn't match
- **Use analytics:** Check the dashboard for insights
- **Save reports:** Keep timestamped reports for records

## 🆘 Need Help?

- Check the **Home** page for detailed information
- Expand the **Quick Guide** in the sidebar
- Review match statistics for insights
- Read the **README.md** for technical details

---

**You're all set! Start with Check Registration and work through the workflow.**
