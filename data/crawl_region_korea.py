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
    confirmed_region = []  # 시도별확진자

    for i, d in enumerate(data):
        region = d.find_all('h4', class_='cityname')[0].text  # 지역이름
        temp = d.find_all('span', class_='num')
        confirmed, _, recovered, deaths, confirmed_rate = [
            element.text.replace(',', '') for element in temp]
        confirmed = int(confirmed)  # 확진자수
        recovered = int(recovered)  # 격리해제수
        deaths = int(deaths)  # 사망자수
        confirmed_rate = float(confirmed_rate)  # 십만명당발생율

        if i != 0:
            slicing = d.find_all('p', class_='citytit')[0].text
            confirmed_region_rate = float(
                slicing[:slicing.find('%')])  # 지역별확진자비율
        else:
            confirmed_region_rate = ''

        confirmed_region.append({
            'region': region,
            'confirmed': confirmed,
            'recovered': recovered,
            'deaths': deaths,
            'confirmed_rate': confirmed_rate,
            'confirmed_region_rate': confirmed_region_rate,
        })

    return confirmed_region


def run():
    data = get_data("http://ncov.mohw.go.kr/bdBoardList_Real.do?brdGubun=13")

    confirmed_region = parse_data(data)

    save_dir = './data/current_korea_region.json'
    crawler_name = 'crawl_region_korea.py'

    write_data(confirmed_region, save_dir, crawler_name)

print("⚙ [한국 지역별 현황] Starting")
run()
print("✔ [한국 지역별 현황] Updated current_korea_region.json")
