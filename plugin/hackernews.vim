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

command! HackerNews edit .hackernews
