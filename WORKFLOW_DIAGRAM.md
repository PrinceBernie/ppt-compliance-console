# PPT Compliance Console - Workflow Diagram

## 📊 Complete Reconciliation Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                    LEGACY SUSPENSE CLEARING WORKFLOW                │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  STEP 1: CHECK REGISTRATION                                         │
│  Purpose: Identify which suspense members are already registered    │
└─────────────────────────────────────────────────────────────────────┘

    INPUT FILES:
    ┌──────────────────────┐         ┌──────────────────────┐
    │  Suspense Data       │         │  Member Dump         │
    │  ─────────────       │         │  ───────────         │
    │  • EMPLOYER          │         │  • First name        │
    │  • MEMBER NAME       │         │  • [Middle name]     │
    │  • CONTACT           │         │  • [Last name]       │
    │  • SSNIT NUMBER      │         │  • Mobile            │
    │  • GH. CARD NUMBER   │         │  • S s n i t         │
    │  • CONTRIBUTION MONTH│         │  • Id number         │
    │  • 5% CONTRIBUTION   │         │  • [Scheme name]     │
    │  • SCHEME            │         │  • Group name        │
    └──────────────────────┘         └──────────────────────┘
              │                                 │
              └────────────┬────────────────────┘
                           ▼
              ┌────────────────────────┐
              │  SELECT SCHEME FILTER  │
              │  (from [Scheme name])  │
              └────────────────────────┘
                           │
                           ▼
    ┌─────────────────────────────────────────────────────┐
    │         THREE-TIER FALLBACK MATCHING                │
    ├─────────────────────────────────────────────────────┤
    │                                                     │
    │  TIER 1: Contact Number Match (70% name similarity) │
    │  ├─ Match suspense CONTACT → member Mobile         │
    │  └─ Verify with fuzzy name match                   │
    │                                                     │
    │  TIER 2: ID Number Match (70% name similarity)      │
    │  ├─ Suspense SSNIT → Member SSNIT                  │
    │  ├─ Suspense SSNIT → Member ID                     │
    │  ├─ Suspense Ghana Card → Member SSNIT             │
    │  ├─ Suspense Ghana Card → Member ID                │
    │  └─ Verify with fuzzy name match                   │
    │                                                     │
    │  TIER 3: Name + Employer Match (80% similarity)     │
    │  ├─ Match name within same employer group          │
    │  └─ Higher threshold for accuracy                  │
    │                                                     │
    └─────────────────────────────────────────────────────┘
                           │
                           ▼
    ┌─────────────────────────────────────────────────────┐
    │              POPULATE RESULTS                       │
    │  • SCHEME NUMBER (from matched member)              │
    │  • MATCHED NAME (from system dump)                  │
    │  • MATCH STATUS (Tier 1/2/3 or No Match)            │
    │  • MATCH SIMILARITY (0.0 - 1.0)                     │
    └─────────────────────────────────────────────────────┘
                           │
                           ▼
    ┌─────────────────────────────────────────────────────┐
    │         DOWNLOAD PROCESSED SUSPENSE DATA            │
    │  suspense_registration_check_[SCHEME]_[DATE].xlsx  │
    └─────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────┐
