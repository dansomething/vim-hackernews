" Vim syntax file


if exists("b:current_syntax")
  finish
endif


syn match Comment /^\s*Comment.*$/
syn region Constant start="\[http" end="\]"


let b:current_syntax = "hackernews"
