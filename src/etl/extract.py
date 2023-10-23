#web scraping libraries
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException

#operational system library
import os

#timer library
from time import sleep

#data manipulation library
import pandas as pd

def scrape(destination, headless=True, export= False):

    """"
    Web-scraping function to read all pages in airbnb and save the results in a dataframe.

    Parameters
    ----------
    destination : str
        Destination of places to scrape on airbnb.

    headless : bool, default = True
        If False, the navigator will not be minimized while doing the web-scraping.

    export_to_csv : bool, default = False
        If True, the dataframe will be exported as a csv file

    Return: A pandas Dataframe with the webscraping data
    """
    
    #creating list named data that will receive all data from airbnb
    data = []

    #setting options
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-crash-reporter")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-in-process-stack-traces")
    options.add_argument("--disable-logging")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")
    options.add_argument("--output=/dev/null")

    if headless == True:
        options.add_argument("--headless")

    #set url and destination to search
    main_url = "https://www.airbnb.com.br/"
    destination = destination

    #going to places adress
    navegador = webdriver.Edge(options=options)
    navegador.get(main_url)

    sleep(2)

    #clicking on where button
    where_button = navegador.find_element("xpath", "//input[@id='bigsearch-query-location-input']")

    try:
        where_button.click()
    except ElementNotInteractableException:
        where_button = navegador.find_element("xpath", "//button[span='Localização']")
        where_button.click()
        
    sleep(2)

    #sending keys to search bar
    search_bar = navegador.find_element("xpath", "//input[@autocomplete='off']")
    search_bar.send_keys(destination)

    sleep(1)

    #click search button
    search_button = navegador.find_element("xpath", "//button[@data-testid='structured-search-input-search-button']")
    search_button.click()

    sleep(2)
    page_content = navegador.page_source
    site = BeautifulSoup(page_content, 'html.parser')

    # finding the list item element
    places = site.findAll("div", attrs={"itemprop": "itemListElement"})
    pages = site.find(
        "nav", attrs={"aria-label": "Paginação de resultados de busca"})
    n_pages = int(pages.findAll("a")[-2].text)

    #clicking the accept cookies button, so we are able to click on next page

    cookies = navegador.find_element(
        "xpath", "//div[@data-testid='main-cookies-banner-container']")
    cookies_button = cookies.find_elements("xpath", ".//button")[1]
    cookies_button.click()

    #scrolling all the way down to load the entire page
    for page in range(n_pages-1):
        sleep(2)
        navegador.execute_script("window.scrollTo(0, 1000)")
        sleep(0.5)

        navegador.execute_script("window.scrollTo(0, 2000)")
        sleep(0.5)

        navegador.execute_script("window.scrollTo(0, 3000)")
        sleep(1)

        #getting the page content
        page_content = navegador.page_source
        site = BeautifulSoup(page_content, 'html.parser')
        places = site.findAll("div", attrs={"itemprop": "itemListElement"})

        #scrape all the places for each page
        for place in places:
            #title
            place_title = place.find(
                "div", attrs={"data-testid": "listing-card-title"}).text

            #subtitle
            place_desc = place.find("meta", attrs={"itemprop": "name"})["content"]

            #url
            place_url = place.find("meta", attrs={"itemprop": "url"})["content"]

            #beds description
            beds = place.findAll(
                "div", attrs={"data-testid": "listing-card-subtitle"})[1].text

            #price
            price_div = place.findAll("div", attrs={
                    "aria-hidden": 'true'})[-1]
        
            place_price = price_div.findAll("span")[1].get_text(
                strip=True).replace("R$", "").replace('noite', "").replace(".", "")

            try:
                place_price = float(place_price)

            except:
                place_price = price_div.findAll("span")[0].get_text(
                    strip=True).replace("R$", "").replace('noite', "").replace(".", "")

                place_price = float(place_price)

            #if the place is superhost
            superhost = place.find(
                "div", attrs={"aria-describedby": "carousel-description"})
            place_host = superhost.findAll("div")[4].text
            if place_host == "Superhost":
                place_host = "Yes"
            else:
                place_host = "No"

            data.append([place_title, place_desc,
                        place_url, place_price, beds, place_host])

        next_button = navegador.find_element("xpath", "//a[@aria-label='Próximo']")
        next_button.click()

    #creating pandas dataframe
    columns_names = ["title", "subtitle", "url", "price_per_night", "beds", "is_superhost"]
    df = pd.DataFrame(data, columns= columns_names)

    #exporting to csv
    if export == True:
        current_directory = os.path.dirname(os.path.realpath(__file__))
        output_dir = os.path.join(current_directory, 'output')
        output_file = f'{destination}.csv'

        output_path = os.path.join(output_dir, output_file)
        df.to_csv(output_path, index=False, sep=";")
    return df