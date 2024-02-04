import pandas as pd
import os

# Specify the directory containing your CSV files
directory = os.path.expanduser('~/ssweb/AML/College Football Team Stats Seasons 2013 to 2022')

# Initialize the main dataframe with cfb13.csv
main_df = pd.read_csv(os.path.join(directory, 'cfb13.csv'))
main_df['Year'] = 2013  # Add 'Year' column for the first file

# Loop through all other CSV files in the specified directory and append them to the main dataframe
for year in range(2014, 2023):  # Loop from 2014 to 2022
    filename = f'cfb{str(year)[2:]}.csv'
    file_path = os.path.join(directory, filename)
    
    if os.path.exists(file_path):  # Check if the file exists
        df = pd.read_csv(file_path, header=0)
        df['Year'] = year  # Add 'Year' column based on the filename
        main_df = main_df._append(df, ignore_index=True)

# Save the updated dataframe back to cfb13.csv
main_df.to_csv(os.path.join(directory, 'cfb13.csv'), index=False)

print(f"Data appended with 'Year' column to {os.path.join(directory, 'cfb13.csv')}")
