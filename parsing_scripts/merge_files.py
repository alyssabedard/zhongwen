import csv
import pandas as pd
import os
from pprint import pprint
import json
from functools import reduce

dirname = os.path.dirname(__file__)
folder = os.path.join(dirname, 'merged')
print(dirname)
print(folder)

FOLDER_NAME = 'input_files'
OUTPUT_FOLDER = 'parsed_files'

NAME_OUTPUT_FILE = 'MERGED.csv'
# Column field used as index 10 compare 2 files
#  Make sure field name is the same for each files
INDEX_COLUMN = 'word_simplified'

# Make sure to change key inside the get_dataframe function
abbr_to_file_name = {
    # "gscc":"general-standard-chinese-characters.csv", 
    "file1":"file1.csv", 
    "file2":"file2.csv",
    # "junda":"junda-modern.csv",
    # "ccm":"chinese-character-map.csv"
    }

def main():
    """
    Works only for unique chinese characters in a list.
    Else will duplicate items
    """
    
    # all_files_name = os.listdir(f'./{FOLDER_NAME}')
    print("Dataframe...")
    hsk, hanzi = get_dataframe()

    print("Merging...")
    df_merged = merge_files(hsk, hanzi)

    print("Saving...")
    save_to_csv(df_merged)

    print("Done.")

def get_dataframe():
    # Get dataframe for each CSV file
    # junda = pd.read_csv(f'data/{abbr_to_file_name["junda"]}', index_col="hanzi_sc")#.to_dict("list")
    # gscc = pd.read_csv(f'data/{abbr_to_file_name["gscc"]}', index_col="hanzi_sc")
    f1 = pd.read_csv(f'{FOLDER_NAME}/{abbr_to_file_name["file1"]}', index_col=f'{INDEX_COLUMN}')
    f2 = pd.read_csv(f'{FOLDER_NAME}/{abbr_to_file_name["file2"]}', index_col=f'{INDEX_COLUMN}')
    # ccm = pd.read_csv(f'data/{abbr_to_file_name["ccm"]}', index_col="hanzi_sc")
    return f1, f2

def  merge_files(f1, f2):
    """
    Takes a list of pandas DataFrames (data_frames) and performs 
    outer merges on them based on a common column specified 
    by the INDEX_COLUMN.The reduce function ensures that the merging 
    operation is applied successively to all DataFrames in the list, 
    resulting in a single DataFrame 
    """
    # Data frame order is important
    #  First item of this list will be the index
    data_frames = [f1, f2]
    df_merged = reduce(lambda  left,right: pd.merge(
        left, right, on=[f'{INDEX_COLUMN}'], how='outer'), data_frames)
    print(df_merged.head(20))
    print(df_merged.index)
    return(df_merged)


def save_to_csv(df_merged):
    df_merged.to_csv(f'./{OUTPUT_FOLDER}/{NAME_OUTPUT_FILE}', encoding='utf-8')



if __name__ == "__main__":
    main()