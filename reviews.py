import csv
import re
import time
import requests
import pandas as pd
import math


new_save_obj = {
    'city': [],
    'name': [],
    'markupDisplayName': [],
    'displayLocation': [],
    'src': [],
    'friendCount': [],
    'reviewCount': [],
    'photoCount': [],
    'text': [],
    'localizedDate': [],
    'rating': []
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Cookie': 'bse=aaf54a8504e5459ca9054b9b9f4710a5; hl=en_US; wdi=2|D2EB2C37FE7743B2|0x1.93bd4df9d0fdp+30|620d088025fbf980; g_state={"i_p":1694152357210,"i_l":3}; recentlocations=Napa%2C+CA%2C+US%3B%3BNapa%2C+CA%3B%3BScottsdale%2C+AZ%2C+US%3B%3Bscottsdale-az-us%3B%3BScottsdale%2C+AZ%3B%3BPhoenix%3B%3BPhoenix%2C%3B%3BPhoenix%2C+AZ; location=%7B%22parent_id%22%3A+45%2C+%22address2%22%3A+%22%22%2C+%22longitude%22%3A+-111.92734753081055%2C+%22unformatted%22%3A+%22Scottsdale%2CAz%2CUs%22%2C+%22country%22%3A+%22US%22%2C+%22state%22%3A+%22AZ%22%2C+%22min_longitude%22%3A+-111.96138300000001%2C+%22county%22%3A+%22Maricopa+County%22%2C+%22city%22%3A+%22Scottsdale%22%2C+%22zip%22%3A+%22%22%2C+%22max_longitude%22%3A+-111.78791197617181%2C+%22accuracy%22%3A+4%2C+%22address1%22%3A+%22%22%2C+%22provenance%22%3A+%22YELP_GEOCODING_ENGINE%22%2C+%22display%22%3A+%22Scottsdale%2C+AZ%22%2C+%22location_type%22%3A+%22locality%22%2C+%22max_latitude%22%3A+33.85662465458778%2C+%22latitude%22%3A+33.499404636990256%2C+%22min_latitude%22%3A+33.45888641584279%2C+%22place_id%22%3A+%221356%22%2C+%22address3%22%3A+%22%22%2C+%22borough%22%3A+%22%22%2C+%22isGoogleHood%22%3A+false%2C+%22language%22%3A+null%2C+%22neighborhood%22%3A+%22%22%2C+%22polygons%22%3A+null%2C+%22usingDefaultZip%22%3A+false%2C+%22confident%22%3A+null%7D; uuac=jtodetbQyzuhlENNTvh6ld1FwqP6O_njNJ916PV9xdc; xcj=1|S5GtD2HESk29dph8RthkrcS0KahFNOu-VJHcEGkX0Os; bsi=1%7C962f2aa9-34f1-4eda-bf8e-98d7a24f6576%7C1693658660936%7C1693658627429; pid=ff8fbdc1a83a132b; OptanonConsent=isGpcEnabled=0&datestamp=Sat+Sep+02+2023+21%3A24%3A15+GMT%2B0800+(China+Standard+Time)&version=202304.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=59068ef4-6e29-4e04-90d8-d198c5b69c75&interactionCount=1&landingPath=https%3A%2F%2Fwww.yelp.com%2Fnot_recommended_reviews%2Fs-and-v-urban-italian-scottsdale%3Fnot_recommended_start%3D10&groups=BG82%3A1%2CC0003%3A1%2CC0002%3A1%2CC0001%3A1%2CC0004%3A1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62'
}

with open('抽样后餐厅列表.csv', 'r',encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        city = row[0]
        name = row[1]
        link = row[5]

        url1 = f'https://www.yelp.com{link}/review_feed?rl=en&q=&sort_by=relevance_desc&start=0'
        print(url1)
        try:
            res = requests.get(url=url1, headers=headers)
        except:
            time.sleep(500)
            res = requests.get(url=url1, headers=headers)
        try:
            count = re.findall('"count": (.*?)}', res.text)[0]
            page = math.ceil(int(count) / 10)
            print(page)
        except:
            page = 0

        for i in range(0, page):
            time.sleep(1)
            url = f'https://www.yelp.com{link}/review_feed?rl=en&q=&sort_by=relevance_desc&start={i * 10}'
            print(url)
            try:
                r = requests.get(url=url, headers=headers)
            except:
                time.sleep(500)
                r = requests.get(url=url, headers=headers)

            al = re.findall('"userId"([\S\s]*?)]}[,\]]', r.text)
            print(len(al))

            if len(al) == 0:
                time.sleep(500)
                r = requests.get(url=url, headers=headers)
                al = re.findall('"userId"([\S\s]*?)]}[,\]]', r.text)
                print(len(al))
                if len(al) == 0:
                    break

            for a in al:
                # print(a)
                markupDisplayName = re.findall('"markupDisplayName": "([\S\s]*?)",', a)[0].strip()  # 用户名
                displayLocation = re.findall('"displayLocation": "([\S\s]*?)",', a)[0].strip()  # 地址
                src = re.findall('"src": "([\S\s]*?)",', a)[0].strip()  # 头像
                friendCount = re.findall('"friendCount": ([\S\s]*?),', a)[0].strip()  # 朋友数
                reviewCount = re.findall('"reviewCount": ([\S\s]*?),', a)[0].strip()  # 评论数
                photoCount = re.findall('"photoCount": ([\S\s]*?),', a)[0].strip()  # 评论数
                text = re.findall('"text": "([\S\s]*?)",', a)[0].strip()
                localizedDate = re.findall('"localizedDate": "([\S\s]*?)",', a)[0].strip()
                rating = re.findall('"rating": ([\S\s]*?),', a)[0].strip()

                print(markupDisplayName, displayLocation, src, friendCount, reviewCount, photoCount, text, localizedDate, rating)

                new_save_obj['city'].append(city)
                new_save_obj['name'].append(name)
                new_save_obj['markupDisplayName'].append(markupDisplayName)
                new_save_obj['displayLocation'].append(displayLocation)
                new_save_obj['src'].append(src)
                new_save_obj['friendCount'].append(friendCount)
                new_save_obj['reviewCount'].append(reviewCount)
                new_save_obj['photoCount'].append(photoCount)
                new_save_obj['text'].append(text)
                new_save_obj['localizedDate'].append(localizedDate)
                new_save_obj['rating'].append(rating)

            df = pd.DataFrame(new_save_obj)
            df.to_csv('所有餐厅评论2.csv', index=False)



#     # for a in al:
#     #     try:
#     #         t = a.xpath('.//h3[@class="css-1agk4wl"]/span[@class=" css-1egxyvc"]/a[@class="css-19v1rkv"]/text()')
#     #     except:
#     #         t = []
#     #     try:
#     #         p = a.xpath('.//span[@class=" css-gutk1c"]/text()')
#     #     except:
#     #         p = ''
#     #     try:
#     #         tag = a.xpath('.//span[@class="css-11bijt4"]/text()')
#     #     except:
#     #         tag = ['']
#     #     try:
#     #         link = a.xpath('.//h3[@class="css-1agk4wl"]/span[@class=" css-1egxyvc"]/a[@class="css-19v1rkv"]/@href')
#     #     except:
#     #         link = ''
#     #     try:
#     #         review = a.xpath('.//span[@class="css-8xcil9"]/text()')
#     #     except:
#     #         review = ''
#     #     try:
#     #         rank = a.xpath('.//h3[@class="css-1agk4wl"]/span[@class=" css-1egxyvc"]/text()')
#     #     except:
#     #         rank = []


