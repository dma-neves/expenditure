import sys
import pandas as pd
import numpy as np
from enum import Enum
import os
from rapidfuzz import process


from config import Config
from util import print_green, print_blue

class Command(Enum):
    EXIT = ("exit", "Exit program")
    SAVE = ("save", "Save current state")
    HELP = ("help", "Show help information")
    PREVIOUS = ("prev", "Go to previous row")
    FORWARD = ("forward", "Forward to next uncategorized row")

    def __init__(self, value, description):
        self._value_ = value  # keep the original value
        self.description = description

def print_help(config):
    print("Categories:")
    for cat in config.categories:
        print_blue(cat)
    print("\nCommands:")
    for command in Command:
        print_blue(f"{command.value}: {command.description}")
    print()

def print_row(row, config):
    date = row[config.launch_date_col]
    value = row[config.value_col]
    desc = row[config.description_col]
    print_green(f"Description: {desc}")
    print_green(f"date: {date}")
    print_green(f"value: {value}\n")
    
def fuzzy_find_category_based_on_user_input(user_input, config):
    allowed = config.categories
    match, score, _ = process.extractOne(user_input, allowed)
    if score > 60:
        print("Categorized as ", end="")
        print_blue(match)
        return match
    else:
        return None
    
def save(df, path):
    df.to_csv(path, index=False)
    print("Saved to", path)
    
def get_next_uncategorized_index(config, index, output_path):
    if not os.path.exists(output_path):
        print("Output path doesn't exist yet. Staying in current row")
        return index

    df = pd.read_csv(output_path)
    idx = df[df[config.category_col].isna()].index[0]
    print("Forwarding to", idx)
    return idx

def get_previous_index(index):
    if index > 0:
        return index - 1
    else:
        print("Already at the first row. Staying in current row")
        return index

def main():
    
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} input.csv output.csv")
        exit()
        
    config = Config("config.json")
    print_help(config)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    df = pd.read_csv(input_path)
    df[config.category_col] = pd.Series(dtype='object')


    index = 0
    while index < len(df):
        print(f"row {index}/{len(df)}")

        row = df.iloc[index]
        print_row(row.to_dict(), config)
        
        category = None
        while category == None:
            user_input = input("category (fuzzyfind) or command: ")
            
            if user_input == Command.SAVE.value:
                save(df, output_path)
            elif user_input == Command.EXIT.value:
                exit()
            elif user_input == Command.HELP.value:
                print_help(config)
            elif user_input == Command.PREVIOUS.value:
                index = get_previous_index(index)
                break
            elif user_input == Command.FORWARD.value:
                index = get_next_uncategorized_index(config, index, output_path)
                break
            else:
                category = fuzzy_find_category_based_on_user_input(user_input, config)
                if category is None:
                    print("Invalid input, try again")
        
        if category is not None:
            df.at[index, config.category_col] = category
            index += 1  # move to next row        
        print()
        
    save(df, output_path)
        

if __name__=="__main__":
    main()