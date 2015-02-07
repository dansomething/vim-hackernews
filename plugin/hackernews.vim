if !has('python')
    echo "HackerNews.vim Error: Requires Vim compiled with +python"
    finish
endif

" Import Python code
execute "python import sys"
execute "python sys.path.append('" . expand("<sfile>:p:h") . "')"
execute "python from hackernews import hacker_news, hacker_news_link"

command! HackerNews python hacker_news()

au! BufRead,BufNewFile *.hackernews set filetype=hackernews
