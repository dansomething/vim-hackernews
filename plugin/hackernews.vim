"  vim-hackernews
"  --------------
"  Browse Hacker News (news.ycombinator.com) inside Vim.
"
"  Author:  ryanss <ryanssdev@icloud.com>
"  Website: https://github.com/ryanss/vim-hackernews
"  License: MIT (see LICENSE file)
"  Version: 0.3-dev


" Filetype plugins need to be enabled
filetype plugin on

" Load ftplugin when opening .hackernews buffer
au! BufRead,BufNewFile *.hackernews set filetype=hackernews


" Set required defaults
if !exists("g:hackernews_arg")
    let g:hackernews_arg = 'news'
endif

if !exists("g:hackernews_marks")
    let g:hackernews_marks = {}
endif


function! HackerNews(...)
    if a:0 > 0
        let g:hackernews_arg = a:1
    else
        let g:hackernews_arg = ""
    endif
    execute "edit .hackernews"
    normal! gg
endfunction

command! -nargs=? HackerNews call HackerNews(<q-args>)
