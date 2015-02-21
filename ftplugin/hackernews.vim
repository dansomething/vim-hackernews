"  vim-hackernews
"  --------------
"  Browse Hacker News (news.ycombinator.com) inside Vim.
"
"  Author:  ryanss <ryanssdev@icloud.com>
"  Website: https://github.com/ryanss/vim-hackernews
"  License: MIT (see LICENSE file)
"  Version: 0.1.1


if has('python')
    command! -nargs=1 Python python <args>
elseif has('python3')
    command! -nargs=1 Python python3 <args>
else
    echo "HackerNews.vim Error: Requires Vim compiled with +python or +python3"
    finish
endif

if !exists("g:hackernews_marks")
    let g:hackernews_marks = {}
endif


" Import Python code
execute "Python import sys"
execute "Python sys.path.append(r'" . expand("<sfile>:p:h") . "')"

Python << EOF
if 'hackernews' not in sys.modules:
    import hackernews
else:
    # Reload python module to avoid errors when updating plugin
    hackernews = reload(hackernews)
EOF


" Load front page
execute "Python hackernews.main()"


noremap <buffer> o :Python hackernews.link()<cr>
noremap <buffer> O :Python hackernews.link(external=True)<cr>
noremap <buffer> gx :Python hackernews.link(external=True)<cr>
noremap <buffer> u u:Python hackernews.recall_pos()<cr>
noremap <buffer> <C-r> <C-r>:Python hackernews.recall_pos()<cr>


" Helper motion to browse front page easier
function! s:NextItem(backwards)
    if match(getline('.'), '^\s\{4}.\+ago') >= 0
        " Move to next/previous comment line
        let pattern = '^\s\{4}[0-9]'
    else
        " Move to next/previous title line
        let pattern = '^\s*\d\+\.\s.'
    endif
    let dir = a:backwards? '?' : '/'
    execute 'silent normal! ' . dir . pattern . dir . 'e\r'
endfunction

noremap <buffer> J :call <SID>NextItem(0)<cr>
noremap <buffer> K :call <SID>NextItem(1)<cr>
