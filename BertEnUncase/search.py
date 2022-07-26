from bs4 import BeautifulSoup
from requests import get
import re
import os
os.environ["CUDA_VISIBLE_DEVICES"]="-1"
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text

Tradition = ["dantri.com.vn", "tuoitre.vn", "vietnamnet.vn", "24h.com.vn",
           "baomoi.com", "nhandan.vn", "tienphong.vn", "doisongphapluat.com",
           "vnexpress.net", "thanhnien.vn", "zingnews.vn","laodong.vn", "vov.vn", "danviet.vn",
           "phunuvietnam.vn", "baotintuc.vn", "vtc.vn", "baogiaothong.vn", "nguoiduatin.vn", "vtv.vn"]

Tradition_names = ["Dân Trí", "Tuổi Trẻ", "Vietnamnet", "24h",
           "Báo Mới", "Nhân Dân", "Tiền Phong", "Đời Sống Pháp Luật",
           "VNexpress", "Thanh Niên", "Zing News", "Lao Động", "VOV", "Dân Việt",
           "Phụ nữ Việt Nam", "Tin Tức", "VTC", "Giao Thông", "Người Đưa Tin", "VTV"]

tf.get_logger().setLevel('ERROR')

saved_model_path = "fakenews.h5"
reloaded_model = tf.keras.models.load_model(saved_model_path, custom_objects={'KerasLayer': hub.KerasLayer})


def search(term, num_results=20, lang="vi"):
    usr_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/61.0.3163.100 Safari/537.36'}
    def no_accent_vietnamese(s):
        s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
        s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
        s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
        s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
        s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
        s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
        s = re.sub(r'[ìíịỉĩ]', 'i', s)
        s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
        s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
        s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
        s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
        s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
        s = re.sub(r'[Đ]', 'D', s)
        s = re.sub(r'[đ]', 'd', s)
        return s


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

    demos = [no_accent_vietnamese(term)]
    reloaded_results = tf.sigmoid(reloaded_model(tf.constant(demos)))

    html = fetch_results(term, num_results, lang)
    tmp = list(parse_results(html))
    final = [float(reloaded_results[0][0])]
    for step in range(1, len(tmp), 2):
        tam = define(tmp[step])
        if tam != -1:
            final.extend([tmp[step-1], tmp[step], Tradition_names[tam]])
    return final

print(search("sinh viên"))