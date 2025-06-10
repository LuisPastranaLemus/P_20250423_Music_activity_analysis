# data_cleaning.py for dataset cleaning
from difflib import SequenceMatcher
from IPython.display import display, HTML
import numpy as np
import pandas as pd
import re
from tqdm import tqdm


def check_existing_missing_values(df):
    
    missing_values = ['', ' ', 'N/A', 'none', 'None', 'null', 'NULL', 'NaN', 'nan', 'NAN', 'nat', 'NaT']
    
    display(HTML(f"> Dataframe missing values:\n"))
    
    for column in df.columns:
        
        if df[column].dtype != 'object':
            
            continue
        
        else:
            
            matches = df[df[column].isin(missing_values)][column].unique()
            
            if df[column].isin(missing_values).any() and matches.size > 0:
                                
                display(HTML(f"> Mising values in ['<i>{column}</i>']: <b>{df[column].isin(missing_values).sum()}</b>"))
                display(HTML(f"&emsp;Matched values: {matches}"))
            
            else:
                
                display(HTML(f"> Missing values in ['<i>{column}</i>']: <b>None</b>"))
                
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
def normalize_string_format(df, include=None, exclude=None):
        
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

           df[column] = df[column].str.lower()
           df[column] = df[column].str.strip()
           df[column] = df[column].str.replace(r'[^\w\s]', ' ', regex=True)
           df[column] = df[column].str.replace(r'\s+', '_', regex=True)
           df[column] = df[column].str.replace(r'__+', '_', regex=True)
    
    return df

# Function for format normalizing type 'object' within column titles(strings)
def normalize_columns_headers_format(df):
    
    title_norm = {}
    
    for title in df.columns:
        
        nt = title.lower().strip()
        nt = re.sub(r'[^\w\s]', ' ', nt)
        nt = re.sub(r'\s+', '_', nt)
        nt = re.sub(r'__+', '_', nt)
        
        title_norm[title] = nt
    
    df = df.rename(columns=title_norm)
    
    return df

# Function for implicit duplicates
def detect_implicit_duplicates(df, include=None, exclude=None, fuzzy_threshold=0.85):
    
    def normalize(value):
        """Devuelve una versión en minúsculas y sin caracteres especiales."""
        return re.sub(r'\W+', '', value.lower()) if isinstance(value, str) else ''

    def split_words(value):
        """Divide por '_' y otras palabras, también separa compuestos pegados."""
        if not isinstance(value, str):
            return []
        return re.findall(r'[A-Za-z0-9]+', value.lower())

    def fuzzy_match(a, b):
        """Devuelve True si a y b son similares sobre el umbral definido."""
        return SequenceMatcher(None, a, b).ratio() >= fuzzy_threshold

    display(HTML(f"> Implicit duplicates:\n"))

    # Filtrado de columnas
    if include:
        columns = [col for col in include if col in df.columns]
    elif exclude:
        columns = [col for col in df.columns if col not in exclude]
    else:
        columns = df.columns.tolist()

    for col in columns:
        display(HTML(f"\n> Processing column: ['<i>{col}</i>']"))

        values = df[col].dropna().unique()
        values = [v for v in values if isinstance(v, str)]
        normalized_values = {v: normalize(v) for v in values}
        results = {}

        for base in tqdm(values, desc=f"> Comparing column ['{col}']", unit=" values"):
            base_norm = normalized_values[base]
            base_parts = set(split_words(base))
            matches = []

            for other in values:
                if base == other:
                    continue
                other_norm = normalized_values[other]
                other_parts = set(split_words(other))

                if (
                    base_norm in other_norm or 
                    other_norm in base_norm or 
                    base_parts & other_parts or 
                    fuzzy_match(base_norm, other_norm)
                ):
                    matches.append(other)

            if matches:
                results[base] = matches

        display(HTML(f"\n> Results for column ['<i>{col}</i>']:"))
        if results:
            for base, found in results.items():
                display(HTML(f"  ['<i>{col}</i>'] '<b>{base}</b>' → '{found}'"))
        else:
            display(HTML("  No implicit duplicated was found."))

    return None



# Function for replacing string date values to datetime values
def normalize_datetime(df, include=None, exclude=None, frmt=None, time_zone='UTC'):
    if exclude is None:
        exclude = []
    
    if include is None:
        target_columns = [col for col in df.columns if col not in exclude]
    else:
        target_columns = [col for col in include if col not in exclude]

    for column in target_columns:
        if pd.api.types.is_object_dtype(df[column]) or pd.api.types.is_string_dtype(df[column]):
            df[column] = pd.to_datetime(df[column], format=frmt, errors='coerce')

        if pd.api.types.is_datetime64_any_dtype(df[column]):
            # If the format is only time, convert to type .dt.time
            if frmt in ["%H:%M:%S", "%H:%M"]:
                df[column] = df[column].dt.time
            else:
                if df[column].dt.tz is None:
                    df[column] = df[column].dt.tz_localize(time_zone)
                else:
                    df[column] = df[column].dt.tz_convert(time_zone)
    
    return df



# Function for finding values ​​that do not allow conversion to numeric
def find_errors_to_numeric(df, column):
    
    mask = pd.to_numeric(df[column], errors='coerce').isna() & df[column].notna()
    non_integer_values = df.loc[mask, column]
    
    if non_integer_values.empty:
        
        pass
   
    else:
        
        print(f"> Non numeric values found in column ['<i>{column}</i>']:\n{non_integer_values}\n")
        print(f"> Conversion <b>unsuccessful</b>, non numeric values amount: {non_integer_values.shape[0]}\n")
                
    numeric_col = pd.to_numeric(df[column], errors='coerce')
    mask = (numeric_col % 1 != 0) & (~numeric_col.isna())
    non_integer_numeric = df.loc[mask, column]
    
    if non_integer_numeric.empty:
        
        pass
   
    else:
        
        print(f"> Numeric values that are <b>not whole integer</b> found in column ['<i>{column}</i>']:\n{non_integer_numeric}\n")
        print(f"> Conversion unsuccessful, numeric values <b>non whole integer</b> amount: <b>{non_integer_numeric.shape[0]}</b>\n")

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


    