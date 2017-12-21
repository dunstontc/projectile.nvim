"""Kind to model data; Create, Read, Update, & Delete said data. (currently files & folders in JSON)."""
#  =============================================================================
#  FILE: bookmark.py
#  AUTHOR: Clay Dunston <dunstontc at gmail.com>
#  License: MIT
#  Last Updated: 2017-12-20
#  =============================================================================

import os
import re
import json
import datetime

from ..kind.openable import Kind as Openable
from denite import util
# from denite.util import clearmatch, input


class Kind(Openable):

    def __init__(self, vim):
        super().__init__(vim)
        self.name             = 'bookmark'
        self.default_action   = 'read'
        self.persist_actions += ['preview', 'highlight', 'delete']
        self.redraw_actions  += ['delete']
        self._previewed_target  = {}
        self._previewed_buffers = {}
        self.vars = {
            'data_dir': vim.vars.get('projectile#data_dir', '~/.cache/projectile'),
            'date_format': '%d %b %Y %H:%M:%S',
            'exclude_filetypes': ['denite'],
            'has_rooter': vim.vars.get('loaded_rooter'),
            'has_devicons': vim.vars.get('loaded_devicons'),
        }

    def action_add(self, context):
        data_file = util.expand(self.vars['data_dir'] + '/bookmarks.json')
        boofer = self.vim.current.buffer.name
        linenr = self.vim.current.window.cursor[0]
        content = util.input(self.vim, context, 'Add as: ')
        if not len(content):
            # FIXME: If this returns null it will overwrite the file with 'null'.
            return
        # if not os.access('~/test.json', os.R_OK):
        #     return

        new_data = {
            'name': content,
            'path': boofer,
            'line': linenr,
            'col' : 1,
            'timestamp': str(datetime.datetime.now().isoformat()),
            'description': str(datetime.datetime.now().isoformat()),
        }

        with open(data_file, 'r') as g:
            json_info   = json.load(g)
            json_info.append(new_data)

        with open(data_file, 'w') as f:
            json.dump(json_info, f, indent=2)

    def action_delete(self, context):
        target = context['targets'][0]
        target_date = target['timestamp']
        data_file = util.expand(self.vars['data_dir'] + '/bookmarks.json')
        confirmation = self.vim.call('confirm', "Delete this bookmark?", "&Yes\n&No")
        if confirmation == 2:
            return
        else:
            with open(data_file, 'r') as g:
                content = json.load(g)
                bookmarks  = content[:]
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
                util.error(self.vim, f"error accessing {path}")
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

    def action_highlight(self, context):
        target = context['targets'][0]
        bufnr = self.vim.call('bufnr', target['action__path'])

        if not (self.vim.call('win_id2win', context['prev_winid']) and
                context['prev_winid'] in self.vim.call('win_findbuf', bufnr)):
            return

        prev_id = self.vim.call('win_getid')
        self.vim.call('win_gotoid', context['prev_winid'])
        self.__jump(context, target)
        self.__highlight(context, int(target.get('action__line', 0)))
        self.vim.call('win_gotoid', prev_id)

    def __highlight(self, context, line):
        util.clearmatch(self.vim)
        self.vim.current.window.vars['denite_match_id'] = self.vim.call(
            'matchaddpos', context['highlight_preview_line'], [line])

    def __jump(self, context, target):
        if 'action__pattern' in target:
            self.vim.call('search', target['action__pattern'], 'w')

        line = int(target.get('action__line', 0))
        col = int(target.get('action__col', 0))

        try:
            if line > 0:
                self.vim.call('cursor', [line, 0])
                if 'action__col' not in target:
                    pos = self.vim.current.line.lower().find(
                        context['input'].lower())
                    if pos >= 0:
                        self.vim.call('cursor', [0, pos + 1])
            if col > 0:
                self.vim.call('cursor', [0, col])
        except Exception:
            pass

        # Open folds
        self.vim.command('normal! zv')

    def __winid(self, target):
        """Needed for openable actions."""
        path = target['action__path']
        bufnr = self.vim.call('bufnr', path)
        if bufnr == -1:
            return None
        winids = self.vim.call('win_findbuf', bufnr)
        return None if len(winids) == 0 else winids[0]


    # def action_test(self, context):
    #     buffer = self.vim.current.buffer.name
    #         # return buffer.name == '' and len(buffer) == 1 and buffer[0] == ''
    #     source_context = context['source']
    #     content = util.input(self.vim, context, 'Add as: ')
    #     if not len(content):
    #         return
    #
    #     test_data = {}
    #     test_data = {
    #         'name': content,
    #         # 'path': self.vim.eval('expand("%:p")'),
    #         # 'path': self.vim.current.buffer.name,
    #         'boofer': buffer,
    #         # 'buffers': self.vim.call('execute', 'ls'),
    #         'source_context': source_context,
    #         'ctx_bufnr': context['bufnr'],
    #         'description': str(datetime.datetime.now().isoformat()),
    #
    #     }
    #     with open('/users/clay/test/test.json', 'w') as f:
    #         json.dump(test_data, f, indent=2)

