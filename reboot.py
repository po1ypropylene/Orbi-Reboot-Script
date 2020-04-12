import logging
import sys
from html.parser import HTMLParser

import requests
from requests.auth import HTTPBasicAuth

logger = logging.getLogger("reboot.py")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
fh = logging.FileHandler('reboot.log')
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)


class RebootRequest:
    def __init__(self, host, username, password):
        self.host = host
        self.auth = HTTPBasicAuth(username, password)
        self.session = requests.Session()
        self.request = self.session.get("http://%s/reboot.htm" % self.host, auth=self.auth)

    def get_html(self):
        return self.request.text

    def execute_reboot(self, token) -> bool:
        r = self.session.post("http://%s%s" % (self.host, token), data={"submit_flag": "reboot", "yes": "Yes"},
                              auth=self.auth)
        logger.debug(r)
        return r.status_code == 200


class RebootFormParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.token = ""

    def handle_starttag(self, tag, attrs):
        if tag == "form":
            self.token = attrs[1][1]

    def error(self, message):
        logger.error(message)

    def get_token(self):
        if self.token.startswith("/apply.cgi?/reboot_waiting.htm"):
            return self.token
        else:
            logger.error("Cannot get token!")
            exit(1)


def main():
    if len(sys.argv) != 4:
        print("Usage: python reboot.py <host> <username> <password>")
        exit(2)
    r = RebootRequest(sys.argv[1], sys.argv[2], sys.argv[3])
    parser = RebootFormParser()
    parser.feed(r.get_html())
    result = r.execute_reboot(parser.get_token())
    if result:
        logger.info("Reboot successful!")
        exit(0)
    else:
        logger.error("Reboot fail!")
        exit(1)


if __name__ == '__main__':
    main()
