"  vim-hackernews
"  --------------
"  Browse Hacker News (news.ycombinator.com) inside Vim.
"
"  Author:  ryanss <ryanssdev@icloud.com>
"  Website: https://github.com/ryanss/vim-hackernews
"  License: MIT (see LICENSE file)
"  Version: 0.1.1


" Filetype plugins need to be enabled
filetype plugin on

" Load ftplugin when opening .hackernews buffer
au! BufRead,BufNewFile *.hackernews set filetype=hackernews

function HackerNews(...)
    if a:0 > 0
        let available_lists = ['news', 'newest', 'ask', 'show', 'shownew',
                              \'jobs', 'best', 'active', 'noobstories']
        if index(available_lists, a:1) >= 0
            let g:hackernews_stories = a:1
        else
            let g:hackernews_stories = 'news'
        end
    else
        let g:hackernews_stories = 'news'
    end
    edit .hackernews
    normal! gg
endfunction

command! -nargs=? HackerNews call HackerNews(<q-args>)
