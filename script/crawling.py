import os
import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import logging
from typing import Dict


class Crawling:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
        }

    def requests_get(self, url: str) -> requests.Response:
        """
        Execute request.get for url
        :param url: url to get requests
        :return: response for url
        """
        with requests.Session() as s:
            response = s.get(url, headers=self.headers)
        return response

    def run(self, data_path: str):
        """
        run all process of crawling and extract data
        :param data_path: data path to write result data
        """
        pass


class CrawlingJumpit(Crawling):
    """
    Crawling of "https://www.jumpit.co.kr"
    """
    def __init__(self):
        super().__init__()
        self.endpoint = "https://www.jumpit.co.kr"
        self.driver = webdriver.Safari()
        self.job_category_id2name = {
            1: "서버/백엔드 개발자",
            2: "프론트엔드 개발자",
            3: "웹 풀스택 개발자",
            4: "안드로이드 개발자",
            5: "게임 클라이언트 개발자",
            6: "게임 서버 개발자",
            7: "DBA",
            8: "인공지능/머신러닝",
            9: "DevOps/시스템 엔지니어",
            10: "정보보안 담당자",
            11: "QA 엔지니어",
            12: "개발 PM",
            13: "HW/임베디드",
            15: "SW/솔루션",
            16: "IOS 개발자",
            17: "웹퍼블리셔",
            18: "크로스플랫폼 앱개발자",
            19: "빅데이터 엔지니어",
            20: "VR/AR/3D",
            22: "블록체인",
            21: "기술지원"
        }
        self.info_key2name = {
            "경력": "career",
            "학력": "academic_background",
            "마감일": "deadline",
            "근무지역": "location"
        }

    def get_url_list(self):
        job_dict = {}
        for job_category in range(1, 23):
            self.driver.get(f"{self.endpoint}/positions?jobCategory={job_category}")
            time.sleep(1)

            _page_source = ""
            while True:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                if _page_source == self.driver.page_source:
                    break
                else:
                    _page_source = self.driver.page_source

            soup = BeautifulSoup(self.driver.page_source, 'html')

            position_list = []
            for a in soup.find_all("a"):
                if a.get("href").startswith("/position/"):
                    position_list.append(a.get("href"))

            job_dict[job_category] = {
                "page_source": self.driver.page_source,
                "position_list": position_list
            }

        return job_dict

    def get_recruit_content_info(self, job_dict):
        position_content_dict = {}
        for job_category, job_info in job_dict.items():
            content_dict = {}
            for position_url in job_info["position_list"]:
                self.driver.get("https://www.jumpit.co.kr" + position_url)
                time.sleep(0.1)
                content_dict[position_url] = self.driver.page_source

            position_content_dict[job_category] = content_dict

        return position_content_dict

    def postprocess(self, position_content_dict):
        postprocess_dict = {}

        for job_category, info_dict in position_content_dict.items():
            if job_category not in self.job_category_id2name:
                continue

            for url, content in info_dict.items():
                soup = BeautifulSoup(content, 'html')
                title = soup.find("h1").text

                try:
                    company = soup.find("div", class_="position_title_box_desc").find("a")
                except:
                    for a in soup.find_all(""):
                        if a.get("href", "").startswith("/company"):
                            company = a
                            break

                company_name = company.text
                company_id = company.get("href")

                tag_info = {}
                position_tags = soup.find("ul", class_="position_tags")
                if position_tags:
                    for li in position_tags.find_all("li"):
                        tag_id = li.find("a").get("href")
                        tag_text = li.text
                        tag_info[tag_id] = tag_text

                tech_list = []
                position_info = soup.find("section", class_="position_info")
                if position_info:
                    for dl in position_info.find_all("dl"):
                        if dl.find("dt").text == '기술스택':
                            break
                    for div in dl.find("dd").find_all("div"):
                        tech_list.append(div.text)

                extra_info = {}
                for dl in soup.find_all('dl'):
                    key = dl.find("dt").text
                    if key in self.info_key2name:
                        value = dl.find("dd").text
                        if key == "마감일" and value == "상시":
                            value = ""
                        extra_info[self.info_key2name[key]] = value

                postprocess_dict[url] = {
                    "job_category": job_category,
                    "job_name": self.job_category_id2name[job_category],
                    "title": title,
                    "company_name": company_name,
                    "company_id": company_id,
                    "tag_id": list(tag_info.keys()),
                    "tag_name": list(tag_info.values()),
                    "tech_list": tech_list
                }
                postprocess_dict[url].update(extra_info)

        return postprocess_dict

    def run(self, data_path: str):
        job_dict = self.get_url_list()
        position_content_dict = self.get_recruit_content_info(job_dict)
        result_dict = self.postprocess(position_content_dict)

        with open(os.path.join(data_path, "jumpit.content.info.jsonl"), "w") as f:
            for url, info in result_dict.items():
                info["url"] = f"{self.endpoint}{url}"
                f.write(json.dumps(info) + "\n")


