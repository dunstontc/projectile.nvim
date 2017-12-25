"""Denite source for bookmarked files."""
#  =============================================================================
#  FILE: bookmark.py
#  AUTHOR: Clay Dunston <dunstontc@gmail.com>
#  License: MIT
#  Last Modified: 2017-12-25
#  =============================================================================

import os
import json
# import pathlib

from .base import Base
from denite import util


class Source(Base):
    """Denite source for bookmarked files."""

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'bookmark'
        self.kind = 'bookmark'
        self.vars = {
            'exclude_filetypes': ['denite'],
            'date_format':       '%d %b %Y %H:%M:%S',
            'data_dir':          vim.vars.get('projectile#data_dir', '~/.cache/projectile'),
            'icon_setting':      vim.vars.get('projectile#enable_devicons'),
        }

    def on_init(self, context):
        """Parse and accept user settings."""
        context['data_file']  = util.expand(self.vars['data_dir'] + '/bookmarks.json')
        if not os.path.exists(context['data_file']):
            util.error(self.vim, f"Error accessing {context['data_file']}")
            return
        # if not os.path.exists(context['data_file']):
        #     pathlib.Path(self.vars['data_dir']).mkdir(parents=True, exist_ok=True)
        #     with open(context['data_file'], 'w+') as f:
        #         json.dump([], f, indent=2)

    def gather_candidates(self, context):
        """Gather candidates from ``projectile#data_dir``/projects.json."""
        candidates = []

        with open(context['data_file'], 'r') as fp:
            try:
                config = json.load(fp)
            except json.JSONDecodeError:
                err_string = 'Decode error for' + context['data_file']
                util.error(self.vim, err_string)
                config = []

            for obj in config:
                candidates.append({
                    'word': obj['path'],
                    'action__path': obj['path'],
                    'action__line': obj['line'],
                    'action__col':  obj['col'],
                    'name':         obj['name'],
                    'timestamp':    obj['timestamp'],
                })

        return self._convert(candidates)

    def _convert(self, candidates):
        """Format and add metadata to gathered candidates.

        Parameters
        ----------
        candidates : list

        Returns
        -------
        A sexy source.

        """
        path_len = self._get_length(candidates, 'short_path')
        name_len = self._get_length(candidates, 'name')

        for candidate in candidates:

            if not os.path.isfile(candidate['action__path']):
                if self.vars['icon_setting'] == 0:
                    err_mark = 'X '
                else:
                    err_mark = '✗ '
            else:
                err_mark = '  '

            if self.vars['icon_setting'] == 1:
                icon = self.vim.funcs.WebDevIconsGetFileTypeSymbol(candidate['action__path'])
            else:
                icon = '  '

            candidate['abbr'] = "{0} {1:^{name_len}} -- {err_mark} {2:<{path_len}} -- {3}".format(
                icon,
                candidate['name'],
                candidate['action__path'].replace(os.path.expanduser('~'), '~'),
                candidate['timestamp'],
                err_mark=err_mark,
                name_len=name_len,
                path_len=(path_len + 3),
            )
        return candidates

    def get_length(self, array, attribute):
        """Get the max string length for an attribute in a collection."""
        max_count = int(0)
        for item in array:
            cur_attr = item[attribute]
            cur_len = len(cur_attr)
            if cur_len > max_count:
                max_count = cur_len
        return max_count

    def define_syntax(self):
        """Define Vim regular expressions for syntax highlighting."""
        self.vim.command(r'syntax match deniteSource_Projectile_Project /^.*$/ '
                         r'containedin=' + self.syntax_name + ' '
                         r'contains=deniteSource_Projectile_Project,deniteSource_Projectile_Noise,deniteSource_Projectile_Name,deniteSource_Projectile_Path,deniteSource_Projectile_Timestamp,deniteSource_Projectile_Error')
        self.vim.command(r'syntax match deniteSource_Projectile_Noise     /\(\s--\s\)/                                          contained ')
        self.vim.command(r'syntax match deniteSource_Projectile_Name      /^\(.*\)\(\(.* -- \)\{2\}\)\@=/                       contained ')
        self.vim.command(r'syntax match deniteSource_Projectile_Path      /\(\(.* -- \)\{1\}\)\@<=\(.*\)\(\(.* -- \)\{1\}\)\@=/ contained ')
        self.vim.command(r'syntax match deniteSource_Projectile_Timestamp /\v((-- .*){2})@<=(.*)/                               contained ')
        self.vim.command(r'syntax match deniteSource_Projectile_Error     /^.*✗.*$/                                             contained ')
        self.vim.command(r'syntax match deniteSource_Projectile_Error     /^.*\sX\s.*$/                                         contained ')

    def highlight(self):
        """Link highlight groups to existing attributes."""
        self.vim.command('highlight link deniteSource_Projectile_Project   Normal')
        self.vim.command('highlight link deniteSource_Projectile_Noise     Comment')
        self.vim.command('highlight link deniteSource_Projectile_Name      String')
        self.vim.command('highlight link deniteSource_Projectile_Path      Directory')
        self.vim.command('highlight link deniteSource_Projectile_Timestamp Number')
        self.vim.command('highlight link deniteSource_Projectile_Error     Error')


