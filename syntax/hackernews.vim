"  vim-hackernews
"  --------------
"  Browse Hacker News (news.ycombinator.com) inside Vim.
"
"  Author:  ryanss <ryanssdev@icloud.com>
"  Website: https://github.com/ryanss/vim-hackernews
"  License: MIT (see LICENSE file)
"  Version: 0.3-dev


if exists("b:current_syntax")
  finish
endif


" Hide hacker news item id or url at end of front page lines
syn match Ignore /\s\[[0-9]\{3,}\]$/
syn match Ignore /\s\[http.\+\] $/

" Make sure `Ignore` highlight group is hidden
" Some colorschemes do not hide the `Ignore` group (ex. Solarized)
" An exception will be raised here if ctermfg=NONE which is sometimes set
" when using a transparent terminal so we wrap these commands in try/catch
try
    if has('gui_running')
        highlight Ignore guifg=bg
    else
        highlight Ignore ctermfg=bg
    endif
catch
endtry

" Remove emphesis from all components of main page item except title
syn match Comment /^\s*[0-9]\{1,2}\.\s/
syn match Comment /\s([^\[]\S\+\.\S\+)/
syn match Comment /^\s\{4}[0-9an]\+\s.\+\sago\s\[/ contains=Ignore
syn match Comment /^\s\{4}[0-9an]\+\spoints.\+\s\s|.*comments/
syn match Comment /^.*ago\s|.*comments/ contains=Question
syn match Comment /^[0-9an]\+\s.\+\sago$/

" Comment titles
syn match Comment /^\s*Comment\sby.\+ago:/ contains=Question

" Highlight links
syn region Constant start="\[http" end="\]"

" Italics <i> tags
syn match Italic /\v<_\_.{-}(_>|^$)/ contains=Statement
highlight Italic gui=italic

" Highlight code blocks
syn region Statement start="^ " end="^ "

" Highlight Hacker News header orange
syn match Title /^┌.*$/
syn match Title /^│.*$/
syn match Title /^└.*$/
highlight Title ctermfg=208 guifg=#ff6600


let b:current_syntax = "hackernews"
