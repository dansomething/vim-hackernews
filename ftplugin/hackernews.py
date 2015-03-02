# -*- coding: utf-8 -*-

#  vim-hackernews
#  --------------
#  Browse Hacker News (news.ycombinator.com) inside Vim.
#
#  Author:  ryanss <ryanssdev@icloud.com>
#  Website: https://github.com/ryanss/vim-hackernews
#  License: MIT (see LICENSE file)
#  Version: 0.1.1


from __future__ import print_function
import binascii
import json
import re
import textwrap
import vim
import webbrowser
import sys
if sys.version_info >= (3, 0):
    from html.parser import HTMLParser
    from urllib.request import urlopen
    from urllib.error import HTTPError
    unicode = bytes
    unichr = chr
else:
    from HTMLParser import HTMLParser
    from urllib2 import urlopen, HTTPError


API_URL = "http://node-hnapi.herokuapp.com"
MARKDOWN_URL = "http://fuckyeahmarkdown.com/go/?read=1&u="


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
    cb = unichr(160)
    if isinstance(cb, unicode):
        cb = cb.encode('utf-8')
    if s == cb and not b[-1]:
        b[-1] = s
        return

    if not b[0]:
        b[0] = s
    else:
        b.append(s)


def hex(s):
    if sys.version_info >= (3, 0):
        return str(binascii.hexlify(bytes(vim.current.buffer[0], 'utf-8')))
    return binascii.hexlify(s)


def main():
    vim.command("edit .hackernews")
    vim.command("setlocal noswapfile")
    vim.command("setlocal buftype=nofile")

    bwrite("┌───┐")
    bwrite("│ Y │ Hacker News (news.ycombinator.com)")
    bwrite("└───┘")
    bwrite("")

    try:
        news1 = json.loads(urlopen(API_URL+"/news", timeout=5)
                           .read().decode('utf-8'))
        news2 = json.loads(urlopen(API_URL+"/news2", timeout=5)
                           .read().decode('utf-8'))
    except HTTPError:
        print("HackerNews.vim Error: %s" % str(sys.exc_info()[1][0]))
        return
    except:
        print("HackerNews.vim Error: HTTP Request Timeout")
        return

    for i, item in enumerate(news1+news2):
        if 'title' not in item:
            continue
        if 'domain' in item:
            line = "%s%d. %s (%s) [%s]%s"
            line %= (" " if i+1 < 10 else "", i+1, item['title'],
                     item['domain'], item['url'], unichr(160))
            bwrite(line)
        else:
            line = "%s%d. %s [%d]"
            line %= (" " if i+1 < 10 else "", i+1, item['title'], item['id'])
            bwrite(line)
        if item['type'] == "link":
            line = "%s%d points by %s %s | %d comments [%s]"
            line %= (" "*4, item['points'], item['user'], item['time_ago'],
                     item['comments_count'], str(item['id']))
            bwrite(line)
        elif item['type'] == "job":
            line = "%s%s [%d]"
            line %= (" "*4, item['time_ago'], item['id'])
            bwrite(line)
        bwrite("")


def link(external=False):
    line = vim.current.line

    # Search for Hacker News [item id]
    m = re.search(r"\[([0-9]{3,})\]$", line)
    if m:
        id = m.group(1)
        if external:
            browser = webbrowser.get()
            browser.open("https://news.ycombinator.com/item?id="+id)
            return
        try:
            item = json.loads(urlopen(API_URL+"/item/"+id, timeout=5)
                              .read().decode('utf-8'))
        except HTTPError:
            print("HackerNews.vim Error: %s" % str(sys.exc_info()[1][0]))
            return
        except:
            print("HackerNews.vim Error: HTTP Request Timeout")
            return

        save_pos()
        del vim.current.buffer[:]
        if 'title' in item:
            if 'domain' in item:
                bwrite("%s (%s)" % (item['title'], item['domain']))
            else:
                bwrite(item['title'])
            if item.get('comments_count', None):
                bwrite("%d points by %s %s | %d comments"
                       % (item['points'], item['user'], item['time_ago'],
                          item['comments_count']))
            else:
                bwrite(item['time_ago'])
            if 'url' in item:
                if item['url'].find("item?id=") == 0:
                    item['url'] = "http://news.ycombinator.com/" + item['url']
                bwrite("[%s]" % item['url'])
            if 'content' in item:
                bwrite("")
                print_content(item['content'])
            bwrite("")
            bwrite("")
        if item['type'] == "comment":
            item['level'] = 0
            print_comments([item,])
        else:
            print_comments(item['comments'])
        # Highlight OP username in comment titles
        vim.command("syn match Question /%s/ contained" % item['user'])
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
        if b[i].find("]", b[i].find("[http")) >= 0:
            url = b[i][b[i].find("[http")+1:b[i].find("]", b[i].find("[http"))]
        else:
            url = b[i][b[i].find("[http")+1:]
            i += 1
            while b[i].find("]") < 0:
                if i != start:
                    url += b[i]
                i += 1
            if i != start:
                url += b[i][:b[i].find("]")]
            url = url.replace(" ", "").replace("\n", "")

        if url.find("news.ycombinator.com/item?id=") > 0:
            id = url[url.find("item?id=")+8:]
            if external:
                browser = webbrowser.get()
                browser.open("https://news.ycombinator.com/item?id="+id)
                return
            try:
                item = json.loads(urlopen(API_URL+"/item/"+id,
                                  timeout=5).read().decode('utf-8'))
            except:
                print("HackerNews.vim Error: HTTP Request Timeout")
                return
            save_pos()
            del vim.current.buffer[:]
            if 'title' in item:
                if 'domain' in item:
                    bwrite("%s (%s)" % (item['title'], item['domain']))
                else:
                    bwrite(item['title'])
                if item.get('comments_count', None):
                    bwrite("%d points by %s %s | %d comments"
                           % (item['points'], item['user'], item['time_ago'],
                              item['comments_count']))
                else:
                    bwrite(item['time_ago'])
                if 'url' in item:
                    bwrite("[http://news.ycombinator.com/item?id=" + str(id) + "]")
                if 'content' in item:
                    bwrite("")
                    print_content(item['content'])
                bwrite("")
                bwrite("")
            if item['type'] == "comment":
                item['level'] = 0
                print_comments([item,])
            else:
                print_comments(item['comments'])
            # Highlight OP username in comment titles
            vim.command("syn match Question /%s/ contained" % item['user'])
            return

        if external:
            browser = webbrowser.get()
            browser.open(url)
            return
        try:
            content = urlopen(MARKDOWN_URL+url, timeout=8)
            content = content.read().decode('utf-8')
        except HTTPError:
            print("HackerNews.vim Error: %s" % str(sys.exc_info()[1][0]))
            return
        except:
            print("HackerNews.vim Error: HTTP Request Timeout")
            return
        content = re.sub(r"(http\S+?)([\<\>\s\n])", "[\g<1>]\g<2>", content)
        save_pos()
        del vim.current.buffer[:]
        for i, line in enumerate(content.split('\n')):
            if not line:
                bwrite("")
                continue
            line = textwrap.wrap(line, width=80)
            for j, wrap in enumerate(line):
                bwrite(wrap)
        return


