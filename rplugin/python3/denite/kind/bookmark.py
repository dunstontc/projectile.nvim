"""Read & write bookmarked paths to json file."""
#  =============================================================================
#  FILE: bookmark.py
#  AUTHOR: Clay Dunston <dunstontc@gmail.com>
#  License: MIT
#  Last Modified: 2017-12-22
#  =============================================================================

import os
import re
import json
import datetime

from denite import util
from ..kind.file import Kind as File


class Kind(File):
    """Bookmark kind, extends File kind.

    Methods
    -------
    action_add()
        Prompts for confirmation of the path and a name for the bookmark,
        then adds it to *bookmarks.json*
    action_delete()
        Prompts for confirmation and removes a bookmark from *bookmarks.json*
    action_read()
        TODO: Make sure a file exists before opening
    super.action_open()
    super.action_preview()
    super.action_highlight()
    super.action_quickfix()

    """

    def __init__(self, vim):
        """Initialize thyself."""
        super().__init__(vim)
        self.name             = 'bookmark'
        self.default_action   = 'open'
        self.persist_actions += ['preview', 'highlight', 'delete']
        self.redraw_actions  += ['delete']
        self._previewed_target  = {}
        self._previewed_buffers = {}
        self.vars = {
            'exclude_filetypes': ['denite'],
            'data_dir':          vim.vars.get('projectile#data_dir', '~/.cache/projectile'),
            'user_cmd':          vim.vars.get('projectile#directory_command'),
            'icon_setting':      vim.vars.get('projectile#enable_devicons'),
            'format_setting':    vim.vars.get('projectile#enable_formatting'),
            'highlight_setting': vim.vars.get('projectile#enable_highlighting'),
        }

    def action_add(self, context):
        """Add a bookmark to ``projectile#data_dir``/bookmarks.json"""
        data_file = util.expand(self.vars['data_dir'] + '/bookmarks.json')
        boofer    = self.vim.current.buffer.name
        linenr    = self.vim.current.window.cursor[0]

        bookmark_path = util.input(self.vim, context, 'Bookmark Path: ', boofer)
        if not len(bookmark_path):
            bookmark_path = boofer

        bookmark_name = util.input(self.vim, context, 'Bookmark Name: ')
        if not len(bookmark_name):
            bookmark_name = ''
            return

        new_data = {
            'name': bookmark_name,
            'path': bookmark_path,
            'line': linenr,
            'col' : 1,            # TODO: get column number when adding bookmarks
            'timestamp': str(datetime.datetime.now().isoformat()),
        }

        with open(data_file, 'r') as g:
            try:
                json_info = json.load(g)
            except json.JSONDecodeError:
                json_info = []
            json_info.append(new_data)

        with open(data_file, 'w') as f:
            json.dump(json_info, f, indent=2)

    def action_delete(self, context):
        """Remove a bookmark from `projectile#data_dir`/bookmarks.json."""
        target       = context['targets'][0]
        target_date  = target['timestamp']
        target_name  = target['name']
        data_file    = util.expand(self.vars['data_dir'] + '/bookmarks.json')

        confirmation = self.vim.call('confirm', "Delete bookmark: '{}' ?", "&Yes\n&No".format(target_name))
        if confirmation == 2:
            return
        else:
            with open(data_file, 'r') as g:
                content   = json.load(g)
                bookmarks = content[:]
                for i in range(len(bookmarks)):
                    if bookmarks[i]['timestamp'] == target_date:
                        bookmarks.pop(i)
                        break

            with open(data_file, 'w') as f:
                json.dump(bookmarks, f, indent=2)

    def action_read(self, context):
        cwd = self.vim.call('getcwd')
        for target in context['targets']:
            path = target['action__path']
            match_path = '^{0}$'.format(path)

            if not os.path.exists(path):
                util.error(self.vim, "error accessing {}".format(path))
                # TODO: Handle this error.

            if re.match('https?://', path):
                # URI
                self.vim.call('denite#util#open', path)
                return
            if path.startswith(cwd):
                path = os.path.relpath(path, cwd)

            if self.vim.call('bufwinnr', match_path) <= 0:
                self.vim.call(
                    'denite#util#execute_path', 'edit', path)
            elif self.vim.call('bufwinnr',
                               match_path) != self.vim.current.buffer:
                self.vim.command('buffer' +
                                 str(self.vim.call('bufnr', path)))
            self.__jump(context, target)

            if path in self._previewed_buffers:
                self._previewed_buffers.pop(path)

