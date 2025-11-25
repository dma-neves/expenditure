def print_green(text):
    print(f"\033[32m{text}\033[0m")
    
def print_blue(text):
    print(f"\033[34m{text}\033[0m")
    
def format_euro(value: float):
    return f"{value:.2f} eur"