# -*- coding: utf-8 -*-

#  vim-hackernews
#  --------------
#  Browse Hacker News (news.ycombinator.com) inside Vim.
#
#  Author:  ryanss <ryanssdev@icloud.com>
#  Website: https://github.com/ryanss/vim-hackernews
#  License: MIT (see LICENSE file)
#  Version: 0.3-dev


from __future__ import print_function, division
import binascii
import json
import re
import sys
import textwrap
import vim
import webbrowser
from datetime import datetime
if sys.version_info >= (3, 0):
    from html.parser import HTMLParser
    from urllib.parse import quote_plus, urlparse
    from urllib.request import urlopen
    from urllib.error import HTTPError
    unicode = bytes
    unichr = chr
else:
    from HTMLParser import HTMLParser
    from urllib import quote_plus
    from urllib2 import urlopen, HTTPError
    from urlparse import urlparse


API_URL = "http://node-hnapi.herokuapp.com"
MARKDOWN_URL = "http://fuckyeahmarkdown.com/go/?read=1&u="
SEARCH = ("https://hn.algolia.com/api/v1/search" +
          "?tags=story&hitsPerPage=60&query=")

html = HTMLParser()


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


def time_ago(timestamp):
    d = datetime.now() - datetime.fromtimestamp(timestamp)
    years = d.days // 365
    if years > 1:
        return "%d years ago" % (years)
    elif years == 1:
        return "%d year ago" % (years)
    months = d.days // 30
    if months > 1:
        return "%d months ago" % (months)
    elif months == 1:
        return "%d month ago" % (months)
    if d.days > 1:
        return "%d days ago" % (d.days)
    elif d.days == 1:
        return "%d day ago" % (d.days)
    hours = d.seconds // 60 // 60
    if hours > 1:
        return "%d hours ago" % (hours)
    elif hours == 1:
        return "%d hour ago" % (hours)
    minutes = d.seconds // 60
    if minutes > 1:
        return "%d minutes ago" % (minutes)
    elif minutes == 1:
        return "%d minute ago" % (minutes)
    return "%d seconds ago" % (d.seconds)


def main():
    vim.command("edit .hackernews")
    vim.command("setlocal noswapfile")
    vim.command("setlocal buftype=nofile")

    if vim.eval("changenr()") == "1":
        vim.command("setlocal undolevels=-1")

    bwrite("┌───┐")
    bwrite("│ Y │ Hacker News (news.ycombinator.com)")
    bwrite("└───┘")
    bwrite("")

    try:
        arg = vim.eval("g:hackernews_arg")
        if arg in ['newest', 'ask', 'show', 'shownew', 'jobs',
                   'best', 'active', 'noobstories']:
            items = json.loads(urlopen(API_URL+"/"+arg, timeout=5)
                               .read().decode('utf-8'))
        elif arg.isdigit():
            link(item_id=arg)
            return
        elif arg[:4] == 'http':
            link(url=arg)
            return
        elif not arg:
            news1 = json.loads(urlopen(API_URL+"/news", timeout=5)
                               .read().decode('utf-8'))
            news2 = json.loads(urlopen(API_URL+"/news2", timeout=5)
                               .read().decode('utf-8'))
            items = news1 + news2
        else:
            items = json.loads(urlopen(SEARCH+quote_plus(arg), timeout=5)
                               .read().decode('utf-8'))['hits']
    except HTTPError:
        print("HackerNews.vim Error: %s" % str(sys.exc_info()[1].reason))
        return
    except:
        print("HackerNews.vim Error: HTTP Request Timeout")
        return

    for i, item in enumerate(items):
        # Test if item is a result from search API
        if 'objectID' in item:
            # Convert search API results into dict similar to regular API
            # results so we can use same code to output results
            item['id'] = int(item['objectID'])
            item['user'] = item['author']
            item['type'] = "link"
            item['time_ago'] = time_ago(item['created_at_i'])
            item['comments_count'] = int(item['num_comments'])
            if item.get('url', False):
                item['domain'] = urlparse(item['url']).netloc

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
        if item['type'] in ("link", "ask"):
            line = "%s%d points by %s %s | %d comments [%s]"
            line %= (" "*4, item['points'], item['user'], item['time_ago'],
                     item['comments_count'], str(item['id']))
            bwrite(line)
        elif item['type'] == "job":
            line = "%s%s [%d]"
            line %= (" "*4, item['time_ago'], item['id'])
            bwrite(line)
        bwrite("")
    vim.command("setlocal undolevels=100")


