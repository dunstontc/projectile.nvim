# Projectile.nvim #


![under_construction](https://raw.githubusercontent.com/dunstontc/assets/master/gifs/pika.gif)

> Collection of features for Vim similar to [bbatsov/projectile](https://github.com/bbatsov/projectile); using [Shougo/denite.nvim](https://github.com/Shougo/denite.nvim) for it's interfaces.  
> I wouldn't recommend using this quite yet, but if you do and you think of anything it needs that isn't already listed in [the todo file](todo.txt), let me know.

## Features ##
> Some of these items have yet to be implemented.
  - Projects
    - Keep a list of project locations with metadata
    - Add, Remove, or Open Projects
    - Check version control status of Projects
    - List todos in a project
  - Bookmarks
    - Keep a list of bookmarked locations that can be jumped to
  - TODOs
    - List todos in the current project folder & jump to them
    - List todos from a todo.txt file
    - Append todos to the quickfix or location list


## Usage ##
### Requirements ###
  - [Shougo/denite.nvim](https://github.com/Shougo/denite.nvim)
  - (currently) [vim-rooter](https://github.com/airblade/vim-rooter)
  - Vim or Neovim with Python3 support

### Configuration ###
  - Settings are persisted in in `$XDG_CACHE_HOME/projectile` by default.  
  - You can change the location by setting `g:projectile#data_dir` to your preferred path.  

```viml
let g:projectile#data_dir = '~/.projectile'
```

## Denite Sources ##
```vim
:Denite projectile
```


```vim
:Denite bookmark
```

```vim
:Denite 
```


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

## Credit & Thanks ##

<!-- > A good portion of this project is just a patchwork of preexisting code. Here's that code:   -->
[Shougo/denite.nvim](https://github.com/Shougo/denite.nvim)  
[chemzqm/denite-extra](https://github.com/chemzqm/denite-extra)  
[rafi/vim-denite-session](https://github.com/rafi/vim-denite-session)
