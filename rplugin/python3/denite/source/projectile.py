#  =============================================================================
#  FILE: projectile.py
#  AUTHOR: Clay Dunston <dunstontc at gmail.com>
#  License: MIT
#  =============================================================================

import os
import json
from .base import Base
from denite import util

class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'projectile'
        self.kind = 'project'
        self.vars = {
            'data_dir': vim.vars.get('projectile#data_dir', '~/.config/projectile'),
            'has_rooter': vim.vars.get('loaded_rooter'),
            'has_devicons': vim.vars.get('loaded_devicons'),
        }

    def on_init(self, context):
        # if not self.vars.get('path'):
            # raise AttributeError('Invalid session directory, please configure')
        context['projects_file'] = util.expand(self.vars['data_dir'] + '/projects.json')
        # if self.vim.vars('g:loaded_rooter') == 1:
            # context['__cwd'] = self.vim.call('FindRootDirectory()')

    def gather_candidates(self, context):
        if not os.access(context['projects_file'], os.R_OK):
            return []

        candidates = []
        with open(context['projects_file']) as fp:
            try:
                config = json.loads(fp.read())
                for obj in config:
                    candidates.append({
                        'word': obj['root'],
                        'abbr': '{0:^25} -- {1:^50} -- {2}'.format(
                            obj['name'],
                            obj['description'],
                            obj['root']
                        ),
                        'action__path': obj['root'],
                        })
            except json.JSONDecodeError:
                util.error(self.vim, 'Decode error for %s' % context['projects_file'])

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
