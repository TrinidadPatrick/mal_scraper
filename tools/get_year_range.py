from datetime import datetime

def get_year_range(start_year=1980):
    current_year = datetime.now().year
    
    years = list(range(start_year, current_year + 1))
    
    return years