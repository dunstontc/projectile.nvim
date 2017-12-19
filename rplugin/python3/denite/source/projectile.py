#  =============================================================================
#  FILE: projectile.py
#  AUTHOR: Clay Dunston <dunstontc at gmail.com>
#  License: MIT
#  =============================================================================

import os
import json
from .base import Base
from denite import util


def get_length(array, attribute):
    """Get the max string length for an attribute in a collection."""
    max_count = int(0)
    for item in array:
        cur_attr = item[attribute]
        cur_len = len(cur_attr)
        if cur_len > max_count:
            max_count = cur_len
    return max_count

class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'projectile'
        self.kind = 'project'
        self.vars = {
            'exclude_filetypes': ['denite'],
            'data_dir':     vim.vars.get('projectile#data_dir', '~/.cache/projectile'),
            'user_cmd':     vim.vars.get('projectile#directory_command'),
            'has_rooter':   vim.vars.get('loaded_rooter'),
            'has_devicons': vim.vars.get('loaded_devicons'),
            'has_nerdtree': vim.vars.get('loaded_nerdtree'),
            'has_vimfiler': vim.vars.get('loaded_vimfiler'),
        }

    def on_init(self, context):
        # if not self.vars.get('path'):
            # raise AttributeError('Invalid session directory, please configure')
        context['projects_file'] = util.expand(self.vars['data_dir'] + '/projects.json')
        # if self.vim.vars('g:loaded_rooter') == 1:
            # context['__cwd'] = self.vim.call('FindRootDirectory()')

    def gather_candidates(self, context):
        # if not os.access(context['projects_file'], os.R_OK):
        #     return []

        candidates = []
        with open(context['projects_file'], 'r') as fp:
            try:
                config = json.loads(fp.read())
                name_len = get_length(config, 'name')
                path_len = get_length(config, 'root')

                for obj in config:
                    candidates.append({
                        'word': obj['root'],
                        'abbr': '{0:>{name_len}} -- {1:<{path_len}} -- {2}'.format(
                            obj['name'],
                            # obj['description'],
                            obj['root'],
                            obj['timestamp'],
                            name_len = name_len,
                            path_len = path_len
                        ),
                        'action__path': obj['root'],
                        'name':         obj['name'],
                        'timestamp':    obj['timestamp'],
                        })
            except json.JSONDecodeError:
                err_string = 'Decode error for' + context['projects_file']
                util.error(self.vim, err_string)

        return candidates

    def define_syntax(self):
        self.vim.command(r'syntax match deniteSource_Projectile_Project /^.*$/ '
                         r'containedin=' + self.syntax_name + ' '
                         r'contains=deniteSource_Projectile_Project,deniteSource_Projectile_Noise,deniteSource_Projectile_Name,deniteSource_Projectile_Description,deniteSource_Projectile_Path,deniteSource_Projectile_Timestamp')
        self.vim.command(r'syntax match deniteSource_Projectile_Noise /\(\s--\s\)/ contained ')
                         # r'contained containedin=deniteSource_Projectile_Project')
        self.vim.command(r'syntax match deniteSource_Projectile_Name /^\(.*\)\(\(.* -- \)\{3\}\)\@=/ contained ')
                         # r'contained containedin=deniteSource_Projectile_Project')
        self.vim.command(r'syntax match deniteSource_Projectile_Description /\(\(.* -- \)\{1\}\)\@<=\(.*\)\(\(.* -- \)\{2\}\)\@=/ contained ')
                         # r'contained containedin=deniteSource_Projectile_Project')
        self.vim.command(r'syntax match deniteSource_Projectile_Path /\(\(.* -- \)\{2\}\)\@<=\(.*\)\(\(.* -- \)\{1\}\)\@=/ contained ')
                         # r'contained containedin=deniteSource_Projectile_Project')
        self.vim.command(r'syntax match deniteSource_Projectile_Timestamp /\v((-- .*){3})@<=(.*)/ contained ')
                         # r'contained containedin=deniteSource_Projectile_Project')

    def highlight(self):
        self.vim.command('highlight link deniteSource_Projectile_Project Normal')
        self.vim.command('highlight link deniteSource_Projectile_Noise Comment')
        self.vim.command('highlight link deniteSource_Projectile_Name Identifier')
        self.vim.command('highlight link deniteSource_Projectile_Description String')
        self.vim.command('highlight link deniteSource_Projectile_Path Directory')
        self.vim.command('highlight link deniteSource_Projectile_Timestamp Number')
