"""Denite source for project directories."""
# ==============================================================================
#  FILE: projectile.py
#  AUTHOR: Clay Dunston <dunstontc@gmail.com>
#  License: MIT License
#  Last Modified: 2017-12-27
# ==============================================================================

from os.path import expanduser, isdir
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
    """Denite source for project directories."""

    def __init__(self, vim):
        """Initialize thyself."""
        super().__init__(vim)

        self.name = 'projectile'
        self.kind = 'projectile'
        self.syntax_name = 'deniteSource_Projectile'
        self.vars = {
            'exclude_filetypes': ['denite'],
            'data_dir':          vim.vars.get('projectile#data_dir', '~/.cache/projectile'),
            'user_cmd':          vim.vars.get('projectile#directory_command'),
            'icon_setting':      vim.vars.get('projectile#enable_devicons'),
        }

    def on_init(self, context):
        """Parse and accept user settings; gather file information from ``context``."""
        context['data_file'] = expand(self.vars['data_dir'] + '/projects.json')

    def gather_candidates(self, context):
        """Gather candidates from ``projectile#data_dir``/projects.json."""
        candidates = []
        with open(context['data_file'], 'r') as fp:
            try:
                config = json.loads(fp.read())

                for obj in config:
                    candidates.append({
                        'word': obj['root'],
                        'action__path': obj['root'],
                        'name':         obj['name'],
                        'is_vsc':       obj['vcs'],
                        'short_root':   obj['root'].replace(expanduser('~'), '~'),
                        'timestamp':    obj['timestamp'],
                    })

            except json.JSONDecodeError:
                err_string = 'Decode error for' + context['data_file']
                error(self.vim, err_string)

        return self._convert(candidates)

    def _convert(self, candidates):
        """Format and add metadata to gathered candidates.

        Parameters
        ----------
        candidates : list

        Returns
        -------
        candidates : list
            A sexy source. Adds error mark if a source's path is inaccessible.

        """
        name_len = self._get_length(candidates, 'name')
        path_len = self._get_length(candidates, 'short_root')

        if self.vars['icon_setting'] == 0:
            err_icon = 'X '
        else:
            err_icon = '✗ '

        if self.vars['icon_setting']   == 0:
            vsc_icon = 'git'
        elif self.vars['icon_setting'] == 1:
            vsc_icon = '  '         # \ue0a0 -- Powerline branch symbol
        elif self.vars['icon_setting'] == 2:
            vsc_icon = '⛕  '

        for candidate in candidates:

            if candidate['is_vsc'] is True:
                is_vsc = vsc_icon
            else:
                is_vsc = '   '

            if not isdir(candidate['action__path']):
                err_mark = err_icon
            else:
                err_mark = '  '

            candidate['abbr'] = "{0}{1:<{name_len}} -- {err_mark}{2:<{path_len}} -- {3}".format(
                is_vsc,
                candidate['name'],
                candidate['short_root'],
                candidate['timestamp'],
                name_len=name_len,
                err_mark=err_mark,
                path_len=(path_len),
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
        items = [x['name'] for x in SYNTAX_GROUPS]
        self.vim.command(f'syntax match {self.syntax_name} /^.*$/ '
                         f"containedin={self.syntax_name} contains={','.join(items)}")
        for pattern in SYNTAX_PATTERNS:
            self.vim.command(f"syntax match {self.syntax_name}_{pattern['name']} {pattern['regex']}")

    def highlight(self):
        """Link highlight groups to existing attributes."""
        for match in SYNTAX_GROUPS:
            self.vim.command(f"highlight default link {match['name']} {match['link']}")

