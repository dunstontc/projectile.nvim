" ==============================================================================
" FILE: projectile.vim
" AUTHOR: Clay Dunston <dunstontc@gmail.com>
" License: MIT license
" Last Modified: December 7th, 2017
" ==============================================================================


let g:projectile#default_command = 'cd'

if !exists('g:projectile#data_dir')
  let g:projectile#data_dir = '~/.cache/projectile'
endif

if !exists('g:projectile#directory_command')
  let g:projectile#directory_command = 'Vimfiler -explorer '
endif

if !exists('g:projectile#todo_terms')
  let g:todo_plugin#todo_terms=['TODO', 'FIXME']
endif

" Say hello so people can see that we're here
let g:projectile#loaded = 1
