" ==============================================================================
" File:        todo.vim
" Author:      Clay Dunston <dunstontc@gmail.com>
" License:     MIT License
" Thanks:      Based on work by Leandro Freitas's todo.txt-vim (http://github.com/freitass/todo.txt-vim)
" ==============================================================================

if exists('b:current_syntax')
  finish
endif

syntax  match  todoItem       '^.*$'                      contains=todoDate,todoProject,todoContext,todoExtra,todoID,todoString,todoOverDue
syntax  match  todoComment    '^#\s.\+$'
syntax  match  todoDone       '^[xX]\s.\+$'
syntax  match  todoPriorityA  '^([aA])\s.\+$'             contains=todoDate,todoProject,todoContext,todoExtra,todoID,todoString,todoOverDue
syntax  match  todoPriorityB  '^([bB])\s.\+$'             contains=todoDate,todoProject,todoContext,todoExtra,todoID,todoString,todoOverDue
syntax  match  todoPriorityC  '^([cC])\s.\+$'             contains=todoDate,todoProject,todoContext,todoExtra,todoID,todoString,todoOverDue
syntax  match  todoPriorityD  '^([dD])\s.\+$'             contains=todoDate,todoProject,todoContext,todoExtra,todoID,todoString,todoOverDue
syntax  match  todoPriorityE  '^([eE])\s.\+$'             contains=todoDate,todoProject,todoContext,todoExtra,todoID,todoString,todoOverDue
syntax  match  todoPriorityF  '^([fF])\s.\+$'             contains=todoDate,todoProject,todoContext,todoExtra,todoID,todoString,todoOverDue
syntax  match  todoPriorityG  '^([gG])\s.\+$'             contains=todoDate,todoProject,todoContext,todoExtra,todoID,todoString,todoOverDue
syntax  match  todoPriorityH  '^([hH])\s.\+$'             contains=todoDate,todoProject,todoContext,todoExtra,todoID,todoString,todoOverDue
syntax  match  todoPriorityI  '^([iI])\s.\+$'             contains=todoDate,todoProject,todoContext,todoExtra,todoID,todoString,todoOverDue
syntax  match  todoPriorityJ  '^([jJ])\s.\+$'             contains=todoDate,todoProject,todoContext,todoExtra,todoID,todoString,todoOverDue
syntax  match  todoPriorityK  '^([kK])\s.\+$'             contains=todoDate,todoProject,todoContext,todoExtra,todoID,todoString,todoOverDue
syntax  match  todoPriorityL  '^([lL])\s.\+$'             contains=todoDate,todoProject,todoContext,todoExtra,todoID,todoString,todoOverDue
syntax  match  todoPriorityM  '^([mM])\s.\+$'             contains=todoDate,todoProject,todoContext,todoExtra,todoID,todoString,todoOverDue
syntax  match  todoPriorityN  '^([nN])\s.\+$'             contains=todoDate,todoProject,todoContext,todoExtra,todoID,todoString,todoOverDue
syntax  match  todoPriorityO  '^([oO])\s.\+$'             contains=todoDate,todoProject,todoContext,todoExtra,todoID,todoString,todoOverDue
syntax  match  todoPriorityP  '^([pP])\s.\+$'             contains=todoDate,todoProject,todoContext,todoExtra,todoID,todoString,todoOverDue
syntax  match  todoPriorityQ  '^([qQ])\s.\+$'             contains=todoDate,todoProject,todoContext,todoExtra,todoID,todoString,todoOverDue
syntax  match  todoPriorityR  '^([rR])\s.\+$'             contains=todoDate,todoProject,todoContext,todoExtra,todoID,todoString,todoOverDue
syntax  match  todoPriorityS  '^([sS])\s.\+$'             contains=todoDate,todoProject,todoContext,todoExtra,todoID,todoString,todoOverDue
syntax  match  todoPriorityT  '^([tT])\s.\+$'             contains=todoDate,todoProject,todoContext,todoExtra,todoID,todoString,todoOverDue
syntax  match  todoPriorityU  '^([uU])\s.\+$'             contains=todoDate,todoProject,todoContext,todoExtra,todoID,todoString,todoOverDue
syntax  match  todoPriorityV  '^([vV])\s.\+$'             contains=todoDate,todoProject,todoContext,todoExtra,todoID,todoString,todoOverDue
syntax  match  todoPriorityW  '^([wW])\s.\+$'             contains=todoDate,todoProject,todoContext,todoExtra,todoID,todoString,todoOverDue
syntax  match  todoPriorityX  '^([xX])\s.\+$'             contains=todoDate,todoProject,todoContext,todoExtra,todoID,todoString,todoOverDue
syntax  match  todoPriorityY  '^([yY])\s.\+$'             contains=todoDate,todoProject,todoContext,todoExtra,todoID,todoString,todoOverDue
syntax  match  todoPriorityZ  '^([zZ])\s.\+$'             contains=todoDate,todoProject,todoContext,todoExtra,todoID,todoString,todoOverDue

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
