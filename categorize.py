import sys
import pandas as pd
import numpy as np

from rapidfuzz import process


from config import Config
from util import print_green, print_blue

EXIT = "exit"
SAVE = "save"
HELP = "help"
        
def print_help(config):    
    
    print("Categories:")
    for cat in config.categories:
        print_blue(cat)
    print("\nCommands:")
    print_blue(EXIT)
    print_blue(SAVE)
    print_blue(HELP)
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
    output_path = path.replace("raw", "categorized")
    df.to_csv(output_path, index=False)
    print("Saved to", output_path)
    
def main():
    
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} balancesheets/raw/balancesheet.csv")
        exit()
        
    config = Config("config.json")
    print_help(config)
    
    path = sys.argv[1]
    df = pd.read_csv(path)
    df[config.category_col] = pd.Series(dtype='object')


    for index, row in df.iterrows():
        print_row(row.to_dict(), config)
        
        category = None
        while category == None:
            user_input = input("category (fuzzyfind) or command: ")
            
            if user_input == SAVE:
                save(df, path)
            elif user_input == EXIT:
                exit()
            elif user_input == HELP:
                print_help(config)
            else:
                category = fuzzy_find_category_based_on_user_input(user_input, config)
                if category is None:
                    print("Invalid input, try again")
        
        df.at[index, config.category_col] = category
        
        print()
        
    save(df, path)
        

if __name__=="__main__":
    main()