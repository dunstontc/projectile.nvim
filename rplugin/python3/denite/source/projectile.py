"""Denite source for project directories."""
#  =============================================================================
#  FILE: projectile.py
#  AUTHOR: Clay Dunston <dunstontc@gmail.com>
#  License: MIT
#  Last Modified: 2017-12-25
#  ============================================================================

import os
import json
# import pathlib
# import subprocess  # TODO: Use denite's util.proc

from .base import Base
from denite import util


class Source(Base):
    """Denite source for project directories."""

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'projectile'
        self.kind = 'project'
        self.vars = {
            'exclude_filetypes': ['denite'],
            'data_dir':          vim.vars.get('projectile#data_dir', '~/.cache/projectile'),
            'user_cmd':          vim.vars.get('projectile#directory_command'),
            'icon_setting':      vim.vars.get('projectile#enable_devicons'),
        }

    def on_init(self, context):
        """Parse and accept user settings; gather file information from ``context``."""
        context['data_file'] = util.expand(self.vars['data_dir'] + '/projects.json')
        # if not os.path.exists(context['data_file']):
        #         pathlib.Path(self.vars['data_dir']).mkdir(parents=True, exist_ok=True)
        #         with open(context['data_file'], 'w+') as f:
        #             json.dump([], f, indent=2)

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
                        'short_root':   obj['root'].replace(os.path.expanduser('~'), '~'),
                        'timestamp':    obj['timestamp'],
                    })

            except json.JSONDecodeError:
                err_string = 'Decode error for' + context['data_file']
                util.error(self.vim, err_string)

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
        name_len = self._get_length(candidates, 'name')
        path_len = self._get_length(candidates, 'short_root')

        if self.vars['icon_setting'] == 0:
            vsc_icon = 'git'
        elif self.vars['icon_setting'] == 1:
            vsc_icon = '  '        # \ue0a0 -- Powerline branch symbol
        elif self.vars['icon_setting'] == 2:
            vsc_icon = '⛕  '

        for candidate in candidates:

            if candidate['is_vsc'] is True:
                is_vsc = vsc_icon
            else:
                is_vsc = '   '

            candidate['abbr'] = "{0}{1:<{name_len}} -- {2:<{path_len}} -- {3}".format(
                is_vsc,
                candidate['name'],
                candidate['short_root'],
                candidate['timestamp'],
                name_len=name_len,
                path_len=path_len,
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
        self.vim.command(r'syntax match deniteSource_Projectile_Project /^.*$/ '
                         r'containedin=' + self.syntax_name + ' '
                         r'contains=deniteSource_Projectile_Project,deniteSource_Projectile_Noise,deniteSource_Projectile_Name,deniteSource_Projectile_Description,deniteSource_Projectile_Path,deniteSource_Projectile_Timestamp')
        self.vim.command(r'syntax match deniteSource_Projectile_Noise       /\(\s--\s\)/                                          contained ')
        self.vim.command(r'syntax match deniteSource_Projectile_Name        /^\(.*\)\(\(.* -- \)\{2\}\)\@=/                       contained ')
        self.vim.command(r'syntax match deniteSource_Projectile_Description /\(\(.* -- \)\{1\}\)\@<=\(.*\)\(\(.* -- \)\{2\}\)\@=/ contained ')
        self.vim.command(r'syntax match deniteSource_Projectile_Path        /\(\(.* -- \)\{1\}\)\@<=\(.*\)\(\(.* -- \)\{1\}\)\@=/ contained ')
        self.vim.command(r'syntax match deniteSource_Projectile_Timestamp   /\(\%(.* -- \)\{2}\)\@<=\(.*\)/                       contained ')

    def highlight(self):
        """Link highlight groups to existing attributes."""
        self.vim.command('highlight link deniteSource_Projectile_Project     Normal')
        self.vim.command('highlight link deniteSource_Projectile_Noise       Comment')
        self.vim.command('highlight link deniteSource_Projectile_Name        Identifier')
        self.vim.command('highlight link deniteSource_Projectile_Description String')
        self.vim.command('highlight link deniteSource_Projectile_Path        Directory')
        self.vim.command('highlight link deniteSource_Projectile_Timestamp   Number')
