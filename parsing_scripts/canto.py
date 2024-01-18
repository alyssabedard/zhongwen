from numpy import empty
import pycantonese
import csv


def main():

    # Open file and convert to py dict
    input_file = csv.DictReader(open("input_files/for_parsing.csv")) # test_data.csv

    # Create a list of tuple with simp and trad
    hanzi_list = row_to_tuple(input_file)
    print(hanzi_list)
    # Parse the data to get jyutping
    parsed_list = parse_hanzi(hanzi_list)
    #print(parsed_list)
    # Save new data to CSV file
    to_csv(parsed_list)


def row_to_tuple(file):
    # [('他', '他'), ('这', '這'), ('个', '個'), ('们', '們'), ('夨', ''), ('㦰', ''), ('凷', '')]
    return [tuple(row.values()) for row in file]

# Not working well, return false for some trad, probalby not in database
# def check_if_trad(hanzi):
#     return hanzidentifier.is_traditional(hanzi)
#     # 们,們

def parse_hanzi(hanzi_list):
    all_hanzi = []

    for hanzi in hanzi_list:
        info = {}

        # Check if trad is empty
        if hanzi[1]:
            info["trad"] = hanzi[1]
            info["jyupting"] = (pycantonese.characters_to_jyutping(hanzi[1]))[0][1]
            all_hanzi.append(info)

        # Else add the hanzi from the simplified column (since high chance to be trad)
        else:
            info["trad"] = hanzi[0]
            info["jyupting"] = (pycantonese.characters_to_jyutping(hanzi[0]))[0][1]
            all_hanzi.append(info)


    return all_hanzi
            
def to_csv(parsed_list):

    # Key the dictionary keys name
    keys = parsed_list[0].keys()
    print(keys)

    # Save to CSV
    with open('parsed_files/parsed_with_jyutping.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(parsed_list)

# then for each simplified hanzi add zhuyun/bopomofo
# zhuyin bom https://pypi.org/project/pyzhuyin/ 

if __name__ == "__main__":
    main()