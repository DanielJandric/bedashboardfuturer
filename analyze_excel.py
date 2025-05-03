import pandas as pd
import json

def analyze_excel_structure(file_path, output_path):
    """Analyzes the structure of an Excel file and saves the analysis to a text file."""
    try:
        xls = pd.ExcelFile(file_path)
        sheet_names = xls.sheet_names
        
        analysis_results = {
            "file_path": file_path,
            "sheets": {}
        }
        
        print(f"Analyzing file: {file_path}")
        print(f"Found sheets: {sheet_names}")
        
        for sheet_name in sheet_names:
            print(f"\nAnalyzing sheet: 	{sheet_name}")
            df = pd.read_excel(xls, sheet_name=sheet_name)
            columns_info = {}
            for col in df.columns:
                # Attempt to infer a more specific numeric type if possible
                col_dtype = str(df[col].dtype)
                if 'int' in col_dtype or 'float' in col_dtype:
                    # Check if all non-null values are integers
                    if pd.api.types.is_integer_dtype(df[col].dropna()):
                         col_dtype = 'integer'
                    elif pd.api.types.is_float_dtype(df[col].dropna()):
                         col_dtype = 'float'
                elif pd.api.types.is_datetime64_any_dtype(df[col].dropna()):
                     col_dtype = 'datetime'
                elif pd.api.types.is_string_dtype(df[col].dropna()):
                     col_dtype = 'string'
                else:
                     col_dtype = 'mixed/object' # Keep original if mixed or other

                columns_info[col] = col_dtype
                print(f"  Column: 	{col} 	(Type: {col_dtype})")
                
            analysis_results["sheets"][sheet_name] = {
                "columns": columns_info,
                "num_rows": len(df)
            }
            
        with open(output_path, 'w') as f:
            json.dump(analysis_results, f, indent=4)
            
        print(f"\nAnalysis complete. Results saved to {output_path}")
        
    except Exception as e:
        print(f"Error analyzing Excel file: {e}")

if __name__ == "__main__":
    excel_file = "/home/ubuntu/upload/Tableau_Evaluations_Fusionne.xlsx"
    output_file = "/home/ubuntu/excel_structure_analysis.json"
    analyze_excel_structure(excel_file, output_file)