│  STEP 2: CHECK CREDITS                                              │
│  Purpose: Verify if members have already been credited             │
└─────────────────────────────────────────────────────────────────────┘

    INPUT FILES:
    ┌──────────────────────┐         ┌──────────────────────┐
    │  Processed Suspense  │         │  Allocation Dump     │
    │  (from Step 1)       │         │  ───────────────     │
    │  ─────────────       │         │  • Batch number      │
    │  • All columns       │         │  • Product type      │
    │  • SCHEME NUMBER ✓   │         │  • [Scheme number]   │
    │  • MATCHED NAME ✓    │         │  • Reference         │
    │  • MATCH STATUS ✓    │         │  • [Contribution]    │
    └──────────────────────┘         │  • [Withdrawal]      │
              │                       └──────────────────────┘
              │                                 │
              └────────────┬────────────────────┘
                           ▼
              ┌────────────────────────┐
              │  SELECT SCHEME FILTER  │
              │  (from Product type)   │
              └────────────────────────┘
                           │
                           ▼
    ┌─────────────────────────────────────────────────────┐
    │       CLEAN ALLOCATION DUMP                         │
    ├─────────────────────────────────────────────────────┤
    │                                                     │
    │  1. REMOVE WITHDRAWALS                              │
    │     └─ Filter out records with "withdrawal" in      │
    │        Reference field                              │
    │                                                     │
    │  2. DETECT & REMOVE REVERSALS                       │
    │     ├─ Find batch numbers ending with /1           │
    │     ├─ Example: PPTY5CH3134729/1                   │
    │     ├─ Find original: PPTY5CH3134729               │
    │     └─ Remove BOTH original and reversed           │
    │                                                     │
    │  3. CLEAN REFERENCE FIELD                           │
    │     └─ Remove "Payment for " prefix                │
    │        Example: "Payment for January 2026"         │
    │                → "January 2026"                     │
    │                                                     │
    └─────────────────────────────────────────────────────┘
                           │
                           ▼
    ┌─────────────────────────────────────────────────────┐
    │         MATCH SCHEME NUMBER + MONTH                 │
    │  For each suspense record:                          │
    │  1. Check if SCHEME NUMBER exists (registered?)     │
    │  2. Match SCHEME NUMBER + CONTRIBUTION MONTH        │
    │     against allocation dump                         │
    │  3. Determine credit status                         │
    └─────────────────────────────────────────────────────┘
                           │
                           ▼
    ┌─────────────────────────────────────────────────────┐
    │              POPULATE RESULTS                       │
    │  • CREDIT STATUS:                                   │
    │    - "Already Credited" ⚠️ (found in allocation)    │
    │    - "Not Credited" ✅ (safe to credit)             │
    │    - "Not Registered" (no scheme number)            │
    │  • ALLOCATION REFERENCE (if found)                  │
    │  • ALLOCATION BATCH (if found)                      │
    └─────────────────────────────────────────────────────┘
                           │
                           ▼
    ┌─────────────────────────────────────────────────────┐
    │         RISK ASSESSMENT                             │
    │  • Count already credited (HIGH RISK)               │
    │  • Count not credited (SAFE)                        │
    │  • Count not registered (NEED REGISTRATION)         │
    │  • Calculate risk percentage                        │
    └─────────────────────────────────────────────────────┘
                           │
                           ▼
    ┌─────────────────────────────────────────────────────┐
    │         DOWNLOAD FINAL REPORT                       │
    │  suspense_credit_check_[SCHEME]_[DATE].xlsx        │
    └─────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────┐
│  STEP 3: ANALYTICS DASHBOARD                                        │
│  Purpose: Review statistics and insights                            │
└─────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────┐
    │  REGISTRATION ANALYTICS                             │
    │  • Total matches by tier                            │
    │  • Match rate percentage                            │
    │  • Match status distribution                        │
    │  • Average similarity scores                        │
    └─────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────┐
    │  CREDIT ANALYTICS                                   │
    │  • Already credited count                           │
    │  • Not credited count                               │
    │  • Not registered count                             │
    │  • Risk assessment                                  │
    └─────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────┐
    │  COMBINED INSIGHTS                                  │
    │  • Reconciliation funnel                            │
    │  • End-to-end statistics                            │
    │  • Success rates                                    │
    └─────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────┐
│  FINAL OUTPUT: ACTIONABLE REPORT                                    │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ✅ SAFE TO CREDIT                                                  │
│     Members with "Not Credited" status                              │
│     → Process these contributions                                   │
│                                                                     │
│  ⚠️  ALREADY CREDITED                                               │
│     Members with "Already Credited" status                          │
│     → DO NOT process (prevents double crediting)                    │
│                                                                     │
│  📋 NOT REGISTERED                                                  │
│     Members with "Not Registered" status                            │
│     → Register first, then credit                                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════

KEY SUCCESS METRICS:

┌────────────────────────────────────────────────────────────┐
│  BEFORE: Manual Process                                    │
│  • Days of manual matching                                 │
│  • High risk of double crediting                           │
│  • Error-prone data entry                                  │
│  • No audit trail                                          │
└────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────┐
│  AFTER: Automated Console                                  │
│  • Minutes to process thousands of records                 │
│  • Automated double-credit prevention                      │
│  • Consistent, accurate matching                           │
│  • Complete audit trail with downloadable reports          │
│  • Risk assessment and analytics                           │
└────────────────────────────────────────────────────────────┘

```

## 🎯 Data Flow Summary

1. **Suspense Data** + **Member Dump** → **Registration Check** → **Populated Scheme Numbers**
2. **Processed Suspense** + **Allocation Dump** → **Credit Check** → **Final Report**
3. **All Results** → **Analytics Dashboard** → **Insights & Statistics**

## 🔐 Data Integrity Safeguards

- ✅ Three-tier matching prevents false positives
- ✅ Fuzzy matching handles data quality issues
- ✅ Reversal detection prevents false credit matches
- ✅ Withdrawal filtering removes noise
- ✅ Scheme filtering ensures mutual exclusivity
- ✅ Risk assessment highlights dangerous records
- ✅ Audit trail through downloadable reports

## 💡 Best Practice Workflow

```
START
  ↓
Prepare Data Files
  ↓
Run Registration Check (Step 1)
  ↓
Review Match Statistics
  ↓
Download & Inspect Results
  ↓
Run Credit Check (Step 2)
  ↓
Review Risk Assessment
  ↓
Identify Risky Records
  ↓
Download Final Report
  ↓
View Analytics Dashboard
  ↓
Process Safe Records Only
  ↓
END
```
