#!/usr/bin/env python3
from urllib.request import urlopen
import re


def UrlTitle(data):
        url = re.search("http[s]?://[^ ]*", data.decode('utf-8'))
        if not url:
            return -1
        #print("Found url", url.group(0))
        rq = urlopen(url.group(0), timeout=4)
        title = re.findall("<title>(.*)</title>", rq.read().decode('utf-8'))
        if title == []:
                return -2
        title = re.sub("[\n\r\t]", "", title[0])
        print("Title is " + title)
        return title

if __name__ == "__main__":
    UrlTitle(b":polprog!~ath0@www.polprog.net PRIVMSG #___# :test url http://example.org test123\r\n")
    print(UrlTitle("https://cnn.com/".encode('utf-8')))
    
