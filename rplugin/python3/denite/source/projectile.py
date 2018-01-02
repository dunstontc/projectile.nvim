"""Denite source for project directories."""
# ==============================================================================
#  FILE: projectile.py
#  AUTHOR: Clay Dunston <dunstontc@gmail.com>
#  License: MIT License
#  Last Modified: 2018-01-02
# ==============================================================================

import re
import errno
import datetime
from os import makedirs
from os.path import exists, expanduser, isdir
from json import dump, load, JSONDecodeError
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
        """Parse and accept user settings; gather file information from `context`."""
        context['data_file'] = expand(self.vars['data_dir'] + '/projects.json')
        self._get_icons()

        if not exists(context['data_file']):  # FIXME: Pull `projects.json` creation into its own function
            project_template = [{
                'name': 'MYVIMRC',
                'root': self.vim.eval('$VIMRUNTIME'),
                'timestamp': str(datetime.datetime.now().isoformat()),
                'vcs': False,
                'description': "",
            }]
            if not exists(self.vars['data_dir']):
                try:
                    makedirs(self.vars['data_dir'])
                except OSError as e:
                    if e.errno != errno.EEXIST:
                        raise
            with open(context['data_file'], 'w+') as nf:
                dump(project_template, nf, indent=2)

    def gather_candidates(self, context):
        """Gather candidates from `projectile#data_dir`/projects.json."""
        candidates = []

        with open(context['data_file'], 'r') as fp:
            try:
                config = load(fp)
            except JSONDecodeError:
                err_string = 'Decode error for' + context['data_file']
                error(self.vim, err_string)
                config = []

            for obj in config:
                self._get_pos(obj['root'])
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
        stamp_pat = re.compile(r'(?P<date>\d{4}-\d{2}-\d{2})T(?P<time>\d{2}:\d{2}:\d{2})')
        # 2017-12-12T01:00:10.504356

        name_len   = self._get_length(candidates, 'name')
        path_len   = self._get_length(candidates, 'short_root')
        branch_len = self._get_length(candidates, 'git_branch')
        stat_len   = self._get_length(candidates, 'git_stats')

        for candidate in candidates:

            # if candidate['is_vcs'] is True:
            #     is_vcs = self.vars['icons']['vcs']
            # else:
            #     is_vcs = '  '

            matchez = stamp_pat.search(candidate['timestamp'])
            nice_date = self._maybe(matchez.group('date')) + '  ' + self._maybe(matchez.group('time'))

            if not isdir(candidate['action__path']):
                err_mark = self.vars['icons']['err']
            else:
                err_mark = '  '

            candidate['abbr'] = "{0:<{branch_len}} {1:<{stat_len}}  {2:<{name_len}} -- {err_mark}{3:<{path_len}} -- {4}".format(
                candidate['git_branch'],
                candidate['git_stats'],
                candidate['name'],
                candidate['short_root'],
                nice_date,
                name_len=name_len,
                stat_len=stat_len,
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
        branches   = re.search(r'(?:^\*\s)(?P<brunch>\S+)(.*$)', branch_res, re.M)
        branch     = ''
        if branches and branches.group('brunch') != 'fatal:':
            branch = self._maybe(branches.group('brunch'))

        return branch

    def _get_pos(self, project_root):
        """Return an abbreviated git status summary.

        Parameters
        ----------
        project_root : string
            Path to the root folder of a git repository.

        """
        # pos_pat = re.compile(r'^\*\s(?P<branch>\S+).+(?<=\[)(?P<pos>.*)(?:].+)', re.M)
        # pos_pat = re.compile(r'(?:^\*\s)(?P<branch>\S+)(?:\s+\w+\s)(?=\[)(?P<position>.*)(?<=])', re.M)
        pos_pat = re.compile(r'\*.+(?<=\[)(\w*)', re.M)

        try:
            q = run(f"git -C {project_root} branch -v",
                    stdout=PIPE,
                    stderr=STDOUT,
                    shell=True)
        except CalledProcessError:
            return 'Error running "git branch -v"'

        stat_res = q.stdout.decode('utf-8').split('\n')
        for x in stat_res:
                matches = pos_pat.search(x)
                if matches:
                    pos = self._maybe(matches.group(1))
                    if pos == 'ahead':
                        return self.vars['icons']['ahead']
                    elif pos == 'behind':
                        return self.vars['icons']['behind']
                    else:
                        return ''
                else:
                    return ''

    def _get_stats(self, project_root):
        """Return an abbreviated git status summary.

        Parameters
        ----------
        project_root : string
            Path to the root folder of a git repository.

        Returns
        -------
        string
            Git status information.

        """
        position = self._get_pos(project_root)
        try:
            p = run(f"git -C {project_root} status --porcelain",
                    stdout=PIPE,
                    stderr=STDOUT,
                    shell=True)
        except CalledProcessError:
            return 'Error running "git status"'

        stat_res    = p.stdout.decode('utf-8').split('\n')
        stat_res[:] = [line.rstrip('\n') for line in stat_res]
        statuses      = ['??', 'M', 'A', 'D', 'R', 'C', 'U']
        messages      = []
        for line in stat_res:
            matches = re.search(r'(?:^\s?)(?P<info>\S+)(?:\s)', line)
            if matches and matches.group('info') != 'fatal:' and matches.group('info') != '##':
                for x in statuses:
                    if matches.group('info') == x and self.vars['icons'][x] not in messages:
                        messages.append(self.vars['icons'][x])

        if not len(messages) and not len(position):
            return f'{"".join(messages)}'
        else:
            return f'[{position}{"".join(messages)}]'

    def _maybe(self, please):
        """Something possibly might be something else.

        Used to wrap ``<compiled_regex>.search(...).group('x')`` results.
        Returns an empty string instead of raising an error.

        Parameters
        ----------
        please : obj, str?
            Possible Regular Expression match group

        Returns
        -------
        value : str
            If the match is not None, returns *match*.
            If the match is None, returns ''.

        """
        if please is not None:
            name = please
        else:
            name = ''
        return name

    def _get_icons(self):
        if self.vars['icon_setting'] == 0:
            self.vars['icons'] = {
                'behind': 'Ah',
                'ahead':  'Bh',
                'err':    'X ',
                'vcs':    ' ',
                ' ':      '',
                'M':      'M',
                'A':      'A',
                'D':      'D',
                'R':      'R',
                'C':      'C',
                'U':      'U',
                '??':     '??',
            }
        elif self.vars['icon_setting'] == 2:
            self.vars['icons'] = {
                'behind': '⇣',
                'ahead':  '⇡',
                'err':    '✗ ',
                'vcs':    ' ',  # \ue0a0 -- Powerline branch symbol
                ' ':      '✔',
                'M':      '!',
                'A':      '+',
                'D':      '✘',
                'R':      '»',
                'C':      '»',
                'U':      '⇡',
                '??':     '?',
            }
        else:
            self.vars['icons'] = {
                'behind': '⇣',   # \u21e3 - Downwards Dashed Arrow
                'ahead':  '⇡',   # \u21e1 - Upwards Dashed Arrow
                'err':    '✗ ',  # \u2717 - Ballot x
                'vcs':    '⛕ ',  # \u26d5 - Alternate One-way Left Way Traffic
                ' ':      '✔',   # \u2714 - Heavy Check Mark
                'M':      '!',
                'A':      '+',
                'D':      '✘',   # \u2718 - Heavy Ballot x
                'R':      '»',   # \u00bb - Right-pointing Double Angle Quotation Mark
                'C':      '»',   # \u00bb
                'U':      '⇡',   # \u21e1
                '??':     '?',
            }

    def define_syntax(self):
        """Define Vim regular expressions for syntax highlighting."""
        # self.vim.command(r'syntax match deniteSource_Projectile_Err /^.*✗.*$/')
        # self.vim.command(r'syntax match deniteSource_Projectile_Err /^.*\sX\s.*$/')

        if self.vars['highlight_setting'] == 1:
            items = [x['name'] for x in SYNTAX_GROUPS]
            self.vim.command(f'syntax match {self.syntax_name} /^.*$/ '
                             f"containedin={self.syntax_name} contains={','.join(items)}")
            for pattern in SYNTAX_PATTERNS:
                self.vim.command(f"syntax match {self.syntax_name}_{pattern['name']} {pattern['regex']}")

    def highlight(self):
        """Link highlight groups to existing attributes."""
        # self.vim.command(r'highlight default link deniteSource_Projectile_Err  Error')

        if self.vars['highlight_setting'] == 1:
            for match in SYNTAX_GROUPS:
                self.vim.command(f"highlight default link {match['name']} {match['link']}")


SYNTAX_GROUPS = [
    {'name': 'deniteSource_Projectile_Project',   'link': 'Normal'    },
    {'name': 'deniteSource_Projectile_Noise',     'link': 'Comment'   },
    {'name': 'deniteSource_Projectile_Name',      'link': 'Identifier'},
    {'name': 'deniteSource_Projectile_Path',      'link': 'Directory' },
    {'name': 'deniteSource_Projectile_Timestamp', 'link': 'Number'    },
    {'name': 'deniteSource_Projectile_Err',       'link': 'Error'     },
    {'name': 'deniteSource_Projectile_Stats',     'link': 'Error'     },
    {'name': 'deniteSource_Projectile_Branch',    'link': 'Keyword'   },
]

SYNTAX_PATTERNS = [
    {'name': 'Noise',     'regex': r'/\(\s--\s\)/                        contained'},
    {'name': 'Name',      'regex': r'/^\(.*\)\(\(.* -- \)\{2\}\)\@=/     contained '
                                   r'contains=deniteSource_Projectile_Branch,deniteSource_Projectile_Stats'},
    {'name': 'Path',      'regex': r'/\(.* -- \)\@<=\(.*\)\(.* -- \)\@=/ contained'},
    {'name': 'Timestamp', 'regex': r'/\v((-- .*){2})@<=(.*)/             contained'},
    {'name': 'Branch',    'regex': r'/\v(^\s)@<=(\S+)/                   contained '
                                   r'contains=deniteSource_Projectile_Stats'       },
    {'name': 'Stats',    'regex':  r'/\v\[.+]/                           contained'},
    {'name': 'Err',      'regex':  r'/^.*✗.*$/                           contained'},
    {'name': 'Err',      'regex':  r'/^.*\sX\s.*$/                       contained'},
]
