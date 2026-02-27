from playwright.sync_api import Page

def parse(book: Page):
    try:
        image_container = book.locator('.image')
        image = image_container.locator('img').get_attribute('src')
        
        title_container = book.locator('.title')
        title = title_container.locator('.link-title').inner_text()
        
        details = book.locator('.prodsrc')
        
        info_items = []
        try:
            info_spans = details.locator('.info .item').all()
            for span in info_spans:
                info_items.append(span.inner_text().strip().replace('\n', ' '))
        except:
            pass
            
        properties = []
        try:
            property_divs = book.locator('.properties > .property').all()
            for prop in property_divs:
                caption = prop.locator('.caption').inner_text().strip()
                items = prop.locator('.item').all()
                item_texts = [item.inner_text().strip() for item in items]
                properties.append({'name': caption, 'values': item_texts})
        except:
            pass
        
        members = book.locator('.member').inner_text()
        
        score = book.locator('.score.score-label').inner_text()
        
        genre_array = book.locator('.genre').all()
        
        mal_id = book.locator('.genres').get_attribute('id')
        
        print(mal_id)
        
        genres = []
        
        for item in genre_array:
            genre = item.locator('a').inner_text()
            mal_id = item.locator('a').get_attribute('href').split("/")[3]
            genres.append({'genre' : genre, 'mal_id' : mal_id})
        
        return {
            'image' : image,
            'title': title, 
            'mal_id': mal_id,
            'genres': genres,
            'properties': properties,
            'info': info_items,
            'members' : members, 
            'score': score
        }
    except Exception as e:
        print(e)