"  vim-hackernews
"  --------------
"  Browse Hacker News (news.ycombinator.com) inside Vim.
"
"  Author:  ryanss <ryanssdev@icloud.com>
"  Website: https://github.com/ryanss/vim-hackernews
"  License: MIT (see LICENSE file)
"  Version: 0.1.1


if exists("b:current_syntax")
  finish
endif


" Hide hacker news item id at end of main page lines
syn match Ignore /\s\[[0-9]\{3,}\]$/

" Remove emphesis from all components of main page item except title
syn match Comment /^\s*[0-9]\{1,2}\.\s/
syn match Comment /\s(\S\+\.\S\+)/
syn match Comment /^\s\{4}.*ago/
syn match Comment /^.*ago\s|.*comments/

" Comment titles
syn match Comment /^\s*Comment.*$/

" Highlight links
syn region Constant start="\[http" end="\]"

" Highlight code blocks
syn region Statement start="^\s+ " end="^\s "

" Highlight Hacker News header orange
syn match Title /^┌.*$/
syn match Title /^│.*$/
syn match Title /^└.*$/
highlight Title ctermfg=208 guifg=#ff6600


let b:current_syntax = "hackernews"
