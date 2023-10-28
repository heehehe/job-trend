import requests
from bs4 import BeautifulSoup
from collections import Counter
from kiwipiepy import Kiwi
from typing import List, Dict


class Crawling:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
        }
        self.tokenizer = Kiwi()

    def requests_get(self, url: str) -> requests.Response:
        """
        Execute request.get for url
        :param url: url to get requests
        :return: response for url
        """
        with requests.Session() as s:
            response = s.get(url, headers=self.headers)
        return response

    def get_recruit_content_dict(self):
        return []

    def tokenize(self, content_list: List[str]) -> Counter:
        """
        tokenize for list of contents
        :param content_list: list of contents
        :return: list of tokens
        """
        token_list = []

        for content in content_list:
            token_list.extend([
                token.form for token in self.tokenizer.tokenize(content) if token.tag == 'NNG'
            ])

        token_counter = Counter(token_list)

        return token_counter


class CrawlingSaramin(Crawling):
    def __init__(self):
        super().__init__()
        self.endpoint = "https://www.saramin.co.kr"

    def get_id_list(self, category_id: int = 83) -> List[str]:
        """
        Crawling id list of recruitment pages
        :param category_id: id of recruit category
        :return: list of recruitment page urls
        """
        def _crawl_id_list(page_number: int) -> List[str]:
            """ Crawling id list for specific page number on recruitment page
            :param page_number: number of page to crawl
            :return: list of recruitment page urls for specific page
            """
            response = self.requests_get(
                f"{self.endpoint}/zf_user/search?cat_kewd={category_id}&recruitPageCount=100&recruitPage={page_number}"
            )
            soup = BeautifulSoup(response.text, 'html.parser')
            contents = soup.find_all('div', class_='item_recruit')

            return [content.get('value') for content in contents]

        id_list = []
        recruit_page = 1
        _id_list = _crawl_id_list(recruit_page)

        while _id_list:
            id_list.extend(_id_list)
            recruit_page += 1
            _id_list = _crawl_id_list(recruit_page)

        return id_list

    def get_recruit_content_dict(self, category_id: int = 83) -> Dict[str, str]:
        """
        Get recruit contents for each url
        :param category_id: id of recruit category
        :return: dict of recruit contents for each url (key: url / value: content)
        """
        recruit_content_dict = {}

        for _id in self.get_id_list(category_id):
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

            recruit_content_dict[url] = recruit_contents.encode('utf-8').decode('unicode_escape')

        return recruit_content_dict


def main(args):
    crawling = Crawling()
    if args.type.lower() == "saramin":
        crawling = CrawlingSaramin()

    recruit_content_dict = crawling.get_recruit_content_dict()
    token_counter = crawling.tokenize(list(recruit_content_dict.values()))

    for token, count in token_counter:
        print(token, count, sep="\t")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type", help="type of site", default="saramin")
    args = parser.parse_args()
    main(args)