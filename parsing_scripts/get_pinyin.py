import csv
from pypinyin import pinyin, lazy_pinyin, Style
from itertools import chain

from cc_cedict_parser import get_list

cc_cedict_list = get_list()

# Name of the CSV file inside your input_files folder
INPUT_FILE = "hsk_words.csv"
# Desired name for the output file
OUTPUT_FILE = "hsk_words_merged2.csv"
# Name of the referenced field inside your csv file
FIELD_NAME = "word_simplified"
# Desired field name for the new appended field
NEW_FIELD_NAME = "pinyin"

def main():
    """
    Opens a CSV file containing a list of Chinese characters (Hanzi),
    parses the list to get the pinyin and appends a new field for Pinyin. 
    The updated data, including the new column, is then saved to a 
    new CSV file.
    """

    # Open file and convert to py dict
    input_file = csv.DictReader(open(f'input_files/{INPUT_FILE}'))

    # Put items in py list
    word_list = row_to_list(input_file)

    # Append pinyin to py list
    parsed = parse(word_list)

    # Export parsed list to csv file
    to_csv(parsed)
    print("Done!")


def row_to_list(file):
    """
    Extracts all elements from a specific field/column across all rows.
    Field name represents the one in your custom CSV file.
    """
    return [row.get(f"{FIELD_NAME}") for row in file]


def parse(word_list):

    list_with_all_elements = []
    print("Adding pinyin to list . . .")

    # For all elements in the csv files
    #  Find matching pinyin and append to list 
    for word in word_list:
        info = {}
        info[f"{FIELD_NAME}"] = word
        info[f"{NEW_FIELD_NAME}"] = get_pinyin(word)
        list_with_all_elements.append(info)

    return list_with_all_elements

def get_pinyin(word):

    # Possibility to pick different styles, check pypinyin documentation
    # pinyin(word, heteronym=True)
    # pinyin(word, style=Style.TONE3, heteronym=True)
    result = pinyin(word)
    # result = pinyin(word, style=Style.TONE3, heteronym=True)

    # Get element inside list [['𢝊']]
    inner_element = result[0][0]  
    if (word == inner_element):
        # Return empty string if pinyin cant be found
        return ""
    else:
        return result

def to_csv(parsed_list):
    print("Saving to new CSV file . . . ")
    # Get the dictionary keys name
    keys = parsed_list[0].keys()
    print(f"Field names : {keys}")

    # Save to CSV
    with open(f'parsed_files/{OUTPUT_FILE}', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(parsed_list)



if __name__ == "__main__":
    main()