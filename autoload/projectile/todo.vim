" ==============================================================================
"  File: todo.vim
"  Author: Clay Dunston <dunstontc@gmail.com>
"  License: MIT license
"  Last Modified: December 7th, 2017
" ==============================================================================

" function! todo#SearchCWD() abort
"   " if executable('ag')
"     execute 'read !' . 'ag -rg --nocolor --silent --nogroup --vimgrep "(TODO:|FIXME:|XXX:).*$" '. shellescape(expand('%:p:h'))
"   " else
"     " execute 'read ! ' . 'grep -Ern ' . "(TODO:|FIXME:|XXX:).*$" . ' ' . expand('%:p:h')
"   " endif
" endfunction

" function! todo_plugin#GrepSearch(engine) abort
"   " if !s:sys.isWindows
"     if executable('rg')
"       " call denite#custom#var('file_rec', 'command',
"       "       \ ['rg', '--hidden', '--files', '--glob', '!.git', '--glob', '']
"       "       \ + zvim#util#Generate_ignore(g:spacevim_wildignore, 'rg')
"       "       \ )
"     elseif executable('ag')
"       " call denite#custom#var('file_rec', 'command',
"       "       \ ['ag' , '--nocolor', '--nogroup', '-g', '']
"       "       \ + zvim#util#Generate_ignore(g:spacevim_wildignore, 'ag')
"       "       \ )
"       execute '!' . 'ag -r --nocolor --silent "(TODO:|FIXME:|XXX:).*$" '. expand('%:p:h')
"     endif
"   " else
"   "   if executable('pt')
"   "     " call denite#custom#var('file_rec', 'command',
"   "           " \ ['pt', '--follow', '--nocolor', '--nogroup', '-g:', ''])
"   "   endif
"   " endif
"   execute "!" . a:engine . " " . bufname("%")
"   " grep -Ern "(TODO:|FIXME:|XXX:).*$" .
"   " ag -r --nocolor --silent "(TODO:|FIXME:|XXX:).*$" .
" endfunction

