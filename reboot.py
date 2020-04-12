import sys
from html.parser import HTMLParser

import requests
from requests.auth import HTTPBasicAuth


class RebootRequest:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.session = requests.Session()
        self._requests = self.session.get("http://%s/reboot.htm" % self.host,
                                          auth=HTTPBasicAuth(self.username, self.password))

    def get_html(self):
        return self._requests.text

    def get_cookies(self):
        return self._requests.cookies

    def execute_reboot(self, token) -> bool:
        r = self.session.post("http://%s%s" % (self.host, token), data={"submit_flag": "reboot", "yes": "Yes"})
        print(r)
        return r.status_code == 200


class RebootFormParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.token = ""

    def handle_starttag(self, tag, attrs):
        if tag == "form":
            self.token = attrs[1][1]
            if not str(self.token).startswith("/apply.cgi?/reboot_waiting.htm"):
                print("cannot get token!")
                exit(1)

    def error(self, message):
        print(message)

    def get_token(self):
        return self.token


def main():
    r = RebootRequest(sys.argv[1], sys.argv[2], sys.argv[3])
    parser = RebootFormParser()
    parser.feed(r.get_html())
    result = r.execute_reboot(parser.get_token())
    if result:
        print("reboot successful")
        exit(0)
    else:
        print("reboot fail")
        exit(1)


if __name__ == '__main__':
    main()
