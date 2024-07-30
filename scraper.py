import time
from selenium import webdriver
from selenium.webdriver.common.by import By

url = 'https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/mazowieckie/warszawa/warszawa/warszawa'
driver = webdriver.Chrome()


if __name__ == '__main__':
    try:
        driver.get(url)
        time.sleep(5)

        list_items = driver.find_elements(By.TAG_NAME, 'li')
        listings = []
        for li in list_items:

            try:
                article = li.find_element(By.TAG_NAME, 'article')
                listings.append(article)
                # print("\n\n ========== \n\n")
                # print(article.text)
                # print("\n\n ========== \n\n")
            except:
                continue
        print(len(listings))
    finally:
        driver.quit()