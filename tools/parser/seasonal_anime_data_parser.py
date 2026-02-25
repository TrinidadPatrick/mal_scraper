from playwright.sync_api import Page

def parse(book: Page):
    try:
        image_container = book.locator('.image')
        image = image_container.locator('img').get_attribute('src')
        
        title_container = book.locator('.title')
        title = title_container.locator('.link-title').inner_text()
        
        details = book.locator('.prodsrc')
        details_child = details.locator('.info').inner_text()
        
        members = book.locator('.member').inner_text()
        
        score = book.locator('.score.score-label').inner_text()
        
        genre_array = book.locator('.genre').all()
        
        genres = []
        
        for item in genre_array:
            genre = item.locator('a').inner_text()
            mal_id = item.locator('a').get_attribute('href').split("/")[3]
            genres.append({'genre' : genre, 'mal_id' : mal_id})
        
        return {
            'image' : image,
            'title': title, 
            # 'type': type, 
            'genres': genres,
            'info': details_child,
            'members' : members, 
            'score': score
        }
    except Exception as e:
        print(e)