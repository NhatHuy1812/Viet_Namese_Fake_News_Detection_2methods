from bs4 import BeautifulSoup
from requests import get

Tradition = ["dantri.com.vn", "tuoitre.vn", "vietnamnet.vn", "24h.com.vn",
           "baomoi.com", "nhandan.vn", "tienphong.vn", "doisongphapluat.com",
           "vnexpress.net", "thanhnien.vn", "zingnews.vn","laodong.vn", "vov.vn", "danviet.vn",
           "phunuvietnam.vn", "baotintuc.vn", "vtc.vn", "baogiaothong.vn", "nguoiduatin.vn", "vtv.vn"]

Tradition_names = ["Dân Trí", "Tuổi Trẻ", "Vietnamnet", "24h",
           "Báo Mới", "Nhân Dân", "Tiền Phong", "Đời Sống Pháp Luật",
           "VNexpress", "Thanh Niên", "Zing News", "Lao Động", "VOV", "Dân Việt",
           "Phụ nữ Việt Nam", "Tin Tức", "VTC", "Giao Thông", "Người Đưa Tin", "VTV"]

def search(term, num_results=20, lang="vi"):
    usr_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/61.0.3163.100 Safari/537.36'}

    def fetch_results(search_term, number_results, language_code):
        escaped_search_term = search_term.replace(' ', '+')

        google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(escaped_search_term, number_results+1,
                                                                              language_code)
        response = get(google_url, headers=usr_agent)
        response.raise_for_status()

        return response.text

    def define(l):
        for co, item in enumerate(Tradition):
            if item in l:
                return co
        return -1

    def parse_results(raw_html):
        soup = BeautifulSoup(raw_html, 'html.parser')
        result_block = soup.find_all('div', attrs={'class': 'g'})
        for result in result_block:
            link = result.find('a', href=True)
            title = result.find('h3')
            if link and title:
                yield title.text
                yield link['href']

    html = fetch_results(term, num_results, lang)
    tmp = list(parse_results(html))
    final = []
    for step in range(1, len(tmp), 2):
        tam = define(tmp[step])
        if tam != -1:
            final.extend([tmp[step-1], tmp[step], Tradition_names[tam]])
    return final
