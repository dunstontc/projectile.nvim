"""Denite source for bookmarked files."""
#  =============================================================================
#  FILE: bookmark.py
#  AUTHOR: Clay Dunston <dunstontc@gmail.com>
#  License: MIT License
#  Last Modified: 2018-01-03
#  =============================================================================

from os.path import exists, expanduser, isfile
import json

from .base import Base
from denite.util import error, expand

SYNTAX_GROUPS = [
    {'name': 'deniteSource_Projectile_Project',   'link': 'Normal'   },
    {'name': 'deniteSource_Projectile_Noise',     'link': 'Comment'  },
    {'name': 'deniteSource_Projectile_Name',      'link': 'String'   },
    {'name': 'deniteSource_Projectile_Path',      'link': 'Directory'},
    {'name': 'deniteSource_Projectile_Timestamp', 'link': 'Number'   },
    {'name': 'deniteSource_Projectile_Err',       'link': 'Error'    },
]

SYNTAX_PATTERNS = [
    {'name': 'Noise',     'regex': r'/\(\s--\s\)/                        contained'},
    {'name': 'Name',      'regex': r'/^\(.*\)\(\(.* -- \)\{2\}\)\@=/     contained'},
    {'name': 'Path',      'regex': r'/\(.* -- \)\@<=\(.*\)\(.* -- \)\@=/ contained'},
    {'name': 'Timestamp', 'regex': r'/\v((-- .*){2})@<=(.*)/             contained'},
    {'name': 'Err',       'regex': r'/^.*✗.*$/                           contained'},
    {'name': 'Err',       'regex': r'/^.*\sX\s.*$/                       contained'},
]


class Source(Base):
    """Denite source for bookmarked files."""

    def __init__(self, vim):
        """Initialize thyself."""
        super().__init__(vim)

        self.name = 'bookmark'
        self.kind = 'bookmark'
        self.syntax_name = 'deniteSource_Projectile'
        self.vars = {
            'highlight_setting': vim.vars.get('projectile#enable_highlighting'),
            'format_setting':    vim.vars.get('projectile#enable_formatting'),
            'icon_setting':      vim.vars.get('projectile#enable_devicons'),
            'data_dir':          vim.vars.get('projectile#data_dir', '~/.cache/projectile'),
        }

    def on_init(self, context):
        """Parse and accept user settings."""
        context['data_file'] = expand(self.vars['data_dir'] + '/bookmarks.json')
        if not exists(context['data_file']):
            error(self.vim, f'Error accessing {context["data_file"]}')
            return

    def gather_candidates(self, context):
        """Gather candidates from ``projectile#data_dir``/projects.json."""
        candidates = []

        with open(context['data_file'], 'r') as fp:
            try:
                config = json.load(fp)
            except json.JSONDecodeError:
                err_string = 'Decode error for' + context['data_file']
                error(self.vim, err_string)
                config = []

            for obj in config:
                candidates.append({
                    'word': obj['path'],
                    'action__path': obj['path'],
                    'action__line': obj['line'],
                    'action__col':  obj['col'],
                    'name':         obj['name'],
                    'short_path':   obj['path'].replace(expanduser('~'), '~'),
                    'timestamp':    obj['timestamp'],
                })

        return self._convert(candidates)

    def _convert(self, candidates):
        """Format and add metadata to gathered candidates.

        Parameters
        ----------
        candidates : list
            Our raw source.

        Returns
        -------
        candidates : list
            A sexy source.
            Aligns candidate properties.
            Adds error mark if a source's path is inaccessible.
            Adds nerdfont icon if ``projectile#enable_devicons`` == ``1``.

        """
        path_len = self._get_length(candidates, 'short_path')
        name_len = self._get_length(candidates, 'name')
        if self.vars['icon_setting'] == 0:
            err_icon = 'X '
        else:
            err_icon = '✗ '

        for candidate in candidates:

            if not isfile(candidate['action__path']):
                err_mark = err_icon
            else:
                err_mark = '  '

            if self.vars['icon_setting'] == 1:
                icon = self.vim.funcs.WebDevIconsGetFileTypeSymbol(candidate['action__path'])
            else:
                icon = '  '

            candidate['abbr'] = "{0} {1:^{name_len}} -- {err_mark} {2:<{path_len}} -- {3}".format(
                icon,
                candidate['name'],
                candidate['short_path'],
                candidate['timestamp'],
                name_len=name_len,
                err_mark=err_mark,
                path_len=(path_len + 3),
            )
        return candidates

    def _get_length(self, array, attribute):
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
        if self.vars['highlight_setting'] == 1:
            items = [x['name'] for x in SYNTAX_GROUPS]
            self.vim.command(f'syntax match {self.syntax_name} /^.*$/ '
                             f'containedin={self.syntax_name} contains={",".join(items)}')
            for pattern in SYNTAX_PATTERNS:
                self.vim.command(f'syntax match {self.syntax_name}_{pattern["name"]} {pattern["regex"]}')

    def highlight(self):
        """Link highlight groups to existing attributes."""
        if self.vars['highlight_setting'] == 1:
            for match in SYNTAX_GROUPS:
                self.vim.command(f'highlight link {match["name"]} {match["link"]}')

