" ==============================================================================
" FILE: projectile.vim
" AUTHOR: Clay Dunston <dunstontc@gmail.com>
" License: MIT license
" Last Modified: December 20th, 2017
" ==============================================================================



if !exists('g:projectile#data_dir')
  let g:projectile#data_dir = '~/.cache/projectile'
endif

if !exists('g:projectile#directory_command')
  let g:projectile#directory_command = 'cd'
endif

if !exists('g:projectile#todo_terms')
  let g:projectile#todo_terms=['BUG', 'FIXME', 'HACK', 'NOTE', 'OPTIMIZE', 'TODO', 'XXX']
endif

if !exists('g:projectile#enable_devicons')
  let g:projectile#enable_devicons = 2
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



function ProjectileInit() abort
  " let l:dirpath = g:projectile#data_dir
    " execute('w ~/test/new')
  if filereadable('~/text/bookmarks.json')
    echo 'The file is there!'
  else
    echo 'No file :('
  endif
endfunction

command -nargs=0 ProjectileInit call <sid>ProjectileInit()

" noremap <silent> <Plug>(projectile-init)
  " \ :ProjectileInit

" noremap <silent> <Plug>(projectile-init)
"   \ :<C-U>call projectile#Init()<CR>

" nnoremap <leader>z <Plug>(projectile-init)
