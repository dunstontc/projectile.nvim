#  =============================================================================
#  FILE: bookmark.py
#  AUTHOR: Clay Dunston <dunstontc at gmail.com>
#  License: MIT
#  Last Modified: 2017-12-20
#  =============================================================================

import os
import json
import pathlib

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
        context['data_file']  = util.expand(self.vars['data_dir'] + '/bookmarks.json')
        # (denite-extra)
        context['__linenr']   = self.vim.current.window.cursor[0]
        context['__bufnr']    = self.vim.current.buffer.number
        context['__bufname']  = self.vim.current.buffer.name
        context['__filename'] = os.path.basename(context['__bufname'])
        # (denite-marks)
        # text = self.vim.call('getline', context['__linenr'])
        # if not os.path.exists(context['data_file']):
            # pathlib.Path(self.vars['data_dir']).mkdir(parents=True, exist_ok=True)
            # with open(context['data_file'], 'w+') as f:
                # json.dump([], f, indent=2)


    def gather_candidates(self, context):
        if not os.path.exists(context['data_file']):
            util.error(self.vim, f"error accessing {context['data_file']}")
            return

        candidates = []
        with open(context['data_file'], 'r') as fp:
            try:
                config   = json.load(fp)
            except json.JSONDecodeError:
                # err_string = 'Decode error for' + context['data_file']
                # util.error(self.vim, err_string)
                config   = []
            path_len = get_length(config, 'path')
            desc_len = get_length(config, 'description')
            name_len = get_length(config, 'name')

            for obj in config:
                if not os.path.isfile(obj['path']):
                    err_mark = '✗ '
                else:
                    err_mark = ''
                candidates.append({
                    'word': obj['path'],
                    'abbr': " {0} {1:^{name_len}} -- {err_mark}{2:<{path_len}} -- {3}".format(
                        self.vim.funcs.WebDevIconsGetFileTypeSymbol(obj['path']),  # TODO: Check avainst @has_devicons
                        obj['name'],
                        obj['path'].replace(os.path.expanduser('~'), '~'),
                        obj['timestamp'],
                        err_mark=err_mark,
                        path_len=path_len,
                        desc_len=desc_len,
                        name_len=name_len
                    ),
                    'action__path': obj['path'],
                    'action__line': obj['line'],
                    'action__col':  obj['col'],
                    'timestamp':    obj['timestamp'],
                })

        return candidates

    def define_syntax(self):
        self.vim.command(r'syntax match deniteSource_Projectile_Project /^.*$/ '
                         r'containedin=' + self.syntax_name + ' '
                         r'contains=deniteSource_Projectile_Project,deniteSource_Projectile_Noise,deniteSource_Projectile_Name,deniteSource_Projectile_Path,deniteSource_Projectile_Timestamp,deniteSource_Projectile_Error')
        self.vim.command(r'syntax match deniteSource_Projectile_Noise     /\(\s--\s\)/                                          contained ')
        self.vim.command(r'syntax match deniteSource_Projectile_Name      /^\(.*\)\(\(.* -- \)\{2\}\)\@=/                       contained ')
        self.vim.command(r'syntax match deniteSource_Projectile_Path      /\(\(.* -- \)\{1\}\)\@<=\(.*\)\(\(.* -- \)\{1\}\)\@=/ contained ')
        self.vim.command(r'syntax match deniteSource_Projectile_Timestamp /\v((-- .*){2})@<=(.*)/                               contained ')
        self.vim.command(r'syntax match deniteSource_Projectile_Error     /✗/                                                   contained ')

    def highlight(self):
        self.vim.command('highlight link deniteSource_Projectile_Project Normal')
        self.vim.command('highlight link deniteSource_Projectile_Noise Comment')
        self.vim.command('highlight link deniteSource_Projectile_Name String')
        self.vim.command('highlight link deniteSource_Projectile_Path Directory')
        self.vim.command('highlight link deniteSource_Projectile_Timestamp Number')
        self.vim.command('highlight link deniteSource_Projectile_Error Error')


