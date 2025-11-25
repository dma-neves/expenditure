import json

class Config:
    
    def __init__(self, config_file):
        with open(config_file, 'r') as file:
                config_data = json.load(file)
                self.categories = config_data["categories"]
                self.stat_clusters = config_data["stat_clusters"]
                self.plot_cluster = config_data["plot_cluster"]
                
                self.launch_date_col = config_data["columns"]["LAUNCH_DATE"]
                self.value_date_col = config_data["columns"]["VALUE_DATE"]
                self.description_col = config_data["columns"]["DESCRIPTION"]
                self.value_col = config_data["columns"]["VALUE"]
                self.balance_col = config_data["columns"]["BALANCE"]
                self.category_col = config_data["columns"]["CATEGORY"]