"  vim-hackernews
"  --------------
"  Browse Hacker News (news.ycombinator.com) inside Vim.
"
"  Author:  ryanss <ryanssdev@icloud.com>
"  Website: https://github.com/ryanss/vim-hackernews
"  License: MIT (see LICENSE file)
"  Version: 0.1.1


if !has('python')
    echo "HackerNews.vim Error: Requires Vim compiled with +python"
    finish
endif

if !exists("g:hackernews_marks")
    let g:hackernews_marks = {}
endif


" Import Python code
execute "python import sys"
execute "python sys.path.append(r'" . expand("<sfile>:p:h") . "')"

python << EOF
if 'hackernews' not in sys.modules:
    import hackernews
else:
    # Reload python module to avoid errors when updating plugin
    hackernews = reload(hackernews)
EOF


" Load front page
execute "python hackernews.main()"


noremap <buffer> o :python hackernews.link()<cr>
noremap <buffer> O :python hackernews.link(external=True)<cr>
noremap <buffer> gx :python hackernews.link(external=True)<cr>
noremap <buffer> u u:python hackernews.recall_pos()<cr>
noremap <buffer> <C-r> <C-r>:python hackernews.recall_pos()<cr>
