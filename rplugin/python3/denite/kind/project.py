"""Kind to model data; Create, Read, Update, & Delete said data. (currently files & folders in JSON)."""
#  =============================================================================
#  FILE: project.py
#  AUTHOR: Clay Dunston <dunstontc at gmail.com>
#  License: MIT
#  Last Updated: 2017-12-11
#  =============================================================================

# import os
# import re
import json
import datetime

from ..kind.openable import Kind as Openable
from denite import util
# from denite.util import clearmatch, input


def __get_id(array, attribute):
    # FIXME: There is a more pythonic way to do this.
    new_id = int(0)
    for item in array:
        cur_id = item['id']
        if cur_id > new_id:
            new_id = cur_id
    return new_id

class Kind(Openable):

    def __init__(self, vim):
        super().__init__(vim)
        self.name             = 'project'
        self.default_action   = 'cd'
        # self.persist_actions += ['preview', 'highlight']
        # TODO: See if there is a way to persist without saving the denite buffer.
        # self.persist_actions += ['add', 'delete', 'edit']
        # self.redraw_actions  += ['add', 'delete', 'edit']
        # self._previewed_target = {}
        # self._previewed_buffers = {}
        self.vars = {
            'data_dir': vim.vars.get('projectile#data_dir', '~/.cache/projectile'),
            'date_format': '%d %b %Y %H:%M:%S',
            'exclude_filetypes': ['denite'],
        }

    def action_add(self, context):
        data_file = util.expand(self.vars['data_dir'] + '/projects.json')
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
            'added': str(datetime.datetime.now().isoformat()),
            'description': '',
        }

        with open(data_file, 'r') as g:
            json_info   = json.load(g)
            json_info.append(new_data)

        with open(data_file, 'w') as f:
            json.dump(json_info, f, indent=2)

    def action_cd(self, context):
        """Change lcd.

        Parameters
        ----------
        context : object
            Used to reference context[targets].

        """
        target = context['targets'][0]
        self.vim.command('lcd {}'.format(target['action__path']))

    def action_narrow(self, context):
        target = context['targets'][0]
        context['sources_queue'].append([
            {'name': 'file', 'args': []},
            {'name': 'file', 'args': ['new']},
        ])
        context['path'] = target['action__path']

    def action_open(self, context):
        for target in context['targets']:
            path = target['action__path']
            match_path = '^{0}$'.format(path)

            if self.vim.call('bufwinnr', match_path) <= 0:
                self.vim.call(
                    'denite#util#execute_path', 'edit', path)
            elif self.vim.call('bufwinnr',
                               match_path) != self.vim.current.buffer:
                self.vim.call(
                    'denite#util#execute_path', 'buffer', path)

    def __winid(self, target):
        """Needed for openable actions."""
        path = target['action__path']
        bufnr = self.vim.call('bufnr', path)
        if bufnr == -1:
            return None
        winids = self.vim.call('win_findbuf', bufnr)
        return None if len(winids) == 0 else winids[0]

    def action_delete(self, context):
        target = context['targets'][0]
        # data_path = context['__data_file']
        # content = util.input(self.vim, context, 'Add as: ')
        confirmation = self.vim.confirm("Save changes?", "&Yes\n&No\n&Cancel")
        # if not len(content):
            #
            # FIXME: If this returns null it will overwrite the file with the worn null.
        # return
        # if not os.access('~/test.json', os.R_OK):
        #     return

        # with open('/users/clay/.cache/projectile/bookmarks.json') as g:
        #     content= json.load(g)
        #     c_copy = testtwo[:]
        #     # TODO: c_copy.pop(target)
        #
        # with open('/users/clay/.cache/projectile/bookmarks.json', 'w') as f:
        #     json.dump(testthree, f, indent=2)


