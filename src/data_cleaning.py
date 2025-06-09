# data_cleaning.py for dataset cleaning

import numpy as np
import pandas as pd
import re
from tqdm import tqdm

def check_existing_missing_values(df, df_name="DataFrame"):
    
    missing_values = ['', ' ', 'N/A', 'none', 'None', 'null', 'NULL', 'NaN', 'nan', 'NAN', 'nat', 'NaT']
    
    print(f"> Dataframe: {df_name}\n")
    
    for column in df.columns:
        
        if df[column].dtype != 'object':
            
            continue
        
        else:
            
            if df[column].isin(missing_values).any():
                                
                print(f"*** Warning ***   > Mising values in '{column}': {df[column].isin(missing_values).sum()}")
            
            else:
                
                print(f"*** Warning ***   > No missing values in '{column}' found")
                
    print()

# Function used for assigning pd.NA to missing values
def replace_missing_values(df, include=None, exclude=None):
    
    missing_values = ['', ' ', 'N/A', 'none', 'None', 'null', 'NULL', 'NaN', 'nan', 'NAN', 'nat', 'NaT']
    
    if exclude is None:
        exclude = []
    
    if include is None:
        available_columns = [col for col in df.columns if col not in exclude]
    else:
        available_columns = [col for col in include if col not in exclude]
 
    for column in available_columns:
        
        if df[column].dtype != 'object':
            
            continue
        
        else:
            
            if df[column].isin(missing_values).any():
                
                df[column] = df[column].replace(missing_values, pd.NA)

    return df

# Function dataframe for format normalizing type 'object' (strings)
def normalize_df_string_format(df, include=None, exclude=None):
        
    if exclude is None:
        exclude = []
    
    if include is None:
        available_columns = [col for col in df.columns if col not in exclude]
    else:
        available_columns = [col for col in include if col not in exclude]
    
    for column in available_columns:
        
       if df[column].dtype != 'object':
           
           continue
       
       else:
                      
           df[column] = df[column].str.replace(r'[^\w\s]', ' ', regex=True)
           df[column] = df[column].str.replace(r'\s+', '_', regex=True)
           df[column] = df[column].str.replace(r'__+', '_', regex=True)
           df[column] = df[column].str.lower()
           df[column] = df[column].str.strip()
    
    return df

# Function for format normalizing type 'object' within column titles(strings)
def normalize_headers_string_format(df):
    
    title_norm = {}
    
    for title in df.columns:
        
        nt = re.sub(r'[^\w\s]', ' ', title)
        nt = re.sub(r'\s+', '_', nt)
        nt = re.sub(r'__+', '_', nt)
        nt = nt.lower().strip()
        
        title_norm[title] = nt
    
    df = df.rename(columns=title_norm)
    
    return df

# Function for implicit duplicates
def detect_implicit_duplicates(df, include=None, exclude=None):
    
    def is_non_composite(value):
        return isinstance(value, str) and re.match(r'^[A-Za-z0-9]+$', value)

    # Column filtering
    if include:
        columns = [col for col in include if col in df.columns]
    elif exclude:
        columns = [col for col in df.columns if col not in exclude]
    else:
        columns = df.columns.tolist()

    for col in columns:
        print(f"\n> Prossesing column: '{col}'")

        # Filtering unique values and non-composite
        values = df[col].dropna().unique()
        values = [v for v in values if is_non_composite(v)]

        results = {}

        # tqdm used for progress bar
        for base in tqdm(values, desc=f"> Comparing in column '{col}'", unit=" values"):
            matches = [other for other in values if base != other and base in other]
            if matches:
                results[base] = matches

        # Ordered results
        print(f"\n> Results for column '{col}':")
        if results:
            for base, matches in sorted(results.items()):
                print(f"  '{base}' -> {matches}")
        else:
            print("  No implicit duplicates were found.")

    # Show results
    if results:
        print("\n[> Simples vs Simples ONLY]")
        for col, base, found in results:
            print(f"  [{col}] '{base}' → '{found}'")
    else:
        print("  No implicit duplicates among simple values.")

    return results

