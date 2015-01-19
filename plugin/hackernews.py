import HTMLParser
import json
import re
import textwrap
import urllib2
import vim


API_URL = "http://node-hnapi.herokuapp.com"


def bwrite(s):
    s = s.encode('utf-8')
    b = vim.current.buffer
    if not s.strip() and not b[-1].strip() and not b[-2].strip():
        # Never write more than two blank lines in a row
        return
    elif not b[0]:
        b[0] = s
    else:
        b.append(s)


def hacker_news():
    vim.command("edit .hackernews")
    vim.command("setlocal noswapfile")
    vim.command("setlocal buftype=nofile")

    bwrite("Hacker News")
    bwrite("===========")
    bwrite("")

    news1 = json.loads(urllib2.urlopen(API_URL+"/news").read())
    news2 = json.loads(urllib2.urlopen(API_URL+"/news2").read())
    for i, item in enumerate(news1+news2):
        if 'title' not in item:
            continue
        line = "%d. %s (%d comments) [%d]"
        line %= (i+1, item['title'], item['comments_count'], item['id'])
        bwrite(line)
        bwrite("")


def hacker_news_link():
    line = vim.current.line

    # Search for Hacker News [item id]
    m = re.search(r"^[0-9]{1,2}.*\[([0-9]+)\]", line)
    if m:
        id = m.group(1)
        item = json.loads(urllib2.urlopen(API_URL+"/item/"+id).read())
        vim.command("edit .hackernews")
        bwrite(item['title'])
        bwrite("Posted %s by %s" % (item['time_ago'], item['user']))
        bwrite("%d Points / %d Comments" % (item['points'], item['comments_count']))
        for i, wrap in enumerate(textwrap.wrap("[%s]" % item['url'], width=80)):
            bwrite(wrap)
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
                    for c in code.split("\n"):
                        bwrite(" "*4*level + c)
                    line = " "*4*level + line.replace("!CODE!", "").strip()
                if line.strip():
                    bwrite(line)
            if contents and line.strip():
                bwrite("")
        bwrite("")
        print_comments(comment['comments'])
