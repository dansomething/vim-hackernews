" Vim syntax file


if exists("b:current_syntax")
  finish
endif


syn match Ignore /\s\[[0-9]\{3,}\]$/
syn match Comment /^\s*Comment.*$/
syn region Constant start="\[http" end="\]"
syn region Statement start="^\s+ " end="^\s "


let b:current_syntax = "hackernews"
