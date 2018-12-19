# Dependencies 
from bs4 import BeautifulSoup
import requests
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import pandas as pd
import time

def scrape():
    # Dictionary to store the scraped data
    mars = {}
   
    # URL to pull
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    # Set the executable path and initialize the chrome browser in splinter
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Loading browser and BeautifulSoup
    browser.visit(url)
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')

    # Pulling the parent I want to look inside
    slide_elem = news_soup.select_one('ul.item_list li.slide')

    # Pulling in title and paragraph
    title = slide_elem.find("div", class_='content_title').get_text()
    paragraph = slide_elem.find("div", class_='article_teaser_body').get_text()
    mars["news"] = (title,paragraph)

    # Set the executable path and initialize the chrome browser in splinter
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # Starting URL
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    # Pull in URL
    browser.visit(url2)

    # Click first button
    full_image = browser.find_by_id('full_image')
    full_image.click()

    # Click second button
    time.sleep(2)
    link = browser.find_link_by_partial_text('more info')
    link.click()



    # Use Beautiful Soup on final page to pull image
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')



    # Pulling in the source 
    img_elem = news_soup.select_one('figure.lede a img').get('src')



    # Putting the 
    format = f"https://www.jpl.nasa.gov{img_elem}"
   
    mars["Image"] = (format)

    # Set the executable path and initialize the chrome browser in splinter
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)



    #
    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')



    mars_weather = soup.find('p','TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    mars["Weather"] = (mars_weather)
   



    url4 = 'https://space-facts.com/mars/'



    # Reading into dataframe
    tables = pd.read_html(url4)

    #Change columns
    tables_df = tables[0]
    tables_df.columns = ['Description','Info']

    tables_df.set_index('Description',inplace=True)
    
    # Printing table as HTML
    tables_html = tables_df.to_html()
    
    mars["Facts"] = (tables_html)


    # URL for scraping
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')



    products = soup.find('div', class_='collapsible results')
    hemisphere = products.find_all('h3')

    image_url_list = []
    title_list =[]

    for record in hemisphere:
        try:
            #Capture the title
            title_list.append(record)
            #Click on the link
            browser.click_link_by_partial_text('Enhanced')
            #find the Original Image link on the new page
            downloads = browser.find_link_by_text('Sample').first
            link = downloads['href']
            #Capture the sample image url
            image_url_list.append(link)
        except ElementDoesNotExist:
            print("Scraping Complete")

    # use zip() to map values
    titles_and_urls = zip(title_list, image_url_list)
    # convert values to print as a set
    titles_and_urls = set(titles_and_urls)

    
    mars["Hemispheres"] = (titles_and_urls)
    
    return(mars)

print(scrape())

    
