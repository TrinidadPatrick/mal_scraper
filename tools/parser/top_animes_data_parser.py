def parse(book):
    try:
        title_container = book.locator('.title')
        title = title_container.locator('.anime_ranking_h3 a').inner_text()
        
        details = book.locator('.detail .information').inner_text()
        details_array = details.split('\n')
        
        score = book.locator('.score .score-label').inner_text()
        
        type = details_array[0].split(' ')[0]
        episodes = details_array[0].split(' ')[1].replace("(", "").replace(")", "")
        members = details_array[2].split(' ')[0]
        parts = details_array[1].split(' - ')
        air = {
            'aired_from': parts[0].strip() if len(parts) > 0 else None,
            'aired_to': parts[1].strip() if len(parts) > 1 else None
        }
    
        return {
            'title': title, 
            'type': type, 
            'episodes': episodes, 
            'air': air, 
            'members' : members, 
            'score': score
        }
    
    except Exception as e:
        print(f"Error parsing an item: {e}")
        return None