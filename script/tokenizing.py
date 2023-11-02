import sys
import logging
from collections import Counter
from kiwipiepy import Kiwi
from typing import List


class Tokenizer:
    def __init__(self):
        self.tokenizer = Kiwi()

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

        return Counter(token_list)


if __name__ == "__main__":
    tokenizer = Tokenizer()
    logging.info("[INFO] Count for tokens")

    content_list = [content.rstrip('\n') for content in sys.stdin]
    token_counter = tokenizer.tokenize(content_list)

    for token, count in token_counter.most_common():
        print(token, count, sep="\t")
