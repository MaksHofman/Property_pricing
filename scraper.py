import time
from multiprocessing import cpu_count, Pool

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

url = 'https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/mazowieckie/warszawa/warszawa/warszawa'


def get_driver():
    chrome_options = Options()
    #chrome_options.add_argument("--headless")  # Run headless for efficiency
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)

    return driver


def get_listings_from_li_tags(driver):
    list_items = driver.find_elements(By.TAG_NAME, 'li')
    listings = []
    for li in list_items:

        try:
            article = li.find_element(By.TAG_NAME, 'article')
            href = article.find_element(By.XPATH, './/a').get_attribute('href')
            listings.append(href)
        except:
            continue
    return listings


def accept_cookies_and_expand_description(driver):

    # Accept cookies
    driver.find_element(By.ID, 'onetrust-accept-btn-handler').click()
    time.sleep(1)

    # Expand description
    try:
        driver.find_element(By.XPATH, '//button[.//*[contains(text(), "Pokaż więcej")]]').click()
    except Exception as e:
        print("Short description")

def get_price_for_square_meter(driver):
    try:
        listing_price_for_square_meter = driver.find_element(By.XPATH,'//div[@aria-label="Cena za metr kwadratowy"]').text
        return listing_price_for_square_meter
    except Exception as e:
        return "null"

def get_basic_listing_info(driver):
    listing_title = driver.find_element(By.TAG_NAME, 'h1').text
    listing_price = driver.find_element(By.TAG_NAME, 'strong').text
    listing_adress = driver.find_element(By.XPATH, '//*[name()="h1"]/following-sibling::*[2]').text
    listing_id = driver.find_element(By.XPATH, '//p[contains(text(), "Zaktualizowano:")]/following-sibling::p').text.split(' ')[1]
    listing_price_for_square_meter = get_price_for_square_meter(driver)

    return listing_title, listing_price, listing_adress, listing_id, listing_price_for_square_meter

def get_main_listing_info(driver):
    listing_square_area = driver.find_element(By.XPATH, '//button/div[2][contains(text(), "m²")]').text.split(' ')[0]
    listing_rooms = driver.find_element(By.XPATH,'//button/div[2][contains(text(), "pokój") or contains(text(), "pokoje") or contains(text(), "pokoi")]').text.split(' ')[0]

    listing_heating = driver.find_element(By.XPATH, '//div[p[contains(text(), "Ogrzewanie")]]').text.split('\n')[1].strip()
    listing_floor = driver.find_element(By.XPATH, '//div[p[contains(text(), "Piętro")]]').text.split('\n')[1].strip()
    # and p[contains(text(), "zł")]
    listing_rent = driver.find_element(By.XPATH, '//div[p[contains(text(), "Czynsz")]]').text.split('\n')[1].strip()
    listing_finish_condition = driver.find_element(By.XPATH, '//div[p[contains(text(), "Stan wykończenia")]]').text.split('\n')[1].strip()
    listing_market_type = driver.find_element(By.XPATH, '//div[p[contains(text(), "Rynek")]]').text.split(':')[1].strip()
    listing_ownership = driver.find_element(By.XPATH, '//div[p[contains(text(), "Forma własności")]]').text.split('\n')[1].strip()
    listing_available_from = driver.find_element(By.XPATH, '//div[p[contains(text(), "Dostępne od")]]').text.split('\n')[1].strip()
    listing_advertiser_type = driver.find_element(By.XPATH, '//div[p[contains(text(), "Typ ogłoszeniodawcy")]]').text.split('\n')[1].strip()
    listing_extra_info = driver.find_element(By.XPATH,'//div[p[contains(text(), "Informacje dodatkowe")]]/*[2]').text.split('\n')

    return listing_square_area, listing_rooms, listing_heating, listing_floor, listing_rent, listing_finish_condition, listing_market_type, listing_ownership, listing_available_from, listing_advertiser_type, str(listing_extra_info)

def get_building_info(driver):
    if not (expand_building_section(driver)):
        return "null", "null", "null", "null", "null", "null", "null"

    listing_year_of_construction = get_year_of_construction(driver)
    time.sleep(0.2)
    listing_lift = get_lift(driver)
    listing_building_type = get_building_type(driver)
    listing_building_material = get_building_material(driver)
    listing_windows = get_windows(driver)
    listing_energy_certificate = get_energy_certificate(driver)
    listing_safety = get_safety(driver)
    return listing_year_of_construction, listing_lift, listing_building_type, listing_building_material, listing_windows, listing_energy_certificate, listing_safety

def get_year_of_construction(driver):
    try:
        listing_year_of_construction = driver.find_element(By.XPATH, '//div[p[contains(text(), "Rok budowy")]]').text.split('\n')[1].strip()
        return listing_year_of_construction
    except Exception as e:
        return "null"
def get_lift(driver):
    try:
        listing_lift = driver.find_element(By.XPATH, '//div[p[contains(text(), "Winda")]]').text.split('\n')[1].strip()
        return listing_lift
    except Exception as e:
        return "null"
def get_building_type(driver):
    try:
        listing_building_type = driver.find_element(By.XPATH, '//div[p[contains(text(), "Rodzaj zabudowy")]]').text.split('\n')[1].strip()
        return listing_building_type
    except Exception as e:
        return "null"
