" Vim syntax file


if exists("b:current_syntax")
  finish
endif


syn match Comment /^\s*Comment.*$/
syn match Constant /\[http.*\]/


let b:current_syntax = "hackernews"
