"  vim-hackernews
"  --------------
"  Browse Hacker News (news.ycombinator.com) inside Vim.
"
"  Author:  ryanss <ryanssdev@icloud.com>
"  Website: https://github.com/ryanss/vim-hackernews
"  License: MIT (see LICENSE file)
"  Version: 0.3-dev


if has('python')
    command! -nargs=1 Python python <args>
elseif has('python3')
    command! -nargs=1 Python python3 <args>
else
    echo "HackerNews.vim Error: Requires Vim compiled with +python or +python3"
    finish
endif


" Import Python code
execute "Python import sys"
execute "Python sys.path.append(r'" . expand("<sfile>:p:h") . "')"

Python << EOF
if 'hackernews' not in sys.modules:
    import hackernews
else:
    import imp
    # Reload python module to avoid errors when updating plugin
    hackernews = imp.reload(hackernews)
EOF


" Load front page
execute "Python hackernews.main()"


noremap <buffer> o :Python hackernews.link()<cr>
noremap <buffer> O :Python hackernews.link(external=True)<cr>
noremap <buffer> gx :Python hackernews.link(external=True)<cr>
noremap <buffer> u :Python hackernews.save_pos()<cr>
                   \u
                   \:Python hackernews.recall_pos("undo")<cr>
noremap <buffer> <C-R> :Python hackernews.save_pos()<cr>
                       \<C-R>
                       \:Python hackernews.recall_pos("redo")<cr>


" Helper motions to browse front page, comments and articles easier
function! s:Move(backwards)
    let dir = a:backwards? '?' : '/'
    if match(getline(1), "┌───┐") == 0
        " Front Page
        if match(getline('.'), '^\s\{4}.\+ago') >= 0
            " Move to next/previous comment line
            let pattern = '^\s\{4}[0-9]'
        else
            " Move to next/previous title line
            let pattern = '^\s*\d\+\.\s.'
        endif
        execute 'silent normal! ' . dir . pattern . dir . '\r'
    elseif match(getline(2), '^\d\+\s.\+ago') == 0
        " Comment Page
        let pattern = '^\s*Comment by'
        execute 'silent normal! ' . dir . pattern . dir . '\rzt'
        " Do not stop on folded lines
        if foldclosed(line('.')) != -1
            execute 'silent normal! ' . dir . pattern . dir . '\rzt'
        endif
    else
        " Article
        if a:backwards
            silent normal! {
        else
            silent normal! }
        endif
    endif
endfunction

noremap <buffer> J :call <SID>Move(0)<cr>
noremap <buffer> K :call <SID>Move(1)<cr>


" Fold comment threads
function! s:FoldComments()
    if match(getline(2), '^\d\+\s.\+ago') != 0
        " Do not continue if this is not a comments page
        return
    endif
    set nowrapscan
    try
        execute 'silent normal! ' . 'jj?^\s*Comment by.*:?\rj'
    catch
        " Nothing to fold
        return
    endtry
    let level = matchstr(getline('.'), '^\s\+')
    try
        execute 'silent normal! ' . 'zf/\n^\s\{0,' . len(level). '}Comment/\r'
    catch
        execute 'silent! normal! ' . 'zf/\n\%$/e\r'
    endtry
    set wrapscan
endfunction

noremap <buffer> F :call <SID>FoldComments()<cr>
