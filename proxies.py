from bs4 import BeautifulSoup
import requests
import pandas as pd

def get_proxies(count=5):
    '''Function to scrape the proxy servers from free-proxy-list.net'''

    # Creating soup object with html content using GET request
    proxy_url = 'https://free-proxy-list.net/'
    response = requests.get(proxy_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Locating the <table>
    table = soup.find('table')

    # Extracting the table headers
    col_titles = [th.text for th in table.find('thead').find('tr').find_all('th')]
    
    # Extracting te table content
    rows = table.find('tbody').find_all('tr')
    data = []
    for row in rows:
        row = [td.text for td in row.find_all('td')]
        data.append(dict((ct,rv) for ct, rv in zip(col_titles, row)))
    
    # Creating pandas DataFrame 
    proxies = pd.DataFrame(data)
    proxies = proxies.head(count)
    
    # Returning the proxy string in format of "<server_IP>:<PORT>"
    proxies = [f'{row[col_titles[0]]}:{row[col_titles[1]]}' for _, row in proxies.iterrows()]
    return proxies