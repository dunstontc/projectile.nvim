"""Denite source for project directories."""
# ==============================================================================
#  FILE: projectile.py
#  AUTHOR: Clay Dunston <dunstontc@gmail.com>
#  License: MIT License
#  Last Modified: 2017-12-29
# ==============================================================================

from os.path import expanduser, isdir
import re
import json
from subprocess import run, PIPE, STDOUT, CalledProcessError

from .base import Base
from denite.util import error, expand


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
            'format_setting':    vim.vars.get('projectile#enable_formatting'),
            'highlight_setting': vim.vars.get('projectile#enable_highlighting'),
        }

    def on_init(self, context):
        """Parse and accept user settings; gather file information from ``context``."""
        context['data_file'] = expand(self.vars['data_dir'] + '/projects.json')
        if self.vars['icon_setting'] == 0:
            self.vars['icons'] = {
                'err': 'X ',
                'vcs': ' ',
                ' ':   '',
                'M':   'M',
                'A':   'A',
                'D':   'D',
                'R':   'R',
                'C':   'C',
                'U':   'U',
                '??':  '??',
            }
        elif self.vars['icon_setting'] == 2:
            self.vars['icons'] = {
                'err': '✗ ',
                'vcs': ' ',  # \ue0a0 -- Powerline branch symbol
                ' ':   '✔',
                'M':   '!',
                'A':   '+',
                'D':   '✘',
                'R':   '»',
                'C':   '»',
                'U':   '⇡',
                '??':  '?',
            }
        else:
            self.vars['icons'] = {
                'err': '✗ ',
                'vcs': '⛕ ',
                ' ':   '✔',
                'M':   '!',
                'A':   '+',
                'D':   '✘',
                'R':   '»',
                'C':   '»',
                'U':   '⇡',
                '??':  '?',
            }

    def gather_candidates(self, context):
        """Gather candidates from ``projectile#data_dir``/projects.json."""
        candidates = []
        with open(context['data_file'], 'r') as fp:
            try:
                config = json.loads(fp.read())

                for obj in config:
                    candidates.append({
                        'word':         obj['root'],
                        'action__path': obj['root'],
                        'name':         obj['name'],
                        'is_vcs':       obj['vcs'],
                        'timestamp':    obj['timestamp'],
                        'git_branch':   self._get_branch(obj['root']),
                        'git_stats':    self._get_stats(obj['root']),
                        'short_root':   obj['root'].replace(expanduser('~'), '~'),
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
        name_len   = self._get_length(candidates, 'name')
        path_len   = self._get_length(candidates, 'short_root')
        branch_len = self._get_length(candidates, 'git_branch')
        stats_len  = self._get_length(candidates, 'git_stats')

        for candidate in candidates:

            # if candidate['is_vcs'] is True:
            #     is_vcs = self.vars['icons']['vcs']
            # else:
            #     is_vcs = '  '

            if not isdir(candidate['action__path']):
                err_mark = self.vars['icons']['err']
            else:
                err_mark = '  '

            candidate['abbr'] = "{0:>{branch_len}} {1:^{stats_len}}  {2:<{name_len}} -- {err_mark}{3:<{path_len}} -- {4}".format(
                candidate['git_branch'],
                candidate['git_stats'],
                candidate['name'],
                candidate['short_root'],
                candidate['timestamp'],
                name_len=name_len,
                stats_len=stats_len,
                branch_len=branch_len,
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

    def _get_branch(self, project_root):
        """Return the current branch of a git repository.

        Parameters
        ----------
        project_root : string
            Path to the root folder of a git repository.
            TODO: expand the root by default.

        Returns
        -------
        string
            Git branch

        """
        try:
            q = run(f"git -C {project_root} branch",
                    stdout=PIPE,
                    stderr=STDOUT,
                    shell=True)
        except CalledProcessError:
            return 'Error running "git branch"'

        branch_res = q.stdout.decode('utf-8')
        branches   = re.search(r'(?:\*?\s?)(?P<brunch>\S+)', branch_res)
        branch     = ''
        if branches and branches.group('brunch') != 'fatal:':
            branch = self._maybe(branches.group('brunch'))

        return branch

    def _get_stats(self, project_root):
        """Return an abbreviated git status summary.

        Parameters
        ----------
        project_root : string
            Path to the root folder of a git repository.

        Returns
        -------
        string
            Git status information [<info>]``

        TODO
        ----
        - Ahead/Behind
        - Diverged
        - Stashed
        - Unmerged

        Notes
        -----
        - ' ' = unmodified
        - M   = modified
        - A   = added
        - D   = deleted
        - R   = renamed
        - C   = copied
        - U   = updated but unmerged

        """
        try:
            p = run(f"git -C {project_root} status --porcelain",
                    stdout=PIPE,
                    stderr=STDOUT,
                    shell=True)
        except CalledProcessError:
            return 'Error running "git status"'

        status_res    = p.stdout.decode('utf-8').split('\n')
        status_res[:] = [line.rstrip('\n') for line in status_res]
        statuses      = ['??', 'M', 'A', 'D', 'R', 'C', 'U']
        messages      = []
        for line in status_res:
            matches = re.search(r'(?:^\s?)(?P<info>\S+)(?:\s)', line)
            if matches and matches.group('info') != 'fatal:' and matches.group('info') != '##':
                for x in statuses:
                    if matches.group('info') == x and self.vars['icons'][x] not in messages:
                        messages.append(self.vars['icons'][x])

        if not len(messages):
            return f'{"".join(messages)}'
        else:
            return f'[{"".join(messages)}]'

    def _maybe(self, match):
        """Something possibly might be something else.

        Used to wrap re.search().group(x) results.
        Returns an empty string instead of raising an error.

        Parameters
        ----------
        match : obj, str?
            Possible Regular Expression match group

        Returns
        -------
        value : str
            If the match is not None, returns *match*.
            If the match is None, returns ''.

        """
        if match is not None:
            name = match
        else:
            name = ''

        return name

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


SYNTAX_GROUPS = [
    {'name': 'deniteSource_Projectile_Project',   'link': 'Normal'    },
    {'name': 'deniteSource_Projectile_Noise',     'link': 'Comment'   },
    {'name': 'deniteSource_Projectile_Name',      'link': 'Identifier'},
    {'name': 'deniteSource_Projectile_Path',      'link': 'Directory' },
    {'name': 'deniteSource_Projectile_Timestamp', 'link': 'Number'    },
    {'name': 'deniteSource_Projectile_Err',       'link': 'Error'     },
    {'name': 'deniteSource_Projectile_Stats',     'link': 'WarningMsg'     },
    {'name': 'deniteSource_Projectile_Branch',    'link': 'Keyword'   },
]

SYNTAX_PATTERNS = [
    {'name': 'Noise',     'regex': r'/\(\s--\s\)/                        contained'},
    {'name': 'Name',      'regex': r'/^\(.*\)\(\(.* -- \)\{2\}\)\@=/     contained '
                                   r'contains=deniteSource_Projectile_Branch,deniteSource_Projectile_Stats'},
    {'name': 'Path',      'regex': r'/\(.* -- \)\@<=\(.*\)\(.* -- \)\@=/ contained'},
    {'name': 'Timestamp', 'regex': r'/\v((-- .*){2})@<=(.*)/             contained'},
    {'name': 'Branch',    'regex': r'/\v(\S+)(\s\[.*]\s)@=/              contained '
                                   r'contains=deniteSource_Projectile_Stats'},
    {'name': 'Stats',    'regex': r'/\v\[.+]/                            contained'},
    {'name': 'Err',       'regex': r'/^.*✗.*$/                           contained'},
    {'name': 'Err',       'regex': r'/^.*\sX\s.*$/                       contained'},
]
