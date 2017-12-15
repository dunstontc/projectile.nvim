#  =============================================================================
#  FILE: bookmark.py
#  AUTHOR: Clay Dunston <dunstontc at gmail.com>
#  License: MIT
#  =============================================================================

# import os
import json
from .base import Base
from denite import util

class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'bookmark'
        self.kind = 'data'
        self.vars = {
            'data_dir': vim.vars.get('projectile#data_dir', '~/.config/projectile'),
            'date_format': '%d %b %Y %H:%M:%S',
            'exclude_filetypes': ['denite'],
        }

    def on_init(self, context):
        # context['is_interactive'] = True
        context['data_file']    = util.expand(self.vars['data_dir'] + '/bookmarks.json')
        context['hacks']        = []
        context['current_buff'] = self.vim.current.buffer.name
        # data_file = util.expand(self.vars['data_dir'] + '/bookmarks.json')
        # context['__db'] = TinyDB(data_file)
        # if not self.vars.get('path'):
        #     raise AttributeError('Invalid session directory, please configure')

    def gather_candidates(self, context):
        # if not os.access(context['data_file'], os.R_OK):
            # return []

        candidates = []
        with open(context['data_file'], 'r') as fp:
            # try:
                config = json.load(fp)
                for obj in config:
                    candidates.append({
                        'word': obj['root'],
                        'abbr': '{0:^25} -- {1:^50} -- {2}'.format(obj['name'], obj['description'], obj['root']),
                        'action__path': obj['root'],
                    })
            # except json.JSONDecodeError:
                # util.error(self.vim, 'Decode error for %s' % context['data_file'])
                return candidates
        # context['hacks'].extend(candidates)

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

