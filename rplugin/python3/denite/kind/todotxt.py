"""Read & write todo.txt files."""
#  =============================================================================
#  FILE: todotxt.py
#  AUTHOR: Clay Dunston <dunstontc@gmail.com>
#  License: MIT
#  Last Modified: 2018-01-12
#  =============================================================================

# import os
# import re
# import json
# import datetime

from denite import util
from ..kind.word import Kind as Word


class Kind(Word):
    """Bookmark kind, extends File kind.

    Methods
    -------
    action_add()
    action_delete()

    """

    def __init__(self, vim):
        """Initialize thyself."""
        super().__init__(vim)
        self.name             = 'todotxt'
        self.default_action   = 'yank'
        self.persist_actions += ['add', 'delete']
        self.redraw_actions  += ['add', 'delete']
        self.vars = {
            'exclude_filetypes': ['denite'],
            'data_dir':          vim.vars.get('projectile#data_dir', '~/.cache/projectile'),
            'user_cmd':          vim.vars.get('projectile#directory_command'),
            'icon_setting':      vim.vars.get('projectile#enable_devicons'),
            'format_setting':    vim.vars.get('projectile#enable_formatting'),
            'highlight_setting': vim.vars.get('projectile#enable_highlighting'),
            'todotxt_cfg_file':  vim.call('expand', r'$TODOTXT_CFG_FILE'),
            'todo_file':         vim.call('expand', r'$TODO_FILE'),
            'done_file':         vim.call('expand', r'$DONE_FILE'),
            'todo_dir':          vim.call('expand', r'$TODO_DIR'),
        }

    def action_add(self, context):
        """Add a new entry to a todo.txt file."""
        data_file = self.vars['todo_file']

        new_todo = util.input(self.vim, context, 'New todo: ')
        if not len(new_todo):
            new_todo = ''
            return

        with open(data_file, 'a') as g:
                g.write(new_todo)

    def action_delete(self, context):
        """Add a new entry to a todo.txt file."""
        data_file      = self.vars['todo_file']
        target         = context['targets'][0]
        target_ln      = target['action__line']
        target_content = target['word']

        confirmation = self.vim.call('confirm', f"Complete item?: '{target_content}' ?", "&Yes\n&No")
        if confirmation == 2:
            return
        else:
            with open(data_file, 'r') as g:
                # try:
                    todos = g.read().split('\n')
                # except json.JSONDecodeError:

            with open('/Users/clay/test/todotest.txt', 'w+') as g:
                # try:
                    todos = g.read().split('\n')
                # except json.JSONDecodeError:
