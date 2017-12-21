" ==============================================================================
" FILE: projectile.vim
" AUTHOR: Clay Dunston <dunstontc@gmail.com>
" License: MIT license
" Last Modified: December 20th, 2017
" ==============================================================================


" let g:projectile#default_command = 'open'

if !exists('g:projectile#data_dir')
  let g:projectile#data_dir = '~/.cache/projectile'
endif

if !exists('g:projectile#directory_command')
  let g:projectile#directory_command = 'Vimfiler -explorer '
endif

if !exists('g:projectile#todo_terms')
  let g:todo_plugin#todo_terms=['TODO', 'FIXME']
endif

if !exists('g:projectile#disable_devicons')
  let g:projectile#disable_devicons=0
endif

if !exists('g:projectile#search_prog')
  let g:projectile#search_prog = 'grep'
  if executable('ag')
    let g:projectile#search_prog = 'ag'
  elseif executable('pt')
    let g:projectile#search_prog = 'pt'
  elseif executable('rg')
    let g:projectile#search_prog = 'rg'
  elseif executable('ack')
    let g:projectile#search_prog = 'ack'
  endif
endif

" Say hello so people can see that we're here
let g:projectile#loaded = 1
