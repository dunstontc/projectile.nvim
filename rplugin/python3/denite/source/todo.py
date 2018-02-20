"""Denite source for TODOS in the current directory."""
# ==============================================================================
#  FILE: todo.py
#  AUTHOR: Clay Dunston <dunstontc@gmail.com>
#  License: MIT license
#  Last Modified: 2018-01-08
# ==============================================================================

import re
import subprocess
from os.path import basename, expanduser

from .base import Base
from denite.util import error


class Source(Base):
    """Denite source for TODOS in the current directory."""

    def __init__(self, vim):
        """Initialize thyself."""
        super().__init__(vim)
        self.name        = 'todo'
        self.syntax_name = 'deniteSource_Todo'
        self.kind        = 'todo'
        self.matchers    = ['matcher_fuzzy']
        self.vars = {
            'data_dir':     vim.vars.get('projectile#data_dir', '~/.cache/projectile'),
            'highlight_setting': vim.vars.get('projectile#enable_highlighting'),
            'format_setting': vim.vars.get('projectile#enable_formatting'),
            'icon_setting': vim.vars.get('projectile#enable_devicons'),
            'search_prog': vim.vars.get('projectile#search_prog'),
            'todo_terms': vim.vars.get('projectile#todo_terms'),
            'encoding': 'utf-8',

            'ack_options'  : ['-r'],
            'ag_options'   : ['-s', '--nocolor', '--nogroup', '--vimgrep'],
            'grep_options' : ['-E', '-r', '-n'],
            'pt_options'   : ['--nogroup', '--nocolor', '--column'],
        }

    def on_init(self, context):
        """Parse user options and set up our search."""
        context['__bufnr']         = self.vim.current.buffer.number
        context['__bufname']       = self.vim.current.buffer.name
        context['__filename']      = basename(context['__bufname'])
        context['__winnr']         = self.vim.eval('bufwinnr("' + context['__bufname'] + '")')

        context['path_pattern']    = re.compile(r'(^.*?)(?:\:.*$)')
        context['line_pattern']    = re.compile(r'(?:\:)(\d*)(?:\:)(\d*)')
        context['terms']           = '|'.join(self.vars.get('todo_terms'))
        context['content_pattern'] = re.compile("({})+(.*$)".format(context['terms']))

        if self.vim.call('getcwd') == expanduser("~"):
            context['todos']       = []
            context['is_async']    = True  # FIXME:
            error(self.vim, 'You might not want to search in \'~\'...')
        else:
            context['searcher']   = self.vars['search_prog']
            context['options']    = self.vars["{}_options".format(context['searcher'])]
            context['terms']      = "\s({})\:\s".format(context['terms'])
            context['search_dir'] = self.vim.call('getcwd')

            context['todos'] = self._run_search(
                context['searcher'],
                context['options'],
                context['terms'],
                context['search_dir']
            )

    def gather_candidates(self, context):
        """Parse segments out of our search results."""
        cur_dir_len = len(self.vim.call('getcwd'))
        candidates  = []

        for item in context['todos']:
            todo_path    = ''
            todo_line    = ''
            todo_col     = ''
            todo_content = ''

            if context['path_pattern'].search(item):
                todo_path = context['path_pattern'].search(item).group(1)

            if context['line_pattern'].search(item):
                todo_line = context['line_pattern'].search(item).group(1)
                todo_col  = context['line_pattern'].search(item).group(2)

            if context['content_pattern'].search(item):
                todo_content = context['content_pattern'].search(item).group(0)

            # if item:
                candidates.append({
                    'word':         item,
                    'action__path': todo_path,
                    'action__line': todo_line,
                    'action__col':  todo_col,
                    'action__text': todo_content,
                    'short_path':   todo_path[cur_dir_len:],
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
            Adds nerdfont icon if ``projectile#enable_devicons`` == ``1``.

        """
        cur_dir_len = len(self.vim.call('getcwd'))
        path_len = self._get_length(candidates, 'short_path')

        for candidate in candidates:

            todo_pos = "[{}:{}]".format(candidate['action__line'], candidate['action__col'])

            if self.vars['icon_setting'] == 1:
                icon = self.vim.funcs.WebDevIconsGetFileTypeSymbol(candidate['action__path'])
            else:
                icon = '  '

            candidate['abbr'] = "{0:<{path_len}} {1} {2:<8} -- {3} ".format(
                candidate['action__path'][cur_dir_len:],
                icon,
                todo_pos,
                candidate['action__text'],
                path_len=path_len
            )
        return candidates

    def _get_length(self, array, attribute):
        """Get the max string length for an attribute in a collection."""
        max_count = int(0)
        for item in array:
            cur_attr = item[attribute]
            cur_len = len(cur_attr)
            if type(item[attribute]) is int:
                cur_len = len(str(cur_attr))
            if cur_len > max_count:
                max_count = cur_len
        return max_count

    def _run_search(self, command, options, pattern, location):
        """Based off of a script by @chemzqm in denite-git."""
        try:
            p = subprocess.run("{} {} \"{}\" {}".format(command, ' '.join(options), pattern, location),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               shell=True)
        except subprocess.CalledProcessError:
            return []
        return p.stdout.decode('utf-8').split('\n')

    def define_syntax(self):
        """Define Vim regular expressions for syntax highlighting."""
        if self.vars['highlight_setting'] == 1:
            items = [x['name'] for x in SYNTAX_GROUPS]
            self.vim.command('syntax match {} /^.*$/ containedin={} contains={}'.format(self.syntax_name, self.syntax_name, ",".join(items)))
            for pattern in SYNTAX_PATTERNS:
                self.vim.command('syntax match {}_{} {}'.format(self.syntax_name, pattern["name"], pattern["regex"]))

    def highlight(self):
        """Link highlight groups to existing attributes."""
        if self.vars['highlight_setting'] == 1:
            for match in SYNTAX_GROUPS:
                self.vim.command('highlight link {} {}'.format(match["name"], match["link"]))


SYNTAX_GROUPS = [
    {'name': 'deniteSource_Todo',        'link': 'Normal'   },
    {'name': 'deniteSource_Todo_Noise',  'link': 'Comment'  },
    {'name': 'deniteSource_Todo_Path',   'link': 'Directory'},
    {'name': 'deniteSource_Todo_Pos',    'link': 'Number'   },
    {'name': 'deniteSource_Todo_Word',   'link': 'Type'     },
    {'name': 'deniteSource_Todo_String', 'link': 'String'   },
]

SYNTAX_PATTERNS = [
    {'name': 'Word',   'regex': r'/\v(BUG|FIXME|HACK|NOTE|OPTIMIZE|TODO|XXX)\:/ contained'},
    {'name': 'Path',   'regex': r'/\%(^\s\)\@<=\(.*\)\%(\[\)\@=/                contained'},
    {'name': 'Noise',  'regex': r'/\S*\%\(--\)\s/                               contained'},
    {'name': 'Noise',  'regex': r'/\[\|\]\|:/                                   contained'},
    {'name': 'Pos',    'regex': r'/\d\+\(:\d\+\)\?/                             contained contains=deniteSource_Todo_Noise'},
    {'name': 'String', 'regex': r'/\s`\S\+`/                                    contained'},
]
