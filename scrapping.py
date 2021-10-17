#Inport splinter and bsoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    #Initiate headless driver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless = False)

    news_title, news_paragraph = mars_news(browser)

    #Store data from scrapping funcs in dict
    data = {"news_title": news_title,
            "news_paragraph": news_paragraph,
            "featured_image": featured_image(browser),
            "facts": mars_facts(),
            "last_modified": dt.datetime.now(),
            "hemispheres": scrape_hemispheres(browser)}
    # data = {"Image 1": {'image_url': 'https://marshemispheres.com/images/f5e372a36edfa389625da6d0cc25d905_cerberus_enhanced.tif_full.jpg',
    #     'title': 'Cerberus Hemisphere Enhanced'},
    #     "Image 2": {'image_url': 'https://marshemispheres.com/images/3778f7b43bbbc89d6e3cfabb3613ba93_schiaparelli_enhanced.tif_full.jpg',
    #  'title': 'Schiaparelli Hemisphere Enhanced'},
    #     "Image 3": {'image_url': 'https://marshemispheres.com/images/555e6403a6ddd7ba16ddb0e471cadcf7_syrtis_major_enhanced.tif_full.jpg',
    #     'title': 'Syrtis Major Hemisphere Enhanced'}, "Image 4": {'image_url': 'https://marshemispheres.com/images/b3c7c6c9138f57b4756be9b9c43e3a48_valles_marineris_enhanced.tif_full.jpg',
    #     'title': 'Valles Marineris Hemisphere Enhanced'}}
    browser.quit()
    return(data)

def mars_news(browser):
    #Visit site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    browser.is_element_present_by_css('div.list_text', wait_time = 1)

    html = browser.html
    news_soup = soup(html, 'html.parser')

    #t/e block
    try: 
        slide_elem = news_soup.select_one('div.list_text')

        #Use parent elem to find first 'a' tag and save
        news_title = slide_elem.find('div', class_ = 'content_title').get_text()

        #Use parent to find text
        news_p = slide_elem.find('div', class_ = 'article_teaser_body').get_text()

    except AttributeError:
        return(None, None)

    return(news_title, news_p)

### Featured Image
def featured_image(browser):
    #Visit image url
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    #Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    #Parse resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    #t/e block
    try:
        #Find relative image url
        img_url_rel = img_soup.find('img', class_ = 'fancybox-image').get('src')

    except AttributeError:
        return(None)

    #Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return(img_url)

def mars_facts():
    #t/e block
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return(None)

    df.columns = ['description', 'Mars', 'Earth']
    df.set_index('description', inplace = True)
    
    return(df.to_html())

def scrape_hemispheres(browser):
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'

    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    i = 0

    while i < 4:
        browser.visit(url)
        full_image_elem = browser.find_by_tag('h3')[i]
        full_image_elem.click()
        
        html = browser.html
        img_soup = soup(html, 'html.parser')
        
        img_url_rel = img_soup.find('img', class_='wide-image').get('src')
        img_url = f'{url}{img_url_rel}'
        
        caption = img_soup.find('h2', class_='title').get_text()
        
        dict_ = {}
        dict_['image_url'] = img_url
        #https://stackoverflow.com/questions/6416131/add-a-new-item-to-a-dictionary-in-python
        dict_['caption'] = caption
        
        hemisphere_image_urls.append(dict_)
        
        i += 1
    
    return(hemisphere_image_urls)

if __name__ == "__main__":
    print(scrape_all())