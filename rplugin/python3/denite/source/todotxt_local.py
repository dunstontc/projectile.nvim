"""Denite source for *.todo.txt files."""
#  =============================================================================
#  FILE: todotxt_local.py
#  AUTHOR: Clay Dunston <dunstontc@gmail.com>
#  License: MIT License
#  Last Modified: 2018-01-01
#  =============================================================================

import re
import fnmatch
from os import listdir
from os.path import isfile

from .base import Base
from denite.util import error, expand, path2project


class Source(Base):
    """Denite source for todo.txt files."""

    def __init__(self, vim):
        """Initialize thyself."""
        super().__init__(vim)

        self.name = 'todotxt_local'
        self.kind = 'word'
        self.syntax_name = 'deniteSource_Todo'
        self.vars = {
            'data_dir':          vim.vars.get('projectile#data_dir', '~/.cache/projectile'),
            'icon_setting':      vim.vars.get('projectile#enable_devicons'),
            'highlight_setting': vim.vars.get('projectile#enable_highlighting'),
            'format_setting':    vim.vars.get('projectile#enable_formatting'),
            'TODOTXT_CFG_FILE':  vim.call('expand', r'$TODOTXT_CFG_FILE'),
            'TODO_FILE':         vim.call('expand', r'$TODO_FILE'),
            'DONE_FILE':         vim.call('expand', r'$DONE_FILE'),
            'TODO_DIR':          vim.call('expand', r'$TODO_DIR'),
        }

    def on_init(self, context):
        """Check for local *todo.txt files."""
        boofer  = self.vim.current.buffer.name
        context['cur_pj_root'] = path2project(self.vim, boofer, ['.git', '.svn', '.hg'])
        for file in listdir(context['cur_pj_root']):
            if fnmatch.fnmatch(file, '*todo.txt'):
                context['TODO_FILE'] = expand(context['cur_pj_root'] + '/' + file)


    def gather_candidates(self, context):
        """Gather candidates from todo.txt files."""
        candidates = []
        linenr = int(0)

        try:
            with open(context['TODO_FILE'], 'r') as f:
                todos = f.read().split('\n')
                for x in todos:
                    if len(x) > 1:
                        # linenr += 1
                        candidates.append({
                            'word': x,
                            'action__line': str(linenr),
                            # 'action__path': obj['path'],
                            # 'action__line': obj['line'],
                            # 'short_path':   obj['path'].replace(expanduser('~'), '~'),
                        })
        except KeyError:
            error(self.vim, f'Error accessing todo file in {context["cur_pj_root"]}')


        # return self._convert(candidates).append({})
        return candidates

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
        # path_len = self._get_length(candidates, 'short_path')
        # name_len = self._get_length(candidates, 'name')
        # PRJ_CON_PATTERN = r'\B(?:\+|@)(?:\S*\w)'
        # TAG_PATTERN     = r'\b\S+:[^/\s]\S*\b'
        # URL_PATTERN     = r'(?:^|\s)(?:\w+:){1}(?://\S+)'
        # BASIC_PRIORITY  = r'(?:^)(\([a-zA-Z]\))'
        TODO_PATTERN = re.compile(
            '''
            (?P<done>x\s)?                           # Optional done mark
            ((?P<done_date>\d{4}-\d{2}-\d{2})(\s))?  # Done date
            ((?P<priority>\([a-zA-Z]\))(\s))?        # Priority
            (?P<date>\d{4}-\d{2}-\d{2})              # Date added
            \s                                       # Single space
            (?P<content>.*)                          # Contents of the TODO
            ''', re.X)

        for candidate in candidates:

            matches = TODO_PATTERN.search(candidate['word'])
            if matches:
                date = self._maybe(matches.group('date'))
                done = self._maybe(matches.group('done'))
                priority = self._maybe(matches.group('priority'))
                done_date = self._maybe(matches.group('done_date'))
                content = self._maybe(matches.group('content'))

            # if not isfile(candidate['action__path']):
            #     err_mark = err_icon
            # else:
            #     err_mark = '  '

            # if self.vars['icon_setting'] == 1:
            #     icon = self.vim.funcs.WebDevIconsGetFileTypeSymbol(candidate['action__path'])
            # else:
            #     icon = '  '

            # candidate['abbr'] = f" -- {priority} -- {date} -- {content}"
            candidate['abbr'] = f" {done}{done_date} {priority} -- {date} -- {content}"
            # candidate['abbr'] = candidate['word']
        return candidates

    def _maybe(self, match):
        """Something possibly might be something else.

        Parameters
        ----------
        match : obj, str?
            Possible Regular Expression match group

        Returns
        -------
        value : str
            If the match is not None, returns *name* = *match*.
            If the match is None, returns *name* = ''.

        """
        if match is not None:
            name = match
        else:
            name = ''

        return name

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
                         f'containedin={self.syntax_name} contains={",".join(items)}')
        for pattern in SYNTAX_PATTERNS:
            self.vim.command(f'syntax match {self.syntax_name}_{pattern["name"]} {pattern["regex"]}')
            self.vim.command(r'syntax cluster TodoData  contains=deniteSource_Todo_Date,deniteSource_Todo_Project,deniteSource_Todo_Context,deniteSource_Todo_Extra,deniteSource_Todo_ID,deniteSource_Todo_String')
            # self.vim.command(r'syntax cluster todoPriority   contains=todoPriorityA,todoPriorityB,todoPriorityC,todoPriorityD,todoPriorityE,todoPriorityF')

    def highlight(self):
        """Link highlight groups to existing attributes."""
        for match in SYNTAX_GROUPS:
            self.vim.command(f'highlight link {match["name"]} {match["link"]}')


