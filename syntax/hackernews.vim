" Vim syntax file


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


let b:current_syntax = "hackernews"
