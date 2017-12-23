" ==============================================================================
" FILE: projectile.vim
" AUTHOR: Clay Dunston <dunstontc@gmail.com>
" License: MIT license
" Last Modified: December 22nd, 2017
" ==============================================================================

""
" @setting(g:projectile#data_dir)
" The location to store files containing saved projects & bookmarks.
if !exists('g:projectile#data_dir')
  let g:projectile#data_dir = expand($XDG_CACHE_HOME != '' ?
         \  $XDG_CACHE_HOME . '/projectile' : '~/.cache/projectile')
endif


""
" @setting(g:projectile#directory_command)
" Command for opening projects.
" Will be passed the absolute path to a project's root directory.
if !exists('g:projectile#directory_command')
  let g:projectile#directory_command = 'cd'
endif


""
" @setting(g:projectile#todo_terms)
" An array of terms to search for with the *:Denite todo* command.
if !exists('g:projectile#todo_terms')
  let g:projectile#todo_terms = ['BUG', 'FIXME', 'HACK', 'NOTE', 'OPTIMIZE', 'TODO', 'XXX']
endif


""
" @setting(g:projectile#enable_devicons)
" Controls the use of icons in source results.
" Set to *0* to disable icons entirely.
" Set to *1* to use devicons. (requires nerdfonts)
" Set to *2* to use unicode icons. (Works with most fonts)
if !exists('g:projectile#enable_devicons')
  let g:projectile#enable_devicons = 0
endif


""
" @setting(g:projectile#search_prog)
" The command used to search for todos.
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

""
" @setting(g:projectile#loaded)
" Used to check if Projectile is installed & loaded.
" TODO: Add load guard
let g:projectile#loaded = 1


" call denite#custom#var('projectile', 'path', '~/.cache/projectile')

""
" @function(ProjectileInit)
" First, checks to see if {g:projectile#data_dir} exists.
" If it doesn't, it prompts to make it & the JSON files.
" If it does, it's checked for projects.json & bookmarks.json.
" If those aren't there, it prompts to write them.
" If they are, you probobly don't need to be reading this.
function ProjectileInit() abort
  " let l:dirpath = g:projectile#data_dir
  let l:data = '[{"name":"MYVIMRC","path":"'.expand("$MYVIMRC").'","line":1,"col":1,"timestamp":"'.strftime("%a %d %b %Y %I:%M:%S %p %Z").'","description":""}]'
  let l:dirpath    = expand($HOME != '' ?
             \  $HOME . '/test/new' : '~/test/new')
  if filereadable(l:dirpath.'/bookmarks.json') && filereadable(l:dirpath.'/projects.json')
    echohl String | echomsg "Looks like you're all set!" | echohl None
  else
      echohl Keyword
    let l:confirmed_1 = confirm('Set up projectile?', "&Yes\n&No", 2)
    if l:confirmed_1 == 2
      echohl String | echomsg "You're the boss." | echohl None
    else
      " try
        silent exe "!mkdir ~/test/projectile; touch ~/test/projectile/bookmarks.json ~/test/projectile/projects.json"
        " execute mkdir('projectile', '~/test/projectile')
      " catch
        " execute('write ~/test/new/bookmarks.json')
        " execute('write ~/test/new/projects.json')
        " execute writefile(["teest"], '~/test/projectile/projects.json')
        " execute writefile(["teest"], '~/test/projectile/bookmarks.json')
        execute writefile([l:data], $HOME.'/test/projectile/bookmarks.json')
        " E739: Cannot create directory projectile: file already exists
      " catch /E482/
        echohl String | echomsg "You're all set!" | echohl None
      " endtry
    endif
  endif
endfunction

command -nargs=0 ProjectileInit call ProjectileInit()

