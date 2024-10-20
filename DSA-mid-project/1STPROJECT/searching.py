import pandas as pd


def filterData(df, column_name, filter_type, search_term):
    if filter_type == 'contains':
        return df[df[column_name].str.contains(search_term, na=False)]
    elif filter_type == 'starts_with':
        return df[df[column_name].str.startswith(search_term, na=False)]
    elif filter_type == 'ends_with':
        return df[df[column_name].str.endswith(search_term, na=False)]
    else:
        return df


def multiColumnSearch(df, selected_columns, search_terms, filter_type='AND'):
    mask = pd.Series([True] * len(df))  # include every row from df

    for i, column in enumerate(selected_columns):
        term = search_terms[i].strip() if i < len(search_terms) else ''

        if column in df.columns:
            df[column] = df[column].astype(str)
            print(f"Filtering Column: {column} with Term: '{term}'")

            column_mask = df[column].str.contains(term, na=False)
            print(f"Column Mask for {column} with term '{
                  term}': {column_mask.sum()} matches")

            if filter_type == 'AND':
                mask &= column_mask
            elif filter_type == 'OR':
                mask |= column_mask
        else:
            print(f"Warning: Column '{
                  column}' does not exist in the DataFrame.")

    filtered_df = df[mask]
    print("Filtered DataFrame shape:", filtered_df.shape)
    return filtered_df