def link(item_id=None, url=None, external=False):
    line = vim.current.line

    if not (item_id or url):
        # Search for Hacker News [item id]
        m = re.search(r"\[([0-9]{3,})\]$", line)
        if m:
            item_id = m.group(1)

        else:
            # Search for [http] link
            b = vim.current.buffer
            y, x = vim.current.window.cursor
            y -= 1
            while b[y].find("[http") < 0 and y >= 0:
                # The line we were on had no part of a link in it
                if b[y-1].find("]") > 0 \
                        and b[y-1].find("]") > b[y-1].find("[http"):
                    return
                y -= 1
            start = y
            loc = max(b[y].find("[http", x, b[y].find("]", x)),
                      b[y].rfind("[http", 0, x))
            if loc >= 0:
                if b[y].find("]", loc) >= 0:
                    a = loc + 1
                    e = b[y].find("]", loc)
                    url = b[y][a:e]
                else:
                    url = b[y][loc+1:]
                    y += 1
                    while b[y].find("]") < 0:
                        if y != start:
                            url += b[y]
                        y += 1
                    if y != start:
                        url += b[y][:b[y].find("]")]
                    url = url.replace(" ", "").replace("\n", "")

    if url and url.find("news.ycombinator.com/item?id=") > 0:
        item_id = url[url.find("item?id=")+8:]

    if item_id:
        if external:
            browser = webbrowser.get()
            browser.open("https://news.ycombinator.com/item?id="+item_id)
            return
        try:
            item = json.loads(urlopen(API_URL+"/item/"+item_id,
                              timeout=5).read().decode('utf-8'))
        except:
            print("HackerNews.vim Error: HTTP Request Timeout")
            return
        save_pos()
        vim.command("set syntax=hackernews")
        del vim.current.buffer[:]
        if 'title' in item:
            if 'domain' in item:
                bwrite("%s (%s)" % (item['title'], item['domain']))
            else:
                bwrite(item['title'])
            if item.get('comments_count', None) is not None \
                    and item['type'] != "job":
                bwrite("%d points by %s %s | %d comments"
                       % (item['points'], item['user'], item['time_ago'],
                          item['comments_count']))
            else:
                bwrite(item['time_ago'])
            if 'url' in item and item['url'].find(item_id) < 0:
                bwrite("[%s]" % item['url'])
            else:
                bwrite("[http://news.ycombinator.com/item?id=%s]" % item_id)
            if 'content' in item:
                bwrite("")
                print_comments([dict(content=item['content'])])
            if 'poll' in item:
                bwrite("")
                max_score = max((c['points'] for c in item['poll']))
                for c in item['poll']:
                    bwrite("%s (%d points)"
                           % (html.unescape(c['item']), c['points']))
                    bar = int(80.0 * c['points'] / max_score)
                    bwrite("#"*bar)
                    bwrite("")
            bwrite("")
            bwrite("")
        if item['type'] == "comment":
            item['level'] = 0
            print_comments([item])
        else:
            print_comments(item['comments'])
        # Prevent syntax issues in long comment threads with code blocks
        vim.command("syntax sync fromstart")
        # Highlight OP username in comment titles
        if 'level' not in item:
            vim.command("syntax clear Question")
        vim.command("syntax match Question /%s/ contained" % item['user'])

    elif url:
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
        vim.command("set syntax=markdown")
        del vim.current.buffer[:]
        for i, line in enumerate(content.split('\n')):
            if not line:
                bwrite("")
                continue
            line = textwrap.wrap(line, width=80)
            for j, wrap in enumerate(line):
                bwrite(wrap)


def save_pos():
    marks = vim.eval("g:hackernews_marks")
    m = hex(vim.current.buffer[0])
    if not m:
        return
    marks[m] = list(vim.current.window.cursor)
    marks[m].append(vim.eval("&syntax"))
    vim.command("let g:hackernews_marks = %s" % str(marks))


def recall_pos(cmd):
    marks = vim.eval("g:hackernews_marks")
    m = hex(vim.current.buffer[0])
    if not m:
        vim.command(cmd)
    if m in marks:
        mark = marks[m]
        vim.current.window.cursor = (int(mark[0]), int(mark[1]))
        vim.command("set syntax=%s" % mark[2])


def print_comments(comments, level=0):
    for comment in comments:
        if 'level' in comment:
            # This is a comment (not content) so add comment header
            bwrite("%sComment by %s %s: [%s]"
                   % (" "*level*4, comment.get('user', '???'),
                      comment['time_ago'], comment['id']))
        if not comment.get('content', False):
            bwrite("")
            bwrite("")
            continue
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
        if 'comments' in comment:
            print_comments(comment['comments'], level+1)
