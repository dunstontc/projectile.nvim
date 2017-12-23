" ==============================================================================
" FILE: projectile.vim
" AUTHOR: Clay Dunston <dunstontc@gmail.com>
" License: MIT license
" Last Modified: December 22nd, 2017
" ==============================================================================
""
" @section Settings, settings
"


if !exists('g:projectile#data_dir')
""
" @setting(g:projectile#data_dir)
" The location to store files containing saved projects & bookmarks.
  let g:projectile#data_dir = expand($XDG_CACHE_HOME != '' ?
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
" The command used to search for todos.
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
" @function(ProjectileInit)
" First, checks to see if {g:projectile#data_dir} exists.
" If it doesn't, it prompts to make it & the JSON files.
" If it does, it's checked for projects.json & bookmarks.json.
" If those aren't there, it'll make them.
function ProjectileInit() abort
  let l:dir_path = expand(g:projectile#data_dir)
  let l:bookmark = '[{"name":"MYVIMRC","path":"'.expand("$MYVIMRC").'","line":1,"col":1,"timestamp":"'.strftime("%a %d %b %Y %I:%M:%S %p %Z").'","description":""}]'

  if filereadable(l:dir_path.'/bookmarks.json') && filereadable(l:dir_path.'/projects.json')
    echohl String | echomsg "Looks like you're all set!" | echohl None
  else
    echohl Keyword
    let l:confirmed_1 = confirm('Set up projectile?', "&Yes\n&No", 2)
    if l:confirmed_1 == 2
      echohl String | echomsg "You're the boss." | echohl None
    else
      silent exe '!mkdir '.l:dir_path.'; touch '.l:dir_path.'/bookmarks.json '.l:dir_path.'/projects.json'
      silent execute writefile([l:bookmark], l:dir_path.'/bookmarks.json')
      echohl String | echomsg "You're all set!" | echohl None
    endif
  endif
endfunction

command -nargs=0 ProjectileInit call ProjectileInit()

