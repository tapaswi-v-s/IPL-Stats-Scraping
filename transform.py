import os
from bs4 import BeautifulSoup
import pandas as pd

# ===== Files =====
batsmen_file_name = '_batsmen.txt'
bowler_file_name = '_bowler.txt'
scrapping_log_file = 'scrapping_log.txt'
transformation_log_file = 'transformation_log.txt'

# ===== Directories =====
raw_data_dir = './scraped_data'
transformed_data_dir = './transformed'
log_dir = './log'

def transform():
    '''Function to transform the scraped html files into .csv files'''
    
    # Fetching all the raw html files from the "scraped_data" directory
    for (_, __, files) in os.walk(raw_data_dir):
        break
    
    # Iterating over each raw file and transforming into csv file
    with open(f'{log_dir}/{transformation_log_file}', 'w') as log:
        for raw_file in files:
            try:
                with open(f'{raw_data_dir}/{raw_file}', 'r') as file:
                    
                    # Initializing the soup object with raw html content
                    soup = BeautifulSoup(file.read(), 'html.parser')
                    t_body = soup.find('tbody')
                    tr_s = t_body.find_all('tr')
                
                    # Extracting the column names from the table header
                    column_names = [th.text for th in tr_s[0].find_all('th')[1:]]

                    # Extracting the content of each row
                    data = []
                    for tr in tr_s[1:]: # Starting from 2nd row because first is header
                        td_s = [td for td in tr.find_all('td')[1:]]

                        # Extracting player name, image, and team from the first cell of the row
                        player_image = td_s[0].find('img') # Player Image URL
                        player_image = player_image['src'] if player_image.has_attr('src') else None
                        a_tag = td_s[0].find('a')
                        player_name = a_tag.find_all('div')[0].text # Player Name 
                        team = a_tag.find_all('div')[1].text # Team Name

                        # Extracting the values from the remaining columns
                        rest_values = [td.text for td in td_s[1:]]
                        row = dict(player=player_name, team=team, image=player_image)
                        row.update(dict((cn,rv) for cn, rv in zip(column_names, rest_values)))
                        data.append(row)
                    
                    # Creating Pandas Dataframe with the list of dictionaries 
                    # and saving the Dataframe into .csv file
                    output_file = raw_file.split('.')[0]+'.csv'
                    pd.DataFrame(data).to_csv(f'{transformed_data_dir}/{output_file}', index=False)
                    log.write(f'Transformed {raw_data_dir}/{raw_file} to {transformed_data_dir}/{output_file}\n')

                    print(f'Transformation Completed for: {raw_file}')
            except FileNotFoundError as e :
                log.write(f'====== File Not Found: {raw_data_dir}/{raw_file} ======\n')
        print(f'====== Transformation Completed, please find the .csv files here: {transformed_data_dir} ======')