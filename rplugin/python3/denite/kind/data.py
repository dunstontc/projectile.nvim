"""Kind to model data; Create, Read, Update, & Delete said data. (currently files & folders in JSON)."""
#  =============================================================================
#  FILE: data.py
#  AUTHOR: Clay Dunston <dunstontc at gmail.com>
#  License: MIT
#  Last Updated: 2017-12-11
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
        self.name             = 'data'
        self.default_action   = 'read'
        self.persist_actions += ['preview', 'highlight']
        # TODO: See if there is a way to persist without saving the denite buffer.
        # self.persist_actions += ['add', 'delete', 'edit']
        # self.redraw_actions  += ['add', 'delete', 'edit']
        self._previewed_target = {}
        self._previewed_buffers = {}
        self.vars = {
            'data_dir': vim.vars.get('projectile#data_dir', '~/.config/projectile'),
            'date_format': '%d %b %Y %H:%M:%S',
            'exclude_filetypes': ['denite'],
        }

    def action_add(self, context):
        # data_path = context['__data_file']
        boofer = self.vim.current.buffer.name
        content = util.input(self.vim, context, 'Add as: ')
        if not len(content):
            # FIXME: If this returns null it will overwrite the file with 'null'.
            return
        # if not os.access('~/test.json', os.R_OK):
        #     return

        new_data = {
            'name': content,
            'root': boofer,
            'line': '',
            'col' : '',
            # 'date': str(datetime.datetime.now().isoformat()),
            'description': str(datetime.datetime.now().isoformat()),
        }

        with open('/users/clay/.config/projectile/bookmarks.json', 'r') as g:
            json_info   = json.load(g)
            json_info.append(new_data)

        with open('/users/clay/.config/projectile/bookmarks.json', 'w') as f:
            json.dump(json_info, f, indent=2)

    def action_read(self, context):
        cwd = self.vim.call('getcwd')
        for target in context['targets']:
            path = target['action__path']
            match_path = '^{0}$'.format(path)

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

    # def action_delete(self, context):
    #     target = context['targets'][0]
    #     # data_path = context['__data_file']
    #     content = util.input(self.vim, context, 'Add as: ')
    #     if not len(content):
    #         #
    #         # FIXME: If this returns null it will overwrite the file with the worn null.
    #         return
    #     # if not os.access('~/test.json', os.R_OK):
    #     #     return
    #
    #     with open('/users/clay/.config/projectile/bookmarks.json') as g:
    #         content= json.load(g)
    #         c_copy = testtwo[:]
    #         # TODO: c_copy.pop(target)
    #
    #     with open('/users/clay/.config/projectile/bookmarks.json', 'w') as f:
    #         json.dump(testthree, f, indent=2)


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
    #         # 'root': self.vim.eval('expand("%:p")'),
    #         # 'root': self.vim.current.buffer.name,
    #         'boofer': buffer,
    #         # 'buffers': self.vim.call('execute', 'ls'),
    #         'source_context': source_context,
    #         'ctx_bufnr': context['bufnr'],
    #         'description': str(datetime.datetime.now().isoformat()),
    #
    #     }
    #     with open('/users/clay/test/test.json', 'w') as f:
    #         json.dump(test_data, f, indent=2)

