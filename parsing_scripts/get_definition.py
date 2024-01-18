import csv
from cc_cedict_parser import get_list

cc_cedict_list = get_list()


# Put the name of the CSV file inside your input_files folder
INPUT_FILE = "hsk_hanzi.csv"
# Desired name for the output file
OUTPUT_FILE = "PARSED.csv"
# Name of the referenced field inside your csv file
FIELD_NAME = "hanzi"
# Desired field name for the new appended field
NEW_FIELD_NAME = "cc_cedict_definitions"

def main():
    """
    Opens a CSV file containing Chinese words or characters and append a column
    for English definitions. This customization can extend to other fields
    like Traditional or Pinyin. The updated data, including the new columns,
    is then saved to a new CSV file.
    """
    # Open file and convert to py dict
    input_file = csv.DictReader(open(f"input_files/{INPUT_FILE}"))

    # Put each word in Python list
    word_list = row_to_list(input_file)

    # Append definition to word list
    parsed = parse(word_list)

    to_csv(parsed)
    print("Done!")

def row_to_list(file):
    """
    Extract all elements from a specific field/column across all rows.
    Field name to represents the one in your custom CSV file.
    """
    return [row.get(f"{FIELD_NAME}") for row in file]
    #return [row.get("pinyin").lower().split(",") for row in file]

def parse(word_list):

    list_with_all_elements = []
    print("Adding definition to lists . . .")

    # For all elements in the csv files
    # Find mataching element in the CC-Cedict dictionary list
    for word in word_list:
        info = {}
        info[f"{FIELD_NAME}"] = word
        
        # Checks entry inside the cc-cedict list
        for entry in cc_cedict_list:
            if entry["simplified"] == word:

                info[f"{NEW_FIELD_NAME}"] = entry["english"]
                
        list_with_all_elements.append(info)

    return list_with_all_elements


def to_csv(parsed_list):
    print("Saving to new CSV file . . . ")
    # Key the dictionary keys name
    keys = parsed_list[0].keys()
    print(f"Field names : {keys}")

    # Save to CSV
    with open(f'parsed_files/{OUTPUT_FILE}', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(parsed_list)



if __name__ == "__main__":
    main()