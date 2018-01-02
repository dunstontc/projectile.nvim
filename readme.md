# projectile.nvim #

[![License](https://img.shields.io/github/license/dunstontc/projectile.nvim.svg)](https://github.com/dunstontc/projectile.nvim/blob/master/LICENSE)
[![Code Climate](https://img.shields.io/codeclimate/issues/github/me-and/mdf.svg)](https://github.com/dunstontc/projectile.nvim/issues)

<div align="center">
    <img src="https://raw.githubusercontent.com/dunstontc/assets/master/gifs/yes.gif" alt="mission-control"/>
</div>


## Features ##

  - Projects
    - Keep a list of projects
    - Access the root directory of a project with a customizable action
    - Check version control status for all added projects
    - List todos in a project directory
  - Bookmarks
    - Keep a list of bookmarked locations
  - TODOs
    - List todos in the current project folder & jump to them
    - List todos from a global or project todo.txt file
    - Append todos to the quickfix or location list **(WIP)**
    - Syntax highlighting & filetype detection for `todo.txt` files
  - Sweet sweet Denite sources:
    - `projectile` - Source for projectile projects
    - `bookmark` - Source for projectile bookmarks
    - `todo` - Source for finding TODOs, FIXMEs, ANYTHINGs
    - `todotxt` - Source for `$TODO_FILE`
    - `todotxt_local` - Source for any todo.txt file
    - `sauce` - Source for Denite sources


## Requirements ##
  - [Shougo/denite.nvim](https://github.com/Shougo/denite.nvim)
  - Neovim (or Vim8) with Python3 support


## Installation ##
  - Install with your favorite plugin manager or management method.


## Configuration ##
  - By default, data is saved in `$XDG_CACHE_HOME/projectile` or `~/.cache/projectile/`.  
  - If you'd like it elsewhere, you can set an alternate path in one of two ways:
    - `g:projectile#data_dir = '<wherever>'`
    - `call denite#custom#var('projectile', 'data_dir', '<wherever>')`
  - Check out documentation.


## Issues ##
If you run into any bugs or if you have a feature request, feel free to
 [open an issue](https://github.com/dunstontc/projectile.nvim/issues)


## Credit & Thanks ##
  - [Shougo/denite.nvim](https://github.com/Shougo/denite.nvim)
  - [neoclide/denite-git](https://github.com/neoclide/denite-git)
  - [chemzqm/denite-extra](https://github.com/chemzqm/denite-extra)
  - [rafi/vim-denite-session](https://github.com/rafi/vim-denite-session)
  - [SpaceVim](https://github.com/SpaceVim/SpaceVim)
  - [freitass/todo.txt-vim](https://github.com/freitass/todo.txt-vim)


## Related Projects ##
  - [projectile](https://github.com/bbatsov/projectile)
    - Projectile is a project interaction library for Emacs.
  - [vim-rooter](https://github.com/airblade/vim-rooter)
    - Rooter changes the working directory to the project root when you open a file or directory.
  - [vim-projectionist](https://github.com/tpope/vim-projectionist)
    - Projectionist provides granular project configuration using "projections".
  - [vim-bookmarks](https://github.com/MattesGroeger/vim-bookmarks)
    - This vim plugin allows toggling bookmarks per line.
  - [TaskList.vim](https://github.com/vim-scripts/TaskList.vim)
    - Script based on the eclipse Task List.
  - [searchtasks.vim](https://github.com/gilsondev/searchtasks.vim)
    - Plugin to search the labels often used as TODO, FIXME and XXX.
  - [gather-todo.txt-vim](https://github.com/lgalke/gather-todo.txt-vim)
    - Gather contents of todo.txt files from a directory tree to display a kind of agenda view in a scratch buffer.
  - [todolist.vim](https://github.com/vim-scripts/todolist.vim)
  - [vim-todo](https://github.com/codegram/vim-todo)

