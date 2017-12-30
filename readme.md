# projectile.nvim #

[![License](https://img.shields.io/github/license/dunstontc/projectile.nvim.svg)](https://github.com/dunstontc/projectile.nvim/blob/master/LICENSE)
[![Code Climate](https://img.shields.io/codeclimate/issues/github/me-and/mdf.svg)](https://github.com/dunstontc/projectile.nvim/issues)

> Collection of utilities similar to those provided by [Projectile](https://github.com/bbatsov/projectile) utilizing [denite.nvim](https://github.com/Shougo/denite.nvim).

<div align="center">
    <img src="https://raw.githubusercontent.com/dunstontc/assets/master/gifs/yes.gif" alt="mission-control"/>
</div>


## Features ##

  - Projects
    - Keep a list of project locations with metadata
    - Check version control status of Projects
    - List todos in a project directory
  - Bookmarks
    - Keep a list of bookmarked locations
  - TODOs
    - Syntax highlighting and filetype detection for `todo.txt` files
    - List todos in the current project folder & jump to them
    - List todos from a global or project todo.txt file **(WIP)**
    - Append todos to the quickfix or location list **(WIP)**


## Usage ##

### Requirements ###
  - [Shougo/denite.nvim](https://github.com/Shougo/denite.nvim)
  - Neovim (or Vim8) with Python3 support

### Installation ###
  - Run `:ProjectileInit` to create a directory at `g:projectile#data_dir` containing `bookmarks.json` & `projects.json`
  - **NOTE:** Running this function more than once will reset your list of bookmarks & projects saved with projectile.

### Configuration ###
  - By default, data is saved in `$XDG_CACHE_HOME/projectile` or `~/.cache/projectile/`.  
```viml
let g:projectile#data_dir = $HOME.'.cache/.projectile'

let g:todo_plugin#todo_terms = ['TODO', 'FIXME', 'XXX']

" Defaults to 'cd'
let g:projectile#directory_command = 'VimFiler -explorer '

" Options: grep, ag, pt, rg, or ack. (Defaults to the first of these found.)
let g:projectile#search_prog = 'grep'

" Options:  0 - No icons,  1 - Use Devicons,  2 - Use Unicode icons (Defaults to 0)
let g:projectile#enable_devicons = 0
```


## Denite Sources ##
```viml
:Denite projectile
```
  - *add*
  - *remove*
  - *open (default)*
  - *directory_command*
    - Passes the project path to a command defined by `g:projectile#directory_command`.
  - Extends `Directory`, so it supports all `Directory` kind actions. *(cd, narrow, .., ...)* 

```viml
:Denite bookmark
```
  - *add*
  - *remove*
  - *open (default)*
  - Extends `File`, so it supports all `File` kind actions. *(jump, open, split, etc.)*

```viml
:Denite todo
```
  - *open (default)*
  - Like `Bookmark`, it supports all `File` kind actions. *(jump, open, split, etc.)*


## Credit & Thanks ##
  - [Shougo/denite.nvim](https://github.com/Shougo/denite.nvim)
  - [neoclide/denite-git](https://github.com/neoclide/denite-git)
  - [chemzqm/denite-extra](https://github.com/chemzqm/denite-extra)
  - [rafi/vim-denite-session](https://github.com/rafi/vim-denite-session)
  - [SpaceVim](https://github.com/SpaceVim/SpaceVim)
  - [freitass/todo.txt-vim](https://github.com/freitass/todo.txt-vim)


## Related Projects ##
  - [projectile](https://github.com/bbatsov/projectile)
  - [vim-rooter](https://github.com/airblade/vim-rooter)
  - [vim-projectionist](https://github.com/tpope/vim-projectionist)
  - [vim-bookmarks](https://github.com/MattesGroeger/vim-bookmarks)
  - [TaskList.vim](https://github.com/vim-scripts/TaskList.vim)
  - [searchtasks.vim](https://github.com/gilsondev/searchtasks.vim)
  - [todolist.vim](vim-scripts/todolist.vim)
  - [vim-todo](https://github.com/codegram/vim-todo)
  - [gather-todo.txt-vim](https://github.com/lgalke/gather-todo.txt-vim)

