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
        self.kind = 'directory'
        self.default_action = 'cd'
        self.vars = {
            'data_dir': vim.vars.get('projectile#data_dir', '~/.config/projectile'),
            # "data_dir": '~/.config/projectile/projects.json' # TODO: Pull from g:projectile#directory
        }


    def on_init(self, context):
        # if not self.vars.get('path'):
            # raise AttributeError('Invalid session directory, please configure')
        context['projects_file'] = util.expand(self.vars['data_dir'] + '/projects.json')

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
                        'abbr': '{0:^25} -- {1:^50} -- {2}'.format(obj['name'], obj['description'], obj['root']),
                        'action__path': obj['root'],
                        })
            except json.JSONDecodeError:
                util.error(self.vim, 'Decode error for %s' % context['projects_file'])

        return candidates

    def define_syntax(self):
        self.vim.command(r'syntax match deniteSource_Projectile_Project /^.*$/ '
                         r'containedin=' + self.syntax_name)
        self.vim.command(r'syntax match deniteSource_Projectile_Noise /\v(\s--\s)/ contained '
                         r'contained containedin=deniteSource_Projectile_Project,deniteSource_Projectile_Name,deniteSource_Projectile_Description')
        # self.vim.command(r'syntax match deniteSource_Projectile_Name /\v^\zs.*\ze(\s--\s)/ contained '
                         # r'contained containedin=deniteSource_Projectile_Project,deniteSource_Projectile_Description')
        # self.vim.command(r'syntax match deniteSource_Projectile_Description /^.*--\s\zs.*\ze--/ contained '
                         # r'contained containedin=deniteSource_Projectile_Project,deniteSource_Projectile_Dir')
        self.vim.command(r'syntax match deniteSource_Projectile_Dir /^.*--.*--\zs.*\ze/ contained '
                         r'contained containedin=deniteSource_Projectile_Project,deniteSource_Projectile_Description')

    def highlight(self):
        self.vim.command('highlight link deniteSource_Projectile_Project Normal')
        self.vim.command('highlight link deniteSource_Projectile_Noise Comment')
        # self.vim.command('highlight link deniteSource_Projectile_Name Number')
        self.vim.command('highlight link deniteSource_Projectile_Dir Directory')
        # self.vim.command('highlight link deniteSource_Projectile_Description String')
