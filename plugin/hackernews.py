import HTMLParser
import json
import re
import textwrap
import urllib2
import vim


API_URL = "http://node-hnapi.herokuapp.com"


def hacker_news():
    vim.command("edit .hackernews")
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


def hacker_news_link():
    line = vim.current.line
    m = re.search(r"\[(http.*)\]", line)
    if m:
        vim.command("edit .hackernews")
        b = vim.current.buffer
        content = urllib2.urlopen("http://fuckyeahmarkdown.com/go/?read=1&u="+m.group(1)).read()
        #content = html.unescape(html)
        for i, line in enumerate(content.split('\n')):
            if not line:
                b.append("")
                continue
            line = textwrap.wrap(line, width=80)
            for j, wrap in enumerate(line):
                if i == 0 and j == 0:
                    b[0] = wrap
                else:
                    b.append(wrap)
        return

    start, end = line.rfind('['), line.rfind(']')
    if start < 0 or end < 0:
        print "HackerNews.vim Error: Could not parse [item id]"
        return
    id = line[start+1:end]

    item = json.loads(urllib2.urlopen(API_URL+"/item/"+id).read())

    vim.command("edit .hackernews")
    b = vim.current.buffer
    b[0] = item['title']
    b.append("Posted %s by %s" % (item['time_ago'], item['user']))
    b.append("%d Points / %d Comments" % (item['points'], item['comments_count']))
    b.append("[%s]" % item['url'])
    b.append("")
    b.append("")
    print_comments(item['comments'], b)


html = HTMLParser.HTMLParser()

def print_comments(comments, b):
    for comment in comments:
        level = comment['level']
        b.append("%sComment by %s %s:" % ("\t"*level, comment.get('user','???'), comment['time_ago']))
        for p in comment['content'].split("<p>"):
            p = html.unescape(p)
            # Convert <a href="http://url/">Text</a> tags
            # to markdown equivalent: (Text)[http://url/]
            s = p.find("a>")
            while s > 0:
                s += 2
                section = p[:s]
                m = re.search(r"<a.*href=[\"\']([^\"\']*)[\"\'].*>(.*)</a>", section)
                # Do not bother with anchor text if it is same as href url
                if m.group(1)[:20] == m.group(2)[:20]:
                    p = p.replace(m.group(0), "[%s]" % m.group(1))
                else:
                    p = p.replace(m.group(0), "(%s)[%s]" % (m.group(2), m.group(1)))
                s = p.find("a>")

            contents = textwrap.wrap(re.sub('<[^<]+?>', '', p),
                                     width=80,
                                     initial_indent=" "*4*level,
                                     subsequent_indent=" "*4*level)
            for line in contents:
                b.append(line)
        b.append("")
        print_comments(comment['comments'], b)
