import sys
import pandas as pd
from enum import Enum
import numpy as np
import matplotlib.pyplot as plt

from config import Config

INVERT_VALUE = True

class CollapseGranularity(Enum):
    MONTH = 0
    WEEK = 1
    DAY = 2

def plot_expenditure_by_category_accumulated_over_time(expenditure_by_category_accumulated, plot_file_path):
    plt.figure(figsize=(12, 6))

    for category, data in expenditure_by_category_accumulated.items():
        dates, values = zip(*data)
        dates = pd.to_datetime(dates, format="%d/%m/%Y")
        dates, values = zip(*sorted(zip(dates, values)))
        plt.plot(dates, values, marker='o', label=category)

    plt.xlabel("Date")
    plt.ylabel("Expenditure")
    plt.title("Expenditure by Category Over Time")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(plot_file_path, dpi=300)
    print("Plot created:", plot_file_path)

def get_collapse_granularity(df, config):
    df_dates = pd.to_datetime(df[config.launch_date_col], format="%d/%m/%Y")
    number_of_days = (df_dates.max() - df_dates.min()).days

    if number_of_days > 365:
        return CollapseGranularity.MONTH
    elif number_of_days > 90:
        return CollapseGranularity.WEEK
    else:
        return CollapseGranularity.DAY

def should_collapse(collapse_granularity, date_0, date_1):
    d0_day, d0_month, d0_year = map(int, date_0.split("/"))
    d1_day, d1_month, d1_year = map(int, date_1.split("/"))

    d0_week = d0_day // 7
    d1_week = d1_day // 7

    if d0_year != d1_year:
        return False

    if collapse_granularity == CollapseGranularity.MONTH:
        return d0_month == d1_month
    elif collapse_granularity == CollapseGranularity.WEEK:
        return d0_month == d1_month and d0_week == d1_week
    else:
        return d0_month == d1_month and d0_day == d1_day

        
def main():
    
    if len(sys.argv) < 1:
        print(f"Usage: {sys.argv[0]} balancesheets/categorized/balancesheet.csv")
        exit()
        
    config = Config("config.json")

    path = sys.argv[1]
    df = pd.read_csv(path)
    df[config.value_col] = df[config.value_col].str.replace(',', '').astype(float) # Convert config.value_col column to float

    collapse_granularity = get_collapse_granularity(df, config)
    print("note: using collapse granularity:", collapse_granularity.name)

    expenditure_by_category = {}
    expenditure_by_category_accumulated = {}

    for _, row in df.iterrows():
        row_dic = row.to_dict()
        category = row_dic[config.category_col]
        value = -row_dic[config.value_col] if INVERT_VALUE else row_dic[config.value_col]
        date = row_dic[config.launch_date_col]
        
        if category not in config.plot_cluster:
            continue
        
        if category not in expenditure_by_category:
            expenditure_by_category[category] = value
            expenditure_by_category_accumulated[category] = [(date,value)]
        else:
            expenditure_by_category[category] += value
            accumulated_value = expenditure_by_category[category]
            
            last_date, _ = expenditure_by_category_accumulated[category][-1]
            
            if should_collapse(collapse_granularity, date, last_date):
                expenditure_by_category_accumulated[category][-1] = (date, accumulated_value)
            else:
                expenditure_by_category_accumulated[category].append( (date, accumulated_value) )
                
    csv_file_name = path.split("/")[-1]
    plot_file_name = csv_file_name.replace("csv", "png")
    plot_file_path = f"plots/{plot_file_name}"
    plot_expenditure_by_category_accumulated_over_time(expenditure_by_category_accumulated, plot_file_path)


    
if __name__=="__main__":
    main()