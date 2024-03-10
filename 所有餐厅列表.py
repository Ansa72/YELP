import csv
import time
import random
import requests
from lxml import etree
import pandas as pd

new_save_obj = {
    'city': [],
    'title': [],
    'rank': [],
    'point': [],
    'tag': [],
    'link': [],
    'review': [],
}

with open('city_links.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        city_url = row[0].replace('/', '').replace('-', ',').title()
        print(city_url)

        for i in [random.randint(0,4),random.randint(5,8),random.randint(9,12),random.randint(13,16),random.randint(17,20)]:
            url = f'https://www.yelp.com/search?cflt=restaurants&find_loc={city_url}&start={i*10}'
            headers = {
                'Cookie': 'bse=aaf54a8504e5459ca9054b9b9f4710a5; hl=en_US; wdi=2|D2EB2C37FE7743B2|0x1.93bd4df9d0fdp+30|620d088025fbf980; g_state={"i_p":1694152357210,"i_l":3}; recentlocations=Napa%2C+CA%2C+US%3B%3BNapa%2C+CA%3B%3BScottsdale%2C+AZ%2C+US%3B%3Bscottsdale-az-us%3B%3BScottsdale%2C+AZ%3B%3BPhoenix%3B%3BPhoenix%2C%3B%3BPhoenix%2C+AZ; location=%7B%22parent_id%22%3A+45%2C+%22address2%22%3A+%22%22%2C+%22longitude%22%3A+-111.92734753081055%2C+%22unformatted%22%3A+%22Scottsdale%2CAz%2CUs%22%2C+%22country%22%3A+%22US%22%2C+%22state%22%3A+%22AZ%22%2C+%22min_longitude%22%3A+-111.96138300000001%2C+%22county%22%3A+%22Maricopa+County%22%2C+%22city%22%3A+%22Scottsdale%22%2C+%22zip%22%3A+%22%22%2C+%22max_longitude%22%3A+-111.78791197617181%2C+%22accuracy%22%3A+4%2C+%22address1%22%3A+%22%22%2C+%22provenance%22%3A+%22YELP_GEOCODING_ENGINE%22%2C+%22display%22%3A+%22Scottsdale%2C+AZ%22%2C+%22location_type%22%3A+%22locality%22%2C+%22max_latitude%22%3A+33.85662465458778%2C+%22latitude%22%3A+33.499404636990256%2C+%22min_latitude%22%3A+33.45888641584279%2C+%22place_id%22%3A+%221356%22%2C+%22address3%22%3A+%22%22%2C+%22borough%22%3A+%22%22%2C+%22isGoogleHood%22%3A+false%2C+%22language%22%3A+null%2C+%22neighborhood%22%3A+%22%22%2C+%22polygons%22%3A+null%2C+%22usingDefaultZip%22%3A+false%2C+%22confident%22%3A+null%7D; uuac=jtodetbQyzuhlENNTvh6ld1FwqP6O_njNJ916PV9xdc; xcj=1|LR1m4NN489ePVwxYRdE6k7vAMkOHh_Hvr4HEdZLeH-Y; bsi=1%7C77f9fac6-e60b-4ef2-a19f-d2f6b594c040%7C1693617740192%7C1693617737929; OptanonConsent=isGpcEnabled=0&datestamp=Sat+Sep+02+2023+09%3A22%3A22+GMT%2B0800+(China+Standard+Time)&version=202304.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=afe311b8-5df9-43aa-b8d6-20ac10139aee&interactionCount=1&landingPath=https%3A%2F%2Fwww.yelp.com%2Fsearch%3Ffind_desc%3DRestaurants%26find_loc%3DPhoenix%26start%3D10&groups=BG82%3A1%2CC0003%3A1%2CC0002%3A1%2CC0001%3A1%2CC0004%3A1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62'
            }
            r = requests.get(url=url, headers=headers)
            tree = etree.HTML(r.text)
            al = tree.xpath('//li[@class="  border-color--default__09f24__NPAKY"]')
            print(len(al))

            if len(al) < 1:
                print(r.text)
                time.sleep(200)
                r = requests.get(url=url, headers=headers)
                tree = etree.HTML(r.text)
                al = tree.xpath('//li[@class="  border-color--default__09f24__NPAKY"]')
                print(len(al))
                if len(al) < 1:
                    continue
            for a in al:
                try:
                    title = a.xpath('.//h3[@class="css-1agk4wl"]/span[@class=" css-1egxyvc"]/a[@class="css-19v1rkv"]/text()')[0].strip()
                except:
                    title = ''
                try:
                    point = a.xpath('.//span[@class=" css-gutk1c"]/text()')[0].strip()
                except:
                    point = ''
                try:
                    tag = a.xpath('.//span[@class="css-11bijt4"]/text()')
                except:
                    tag = []
                try:
                    link = a.xpath('.//h3[@class="css-1agk4wl"]/span[@class=" css-1egxyvc"]/a[@class="css-19v1rkv"]/@href')[0].strip()
                except:
                    link = ''
                try:
                    review = a.xpath('.//span[@class="css-8xcil9"]/text()')[0].strip()
                except:
                    review = ''
                try:
                    rank = a.xpath('.//h3[@class="css-1agk4wl"]/span[@class=" css-1egxyvc"]/text()')[0].strip()
                except:
                    rank = ''
                if rank != '':
                    new_save_obj['city'].append(row[1])
                    new_save_obj['title'].append(title)
                    new_save_obj['point'].append(point)
                    new_save_obj['tag'].append(tag)
                    new_save_obj['link'].append(link)
                    new_save_obj['review'].append(review)
                    new_save_obj['rank'].append(rank)
                    print(rank, title, point, tag, review, 'https://www.yelp.com' + link)

            time.sleep(5)

            df = pd.DataFrame(new_save_obj)
            df.to_csv('很多城市餐厅列表2.csv', index=False)

