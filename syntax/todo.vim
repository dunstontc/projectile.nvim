" ==============================================================================
" Vim syntax file
" Language:      todo.txt
" File:          todo.vim
" Maintainer:    Clay Dunston <dunstontc@gmail.com>
" License:       MIT License
" Last Modified: 2017-12-25
" Remark:        Based on work by Leandro Freitas's todo.txt-vim (http://github.com/freitass/todo.txt-vim)
" ==============================================================================

if version < 600
  syntax clear
elseif exists("b:current_syntax")
  finish
endif

syntax  match  todoItem       '^.*$'                      contains=@todoData
syntax  match  todoComment    '^#\s.\+$'
syntax  match  todoDone       '^[xX]\s.\+$'

syntax  cluster todoPriority  contains=todoPriorityA,todoPriorityB,todoPriorityC,todoPriorityD,todoPriorityE,todoPriorityF,todoPriorityG,todoPriorityH,todoPriorityI,todoPriorityJ,todoPriorityK,todoPriorityL,todoPriorityM,todoPriorityN,todoPriorityO,todoPriorityP,todoPriorityQ,todoPriorityR,todoPriorityS,todoPriorityT,todoPriorityU,todoPriorityV,todoPriorityW,todoPriorityX,todoPriorityY,todoPriorityZ
syntax  cluster todoData      contains=todoDate,todoProject,todoContext,todoExtra,todoID,todoString,todoOverDue

syntax  match  todoPriorityA  '^([aA])\s.\+$'             contains=@todoData
syntax  match  todoPriorityB  '^([bB])\s.\+$'             contains=@todoData
syntax  match  todoPriorityC  '^([cC])\s.\+$'             contains=@todoData
syntax  match  todoPriorityD  '^([dD])\s.\+$'             contains=@todoData
syntax  match  todoPriorityE  '^([eE])\s.\+$'             contains=@todoData
syntax  match  todoPriorityF  '^([fF])\s.\+$'             contains=@todoData
syntax  match  todoPriorityG  '^([gG])\s.\+$'             contains=@todoData
syntax  match  todoPriorityH  '^([hH])\s.\+$'             contains=@todoData
syntax  match  todoPriorityI  '^([iI])\s.\+$'             contains=@todoData
syntax  match  todoPriorityJ  '^([jJ])\s.\+$'             contains=@todoData
syntax  match  todoPriorityK  '^([kK])\s.\+$'             contains=@todoData
syntax  match  todoPriorityL  '^([lL])\s.\+$'             contains=@todoData
syntax  match  todoPriorityM  '^([mM])\s.\+$'             contains=@todoData
syntax  match  todoPriorityN  '^([nN])\s.\+$'             contains=@todoData
syntax  match  todoPriorityO  '^([oO])\s.\+$'             contains=@todoData
syntax  match  todoPriorityP  '^([pP])\s.\+$'             contains=@todoData
syntax  match  todoPriorityQ  '^([qQ])\s.\+$'             contains=@todoData
syntax  match  todoPriorityR  '^([rR])\s.\+$'             contains=@todoData
syntax  match  todoPriorityS  '^([sS])\s.\+$'             contains=@todoData
syntax  match  todoPriorityT  '^([tT])\s.\+$'             contains=@todoData
syntax  match  todoPriorityU  '^([uU])\s.\+$'             contains=@todoData
syntax  match  todoPriorityV  '^([vV])\s.\+$'             contains=@todoData
syntax  match  todoPriorityW  '^([wW])\s.\+$'             contains=@todoData
syntax  match  todoPriorityX  '^([xX])\s.\+$'             contains=@todoData
syntax  match  todoPriorityY  '^([yY])\s.\+$'             contains=@todoData
syntax  match  todoPriorityZ  '^([zZ])\s.\+$'             contains=@todoData

syntax  match  todoDate       '\d\d\d\d\-\d\{2\}-\d\{2\}'       contained
syntax  match  todoProject    '\(^\|\W\)+[^[:blank:]]\+'        contained
syntax  match  todoContext    '\(^\|\W\)@[^[:blank:]]\+'        contained
syntax  match  todoExtra      '\(due\|t\|rec\|link\)\:\S*'      contained
syntax  match  todoID         'id\:\d\+s*'                      contained
syntax  match  todoString     '`\(.*\)`'                        contained

highlight  default  link  todoItem       Normal
highlight  default  link  todoDone       Comment
highlight  default  link  todoPriorityA  Constant
highlight  default  link  todoPriorityB  Statement
highlight  default  link  todoPriorityC  Identifier
highlight  default  link  todoDate       PreProc
highlight  default  link  todoOverDue    Error
highlight  default  link  todoProject    Special
highlight  default  link  todoContext    Special
highlight  default  link  todoExtra      Special
highlight  default  link  todoID         Number
highlight  default  link  todoString     String

let b:current_syntax = "todo"
