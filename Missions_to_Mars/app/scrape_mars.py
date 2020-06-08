# Import dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
import re
import time


def scrape_all():


# Set the executable path and initialize the chrome browser in splinter
    executable_path = {'executable_path' :'chromedriver'}

#executable_path = {'executable_path':'C:\\Users\\User\Desktop\web-scraping-challenge\Missions_to_Mars\chromedriver'}
    browser = Browser('chrome', **executable_path)
    news_title, news_p = mars_news(browser)
    #browser.visit('https://google.com')

    # Run all scraping functions and store in dictionary.
    data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": new_featured_image_url(browser),
        "hemispheres": hemispheres(browser),
        "weather": weather(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data




#-----------------------------------

def mars_news(browser):


    # Visit Nasa news url through splinter module
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # HTML Object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    slide_elem = soup.select_one('ul.item_list li.slide')
    slide_elem.find("div", class_='content_title')


    news_title = slide_elem.find('div', class_='content_title').text
    news_p = slide_elem.find('div', class_='article_teaser_body').text

    except AttributeError:
    return None, None



#news_title = soup.find('div', class_='content_title').find('a').text
#news_p = soup.find('div', class_='article_teaser_body').text

# Return scrapped data 
    #print(news_title)
    #print(news_p)
    return news_title, news_p



#----------------------------------------------
def new_featured_image_url(browser):

    source_featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(source_featured_image_url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id("full_image")
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text("more info", wait_time=0.5)
    more_info_elem = browser.links.find_by_partial_text("more info")
    more_info_elem.click()



    # HTML Object 
    html_image = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_image, 'html.parser')

    # Retrieve background-image url from style tag (Scrapped url)
    featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

    # Main Website Url 
    main_url = 'https://www.jpl.nasa.gov'

    # Concatenate main website url with scrapped route
    new_featured_image_url = main_url + featured_image_url


    # Display full link to featured image
    return new_featured_image_url

#----------------------------------------------------------

def weather(browser):


    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)



    # HTML Object 
    html_weather = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_weather, 'html.parser')

    # Find all elements that contain tweets

    weather = soup.find('div', class_='js-tweet-text-container')

    try:
        mars_weather= weather.p.text.lstrip()
    except AttributeError:

        pattern = re.compile(r'sol')
        mars_weather = soup.find('span', text=pattern).text
    
    return mars_weather
    
    
#-----------------------------------------------------
def mars_facts():

    # Visit Mars facts url 
    facts_url = 'http://space-facts.com/mars/'

    # Use Panda's `read_html` to parse the url

    mars_facts = pd.read_html(facts_url)
    

    # To find the mars facts DataFrame in the list of DataFrames and assign it to `mars_facts_df`
    mars_facts_df = mars_facts[0]

    # Assign the columns `['Description', 'Value']`
    mars_facts_df.columns = ['Description','Value']

    # Set the index to the `Description` column.
    mars_facts_df.set_index('Description', inplace=True)

    # Save html code to folder Assets
    mars_facts_df.to_html()

    data = mars_facts_df.to_dict(orient='records')  # Here's our added param..

    # Return mars_df
    return mars_facts_df



#---------------------------------------------------

def hemispheres(browser):


    mars_hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemispheres_url)

    # HTML Object
    html_hemispheres = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_hemispheres, 'html.parser')

    # Scrape to retreive all items containing mars hemispheres information
    items = soup.find_all('div', class_='item')

    # Create empty list for hemisphere urls 
    hemisphere_image_urls = []

    # Store the main_ul 
    hemispheres_main_url = 'https://astrogeology.usgs.gov'


    # Looping through the items previously stored

    for i in items: 
        # Store title
        title = i.find('h3').text
    
        # Store link that leads to full image website
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
    
        # Visit the link that contains the full image website 
        browser.visit(hemispheres_main_url + partial_img_url)
    
        # HTML Object of individual hemisphere information website 
        partial_img_html = browser.html
    
        # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        soup = BeautifulSoup( partial_img_html, 'html.parser')
    
        # Retrieve full image source 
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
    
        # Append the retreived information into a list of dictionaries 
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    

    # Display hemisphere_image_urls
    return hemisphere_image_urls


if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())

