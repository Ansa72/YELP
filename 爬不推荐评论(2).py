import re
import requests
from lxml import etree
import math
import pandas as pd
import csv
import time

new_save_obj = {
    'city': [],
    'r_name': [],
    'username': [],
    'text': [],
    'address': [],
    'star': [],
    'src': [],
    'time': [],
    'friend_count': [],
    'review_count': [],
    'photo_count': []
}

with open('抽样后餐厅列表.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
        city = row[0]
        r_name = row[1]
        link = re.findall('/biz/([\s\S]+)', row[5])[0]
        print(city, r_name, link)
        time.sleep(1)

        try:
            url = f'https://www.yelp.com/not_recommended_reviews/{link}?not_recommended_start=0'
            headers = {
                'Cookie': 'bse=aaf54a8504e5459ca9054b9b9f4710a5; hl=en_US; wdi=2|D2EB2C37FE7743B2|0x1.93bd4df9d0fdp+30|620d088025fbf980; g_state={"i_p":1694152357210,"i_l":3}; recentlocations=Napa%2C+CA%2C+US%3B%3BNapa%2C+CA%3B%3BScottsdale%2C+AZ%2C+US%3B%3Bscottsdale-az-us%3B%3BScottsdale%2C+AZ%3B%3BPhoenix%3B%3BPhoenix%2C%3B%3BPhoenix%2C+AZ; location=%7B%22parent_id%22%3A+45%2C+%22address2%22%3A+%22%22%2C+%22longitude%22%3A+-111.92734753081055%2C+%22unformatted%22%3A+%22Scottsdale%2CAz%2CUs%22%2C+%22country%22%3A+%22US%22%2C+%22state%22%3A+%22AZ%22%2C+%22min_longitude%22%3A+-111.96138300000001%2C+%22county%22%3A+%22Maricopa+County%22%2C+%22city%22%3A+%22Scottsdale%22%2C+%22zip%22%3A+%22%22%2C+%22max_longitude%22%3A+-111.78791197617181%2C+%22accuracy%22%3A+4%2C+%22address1%22%3A+%22%22%2C+%22provenance%22%3A+%22YELP_GEOCODING_ENGINE%22%2C+%22display%22%3A+%22Scottsdale%2C+AZ%22%2C+%22location_type%22%3A+%22locality%22%2C+%22max_latitude%22%3A+33.85662465458778%2C+%22latitude%22%3A+33.499404636990256%2C+%22min_latitude%22%3A+33.45888641584279%2C+%22place_id%22%3A+%221356%22%2C+%22address3%22%3A+%22%22%2C+%22borough%22%3A+%22%22%2C+%22isGoogleHood%22%3A+false%2C+%22language%22%3A+null%2C+%22neighborhood%22%3A+%22%22%2C+%22polygons%22%3A+null%2C+%22usingDefaultZip%22%3A+false%2C+%22confident%22%3A+null%7D; uuac=8Z-ed34nC9QzNfzXVSYaCk1Ms9Wriixl-3R4Z13bck8; xcj=1|scCpKe9qvNguwAq4c3UElPl46F8Qjv_-QrGY-qMpDyc; pid=5407bc2656dd1e95; bsi=1%7C89801f15-bb89-4c3d-a53c-b0d0d80ca82f%7C1693787054327%7C1693787054324; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Sep+04+2023+08%3A25%3A08+GMT%2B0800+(China+Standard+Time)&version=202304.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=05cf4f18-d283-4cd8-9fb8-4efb8c3dcc82&interactionCount=1&landingPath=https%3A%2F%2Fwww.yelp.com%2Fnot_recommended_reviews%2Fs-and-v-urban-italian-scottsdale%3Fnot_recommended_start%3D10&groups=BG82%3A1%2CC0003%3A1%2CC0002%3A1%2CC0001%3A1%2CC0004%3A1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62'
            }
            r = requests.get(url=url,headers=headers)
            tree = etree.HTML(r.text)
            try:
                count_info = tree.xpath('.//div[@class="ysection not-recommended-reviews review-list-wide"]/h3/text()')[0]
                count = re.findall('([0-9]*?) reviews', count_info)[0].strip()
                page = math.ceil(int(count) / 10)
                print(f'页数:{page}')
                al = tree.xpath('.//div[@class="ysection not-recommended-reviews review-list-wide"]/ul[@class="ylist ylist-bordered reviews"]/li')
                print(len(al))
            except:
                continue
            for a in al:
                try:
                    username = a.xpath('.//span[@class="user-display-name"]/text()')[0]
                except:
                    username = ''
                try:
                    text1 = a.xpath('.//div[@class="review-content"]/p/text()')
                    text2 = a.xpath(('.//div[@class="review-content"]/p/br/text()'))
                    text = ''.join(text1+text2)
                except:
                    text = ''
                try:
                    address = a.xpath('.//li[@class="user-location responsive-hidden-small"]/b/text()')[0]
                except:
                    address = ''
                try:
                    src = a.xpath('.//div[@class="photo-box pb-60s"]/img/@src')[0]
                except:
                    src = ''
                try:
                    star = a.xpath('.//div[@class="biz-rating__stars"]/div/@title')[0]
                    star = re.findall('([\s\S]*?)star rating', star)[0].strip()
                except:
                    star = ''
                try:
                    time1 = a.xpath('.//span[@class="rating-qualifier"]/text()')[0].strip()
                except:
                    time1 = ''
                try:
                    friend_count = a.xpath('.//li[@class="friend-count responsive-small-display-inline-block"]/b/text()')[0]
                except:
                    friend_count = ''
                try:
                    review_count = a.xpath('.//li[@class="review-count responsive-small-display-inline-block"]/b/text()')[0]
                except:
                    review_count = ''
                try:
                    photo_count = a.xpath('.//li[@class="photo-count responsive-small-display-inline-block"]/b/text()')[0]
                except:
                    photo_count = ''

                new_save_obj['city'].append(city)
                new_save_obj['r_name'].append(r_name)
                new_save_obj['username'].append(username)
                new_save_obj['text'].append(text)
                new_save_obj['address'].append(address)
                new_save_obj['src'].append(src)
                new_save_obj['star'].append(star)
                new_save_obj['time'].append(time1)
                new_save_obj['friend_count'].append(friend_count)
                new_save_obj['review_count'].append(review_count)
                new_save_obj['photo_count'].append(photo_count)
                try:
                    print(username,address, text,star, time1, src, friend_count, review_count, photo_count)
                except:
                    print('打不出来')
            df = pd.DataFrame(new_save_obj)
            df.to_csv('不推荐评论.csv', index=False)
        except:
            continue


        for i in range(1, int(page)):
            try:
                time.sleep(2)
                url1 = f'https://www.yelp.com/not_recommended_reviews/{link}?not_recommended_start={10*i}'
                print(url1)
                r = requests.get(url=url1,headers=headers)
                tree = etree.HTML(r.text)
                al = tree.xpath('.//div[@class="ysection not-recommended-reviews review-list-wide"]/ul[@class="ylist ylist-bordered reviews"]/li')
                print(len(al))
                for a in al:
                    try:
                        username = a.xpath('.//span[@class="user-display-name"]/text()')[0]
                    except:
                        username = ''
                    try:
                        text1 = a.xpath('.//div[@class="review-content"]/p/text()')
                        text2 = a.xpath(('.//div[@class="review-content"]/p/br/text()'))
                        text = ''.join(text1 + text2)
                    except:
                        text = ''
                    try:
                        address = a.xpath('.//li[@class="user-location responsive-hidden-small"]/b/text()')[0]
                    except:
                        address = ''
                    try:
                        src = a.xpath('.//div[@class="photo-box pb-60s"]/img/@src')[0]
                    except:
                        src = ''
                    try:
                        star = a.xpath('.//div[@class="biz-rating__stars"]/div/@title')[0]
                        star = re.findall('([\s\S]*?)star rating', star)[0].strip()
                    except:
                        star = ''
                    try:
                        time1 = a.xpath('.//span[@class="rating-qualifier"]/text()')[0].strip()
                    except:
                        time1 = ''
                    try:
                        friend_count = a.xpath('.//li[@class="friend-count responsive-small-display-inline-block"]/b/text()')[0]
                    except:
                        friend_count = ''
                    try:
                        review_count = a.xpath('.//li[@class="review-count responsive-small-display-inline-block"]/b/text()')[0]
                    except:
                        review_count = ''
                    try:
                        photo_count = a.xpath('.//li[@class="photo-count responsive-small-display-inline-block"]/b/text()')[0]
                    except:
                        photo_count = ''

                    new_save_obj['city'].append(city)
                    new_save_obj['r_name'].append(r_name)
                    new_save_obj['username'].append(username)
                    new_save_obj['text'].append(text)
                    new_save_obj['address'].append(address)
                    new_save_obj['src'].append(src)
                    new_save_obj['star'].append(star)
                    new_save_obj['time'].append(time1)
                    new_save_obj['friend_count'].append(friend_count)
                    new_save_obj['review_count'].append(review_count)
                    new_save_obj['photo_count'].append(photo_count)

                    print(username, address, text, star, time1, src, friend_count, review_count, photo_count)
                df = pd.DataFrame(new_save_obj)
                df.to_csv('不推荐评论.csv', index=False)
            except:
                continue

