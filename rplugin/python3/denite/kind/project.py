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

def get_length(array):
    """Get the max string length for an attribute in a collection."""
    max_count = int(0)
    for item in array:
        cur_len = len(item)
        if cur_len > max_count:
            max_count = cur_len
    return max_count

class Kind(Openable):

    def __init__(self, vim):
        super().__init__(vim)
        self.name             = 'project'
        self.default_action   = 'add'
        # self.default_action   = 'prompt' TODO: prompt for action
        # TODO: See if there is a way to persist without saving the denite buffer.
        self.persist_actions += ['delete', 'edit']
        self.redraw_actions  += ['delete', 'edit']
        self.vars = {
            'exclude_filetypes': ['denite'],
            'date_format': '%d %b %Y %H:%M:%S',
            'data_dir': vim.vars.get('projectile#data_dir', '~/.cache/projectile'),
            'has_rooter': vim.vars.get('loaded_rooter'),
            'has_devicons': vim.vars.get('loaded_devicons')
        }

    def action_add(self, context):
        data_file = util.expand(self.vars['data_dir'] + '/projects.json')
        root_dir = self.vim.call('getcwd')
        new_data = {}
        if self.vars['has_rooter'] == 1:
            rooter_dir = self.vim.eval('FindRootDirectory()')

        propt_string = f'Add project at \"{root_dir}\" as: '

        content = util.input(self.vim, context, propt_string)
        # content = util.input(self.vim, context, 'Add as: ')
        if not len(content):
            # FIXME: If this returns null it will overwrite the file with 'null'.
            return
        # if not os.access('~/test.json', os.R_OK):
        #     return
        new_data = {
            'name': content,
            'root': rooter_dir,
            'timestamp': str(datetime.datetime.now().isoformat()),
            'description': '',
        }

        with open(data_file, 'r') as g:
            json_info   = json.load(g)
            json_info.append(new_data)

        with open(data_file, 'w') as f:
            json.dump(json_info, f, indent=2)

    def action_delete(self, context):
        target = context['targets'][0]
        target_date = target['timestamp']
        data_file = util.expand(self.vars['data_dir'] + '/projects.json')
        confirmation = self.vim.call('confirm', "Remove this project?", "&Yes\n&No")
        if confirmation == 2:
            return
        else:
            with open(data_file, 'r') as g:
                content = json.load(g)
                projects  = content[:]
                for i in range(len(projects)):
                    if projects[i]['timestamp'] == target_date:
                        projects.pop(i)
                        break

            with open(data_file, 'w') as f:
                json.dump(projects, f, indent=2)

    def action_cd(self, context):
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



