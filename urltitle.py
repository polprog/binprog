#!/usr/bin/env python3
from urllib.request import urlopen
import re

YTapiURL='http://gdata.youtube.com/feeds/api/videos/%s?alt=json&v=2'


def UrlTitle(data):
        url = re.search("http[s]?://[^ ]*", data)
        if not url:
            return "I007 Usage: !t <http[s] url>"
        rq = urlopen(url.group(0), timeout=4)
        title = re.findall("<title>(.*)</title>", rq.read().decode('utf-8'))
        if title == []:
                return -2
        title = re.sub("[\n\r\t]", "", title[0])
        print("Title is " + title)
        return str(title)



if __name__ == "__main__":
    print(UrlTitle(":polprog!~ath0@www.polprog.net PRIVMSG #___# :test url http://example.org test123\r\n"))
    print(UrlTitle("https://cnn.com/"))
    print(UrlTitle("https://www.youtube.com/watch?v=dQw4w9WgXcQ"))
        
