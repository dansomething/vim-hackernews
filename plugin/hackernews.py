import HTMLParser
import json
import re
import textwrap
import urllib2
import vim


API_URL = "http://node-hnapi.herokuapp.com"


def hacker_news():
    vim.command("edit -HackerNews-")
    vim.command("setlocal noswapfile")
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


def hacker_news_item():
    line = vim.current.line
    start, end = line.rfind('['), line.rfind(']')
    if start < 0 or end < 0:
        print "HackerNews.vim Error: Could not parse [item id]"
        return
    id = line[start+1:end]

    item = json.loads(urllib2.urlopen(API_URL+"/item/"+id).read())

    vim.command("edit -HackerNews-")
    b = vim.current.buffer
    b[0] = item['title']
    b.append("Posted %s by %s" % (item['time_ago'], item['user']))
    b.append("%d Points / %d Comments" % (item['points'], item['comments_count']))
    b.append(item['url'])
    b.append("")
    b.append("")
    print_comments(item['comments'], b)


html = HTMLParser.HTMLParser()

def print_comments(comments, b):
    for comment in comments:
        level = comment['level']
        b.append("%sComment by %s %s:" % ("\t"*level, comment.get('user','???'), comment['time_ago']))
        for p in comment['content'].split("<p>"):
            contents = textwrap.wrap(html.unescape(re.sub('<[^<]+?>', '', p)),
                                     width=80,
                                     initial_indent=" "*4*level,
                                     subsequent_indent=" "*4*level)
            for line in contents:
                b.append(line)
        b.append("")
        print_comments(comment['comments'], b)
