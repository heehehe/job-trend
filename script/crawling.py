import os
import json
import requests
import time
import logging
import sys
import re

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

from typing import Dict


class Crawling:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
        }
        self.driver = webdriver.Safari() if sys.platform.lower() == "darwin" else webdriver.Chrome()

        self.info_key2name = {
            "경력": "career",
            "학력": "academic_background",
            "마감일": "deadline",
            "근무지역": "location"
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
        Run all process of crawling and extract data
        :param data_path: data path to write result data
        """
        pass

    def scroll_down_page(self):
        """
        Extract full-page source if additional pages appear when scrolling down
        :return page_source: extracted page source
        """
        page_source = ""
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            if page_source == self.driver.page_source:
                break
            else:
                page_source = self.driver.page_source

        return page_source

class CrawlingJumpit(Crawling):
    """
    Crawling of "https://www.jumpit.co.kr"
    """
    def __init__(self):
        super().__init__()

        self.endpoint = "https://www.jumpit.co.kr"
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
        

    def get_url_list(self):
        job_dict = {}
        for job_category in range(1, 23):
            self.driver.get(f"{self.endpoint}/positions?jobCategory={job_category}")
            time.sleep(1)

            page_source = self.scroll_down_page()

            soup = BeautifulSoup(page_source, 'html')
            position_list = [
                a_tag["href"] for a_tag in soup.find_all("a") if a_tag.get("href", "").startswith("/position/")
            ]

            job_dict[job_category] = {
                "page_source": page_source,
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


class CrawlingJobPlanet(Crawling) :
    """
    Crawling of "https://www.jobplanet.co.kr" 
    """
    def __init__(self) -> None:
        super().__init__()
        self.endpoint = "https://www.jobplanet.co.kr"

    def get_url_list(self,get_once=False) -> dict[str,dict[str,str]]:
        def job_find_window(job_filter) :
            self.driver.find_element(By.CLASS_NAME,"jply_btn_sm.inner_text.jf_b2").click()
            dev_tab = self.driver.find_element(By.CLASS_NAME,"filter_depth1_list").find_elements(By.CLASS_NAME,"filter_depth1_btn.jf_b1")
            for i in dev_tab:
                if i.text == job_filter :
                    i.click()
                else :
                    continue

        def apply_btn() :
            panel = self.driver.find_element(By.CLASS_NAME,"panel_bottom")
            apply_btn = panel.find_element(By.CLASS_NAME,"jply_btn_sm.ty_solid")
            apply_btn.click()

        def release_checked(before_obj) :
            clicked_list = before_obj.find_elements(By.CLASS_NAME,"jp-checkbox-checked_fill.checked")   
            for clk in clicked_list :
                clk.click() # 이전 직무 checkbox release


        self.driver.get(self.endpoint+"/job")
        time.sleep(1)

        for job_filter in ["개발","데이터"] :
            # job_find_window(job_filter)
            job_chkbox = [0]*10
            job_list_idx = 0
            job_dict = {}

            while len(job_chkbox) > job_list_idx :
                job_find_window(job_filter)
                job_chkbox = self.driver.find_elements(By.CLASS_NAME,"jply_checkbox_box")
                current_obj = job_chkbox[job_list_idx]  # index = 0은 직무 전체이므로 패스
                before_obj = job_chkbox[job_list_idx-1]
                release_checked(before_obj)

                job_name = current_obj.find_element(By.CLASS_NAME,"jf_b1").text
                
                if not job_name or job_name == f"{job_filter} 전체" :
                    job_list_idx +=1
                    apply_btn()
                    continue
                


                unchk_box = current_obj.find_element(By.CLASS_NAME,"jp-checkbox-unchecked.unchecked")
                unchk_box.click()
                    
                apply_btn()

                time.sleep(1)
                
                _page_source = ""
                
                while True:
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(1)
                    if get_once :
                        self.driver.execute_script("window.scrollTo(0, 0);")
                        break

                    if _page_source == self.driver.page_source:
                        self.driver.execute_script("window.scrollTo(0, 0);")
                        break
                    else:
                        _page_source = self.driver.page_source
                    


                soup = BeautifulSoup(self.driver.page_source,"html.parser")
                card_list = soup.select("div.item-card")
                
                href_list = [card.select_one("a").get("href") for card in card_list]
                content_dict = {}

                for href in href_list :
                    url = "https://www.jobplanet.co.kr" + href
                    content_dict[href] = url
                job_dict[job_name] = content_dict
                
                job_list_idx += 1
                
                time.sleep(1)
                if get_once : break

            job_find_window(job_filter)
            job_chkbox = self.driver.find_elements(By.CLASS_NAME,"jply_checkbox_box")
            before_obj = job_chkbox[job_list_idx-1]
            release_checked(before_obj)
            apply_btn()
        
        return job_dict

    def postprocess(self,job_dict:dict) -> dict:
        postprocess_dict = {}
        
        for job_name,info_dict in job_dict.items() :
            
            for job_detail_href, url in info_dict.items() :
                
                self.driver.get(url)
                time.sleep(1)

                soup = BeautifulSoup(self.driver.page_source,"html.parser")
                dd_list= soup.select("dd.recruitment-summary__dd")
                dt_list = soup.select("dt.recruitment-summary__dt")

            
                deadline = None                
                tech_list = []
                extra_info = {}
                for dt_num in range(len(dt_list)) :
                    key = dt_list[dt_num].get_text(strip=True)
                    value = dd_list[dt_num].get_text(strip=True)
                    if  key == "스킬" :                                                
                        tech_list = list(map(lambda x: x.strip(),value.split(",")))
                                            
                    elif key == "마감일" :                        
                        date_pat = re.compile("\d+\.\d+\.\d+")
                        deadline_pat = date_pat.search(value)
                        if "상시" in value or deadline_pat is None:
                            deadline = ""
                        else :                            
                            deadline = deadline_pat.group().strip()
                        extra_info[self.info_key2name["마감일"]] = deadline

                    elif key in self.info_key2name.keys() :
                        
                        extra_info[self.info_key2name[key]] = value
                    
                        

                title= soup.select_one('h1.ttl').get_text(strip=True)
                
                company = soup.select_one("span.company_name")
                company_id = company.find("a").get('href')
                company_name = company.get_text(strip=True)
                
                
                postprocess_dict[url] = {
                            "job_name": job_name,
                            "title": title,
                            "company_name": company_name,
                            "company_id": company_id,
                            "tag_id": [],
                            "tag_name": [],
                            "tech_list": tech_list
                        }
                postprocess_dict[url].update(extra_info)
            
        return postprocess_dict
        

    def run(self, data_path: str):
        job_dict = self.get_url_list()
        result_dict = self.postprocess(job_dict)


        with open(os.path.join(data_path, "jobplanet.content.info.jsonl"), "w") as f:
            for url, info in result_dict.items():
                info["url"] = f"{self.endpoint}{url}"
                f.write(json.dumps(info) + "\n")
    
        self.driver.close()


class CrawlingWanted(Crawling):
    """
    Crawling of "https://www.wanted.co.kr"
    """

    def __init__(self):
        super().__init__()
        self.endpoint = "https://www.wanted.co.kr"
        self.job_parent_category = 518
        self.job_category_id2name = {
            10110: "소프트웨어 엔지니어",
            873: "웹 개발자",
            872: "서버 개발자",
            669: "프론트엔드 개발자",
            660: "자바 개발자",
            900: "C,C++ 개발자",
            899: "파이썬 개발자",
            1634: "머신러닝 엔지니어",
            674: "DevOps / 시스템 관리자",
            665: "시스템,네트워크 관리자",
            655: "데이터 엔지니어",
            895: "Node.js 개발자",
            677: "안드로이드 개발자",
            678: "iOS 개발자",
            658: "임베디드 개발자",
            877: "개발 매니저",
            1024: "데이터 사이언티스트",
            1026: "기술지원",
            676: "QA,테스트 엔지니어",
            672: "하드웨어 엔지니어",
            1025: "빅데이터 엔지니어",
            671: "보안 엔지니어",
            876: "프로덕트 매니저",
            10111: "크로스플랫폼 앱 개발자",
            1027: "블록체인 플랫폼 엔지니어",
            10231: "DBA",
            893: "PHP 개발자",
            661: ".NET 개발자",
            896: "영상,음성 엔지니어",
            10230: "ERP전문가",
            939: "웹 퍼블리셔",
            898: "그래픽스 엔지니어",
            795: "CTO,Chief Technology Officer",
            10112: "VR 엔지니어",
            1022: "BI 엔지니어",
            894: "루비온레일즈 개발자",
            793: "CIO,Chief Information Officer"
        }
        self.tag2field_map = {
            "설명": "description",
            "주요업무": "main_work",
            "자격요건": "qualification",
            "우대사항": "preferences",
            "혜택 및 복지": "welfare",
            "기술스택 ・ 툴": "tech_list"
        }

    def get_url_list(self):
        job_dict = {}
        for job_category in self.job_category_id2name:
            self.driver.get(f"{self.endpoint}/wdlist/{self.job_parent_category}/{job_category}")

            page_source = self.scroll_down_page()

            soup = BeautifulSoup(page_source, 'html.parser')
            ul_element = soup.find('ul', {'data-cy': 'job-list'})
            position_list = [
                a_tag['href'] for a_tag in ul_element.find_all('a') if a_tag.get('href', '').startswith('/wd/')
            ]

            job_dict[job_category] = {
                "page_source": page_source,
                "position_list": position_list
            }

        return job_dict

    def get_recruit_content_info(self, job_dict):
        position_content_dict = {}

        for job_category, job_info in job_dict.items():
            content_dict = {}
            for position_url in job_info["position_list"]:
                self.driver.get(f"self.endpoint{position_url}")
                time.sleep(0.1)
                content_dict[position_url] = self.driver.page_source

            position_content_dict[job_category] = content_dict

        return position_content_dict

    def postprocess(self, position_content_dict):
        postprocess_dict = {}

        for job_category, info_dict in position_content_dict.items():
            for url, content in info_dict.items():
                result = {}

                soup = BeautifulSoup(content, 'html')

                job_header = soup.find("section", class_="JobHeader_className__HttDA")

                result['title'] = job_header.find("h2").text

                _company_info = job_header.find("span", class_="JobHeader_companyNameText__uuJyu")
                result['company_name'] = _company_info.text
                result['company_id'] = _company_info.find("a")["href"]

                _tag_list = job_header.find("div", class_="Tags_tagsClass__mvehZ").find_all("a")
                result['tag_name'] = [tag.text.lstrip("#") for tag in _tag_list]
                result['tag_id'] = [tag["href"] for tag in _tag_list]

                job_body = soup.find("section", class_="JobDescription_JobDescription__VWfcb")

                p_tags = job_body.find_all("p")
                h3_tags = job_body.find_all("h3")

                for i, p_tag in enumerate(p_tags):
                    h3_tag = h3_tags[i - 1].text if i != 0 else "설명"
                    if h3_tag not in self.tag2field_map:
                        continue

                    field_name = self.tag2field_map[h3_tag]
                    if field_name == "tech_list":
                        result[field_name] = [
                            skill.text for skill in p_tag.find("div").find_all("div")
                        ]
                    else:
                        result[field_name] = [
                            line for lines in p_tag.text.split("<br>") for line in lines.split("• ") if line
                        ]

                postprocess_dict[url] = result

        return postprocess_dict

    def run(self, data_path: str):
        job_dict = self.get_url_list()
        position_content_dict = self.get_recruit_content_info(job_dict)
        result_dict = self.postprocess(position_content_dict)

        with open(os.path.join(data_path, "wanted.content.info.jsonl"), "w") as f:
            for url, info in result_dict.items():
                info["url"] = f"{self.endpoint}{url}"
                f.write(json.dumps(info) + "\n")


CRAWLING_CLASS = {
    "jumpit": CrawlingJumpit,
    "saramin": CrawlingSaramin,
    "jobplanet": CrawlingJobPlanet,
    "wanted": CrawlingWanted
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
    parser.add_argument("-s", "--site_type", help="type of site", default="jobplanet")
    parser.add_argument("-l", "--log_type", help="type of log", default="info")
    parser.add_argument("-d", "--data_path", help="path of data")
    args = parser.parse_args()
    main(args)
