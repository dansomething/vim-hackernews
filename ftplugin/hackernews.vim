"  vim-hackernews
"  --------------
"  Browse Hacker News (news.ycombinator.com) inside Vim.
"
"  Author:  ryanss <ryanssdev@icloud.com>
"  Website: https://github.com/ryanss/vim-hackernews
"  License: MIT (see LICENSE file)
"  Version: 0.1.1


if !exists("g:hackernews_marks")
    let g:hackernews_marks = {}
endif


noremap <buffer> o :python hacker_news_link()<cr>
noremap <buffer> O :python hacker_news_link(external=True)<cr>
noremap <buffer> u u:python recall_pos()<cr>
noremap <buffer> <C-r> <C-r>:python recall_pos()<cr>
