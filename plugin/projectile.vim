" ==============================================================================
" FILE: projectile.vim
" AUTHOR: Clay Dunston <dunstontc@gmail.com>
" License: MIT license
" Last Modified: December 27th, 2017
" ==============================================================================
""
" @section Settings, settings
"


if !exists('g:projectile#data_dir')
""
" @setting(g:projectile#data_dir)
" The location to store files containing saved projects & bookmarks.
  let g:projectile#data_dir = expand($XDG_CACHE_HOME !=? '' ?
          \  $XDG_CACHE_HOME . '/projectile' : '~/.cache/projectile')
endif


if !exists('g:projectile#directory_command')
""
" @setting(g:projectile#directory_command)
" Command for opening projects.
" Will be passed the absolute path to a project's root directory.
  let g:projectile#directory_command = 'cd'
endif


if !exists('g:projectile#todo_terms')
""
" @setting(g:projectile#todo_terms)
" An array of terms to search for with the *:Denite todo* command.
  let g:projectile#todo_terms = ['BUG', 'FIXME', 'HACK', 'NOTE', 'OPTIMIZE', 'TODO', 'XXX']
endif


if !exists('g:projectile#enable_highlighting')
""
" @setting(g:projectile#enable_highlights)
" Controls the use of highlighting for Projectile's Denite sources.
  let g:projectile#enable_highlighting = 1
endif


if !exists('g:projectile#enable_highlights')
""
" @setting(g:projectile#enable_formatting)
" Controls the use of highlighting for Projectile's Denite sources.
  let g:projectile#enable_formatting = 1
endif


if !exists('g:projectile#enable_devicons')
""
" @setting(g:projectile#enable_devicons)
" Controls the use of icons in source results.
" Set to *0* to disable icons entirely.
" Set to *1* to use devicons. (requires nerdfonts)
" Set to *2* to use unicode icons. (Works with most fonts)
  let g:projectile#enable_devicons = 0
endif


if !exists('g:projectile#search_prog')
""
" @setting(g:projectile#search_prog)
"   The command used to search for todos.
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


""
" @setting(g:projectile#loaded)
" Used to check if Projectile is installed & loaded.
let g:projectile#loaded = 1


""
" @function(Projectile_Init)
" Checks for projects.json & bookmarks.json in {g:projectile#data_dir}.
" If those aren't there, or if the directory doesn't exist, it'll make them.
function Projectile_Init() abort
  let l:dir_path = expand(g:projectile#data_dir)
  let l:bookmark = '[{"name":"MYVIMRC","path":"'.expand("$MYVIMRC").'","line":1,"col":1,"timestamp":"123456","description":""}]'
  let l:project  = '[{"name":"MYVIMRC","root":"'.expand("$VIMRUNTIME").'","timestamp":"123456","vcs":false,"description":""}]'

  echo "   Set up projectile?."
  let l:confirmed_1 = confirm("-- This will overwrite any existing projectile.nvim projects and bookmarks --", "&Yes\n&No", 2)
  if l:confirmed_1 == 2
    echo "You're the boss."
  else
    if !isdirectory(l:dir_path)
      silent exe '!mkdir '.l:dir_path.'; touch '.l:dir_path.'/bookmarks.json '.l:dir_path.'/projects.json'
    else
      silent exe '!touch '.l:dir_path.'/bookmarks.json '.l:dir_path.'/projects.json'
    endif
    silent execute writefile([l:bookmark], l:dir_path.'/bookmarks.json')
    silent execute writefile([l:project], l:dir_path.'/projects.json')
    echohl Keyword | echo "You're all set!" | echohl None
  endif
endfunction


""
" @command(ProjectileInit)
" Calls @function(Projectile_Init),
" Creates {g:projectile#data_dir}/*.json
command -nargs=0 ProjectileInit call Projectile_Init()

