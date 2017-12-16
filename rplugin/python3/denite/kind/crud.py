#  =============================================================================
#  FILE: data.py
#  AUTHOR: Clay Dunston <dunstontc at gmail.com>
#  License: MIT
#  Last Updated: 2017-12-11
#  =============================================================================

# import os
import datetime
import json
from .base import Base
from denite import util


class Kind(Base):

    def __init__(self, vim):
        super().__init__(vim)
        self.name             = 'crud'
        self.default_action   = 'create'
        # TODO: See if there is a way to persist without saving the denite buffer.
        # self.persist_actions += ['create', 'read','delete', 'update']
        # self.redraw_actions  += ['create', 'read', 'delete', 'update']
        self.vars = {
            'data_dir': vim.vars.get('projectile#data_dir', '~/.config/projectile'),
            'date_format': '%d %b %Y %H:%M:%S',
            'exclude_filetypes': ['denite'],
        }

    def action_create(self, context):
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
            'description': str(datetime.datetime.now().isoformat()),
        }

        with open('/users/clay/.config/projectile/bookmarks.json', 'r') as g:
            json_info   = json.load(g)
            json_info.append(new_data)

        with open(context['json_file'], 'w') as f:
            json.dump(json_info, f, indent=2)


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

