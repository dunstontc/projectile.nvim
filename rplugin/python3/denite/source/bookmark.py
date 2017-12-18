#  =============================================================================
#  FILE: bookmark.py
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

        self.name = 'bookmark'
        self.kind = 'bookmark'
        self.vars = {
            'data_dir': vim.vars.get('projectile#data_dir', '~/.cache/projectile'),
            'date_format': '%d %b %Y %H:%M:%S',
            'exclude_filetypes': ['denite'],
            'has_rooter': vim.vars.get('loaded_rooter'),
            'has_devicons': vim.vars.get('loaded_devicons'),
        }

    def on_init(self, context):
        # context['is_interactive'] = True
        context['data_file']  = util.expand(self.vars['data_dir'] + '/bookmarks.json')
        # (denite-extra)
        context['__linenr']   = self.vim.current.window.cursor[0]
        context['__bufnr']    = self.vim.current.buffer.number
        context['__bufname']  = self.vim.current.buffer.name
        context['__filename'] = os.path.basename(context['__bufname'])
        # (denite-marks)
        # text = self.vim.call('getline', context['__linenr'])
        # if not self.vars.get('path'):
        #     raise AttributeError('Invalid directory, please configure')

    def gather_candidates(self, context):
        # if not os.access(context['data_file'], os.R_OK):
            # return []

        candidates = []
        with open(context['data_file'], 'r') as fp:
            try:
                config  = json.load(fp)
                path_width = get_length(config, 'path')
                desc_width = get_length(config, 'description')
                for obj in config:
                    candidates.append({
                        'word': obj['path'],
                        'abbr': "{0:>{width1}}  {1} -- {2:<{width2}} -- {4} --".format(
                            obj['path'],
                            self.vim.funcs.WebDevIconsGetFileTypeSymbol(obj['path']),
                            obj['name'],
                            obj['description'],
                            obj['timestamp'],
                            width1=path_width,
                            width2=desc_width,
                            ),
                        'action__path': obj['path'],
                        'action__line': obj['line'],
                        'action__col':  obj['col'],
                        'timestamp':    obj['timestamp'],
                    })
            except json.JSONDecodeError:
                err_string = 'Decode error for' + context['data_file']
                util.error(self.vim, err_string)
                # util.error(self.vim, f'Decode error for {context["data_file"]}')

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


