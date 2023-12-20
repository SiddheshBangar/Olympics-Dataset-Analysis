import pandas as pd

def preprocess(df, region_df):
    # Filtering Summer Olympics
    df = df[df['Season'] == 'Summer']

    # Merge with region_df
    df = df.merge(region_df, how='left', on='NOC')

    # Dropping Duplicates
    df.drop_duplicates(inplace=True)

    # One hot encoding for medals
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
    return df
