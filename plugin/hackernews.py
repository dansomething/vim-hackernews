import json
import urllib2
import vim


API_URL = "http://node-hnapi.herokuapp.com"


def hacker_news():
    vim.command("edit -HackerNews-")
    vim.command("setlocal noswapfile")
    vim.command("setlocal nobuflisted")
    vim.command("setlocal buftype=nofile")

    b = vim.current.buffer
    b[0] = "Hacker News"
    b.append("===========")
    b.append("")

    news1 = json.loads(urllib2.urlopen(API_URL+"/news").read())
    news2 = json.loads(urllib2.urlopen(API_URL+"/news2").read())
    for i, item in enumerate(news1+news2):
        line = "%d. %s (%d comments) [%d]"
        line %= (i+1, item['title'], item['comments_count'], item['id'])
        b.append(line)
        b.append("")
