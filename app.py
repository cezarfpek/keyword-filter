import streamlit as st
import pandas as pd
import io

def main():
    st.title("CSV Keyword Filter")
    
    # Instructions section
    with st.expander("📋 How to Use This App", expanded=True):
        st.markdown("""
        ### Instructions:
        1. **Upload a CSV file** using the file uploader below
        2. **Select a column** from your data that you want to filter on
        3. **Enter keywords** separated by commas (e.g., apple,orange,banana)
        4. **Choose a filter method**:
           - *Contains any keyword*: Shows rows that contain at least one of your keywords
           - *Contains all keywords*: Shows only rows that contain all of your keywords
        5. **Click "Filter Data"** to see your filtered results
        6. You can **download the filtered data** using the download button that appears
        
        **Note**: All filtering is case-insensitive, so "Apple" will match "apple" or "APPLE".
        """)
    
    st.markdown("---")
    
    # File upload section
    st.subheader("Step 1: Upload Your CSV File")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        # Read the CSV file
        try:
            df = pd.read_csv(uploaded_file)
            st.success("✅ File successfully uploaded!")
            
            # Display sample of the original dataframe
            st.subheader("Preview of Your Data")
            st.dataframe(df.head(5))
            st.caption(f"Showing first 5 rows of {len(df)} total rows and {len(df.columns)} columns")
            
            # Column selector
            st.subheader("Step 2: Select a Column to Filter")
            column_options = df.columns.tolist()
            selected_column = st.selectbox("Which column contains the text you want to filter by?", column_options)
            
            # Show sample values from selected column
            unique_values = df[selected_column].astype(str).unique()
            sample_values = ", ".join(unique_values[:5]) + ("..." if len(unique_values) > 5 else "")
            st.caption(f"Sample values in this column: {sample_values}")
            
            # Keyword input
            st.subheader("Step 3: Enter Keywords for Filtering")
            keyword_input = st.text_input(
                "Enter keywords separated by commas:",
                placeholder="e.g., apple,orange,banana"
            )
            
            if keyword_input:
                # Split the input into a list of keywords and strip whitespace
                keywords = [k.strip() for k in keyword_input.split(",")]
                st.caption(f"You've entered {len(keywords)} keywords: {', '.join(keywords)}")
                
                # Filter method selector
                st.subheader("Step 4: Choose Filter Method")
                filter_method = st.radio(
                    "How do you want to filter?",
                    ["Contains any keyword", "Contains all keywords"],
                    help="'Any' is more inclusive, 'All' is more restrictive"
                )
                
                # Filter button
                st.subheader("Step 5: Apply Filter")
                if st.button("🔍 Filter Data", use_container_width=True):
                    if selected_column in df.columns:
                        with st.spinner("Filtering your data..."):
                            # Ensure the column data is string type for filtering
                            df[selected_column] = df[selected_column].astype(str)
                            
                            if filter_method == "Contains any keyword":
                                # Filter rows that contain any of the keywords
                                filtered_df = df[df[selected_column].str.contains('|'.join(keywords), case=False)]
                            else:
                                # Filter rows that contain all keywords
                                filtered_df = df.copy()
                                for keyword in keywords:
                                    filtered_df = filtered_df[filtered_df[selected_column].str.contains(keyword, case=False)]
                            
                            # Display results
                            st.subheader("Filtered Results")
                            if len(filtered_df) > 0:
                                st.dataframe(filtered_df)
                                
                                # Display some stats
                                match_percentage = (len(filtered_df) / len(df)) * 100
                                st.info(f"✅ Found {len(filtered_df)} rows matching your keywords ({match_percentage:.1f}% of your data)")
                                
                                # Download button for filtered data
                                csv = filtered_df.to_csv(index=False)
                                st.download_button(
                                    label="💾 Download filtered data as CSV",
                                    data=csv,
                                    file_name="filtered_data.csv",
                                    mime="text/csv",
                                    use_container_width=True
                                )
                            else:
                                st.warning("No matching rows found. Try different keywords or another column.")
        
        except Exception as e:
            st.error(f"Error: {e}")
            st.warning("Please make sure you've uploaded a valid CSV file.")
    else:
        st.info("👆 Please upload a CSV file to get started")

if __name__ == "__main__":
    main()