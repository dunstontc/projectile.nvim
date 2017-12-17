# Projectile.nvim #

> Collection of features for Vim similar to [bbatsov/projectile](https://github.com/bbatsov/projectile); using [Shougo/denite.nvim](https://github.com/Shougo/denite.nvim) for it's interfaces.

## Features ##
  - Projects
  - Bookmarks
  - TODOs

### TODO: ###
  - Find todos recursively in the current directory & push them to either the location list or the quickfix list.
    - [Running an external command in python](https://stackoverflow.com/questions/4760215/running-shell-command-from-python-and-capturing-the-output)
  - Compile TODOS from *todo.txt* files
  - Provide Denite source **not needed if pushed to location/quickfix list?**
    - [denite-ale](https://github.com/iyuuya/denite-ale/blob/master/rplugin/python3/denite/source/ale.py) - Might be handy as a starting point
    - [denite-extra/quickfix.py](https://github.com/chemzqm/denite-extra/blob/master/rplugin/python3/denite/source/quickfix.py)
    - [denite.nvim/grep source](/Users/clay/Projects/Vim/Denite/denite.nvim/rplugin/python3/denite/source/grep.py) ##

#### Todo/rec ####
  - [grep](https://www.gnu.org/software/grep/manual/grep.html)
  - [ack](https://beyondgrep.com/documentation/)
    - [also ack](http://conqueringthecommandline.com/book/ack_ag)
  - [Silver Searcher](https://github.com/ggreer/the_silver_searcher/wiki/Advanced-Usage)
    - [also ag](http://manpages.ubuntu.com/manpages/zesty/man1/ag.1.html)
    - [ag](https://www.mankier.com/1/ag)
  - [ripgrep](https://github.com/BurntSushi/ripgrep)

```sh
# -E - RegEx
# -r - Recursive
# -n - Show line Numbers
grep -Ern "(TODO:|FIXME:|XXX:)" .
grep -Ern "(TODO:|FIXME:|XXX:).*$" .
# r - recursive
ack -r "(TODO:|FIXME:|XXX:).*$" .
# -r       - Recursive
# -o       - Only print the matching parts of lines
# --silent - Suppress error messages
# -s       - Case sensitive
ag -r --nocolor --silent "(TODO:|FIXME:|XXX:).*$" .
```


## Usage ##

  Settings are persisted in in `$XDG_CONFIG_HOME/projectile` by default.  
  You can change the location by setting `g:projectile#data_dir` to your preferred path.  


## Denite ##
  - [usr_41.html#41.6: Using Functions](https://neovim.io/doc/user/usr_41.html#41.6)

### Sources ###

  **projects**

  **bookmarks**

### Kinds ###

  **JSON**

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

> This project is just a patchwork of preexisting code. Here's that code:  
[Shougo/denite.nvim](https://github.com/Shougo/denite.nvim)  
[chemzqm/denite-extra](https://github.com/chemzqm/denite-extra)  
