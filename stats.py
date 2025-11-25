import sys
import pandas as pd
from enum import Enum
import numpy as np
from tabulate import tabulate


from config import Config
from util import print_green, format_euro

def print_expenditure_by_category(expenditure_by_category):
    data = [(category, format_euro(value)) for category, value in sorted(expenditure_by_category.items(), key=lambda item: item[1])]
    
    total = sum(expenditure_by_category.values())
    data.append(("total", format_euro(total)))

    print(tabulate(data, headers=["Category", "Amount"], tablefmt="simple", stralign="left", numalign="right"))
    print()
    
def category_stats(target_category, df, config):
    print_green(f"[{target_category}]\n")


    filtered_df = df[df[config.category_col] == target_category]
    data = [
        [
            format_euro(row[config.value_col]),
            row[config.description_col],
            row[config.launch_date_col]
        ]
        for _, row in filtered_df.iterrows()
    ]

    print(tabulate(data, headers=["Value", "Description", "Date"], tablefmt="simple", stralign="left", numalign="right"))
    print()
            
def complete_stats(df, config):
    expenditure_by_category = {}
    
    for _, row in df.iterrows():
        row_dic = row.to_dict()
        category = row_dic[config.category_col]
        value = row_dic[config.value_col]
        if category in expenditure_by_category:
            expenditure_by_category[category] += value
        else:
            expenditure_by_category[category] = value

    print_green("[all]")
    print_expenditure_by_category(expenditure_by_category)
    

    for cluster_name, cluster_categories in config.stat_clusters.items():

        print_green(f"[{cluster_name}]")
        filtered_expenditure_by_category = { cat: val for cat,val in expenditure_by_category.items() if cat in cluster_categories}
        print_expenditure_by_category(filtered_expenditure_by_category)
        
def main():
    
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} balancesheets/categorized/balancesheet.csv [category]")
        print("category: optional field to see detailed information about specific category")
        exit()

    config = Config("config.json")
    
    path = sys.argv[1]
    df = pd.read_csv(path)
    df[config.value_col] = df[config.value_col].str.replace(',', '').astype(float) # Convert value_col to float

    if len(sys.argv) == 3:
        target_category = sys.argv[2]
        category_stats(target_category, df, config)
    else:
        complete_stats(df, config)

    
if __name__=="__main__":
    main()