# Function for replacing string date values to datetime values
def replace_string_values_datetime(df, include=None, exclude=None, frmt=None, time_zone='UTC'):
    
    if exclude is None:
        exclude = []
    
    if include is None:
        available_columns = [col for col in df.columns if col not in exclude]
    else:
        available_columns = [col for col in include if col not in exclude]
    
    for column in available_columns:
        
        if df[column].dtype != 'object':
            
            continue
        
        else:
            
            df[column] = pd.to_datetime(df[column], format=frmt, errors='coerce')
            
            try:
                
                df[column] = df[column].dt.tz_localize(time_zone)
            
            except TypeError:
                
                df[column] = df[column].dt.tz_convert(time_zone)
    
    return df

# Function for findingv alues ​​that do not allow conversion to numeric
def find_errors_to_numeric(df, column):
    
    mask = pd.to_numeric(df[column], errors='coerce').isna() & df[column].notna()
    non_integer_values = df.loc[mask, column]
    
    if non_integer_values.empty:
        
        pass
   
    else:
        
        print(f"*** Warning ***   > Non numeric values found in column [{column}]:\n{non_integer_values}\n")
        print(f"> Conversion unsuccessful, non numeric values amount: {non_integer_values.shape[0]}\n")
                
    numeric_col = pd.to_numeric(df[column], errors='coerce')
    mask = (numeric_col % 1 != 0) & (~numeric_col.isna())
    non_integer_numeric = df.loc[mask, column]
    
    if non_integer_numeric.empty:
        
        pass
   
    else:
        
        print(f"*** Warning ***   > Numeric values that are not whole integer found in column [{column}]:\n{non_integer_numeric}\n")
        print(f"> Conversion unsuccessful, numeric values non whole integer amount: {non_integer_numeric.shape[0]}\n")

# Function for converting values to integer data type
def convert_ndtype_to_numeric(df, type=None, include=None, exclude=None):
    
    if exclude is None:
        exclude = []
    
    if include is None:
        available_columns = [col for col in df.columns if col not in exclude]
    else:
        available_columns = [col for col in include if col not in exclude]
    
    for column in available_columns:
        
        if type == 'integer':
            
            if np.array_equal(df[column], df[column].astype('int')):
                
                df[column] = pd.to_numeric(df[column], downcast='integer', errors="coerce")
            
            else:
                
                find_errors_to_numeric(df, column)                

            
        elif type == 'float':
                
                df[column] = pd.to_numeric(df[column], downcast='float', errors="coerce")
            
        else:
            
            if np.array_equal(df[column], df[column].astype('int')):
                
                df[column] = pd.to_numeric(df[column], errors="coerce")
            
            else:
                
                find_errors_to_numeric(df, columns)    
                
                df[column] = pd.to_numeric(df[column], errors="coerce")
    
    return df

# Function for converting integer values to boolean data type
def convert_integer_to_boolean(df, include=None, exclude=None):
    
    if exclude is None:
        exclude = []
    
    if include is None:
        available_columns = [col for col in df.columns if col not in exclude]
    else:
        available_columns = [col for col in include if col not in exclude]
    
    for column in available_columns:
        
        if df[column].dtype != 'int':
            
            continue
        
        else:
            
            df[column] = df[column].astype(bool)
    
    return df


# Function for converting abbreviated gender values to complete gender
def standardize_gender_values(df, include=None, exclude=None):    
    
    if exclude is None:
        exclude = []
    
    if include is None:
        available_columns = [col for col in df.columns if col not in exclude]
    else:
        available_columns = [col for col in include if col not in exclude]
    
    for column in available_columns:
        
        if df[column].dtype != 'object':
            
            continue
        
        else:
            
            df[column] = df[column].replace('f', 'female')
            df[column] = df[column].replace('m', 'male')
    
    return df


    