def save_pos():
    marks = vim.eval("g:hackernews_marks")
    m = hex(vim.current.buffer[0])
    marks[m] = list(vim.current.window.cursor)
    vim.command("let g:hackernews_marks = %s" % str(marks))


def recall_pos():
    marks = vim.eval("g:hackernews_marks")
    m = hex(vim.current.buffer[0])
    if m in marks:
        mark = marks[m]
        vim.current.window.cursor = (int(mark[0]), int(mark[1]))


html = HTMLParser()


def print_content(content):
    for p in content.split("<p>"):
        if not p:
            continue
        p = html.unescape(p)
        p = p.replace("<i>", "_").replace("</i>", "_")

        # Convert <a href="http://url/">Text</a> tags
        # to markdown equivalent: (Text)[http://url/]
        s = p.find("a>")
        while s > 0:
            s += 2
            section = p[:s]
            m = re.search(r"<a.*href=[\"\']([^\"\']*)[\"\'].*>(.*)</a>",
                          section)
            if m:
                # Do not bother with anchor text if it is same as href url
                if m.group(1)[:20] == m.group(2)[:20]:
                    p = p.replace(m.group(0), "[%s]" % m.group(1))
                else:
                    p = p.replace(m.group(0),
                                  "(%s)[%s]" % (m.group(2), m.group(1)))
                s = p.find("a>")
            else:
                s = p.find("a>", s)

        contents = textwrap.wrap(p, width=80)
        for line in contents:
            if line.strip():
                bwrite(line)
        if contents and line.strip():
            bwrite("")


def print_comments(comments, level=0):
    for comment in comments:
        bwrite("%sComment by %s %s:"
               % ("\t"*level, comment.get('user', '???'), comment['time_ago']))
        for p in comment['content'].split("<p>"):
            if not p:
                continue
            p = html.unescape(p)
            p = p.replace("<i>", "_").replace("</i>", "_")

            # Extract code block before textwrap to conserve whitespace
            code = None
            if p.find("<code>") >= 0:
                m = re.search("<pre><code>([\S\s]*?)</code></pre>", p)
                code = m.group(1)
                p = p.replace(m.group(0), "!CODE!")

            # Convert <a href="http://url/">Text</a> tags
            # to markdown equivalent: (Text)[http://url/]
            s = p.find("a>")
            while s > 0:
                s += 2
                section = p[:s]
                m = re.search(r"<a.*href=[\"\']([^\"\']*)[\"\'].*>(.*)</a>",
                              section)
                if m:
                    # Do not bother with anchor text if it is same as href url
                    if m.group(1)[:20] == m.group(2)[:20]:
                        p = p.replace(m.group(0), "[%s]" % m.group(1))
                    else:
                        p = p.replace(m.group(0),
                                      "(%s)[%s]" % (m.group(2), m.group(1)))
                    s = p.find("a>")
                else:
                    s = p.find("a>", s)

            contents = textwrap.wrap(p, width=80,
                                     initial_indent=" "*4*level,
                                     subsequent_indent=" "*4*level)
            for line in contents:
                if line.find("!CODE!") >= 0:
                    bwrite(unichr(160))
                    for c in code.split("\n"):
                        if c.strip():
                            bwrite(" "*4*level + c)
                    bwrite(unichr(160))
                    line = " "*4*level + line.replace("!CODE!", "").strip()
                if line.strip():
                    bwrite(line)
            if contents and line.strip():
                bwrite("")
        bwrite("")
        print_comments(comment['comments'], level+1)