class CrawlingSaramin(Crawling):
    """
    Crawling of "https://www.saramin.co.kr" (cannot distinguish details of content)
    """
    def __init__(self):
        super().__init__()
        self.endpoint = "https://www.saramin.co.kr"

    def get_id_dict(self, category_id: int = 83) -> Dict[str, str]:
        """
        Crawling id and title for recruitment pages
        :param category_id: id of recruit category
        :return: dict of recruitment page urls with title (key: url / value: title)
        """
        def _crawl_id(page_number: int) -> Dict[str, str]:
            """ Crawling id list for specific page number on recruitment page
            :param page_number: number of page to crawl
            :return: list of recruitment page urls for specific page
            """
            response = self.requests_get(
                f"{self.endpoint}/zf_user/search?cat_kewd={category_id}&recruitPageCount=100&recruitPage={page_number}"
            )
            soup = BeautifulSoup(response.text, 'html.parser')
            contents = soup.find_all('div', class_='item_recruit')

            id_dict = {}
            for content in contents:
                _id = content.get('value')
                title = content.find('h2', class_='job_tit').find('a').get('title')
                id_dict[_id] = title

            return id_dict

        id_dict = {}
        recruit_page = 1
        _id_dict = _crawl_id(recruit_page)

        while _id_dict:
            id_dict.update(_id_dict)
            recruit_page += 1
            _id_dict = _crawl_id(recruit_page)

        return id_dict

    def get_recruit_content_info(self, category_id: int = 83) -> Dict[str, Dict[str, str]]:
        """
        Get recruit contents for each url
        :param category_id: id of recruit category
        :return: dict of recruit contents for each url (key: url / value: title, content)
        """
        recruit_content_dict = {}

        for _id, title in self.get_id_dict(category_id).items():
            url = f"https://www.saramin.co.kr/zf_user/jobs/relay/view?rec_idx={_id}"
            response = self.requests_get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            recruit_content = ""
            for content in soup.find_all('script'):
                if 'recruit_content' in content.text:
                    recruit_content = content
                    break

            if recruit_content == "":
                continue

            content_text = recruit_content.text
            start_index = content_text.index('"recruit_contents":"')
            end_index = content_text.index('","kindness_expired_dt"')
            recruit_contents = content_text[start_index + len('"recruit_contents":"'):end_index]

            recruit_content_dict[url] = {
                "title": title,
                "content": recruit_contents.encode('utf-8').decode('unicode_escape')
            }

        return recruit_content_dict

    def run(self, data_path: str):
        """
        run all process of crawling and extract data
        :param data_path: data path to write result data
        """
        recruit_content_infos = self.get_recruit_content_info()

        with open(os.path.join(data_path, f"url.{args.site_type}.tsv"), "w") as f:
            for url, info in recruit_content_infos.items():
                f.write("\t".join([
                    url, info.get("title", ""), info.get("content", "")
                ]) + "\n")


CRAWLING_CLASS = {
    "jumpit": CrawlingJumpit,
    "saramin": CrawlingSaramin
}


def main(args):
    logger = logging.getLogger()
    logger.setLevel(
        logging.DEBUG if args.log_type.lower() == "debug" else logging.INFO
    )

    logging.info("[INFO] Set instance of crawling")
    crawling = CRAWLING_CLASS.get(args.site_type.lower(), Crawling)()

    logging.info("[INFO] Get recruit content info")
    crawling.run(args.data_path)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--site_type", help="type of site", default="saramin")
    parser.add_argument("-l", "--log_type", help="type of log", default="info")
    parser.add_argument("-d", "--data_path", help="path of data")
    args = parser.parse_args()
    main(args)
