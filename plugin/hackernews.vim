if !has('python')
    echo "HackerNews.vim Error: Requires Vim compiled with +python"
    finish
endif


" Import Python code
let s:path = expand("<sfile>:p:h")
execute "pyfile " . s:path . "/hackernews.py"


command! HackerNews python hacker_news()

map <return> :python hacker_news_item()<cr>


au! BufRead,BufNewFile *.hackernews set filetype=hackernews
