from bs4 import BeautifulSoup
from requests import get

usr_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/61.0.3163.100 Safari/537.36'}

def fetch_results(html):
    response = get(html, headers=usr_agent)
    response.raise_for_status()
    return response.text

def parse_results(raw_html):
    soup = BeautifulSoup(raw_html, 'html.parser')
    result_block = soup.find_all('article')
    for result in result_block:
        title = result.find('h2')
        if title:
            yield title.text.replace('\n', '')


query_arr = list(parse_results(fetch_results('https://thanhnien.vn')))
print(len(query_arr))