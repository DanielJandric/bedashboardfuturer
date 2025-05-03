import pandas as pd
import json
import numpy as np

def convert_excel_to_json(excel_path, json_path, sheet_name='Sheet1'):
    """Converts an Excel sheet to a JSON file, handling potential data type issues."""
    try:
        df = pd.read_excel(excel_path, sheet_name=sheet_name)
        
        # Clean column names (replace special chars, spaces)
        df.columns = df.columns.str.replace(r'[^A-Za-z0-9_]+', '', regex=True)
        df.columns = df.columns.str.replace(' ', '_')
        df.columns = df.columns.str.lower()
        
        print(f"Cleaned column names: {df.columns.tolist()}")

        # Convert specific columns if needed (e.g., dates)
        # Example: df['date_column'] = pd.to_datetime(df['date_column']).dt.strftime('%Y-%m-%d')
        # Check for datetime columns identified in analysis
        if 'annee_constr' in df.columns:
             # Ensure it's treated as integer/string, not date
             df['annee_constr'] = df['annee_constr'].astype(str)
        if 'date_evaluation' in df.columns:
             # Attempt to convert to standard date format if possible, else keep as string
             try:
                 df['date_evaluation'] = pd.to_datetime(df['date_evaluation'], errors='coerce').dt.strftime('%Y-%m-%d')
             except Exception:
                 print("Could not parse 'date_evaluation' as datetime, keeping as string.")
                 df['date_evaluation'] = df['date_evaluation'].astype(str)

        # Handle potential NaN values gracefully for JSON conversion
        # Replace NaN with None (null in JSON)
        df = df.replace({np.nan: None})
        
        # Convert DataFrame to list of dictionaries (records format)
        data = df.to_dict(orient='records')
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False, default=str) # Use default=str for non-serializable types
            
        print(f"Successfully converted '{sheet_name}' from '{excel_path}' to '{json_path}'")
        
    except FileNotFoundError:
        print(f"Error: Excel file not found at {excel_path}")
    except Exception as e:
        print(f"Error converting Excel to JSON: {e}")

if __name__ == "__main__":
    excel_file = "/home/ubuntu/upload/Tableau_Evaluations_Fusionne.xlsx"
    json_output_file = "/home/ubuntu/real_estate_data.json"
    # Assuming the data is in the first sheet, as per previous analysis
    convert_excel_to_json(excel_file, json_output_file, sheet_name='Sheet1')

