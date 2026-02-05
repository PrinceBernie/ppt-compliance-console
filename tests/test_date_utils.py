import sys
import os
import pandas as pd
from datetime import datetime

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.data_cleaning import parse_date
import config

def test_date_standardization():
    print("Running Date Standardization Tests...\n")
    
    test_cases = [
        ("Jan 25", datetime(2025, 1, 1)),
        ("Jan-25", datetime(2025, 1, 1)),
        ("January 2025", datetime(2025, 1, 1)),
        ("01/01/2025", datetime(2025, 1, 1)),
        ("Feb 24", datetime(2024, 2, 1)),
        ("March 2023", datetime(2023, 3, 1)),
        ("Invalid Date", None),
        ("Reference for Jan 25", None), # Should fail as clean_reference handles stripping
        ("", None),
        (None, None)
    ]
    
    failed = False
    print(f"{'Input':<20} | {'Output':<30} | {'Status'}")
    print("-" * 65)
    
    for input_str, expected in test_cases:
        result = parse_date(input_str)
        # Compare as timestamps
        if expected is None:
            match = result is None
        else:
            match = result == pd.Timestamp(expected)
            
        status = "✅ PASS" if match else "❌ FAIL"
        if not match:
            failed = True
            
        print(f"{str(input_str):<20} | {str(result):<30} | {status}")
        
    if not failed:
        print("\n🎉 All date parsing tests passed!")
    else:
        print("\n⚠️ Some date parsing tests failed.")
        
def test_matching_simulation():
    print("\nRunning Matching Simulation...\n")
    
    # Suspense Data (Contribution Month as specific format)
    suspense_df = pd.DataFrame({
        'SCHEME NUMBER': ['123', '456', '789'],
        'CONTRIBUTION MONTH': ['Jan 25', '01/01/2025', 'Feb 25']
    })
    
    # Allocation Data (Reference as text)
    allocation_df = pd.DataFrame({
        'SCHEME NUMBER': ['123', '456', '789'],
        'Reference_CLEAN': ['January 2025', 'Jan 25', 'February 2025']
    })
    
    print("Suspense DataFrame:")
    print(suspense_df)
    print("\nAllocation DataFrame:")
    print(allocation_df)
    print("-" * 30)
    
    # Simulate processing
    suspense_df['parsed_date'] = suspense_df['CONTRIBUTION MONTH'].apply(parse_date)
    allocation_df['Reference_DATE'] = allocation_df['Reference_CLEAN'].apply(parse_date)
    
    matches = 0
    for idx, row in suspense_df.iterrows():
        s_date = row['parsed_date']
        matches_found = allocation_df[
            (allocation_df['SCHEME NUMBER'] == row['SCHEME NUMBER']) &
            (allocation_df['Reference_DATE'] == s_date)
        ]
        
        if not matches_found.empty:
            print(f"Match found for {row['SCHEME NUMBER']} ({row['CONTRIBUTION MONTH']})")
            matches += 1
        else:
            print(f"NO match for {row['SCHEME NUMBER']} ({row['CONTRIBUTION MONTH']})")
            
    if matches == 3:
        print("\n🎉 All simulation matches successful!")
    else:
        print(f"\n⚠️ Expected 3 matches, got {matches}")

if __name__ == "__main__":
    test_date_standardization()
    test_matching_simulation()
