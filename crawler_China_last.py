import requests
from bs4 import BeautifulSoup
import re
import json
from tqdm import tqdm

class  CoronaVirusSpider(object):
    def __init__(self):
        self.home_url = 'https://ncov.dxy.cn/ncovh5/view/pneumonia'
        self.headers= {'user-agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36"}

    def get_content_from_url(self,url):
        """
        发送请求，根据url获取响应的hml
        :param url:
        :return:
        """
        # 发送请求，
        reponse = requests.get(url,headers=self.headers)
        return reponse.content.decode()

    def parse_home_page(self,home_page,tag_id):
        """
        解析首页内容，获取解析后的python数据
        :param home_page: 首页的内容
        :return: 解析后的python数据
        """
        #解析
        soup = BeautifulSoup(home_page,'lxml')
        #print(soup)

        #提取数据，获取json格式的字符串
        script = soup.find(id= tag_id)
        text = script.text
        json_str = re.findall(r'\[.+\]',text)[0]
        #print(json_str)

        #将json字符串转换为python类型
        data = json.loads(json_str)
        return data
        #print(last_day_corona_virus)

    def save(self,data,path):
        """
        :param data: 要保存的数据
        :param path: 保存的路径
        :return:
        """
        #存储为json格式
        with open(path,'w',encoding='utf-8') as  fp:
            json.dump(data,fp,ensure_ascii=False,indent=4)

    def crawl_lasday_corona_virus(self):
        """
        采集最近一天的各国疫情数据
        :return:
        """
        #发送请求，获取首页内容
        home_page = self.get_content_from_url(self.home_url)
        #解析首页内容，获取最近一天的各国疫情数据
        last_day_corona_virus = self.parse_home_page(home_page,tag_id="getListByCountryTypeService2true")
        #保存数据
        self.save(last_day_corona_virus,'data/last_day_corona_virus.json')
    def craw_corona_virus(self):
        """
        采集2020-1-23以来各国疫情数据
        :return:
        """
        #1.加载各国疫情数据
        with open('data/last_day_corona_virus.json',encoding='utf-8') as  fp:
            last_day__corona_virus = json.load(fp)
        #print(last_day__corona_virus)
        #2.遍历各国疫情数据，获取统计的url
        corona_virus = []   #定义列表，用于存储各国至今的疫情数据
        for country in tqdm(last_day__corona_virus,'采集自今为止各国疫情信息'):
            #3.发送请求，获取各国至今的json数据
            statistics_data_url = country['statisticsData']
            statistics_data_json_str = self.get_content_from_url(statistics_data_url)
            #4.把json数据转换为python类型的数据，添加到列表中
            statistics_data = json.loads(statistics_data_json_str)['data']
            #print(statistics_data)
            for one_day in statistics_data:
                one_day['provinceName'] = country['provinceName']
                one_day['countryShortCode'] = country['countryShortCode']
            #print(statistics_data)
            corona_virus.extend(statistics_data)
        #5.把列表以json格式保存为文件
        self.save(corona_virus,'data/corona_virus.json')

    def crawl_lasday_corona_virus_of_china(self):
        """
        采集最近一天的各省疫情数据
        :return:
        """
        #1.发送请求，获取首页内容
        home_page = self.get_content_from_url(self.home_url)
        #2.解析首页内容，获取最近一天的各省疫情数据
        last_day_corona_virus_of_china = self.parse_home_page(home_page, tag_id="getAreaStat")
        #3.保存数据
        self.save(last_day_corona_virus_of_china,'data/last_day_corona_virus_of_china.json')

    def crawl_corona_virus_of_china(self):
        """
                采集2020-1-23以来各省疫情数据
                :return:
                """
        # 1.加载各省疫情数据
        with open('data/last_day_corona_virus_of_china.json', encoding='utf-8') as  fp:
            last_day__corona_virus_of_china = json.load(fp)
        # print(last_day__corona_virus)
        # 2.遍历各省疫情数据，获取统计的url
        corona_virus_of_china = []  # 定义列表，用于存储各省至今的疫情数据
        for country in tqdm(last_day__corona_virus_of_china, '采集自今为止各省疫情信息'):
            # 3.发送请求，获取各国至今的json数据
            statistics_data_url = country['statisticsData']
            statistics_data_json_str = self.get_content_from_url(statistics_data_url)
            # 4.把json数据转换为python类型的数据，添加到列表中
            statistics_data_of_china = json.loads(statistics_data_json_str)['data']
            # statistics_data = demjson.decode(statistics_data_json_str,encoding='utf-8')['data']
            # print(statistics_data)
            for one_day in statistics_data_of_china:
                one_day['provinceName'] = country['provinceName']
                one_day['provinceShortName'] = country['provinceShortName']
            # print(statistics_data)
            corona_virus_of_china.extend(statistics_data_of_china)
        # 5.把列表以json格式保存为文件
        self.save(corona_virus_of_china, 'data/corona_virus_of_china.json')

    def run(self):
        self.crawl_lasday_corona_virus()
        self.craw_corona_virus()
        self.crawl_lasday_corona_virus_of_china()
        self.crawl_corona_virus_of_china()

if __name__ == '__main__':
    spider = CoronaVirusSpider()
    spider.run()

