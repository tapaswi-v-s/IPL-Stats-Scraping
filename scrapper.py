from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from transform import transform
import time, os
from proxies import get_proxies
from selenium.common.exceptions import WebDriverException

URL = 'https://www.iplt20.com/stats/'

# ===== Files =====
batsmen_file_name = '_batsmen.txt'
bowler_file_name = '_bowler.txt'
scrapping_log_file = 'scrapping_log.txt'
transformation_log_file = 'transformation_log.txt'

# ===== Directories =====
raw_data_dir = './scraped_data'
transformed_data_dir = './transformed'
log_dir = './log'

# ===== Create Necessary Directories =====
if not os.path.exists(raw_data_dir):
    os.mkdir(raw_data_dir)

if not os.path.exists(transformed_data_dir):
    os.mkdir(transformed_data_dir)

if not os.path.exists(log_dir):
    os.mkdir(log_dir)

            
ipl_years = list(range(2008, 2025))

def create_driver_with_proxy(proxy):
    '''Function to create web driver with given proxy server'''

    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument(f'--proxy-server={proxy}')
    firefox_options.page_load_strategy = 'none'
    return webdriver.Firefox(options=firefox_options)


def scrape(ipl_years = []):
    '''Function to scrape the batsman and the bowler data from the IPL Stats website'''
    
    global failed_years
    failed_years = []

    proxies = get_proxies(len(ipl_years))   
    print(f'Proxies: {proxies}') 

    with open(f'{log_dir}/{scrapping_log_file}', 'w') as log:
        for index, year in enumerate(ipl_years):
            bat_file_name = f'./scraped_data/{year}{batsmen_file_name}'
            try:
                driver = create_driver_with_proxy(proxies[index])
                driver.get(f'{URL}{year}')
                time.sleep(5)
                try:
                    # ====== Accept Cookies button click ====== 
                    wait = WebDriverWait(driver, 5)
                    accept_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.cookie__accept.cookie__accept_btn')))
                    accept_button.click()
                    
                    # ====== View All button click ====== 
                    wait = WebDriverWait(driver, 5)
                    view_all = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@ng-click="showAllBattingStatsList()"]')))
                    driver.execute_script("arguments[0].click();", view_all)
                    
                    # ====== Locate the <table> ====== 
                    wait = WebDriverWait(driver, 5)
                    table = driver.find_element(By.TAG_NAME, 'table')
                    wait.until(lambda _: table.is_displayed())

                    # ====== Dumping the table html in the .txt file ====== 
                    with open(bat_file_name, 'w') as file:
                        file.write(table.get_attribute('innerHTML'))
                    
                    # ====== Scroll to drop-down row ====== 
                    driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight/40);")
                    time.sleep(2)
                    
                    # ====== Bowlers Selection Workflow ====== 
                    row = driver.find_elements(By.XPATH, '//div[contains(@class, "cSBDisplay") \
                                            and @ng-click="cSBShowList($event)"]')
                    row[1].click()
                    time.sleep(1)
                    span = driver.find_element(By.XPATH, '//span[contains(@class, "cSBListFItems")\
                                                and @ng-click="statsTypeFilterChange(\'bowlers\')"]')
                    span.click()
                    time.sleep(1)

                    div = driver.find_element(By.XPATH, '//div[contains(@class, "cSBListItems")\
                                            and contains(text(), "Purple Cap")]')
                    div.click()
                    
                    # ====== View All button click ====== 
                    view_all = driver.find_element(By.XPATH, '//a[@ng-click="showAllBattingStatsList()"]')
                    driver.execute_script("arguments[0].click();", view_all)

                    # ====== Locate the <table> ====== 
                    wait = WebDriverWait(driver, 5)
                    table = driver.find_element(By.TAG_NAME, 'table')
                    wait.until(lambda _: table.is_displayed())
                    time.sleep(5)
                    
                    # ====== Dumping the bowler's table html in the .txt file ======  
                    bowl_file_name = f'./scraped_data/{year}{bowler_file_name}'
                    with open(bowl_file_name, 'w') as file:
                        file.write(table.get_attribute('innerHTML'))
                    time.sleep(8)

                    print(f"Scrapping completed for the year: {year}")
                    log.write(f'Scrapping completed for the year: {year}\n')
                except: 
                    log.write(f'\n======= Scrapping failed for the year: {year} =======\n')
                    print(f'\n======= Scrapping failed for the year: {year} =======\n')
                    failed_years.append(year)
                driver.quit()
            except WebDriverException as e:
                print('Please install firefox browser to run this script')
                print(f'\nError: {e}')


scrape(ipl_years=ipl_years)

# Try scraping again for the failed years
while failed_years:
    print(f'Scrapping Failed for the years: {", ".join(list(map(str,failed_years)))}')
    response = input('Try scraping again for the failed years? (y/n): ')
    if response.lower() == 'y':
        scrape(ipl_years=failed_years) 
    else:
        break

transform()