def get_building_material(driver):
    try:
        listing_building_material = driver.find_element(By.XPATH,'//div[p[contains(text(), "Materiał budynku")]]/*[2]').text
        return listing_building_material
    except Exception as e:
        return "null"
def get_windows(driver):
    try:
        listing_windows = driver.find_element(By.XPATH, '//div[p[contains(text(), "Okna")]]').text.split('\n')[1].strip()
        return listing_windows
    except Exception as e:
        return "null"
def get_energy_certificate(driver):
    try:
        listing_energy_certificate = driver.find_element(By.XPATH, '//div[p[contains(text(), "Certyfikat energetyczny")]]').text.split('\n')[1].strip()
        return listing_energy_certificate
    except Exception as e:
        return "null"

def get_safety(driver):
    try:
        listing_safety = driver.find_element(By.XPATH, '//div[p[contains(text(), "Bezpieczeństwo")]]/*[2]').text.split('\n')
        return str(listing_safety)
    except Exception as e:
        return "null"
def expand_building_section(driver):
    try:
        driver.find_element(By.XPATH, '//header[.//*[contains(text(), "Budynek i materiały")]]').click()
        return True
    except Exception as e:
        print("No building info section")
        return False

# Get info from the whole equipment section
def get_equipment_info(driver):
    if not expand_equipment_section(driver):
        return "null", "null", "null"
    listing_equipment = get_equipment(driver)
    listing_security_type = get_security_type(driver)
    listing_media = get_media(driver)
    return listing_equipment, listing_security_type, listing_media
def expand_equipment_section(driver):
    try:
        driver.find_element(By.XPATH, '//header[.//*[contains(text(), "Wyposażenie")]]').click()
        return True
    except Exception as e:
        print("No equipment section")
        return False

def get_equipment(driver):
    try:
        time.sleep(0.1)
        listing_equipment = driver.find_element(By.XPATH,'//div[p[contains(text(), "Wyposażenie")]]/*[2]').text.split('\n')
        return str(listing_equipment)
    except Exception as e:
        return "null"
def get_security_type(driver):
    try:
        listing_security_type = driver.find_element(By.XPATH,'//div[p[contains(text(), "Zabezpieczenia")]]/*[2]').text.split('\n')
        return str(listing_security_type)
    except Exception as e:
        return "null"
def get_media(driver):
    try:
        listing_media = driver.find_element(By.XPATH,'//div[p[contains(text(), "Media")]]/*[2]').text.split('\n')
        return str(listing_media)
    except Exception as e:
        return "null"

def get_listing_last_updated_and_description(driver):
    listing_last_updated = driver.find_element(By.XPATH, "//p[contains(text(), 'Zaktualizowano:')]").text.split(':')[1].strip()
    listing_description = driver.find_element(By.XPATH, "//*[text()='Opis']/following-sibling::div").text
    return listing_last_updated, listing_description

def scrape_listing(listing):
    print("Scraping " + listing)

    driver = get_driver()
    driver.get(listing)
    time.sleep(2)

    accept_cookies_and_expand_description(driver)

    listing_title, listing_price, listing_adress, listing_id, listing_price_for_square_meter = get_basic_listing_info(driver)

    listing_square_area, listing_rooms, listing_heating, listing_floor, listing_rent, listing_finish_condition, listing_market_type, listing_ownership, listing_available_from, listing_advertiser_type, listing_extra_info = get_main_listing_info(driver)

    listing_year_of_construction, listing_lift, listing_building_type, listing_building_material, listing_windows, listing_energy_certificate, listing_safety = get_building_info(driver)

    listing_equipment, listing_security_type, listing_media = get_equipment_info(driver)

    listing_last_updated, listing_description = get_listing_last_updated_and_description(driver)



    print("Title: " + listing_title)
    print("Price: " + listing_price)
    print("Adress: " + listing_adress)
    print("ID: " + listing_id)
    print("Price for square-meter: " + listing_price_for_square_meter)

    print("Area: " + listing_square_area)
    print("Rooms: " + listing_rooms)
    print("Heating: " + listing_heating)
    print("Floor: " + listing_floor)
    print("Rent: " + listing_rent)
    print("Finish condition: " + listing_finish_condition)
    print("Market Type: " + listing_market_type)
    print("Ownership: " + listing_ownership)
    print("Available from: " + listing_available_from)
    print("Advertiser Type: " + listing_advertiser_type)
    print("Extra info: " + listing_extra_info)

    print("Year of construction:  " + listing_year_of_construction)
    print("Lift: " + listing_lift)
    print("Building Type: " + listing_building_type)
    print("Building Material: " + listing_building_material)
    print("Windows: " + listing_windows)
    print("Energy Certificate: " + listing_energy_certificate)
    print("Safety: " + listing_safety)

    print("Equipment: " + listing_equipment)
    print("Security Type: " + listing_security_type)
    print("Media: " + listing_media)


    print("Updated: " + listing_last_updated)
    print("Description: " + listing_description)




if __name__ == '__main__':
    driver = get_driver()
    try:
        driver.get(url)
        time.sleep(2)

        # Accept cookies
        driver.find_element(By.ID, 'onetrust-accept-btn-handler').click()

        listings = get_listings_from_li_tags(driver)
        print(str(listings))

        with Pool(cpu_count()) as p:
            p.map(scrape_listing, listings)

    finally:
        driver.quit()
