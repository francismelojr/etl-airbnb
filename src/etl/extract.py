#web scraping libraries
import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException

#timer
from time import sleep

#data manipulation
import pandas as pd

def scrape(destination, headless=True, export_to_csv= False):

    """"
    Web-scraping function to read all pages in airbnb and save them in a dataframe.

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
    #setting options
    options = Options()
    options.add_argument("--start-maximized")
    if headless == True:
        options.add_argument("--headless")

    #set url and destination to search
    main_url = "https://www.airbnb.com.br/"
    destination = destination

    #going to places adress
    navegador = webdriver.Edge(options=options)
    navegador.get(main_url)

    sleep(2)

    where_button = navegador.find_element("xpath", "//input[@id='bigsearch-query-location-input']")

    try:
        where_button.click()
    except ElementNotInteractableException:
        where_button = navegador.find_element("xpath", "//button[span='Localização']")
        where_button.click()
        
    sleep(2)

    search_bar = navegador.find_element("xpath", "//input[@autocomplete='off']")
    search_bar.send_keys(destination)

    sleep(2)

    search_button = navegador.find_element("xpath", "//button[@data-testid='structured-search-input-search-button']")
    search_button.click()

    data = []
    sleep(2)
    page_content = navegador.page_source
    site = BeautifulSoup(page_content, 'html.parser')

    places = site.findAll("div", attrs={"itemprop": "itemListElement"})
    pages = site.find(
        "nav", attrs={"aria-label": "Paginação de resultados de busca"})
    n_pages = int(pages.findAll("a")[-2].text)

    cookies = navegador.find_element(
        "xpath", "//div[@data-testid='main-cookies-banner-container']")
    cookies_button = cookies.find_elements("xpath", ".//button")[1]
    cookies_button.click()

    for page in range(n_pages-1):
        sleep(2)
        navegador.execute_script("window.scrollTo(0, 1000)")
        sleep(0.5)

        navegador.execute_script("window.scrollTo(0, 2000)")
        sleep(0.5)

        navegador.execute_script("window.scrollTo(0, 3000)")
        sleep(1)

        page_content = navegador.page_source
        site = BeautifulSoup(page_content, 'html.parser')
        places = site.findAll("div", attrs={"itemprop": "itemListElement"})

        for place in places:
            # title
            place_title = place.find(
                "div", attrs={"data-testid": "listing-card-title"}).text

            # subtitle
            place_desc = place.find("meta", attrs={"itemprop": "name"})["content"]

            # link
            place_url = place.find("meta", attrs={"itemprop": "url"})["content"]

            # beds
            beds = place.findAll(
                "div", attrs={"data-testid": "listing-card-subtitle"})[1].text

            # price
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

            # superhost
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

    if export_to_csv == True:
        current_directory = os.path.dirname(os.path.realpath(__file__))
        output_dir = os.path.join(current_directory, 'output')
        output_file = f'{destination}.csv'

        output_path = os.path.join(output_dir, output_file)
        df.to_csv(output_path, index=False, sep=";")
    return df 