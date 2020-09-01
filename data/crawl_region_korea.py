import requests

from bs4 import BeautifulSoup
from utils import write_data


def get_data(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    data = soup.select('.rpsa_detail > div > div')
    data.pop()
    return data


def parse_data(data):
    confirmed_region = []

    for i, d in enumerate(data):
        region = d.find_all('h4', class_='cityname')[0].text
        temp = d.find_all('span', class_='num')
        confirmed, _, recovered, deaths, confirmed_rate = [
            element.text.replace(',', '') for element in temp]
        confirmed = int(confirmed)
        recovered = int(recovered)
        deaths = int(deaths)
        confirmed_rate = float(confirmed_rate)

        if i != 0:
            slicing = d.find_all('p', class_='citytit')[0].text
            confirmed_region_rate = float(slicing[:slicing.find('%')])
            confirmed_region_class = 'none'
            if confirmed_region_rate > 30.0:
                confirmed_region_class = 'severe'
            elif confirmed_region_rate > 7.0:
                confirmed_region_class = 'moderate'
            elif confirmed_region_rate > 0.3:
                confirmed_region_class = 'mild'
        else:
            confirmed_region_rate = ''
            confirmed_region_class = ''

        confirmed_region.append({
            'region': region,
            'confirmed': confirmed,
            'recovered': recovered,
            'deaths': deaths,
            'confirmed_rate': confirmed_rate,
            'confirmed_region_rate': confirmed_region_rate,
            'confirmed_region_class': confirmed_region_class,
        })

    return confirmed_region

def update_svg_map(confirmed_region):
    map_template = open('./resources/templates/korea_map.svg', 'r', encoding='UTF-8').read()
    korea_map = open('./data/current_korea_region.svg', 'w', encoding='UTF-8')
    for data in confirmed_region:
        map_template = map_template.replace(data['region'], data['confirmed_region_class'])
    korea_map.write(map_template)
    korea_map.close()


def run():
    data = get_data("http://ncov.mohw.go.kr/bdBoardList_Real.do?brdGubun=13")

    confirmed_region = parse_data(data)

    save_dir = './data/current_korea_region.json'
    crawler_name = 'crawl_region_korea.py'

    write_data(confirmed_region, save_dir, crawler_name)

    update_svg_map(confirmed_region)

print("⚙ [한국 지역별 현황] Starting")
run()
print("✔ [한국 지역별 현황] Updated current_korea_region.json, current_korea_region.svg")
