# IPL Statistics Web Scraping

## Introduction
The Indian Premier League (IPL) is a professional Twenty20 cricket league in India, founded in 2008 by the Board of Control for Cricket in India (BCCI). IPL features franchise teams representing different Indian cities, with top cricket players from around the world participating. The league is one of the most popular and lucrative cricket competitions globally, attracting millions of viewers and large sponsorship deals. 

At the end of each IPL season, top-performing players are recognized with prestigious awards such as the Orange Cap (for the batsman with the highest runs) and the Purple Cap (for the bowler with the most wickets).

This project focuses on scraping detailed statistics of both batsmen and bowlers from all IPL seasons, spanning from 2009 to 2024. The data collected for batsmen includes runs scored, matches and innings played, batting position, highest score, average runs, strike rate, centuries, half-centuries, and boundaries (4s and 6s). For bowlers, the data includes wickets taken, matches and innings played, overs bowled, runs conceded, bowling average, and economy rate.

## Project Motivation
The goal of this project is to create a comprehensive dataset of IPL player statistics, which can then be used for future data analysis projects. While this project focuses solely on scraping the data, it lays the groundwork for insightful analytics, such as exploring trends, comparing players' performances over time, and predicting outcomes based on past statistics.

## Prerequisites
- A **Firefox** browser is required for this project, as it is not compatible with Chrome.
- Python [requirements](requirements.txt) used include:
  - Selenium
  - BeautifulSoup
  - Pandas

## Methodology
The IPL statistics website provides dedicated pages for each season. The methodology involves visiting these pages and scraping the data for both batsmen and bowlers. 

Key steps include:
- **Selenium**: Used for web navigation and simulating user interactions (e.g., clicking buttons and drop-down menus).
- **BeautifulSoup**: Used for parsing HTML content and extracting relevant table data.
- Handling elements like "Accept Cookies" and "View All" buttons, selecting dropdowns, and navigating between batsman and bowler stats.
- Rate limiting is tackled using proxy servers scraped from `free-proxy-list.net`.
- The scraped raw data is stored in text files and transformed into CSV files using Pandas.

## Solution Design
- **Wait Times**: Pauses execution between steps to allow content to load, mimicking human behavior to avoid bot detection.
- **Proxy Management**: A rotating proxy setup is used to avoid rate limits.
- **Retry Mechanism**: Retries scraping for failed web pages to ensure all seasons are successfully processed.

## Data Storage and Transformation
- The raw HTML data is stored in text files in the `./scraped_data` directory.
- The raw HTML is then transformed into structured CSV files using Pandas, stored in the `./transformed_data` directory.

## Project Structure
- [scrapper.py](scrapper.py): Main script for scraping data from the IPL stats website.
- [proxies.py](proxies.py): Script for scraping and managing proxy servers.
- [transform.py](transform.py): Script for transforming raw HTML data into CSV files.
- [./log](./log): Contains log files for web scraping and transformation processes.
- [./scraped_data](./scraped_data): Directory containing raw HTML data.
- [./transformed_data](./transformed_data): Directory containing processed CSV files.

## Challenges Faced
- **Rate Limiting**: Proxy servers were employed to avoid getting blocked after making too many requests.
- **Website Slowness and JavaScript Errors**: Selenium was used with interrupts to wait for elements to load. A retry mechanism handled website errors that prevented data loading on certain pages.

## Conclusion
This IPL web scraping project successfully gathers comprehensive statistics on both batsmen and bowlers from all IPL seasons, setting the stage for further data analysis. The data can be used to analyze player performances, identify trends, and gain insights into IPL matches.

## Contact
Feel free to reach out for any questions or collaborations!

- **Email**: [satyapanthi.t@northeastern.edu](mailto:satyapanthi.t@northeastern.edu)
- **LinkedIn**: [@tapaswi-v-s](https://www.linkedin.com/in/tapaswi-v-s/)