SYNTAX_GROUPS = [
    {'name': 'deniteSource_Todo',           'link': 'Normal'        },
    {'name': 'deniteSource_Todo_Noise',     'link': 'Comment'       },
    {'name': 'deniteSource_Todo_Done',      'link': 'todoDone'      },
    {'name': 'deniteSource_Todo_ID',        'link': 'todoID'        },
    {'name': 'deniteSource_Todo_Context',   'link': 'todoContext'   },
    {'name': 'deniteSource_Todo_Project',   'link': 'todoProject'   },
    {'name': 'deniteSource_Todo_Date',      'link': 'Comment'       },
    {'name': 'deniteSource_Todo_String',    'link': 'String'        },
    {'name': 'deniteSource_Todo_Extra',     'link': 'todoExtra'     },
    {'name': 'deniteSource_Todo_PriorityA', 'link': 'todoPriorityA' },
    {'name': 'deniteSource_Todo_PriorityB', 'link': 'todoPriorityB' },
    {'name': 'deniteSource_Todo_PriorityC', 'link': 'todoPriorityC' },
    {'name': 'deniteSource_Todo_PriorityD', 'link': 'todoPriorityD' },
    {'name': 'deniteSource_Todo_PriorityE', 'link': 'todoPriorityE' },
    {'name': 'deniteSource_Todo_PriorityF', 'link': 'todoPriorityF' },
]

SYNTAX_PATTERNS = [
    {'name': 'Done',      'regex': r'/^\s[xX]\s.\+$/              contained'},
    {'name': 'ID',        'regex': r'/id\:\d\+/                   contained'},
    {'name': 'Context',   'regex': r'/\(^\|\W\)@[^[:blank:]]\+/   contained'},
    {'name': 'Project',   'regex': r'/+\w\+/                      contained'},
    {'name': 'Date',      'regex': r'/\d\{4\}-\d\{2\}-\d\{2\}/    contained'},
    {'name': 'String',    'regex': r'/\s`\S\+`/                   contained'},
    {'name': 'Extra',     'regex': r'/\(due\|t\|rec\|link\)\:\S*/ contained'},
    {'name': 'PriorityA', 'regex': r'/^\s([aA])\s.\+$/            contained contains=@TodoData '},
    {'name': 'PriorityB', 'regex': r'/^\s([bB])\s.\+$/            contained contains=@TodoData '},
    {'name': 'PriorityC', 'regex': r'/^\s([cC])\s.\+$/            contained contains=@TodoData '},
    {'name': 'PriorityD', 'regex': r'/^\s([dD])\s.\+$/            contained contains=@TodoData '},
    {'name': 'PriorityE', 'regex': r'/^\s([eE])\s.\+$/            contained contains=@TodoData '},
    {'name': 'PriorityF', 'regex': r'/^\s([fF])\s.\+$/            contained contains=@TodoData '},
]
