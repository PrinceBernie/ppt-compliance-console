"""
Surcharges Module
Calculates surcharges for defaulters (members who have missed contributions)
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from components.file_uploader import upload_file, display_dataframe_preview, download_button
import config


def calculate_ops_surcharge(contribution_amount, num_months):
    """
    Calculate surcharge when monthly contributions are the same.
    
    Args:
        contribution_amount: Monthly contribution amount
        num_months: Number of months in default
        
    Returns:
        Tuple of (amount_due, surcharge)
    """
    A = 0  # Running amount due
    s = 0.03  # Surcharge percentage (3%)
    
    for i in range(int(num_months)):
        A_due = (1 + s) * (A + contribution_amount)
        A = A_due
    
    surcharge = A_due - (contribution_amount * num_months)
    
    return round(A_due, 2), round(surcharge, 2)


def calculate_different_surcharge(contribution_amount, num_months):
    """
    Calculate surcharge when monthly contributions are not the same.
    
    Args:
        contribution_amount: Contribution amount for this specific month
        num_months: Number of months the contribution has been in default
        
    Returns:
        Tuple of (surcharge, amount_due)
    """
    A = contribution_amount
    s = 0.03  # Surcharge percentage (3%)
    
    for i in range(num_months):
        A_due = (1 + s) * A
        A = A_due
    
    surcharge = A_due - contribution_amount
    
    return round(surcharge, 2), round(A_due, 2)


def run_surcharges():
    """
    Main function for Surcharges module.
    """
    st.title("📊 Surcharge Calculator")
    st.markdown("Calculate surcharges for defaulters based on contribution amounts and months in default.")
    
    st.markdown("---")
    
    # File upload section
    st.subheader("📄 Upload Defaulters Data")
    
    defaulters_df = upload_file(
        label="Upload Defaulters Surcharge File",
        key="defaulters_surcharge_upload",
        help_text="Excel or CSV file with defaulters data (must include Contribution Amount and Number of Months columns)",
        required_columns=None  # Will validate manually
    )
    
    if defaulters_df is None:
        st.info("👆 Please upload a file to continue")
        
        # Display expected format
        with st.expander("📋 Expected File Format", expanded=True):
            st.markdown("""
            Your file should contain the following columns:
            
            **Required Columns:**
            - **Contribution Amount Defaulted** or **Contribution Amount**: The amount owed for each contribution
            - **Number of Months Run** or **Number of Months**: How many months the contribution has been outstanding
            
            **Optional Columns:**
            - **Member Name**: Name of the member
            - **Scheme Number**: Member's scheme/registration number
            - **Employer**: Employer name
            - Any other relevant information
            
            **Note:** The calculation applies a 3% monthly surcharge compounded over the default period.
            """)
            
            # Show sample format
            sample_data = pd.DataFrame({
                'Member Name': ['John Doe', 'Jane Smith', 'Bob Johnson'],
                'Scheme Number': ['SCH001', 'SCH002', 'SCH003'],
                'Employer': ['Company A', 'Company B', 'Company C'],
                'Contribution Amount Defaulted': [5000.00, 7500.00, 3200.00],
                'Number of Months Run': [3, 6, 12]
            })
            st.dataframe(sample_data, use_container_width=True)
        
        return
    
    # Display preview of uploaded data
    display_dataframe_preview(defaulters_df, "📊 Uploaded Data Preview", max_rows=10)
    
    st.markdown("---")
    
    # Column mapping section
    st.subheader("🔧 Configure Column Mapping")
    
    st.info("Select the columns from your file that contain the contribution amount and number of months")
    
    available_columns = defaulters_df.columns.tolist()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Auto-detect contribution amount column
        contribution_col_default = None
        for col in available_columns:
            if 'contribution' in col.lower() and 'amount' in col.lower():
                contribution_col_default = col
                break
        
        contribution_column = st.selectbox(
            "Contribution Amount Column",
            options=available_columns,
            index=available_columns.index(contribution_col_default) if contribution_col_default else 0,
            help="Select the column containing contribution amounts"
        )
    
    with col2:
        # Auto-detect months column
        months_col_default = None
        for col in available_columns:
            if 'month' in col.lower() and ('number' in col.lower() or 'run' in col.lower()):
                months_col_default = col
                break
        
        months_column = st.selectbox(
            "Number of Months Column",
            options=available_columns,
            index=available_columns.index(months_col_default) if months_col_default else 0,
            help="Select the column containing the number of months in default"
        )
    
    st.markdown("---")
    
    # Calculation method selection
    st.subheader("⚙️ Calculation Method")
    
    calculation_method = st.radio(
        "Select calculation method:",
        options=[
            "Same Monthly Contributions (OPS Method)",
            "Different Monthly Contributions"
        ],
        help="""
        - **Same Monthly Contributions**: Use when the member's contribution amount is the same each month. Amount compounds over all months.
        - **Different Monthly Contributions**: Use when each contribution period may have different amounts. Each amount is calculated independently.
        """
    )
    
    # Display the formula
    with st.expander("ℹ️ How the calculation works", expanded=False):
        if calculation_method == "Same Monthly Contributions (OPS Method)":
            st.markdown("""
            **OPS Surcharge Method (Same Monthly Contributions)**
            
            This method assumes:
            - Monthly contribution amount (C) is constant
            - Surcharge rate (s) = 3% per month
            - Running amount (A) compounds each month
            
            **Formula:**
            ```
            For each month i from 1 to N:
                A_due = (1 + s) × (A + C)
                A = A_due
            
            Surcharge = A_due - (C × N)
            ```
            
            **Example:** If C = 5,000 and N = 3 months:
            - Month 1: A = (1.03)×(0 + 5,000) = 5,150
            - Month 2: A = (1.03)×(5,150 + 5,000) = 10,454.50
            - Month 3: A = (1.03)×(10,454.50 + 5,000) = 15,918.14
            - Surcharge = 15,918.14 - (5,000×3) = 918.14
            """)
        else:
            st.markdown("""
            **Different Contributions Method**
            
            This method is used when:
            - Each contribution period may have a different amount
            - Each contribution is calculated separately
            - Surcharge rate (s) = 3% per month
            
            **Formula:**
            ```
            For each month i from 1 to M (months in default):
                A_due = (1 + s) × A
                A = A_due
            
            Starting with A = C (contribution amount)
            Surcharge = A_due - C
            ```
            
            **Example:** If C = 5,000 and M = 3 months:
            - Month 1: A = (1.03)×5,000 = 5,150
            - Month 2: A = (1.03)×5,150 = 5,304.50
            - Month 3: A = (1.03)×5,304.50 = 5,463.64
            - Surcharge = 5,463.64 - 5,000 = 463.64
            """)
    
    st.markdown("---")
    
    # Calculate button
    if st.button("🚀 Calculate Surcharges", type="primary", use_container_width=True):
        
        # Validate columns exist
        if contribution_column not in defaulters_df.columns:
            st.error(f"❌ Column '{contribution_column}' not found in the uploaded file")
            return
        
        if months_column not in defaulters_df.columns:
            st.error(f"❌ Column '{months_column}' not found in the uploaded file")
            return
        
        # Validate data types
        try:
            defaulters_df[contribution_column] = pd.to_numeric(defaulters_df[contribution_column], errors='coerce')
            defaulters_df[months_column] = pd.to_numeric(defaulters_df[months_column], errors='coerce')
        except Exception as e:
            st.error(f"❌ Error converting columns to numeric: {str(e)}")
            return
        
        # Check for missing values
        missing_contribution = defaulters_df[contribution_column].isna().sum()
        missing_months = defaulters_df[months_column].isna().sum()
        
        if missing_contribution > 0 or missing_months > 0:
            st.warning(f"⚠️ Found {missing_contribution} missing contribution amounts and {missing_months} missing month values. These will be skipped.")
        
        with st.spinner("Calculating surcharges..."):
            
            # Create a copy for results
            result_df = defaulters_df.copy()
            
            # Initialize result columns (Surcharge before Amount Due)
            result_df['Surcharge'] = 0.0
            result_df['Amount Due'] = 0.0
            result_df['Calculation Status'] = 'Pending'
            
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            total_records = len(result_df)
            successful_calcs = 0
            failed_calcs = 0
            
            # Perform calculations
            for idx, row in result_df.iterrows():
                # Update progress
                progress = (idx + 1) / total_records
                progress_bar.progress(progress)
                status_text.text(f"Processing record {idx + 1} of {total_records:,}...")
                
                contribution = row[contribution_column]
                months = row[months_column]
                
                # Skip if missing values
                if pd.isna(contribution) or pd.isna(months):
                    result_df.at[idx, 'Calculation Status'] = 'Missing Data'
                    failed_calcs += 1
                    continue
                
                # Skip if invalid values
                if contribution <= 0 or months <= 0:
                    result_df.at[idx, 'Calculation Status'] = 'Invalid Values'
                    failed_calcs += 1
                    continue
                
                try:
                    if calculation_method == "Same Monthly Contributions (OPS Method)":
                        amount_due, surcharge = calculate_ops_surcharge(contribution, months)
                    else:
                        surcharge, amount_due = calculate_different_surcharge(contribution, months)
                    
                    result_df.at[idx, 'Surcharge'] = surcharge
                    result_df.at[idx, 'Amount Due'] = amount_due
                    result_df.at[idx, 'Calculation Status'] = 'Success'
                    successful_calcs += 1
                    
                except Exception as e:
                    result_df.at[idx, 'Calculation Status'] = f'Error: {str(e)}'
                    failed_calcs += 1
            
            progress_bar.empty()
            status_text.empty()
            
            # Display results
            st.success("✅ Surcharge calculation completed!")
            
            st.markdown("---")
            st.subheader("📊 Calculation Statistics")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Records", total_records)
            
            with col2:
                st.metric("Successful", successful_calcs, 
                         delta=f"{(successful_calcs/total_records*100):.1f}%")
            
            with col3:
                st.metric("Failed/Skipped", failed_calcs,
                         delta=f"{(failed_calcs/total_records*100):.1f}%",
                         delta_color="inverse")
            
            # Summary statistics
            if successful_calcs > 0:
                st.markdown("---")
                st.subheader("💰 Financial Summary")
                
                successful_records = result_df[result_df['Calculation Status'] == 'Success']
                
                total_contributions = successful_records[contribution_column].sum()
                total_surcharges = successful_records['Surcharge'].sum()
                total_amount_due = successful_records['Amount Due'].sum()
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Original Contributions", f"GHS {total_contributions:,.2f}")
                
                with col2:
                    st.metric("Total Surcharges", f"GHS {total_surcharges:,.2f}",
                             help="Total surcharge amount calculated")
                
                with col3:
                    st.metric("Total Amount Due", f"GHS {total_amount_due:,.2f}",
                             help="Original contributions + surcharges")
                
                # Average surcharge percentage
                avg_surcharge_pct = (total_surcharges / total_contributions * 100) if total_contributions > 0 else 0
                st.info(f"📈 Average surcharge rate: {avg_surcharge_pct:.2f}% of original contributions")
            
            # Preview results
            st.markdown("---")
            display_dataframe_preview(result_df, "Results Preview", max_rows=20)
            
            # Show failed records if any
            if failed_calcs > 0:
                failed_records = result_df[result_df['Calculation Status'] != 'Success']
                
                with st.expander(f"⚠️ View {failed_calcs} Failed/Skipped Records"):
                    st.dataframe(failed_records, use_container_width=True)
            
            # Download button
            st.markdown("---")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            method_suffix = "ops" if calculation_method == "Same Monthly Contributions (OPS Method)" else "different"
            filename = f"surcharge_calculation_{method_suffix}_{timestamp}.xlsx"
            
            download_button(result_df, filename, "📥 Download Surcharge Report")
            
            # Store in session state
            st.session_state['surcharge_results'] = result_df
            
            st.success(f"✅ Results saved to session. Use the download button above to get the complete report.")
