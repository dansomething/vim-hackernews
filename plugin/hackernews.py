# -*- coding: utf-8 -*-

import HTMLParser
import json
import re
import textwrap
import urllib2
import vim


API_URL = "http://node-hnapi.herokuapp.com"


def bwrite(s):
    b = vim.current.buffer
    # Never write more than two blank lines in a row
    if not s.strip() and not b[-1].strip() and not b[-2].strip():
        return

    # Vim buffer.append() cannot accept unicode type,
    # must first encode to UTF-8 string
    if isinstance(s, unicode):
        s = s.encode('utf-8', errors='replace')

    # Code block markers for syntax highlighting
    if s and s[-1] == unichr(160).encode('utf-8'):
        b[-1] = s
        return

    if not b[0]:
        b[0] = s
    else:
        b.append(s)


def hacker_news():
    vim.command("edit .hackernews")
    vim.command("setlocal noswapfile")
    vim.command("setlocal buftype=nofile")

    bwrite("┌───┐")
    bwrite("│ Y │ Hacker News")
    bwrite("└───┘")
    bwrite("")

    news1 = json.loads(urllib2.urlopen(API_URL+"/news").read())
    news2 = json.loads(urllib2.urlopen(API_URL+"/news2").read())
    for i, item in enumerate(news1+news2):
        if 'title' not in item:
            continue
        if item['type'] == "link" and item['url'][:4] == "http":
            line = "%s%d. %s (%s) [%d]"
            line %= (" " if i+1 < 10 else "", i+1, item['title'],
                     item['domain'], item['id'])
            bwrite(line)
            line = "%s%d points by %s %s | %d comments [%d]"
            line %= (" "*4, item['points'], item['user'], item['time_ago'],
                     item['comments_count'], item['id'])
            bwrite(line)
        elif item['type'] == "link":
            line = "%s%d. %s [%d]"
            line %= (" " if i+1 < 10 else "", i+1, item['title'], item['id'])
            bwrite(line)
            line = "%s%d points by %s %s | %d comments [%s]"
            line %= (" "*4, item['points'], item['user'], item['time_ago'],
                     item['comments_count'], item['id'])
            bwrite(line)
        elif item['type'] == "job":
            line = "%s%d. %s [%d]"
            line %= (" " if i+1 < 10 else "", i+1, item['title'], item['id'])
            bwrite(line)
            line = "%s%s [%d]"
            line %= (" "*4, item['time_ago'], item['id'])
            bwrite(line)
        bwrite("")


def hacker_news_link():
    line = vim.current.line

    # Search for Hacker News [item id]
    m = re.search(r"\[([0-9]+)\]$", line)
    if m:
        id = m.group(1)
        item = json.loads(urllib2.urlopen(API_URL+"/item/"+id).read())
        vim.command("edit .hackernews")
        bwrite(item['title'])
        bwrite("Posted %s by %s" % (item['time_ago'], item['user']))
        bwrite("%d Points / %d Comments" % (item['points'], item['comments_count']))
        if item['url'].find("item?id=") == 0:
            item['url'] = "http://news.ycombinator.com/" + item['url']
        bwrite("[%s]" % item['url'])
        bwrite("")
        bwrite("")
        print_comments(item['comments'])
        return

    # Search for [http] link
    b = vim.current.buffer
    i = vim.current.range.start
    while b[i].find("[http") < 0 and i >= 0:
        # The line we were on had no part of a link in it
        if b[i-1].find("]") > 0 and b[i-1].find("]") > b[i-1].find("[http"):
            return
        i -= 1
    start = i
    if b[i].find("[http") >= 0:
        if b[i].find("]") >= 0:
            url = b[i][b[i].find("[http")+1:b[i].find("]")]
        else:
            url = b[i][b[i].find("[http")+1:]
            while b[i].find("]") < 0:
                if i != start:
                    url += b[i]
                i += 1
            if i != start:
                url += b[i][:b[i].find("]")]
            url = url.replace(" ", "").replace("\n", "")
        vim.command("edit .hackernews")

        if url.find("http://news.ycombinator.com/item?id=") == 0:
            id = url[url.find("item?id=")+8:]
            item = json.loads(urllib2.urlopen(API_URL+"/item/"+id).read())
            bwrite(item['title'])
            bwrite("Posted %s by %s" % (item['time_ago'], item['user']))
            bwrite("%d Points / %d Comments" % (item['points'], item['comments_count']))
            bwrite("[http://news.ycombinator.com/item?id=" + str(id) + "]")
            bwrite("")
            bwrite("")
            print_comments(item['comments'])
            return

        content = urllib2.urlopen("http://fuckyeahmarkdown.com/go/?read=1&u="+url).read()
        for i, line in enumerate(content.split('\n')):
            if not line:
                bwrite("")
                continue
            line = textwrap.wrap(line, width=80)
            for j, wrap in enumerate(line):
                bwrite(wrap)
        return

    print "HackerNews.vim Error: Could not parse [item id]"


html = HTMLParser.HTMLParser()

def print_comments(comments):
    for comment in comments:
        level = comment['level']
        bwrite("%sComment by %s %s:" % ("\t"*level, comment.get('user','???'), comment['time_ago']))
        for p in comment['content'].split("<p>"):
            if not p:
                continue
            p = html.unescape(p)

            # Extract code block before textwrap to conserve whitespace
            code = None
            if p.find("<code>") >= 0:
                m = re.search("<pre><code>([\S\s]*?)</code></pre>\n", p)
                code = m.group(1)
                p = p.replace(m.group(0), "!CODE!")

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
                if line.find("!CODE!") >= 0:
                    bwrite(" "*4*level + unichr(160))
                    for c in code.split("\n"):
                        bwrite(" "*4*level + c)
                    bwrite(" "*4*level + unichr(160))
                    line = " "*4*level + line.replace("!CODE!", "").strip()
                if line.strip():
                    bwrite(line)
            if contents and line.strip():
                bwrite("")
        bwrite("")
        print_comments(comment['comments'])
