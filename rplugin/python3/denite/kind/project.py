"""Kind to model data; Create, Read, Update, & Delete said data. (currently files & folders in JSON)."""
#  =============================================================================
#  FILE: project.py
#  AUTHOR: Clay Dunston <dunstontc@gmail.com>
#  License: MIT
#  Last Modified: 2017-12-25
#  =============================================================================

# import re
import os
import json
import datetime
import subprocess  # TODO: Use denite's proc

from ..kind.openable import Kind as Openable
from denite import util


class Kind(Openable):

    def __init__(self, vim):
        super().__init__(vim)
        self.name             = 'project'
        self.default_action   = 'open'
        self.persist_actions += ['delete']
        self.redraw_actions  += ['delete']
        self.vars = {
            'exclude_filetypes': ['denite'],
            'date_format':       '%d %b %Y %H:%M:%S',
            'data_dir':          vim.vars.get('projectile#data_dir', '~/.cache/projectile'),
            'user_cmd':          vim.vars.get('projectile#directory_command'),
            'has_nerdtree':      vim.vars.get('loaded_nerdtree'),
            'has_vimfiler':      vim.vars.get('loaded_vimfiler'),
        }

    def action_add(self, context):
        """Add a project to ``projectile#data_dir``/projects.json."""
        data_file = util.expand(self.vars['data_dir'] + '/projects.json')
        root_dir  = self.vim.call('getcwd')
        boofer    = self.vim.current.buffer.name
        pj_root   = util.path2project(self.vim, boofer, '.git')
        pj_name   = os.path.basename(os.path.normpath(pj_root))
        new_data  = {}

        project_root = util.input(self.vim, context, 'Project Root: ', pj_root)
        if not len(project_root):
            project_root = pj_root

        project_name = util.input(self.vim, context, 'Project Name: ', pj_name)
        if not len(project_name):
            project_name = pj_name

        new_data = {
            'name': project_name,
            'root': project_root,
            'timestamp': str(datetime.datetime.now().isoformat()),
            'description': '',
            'vcs': os.path.isdir(f"{root_dir}/.git")  # TODO: Also check for .hg/ and .svn
        }

        with open(data_file, 'r') as g:
            try:
                json_info = json.load(g)
            except json.JSONDecodeError:
                json_info = []
            json_info.append(new_data)

        with open(data_file, 'w') as f:
            json.dump(json_info, f, indent=2)

    def action_delete(self, context):
        """Remove a project from *projects.json*."""
        target       = context['targets'][0]
        target_date  = target['timestamp']
        target_name  = target['name']
        data_file    = util.expand(self.vars['data_dir'] + '/projects.json')
        confirmation = self.vim.call('confirm', f"Remove {target_name}?", "&Yes\n&No")
        if confirmation == 2:
            return
        else:
            with open(data_file, 'r') as g:
                content  = json.load(g)
                projects = content[:]
                for i in range(len(projects)):
                    if projects[i]['timestamp'] == target_date:
                        projects.pop(i)
                        break

                with open(data_file, 'w') as f:
                    json.dump(projects, f, indent=2)

    def action_cd(self, context):
        """Change cwd to the project's root."""
        target = context['targets'][0]
        if not os.access(target['action__path']):
            return
        self.vim.command('lcd {}'.format(target['action__path']))

    def action_narrow(self, context):
        """Traverse the path of a target."""
        target = context['targets'][0]
        context['sources_queue'].append([
            {'name': 'file', 'args': []},
            {'name': 'file', 'args': ['new']},
        ])
        context['path'] = target['action__path']

    def action_open(self, context):
        """Open the target's action__path."""
        for target in context['targets']:
            path = target['action__path']
            match_path = '^{0}$'.format(path)

            if self.vim.call('bufwinnr', match_path) <= 0:
                self.vim.call(
                    'denite#util#execute_path', 'edit', path)
            elif self.vim.call('bufwinnr',
                               match_path) != self.vim.current.buffer:
                self.vim.call(
                    'denite#util#execute_path', 'buffer', path)

    def __winid(self, target):
        """Needed for openable actions."""
        path = target['action__path']
        bufnr = self.vim.call('bufnr', path)
        if bufnr == -1:
            return None
        winids = self.vim.call('win_findbuf', bufnr)
        return None if len(winids) == 0 else winids[0]

    def __git_do(location, command):
        """Run git commands from Python scripts.

        Arguments
        ---------
        location : str
            The target directory
        command : str
            The git command to execute

        Returns
        -------
        list    : The utf-8 decoded search results, split by newline

        """
        # cmd = f"git -C {location} {command}"
        cmd = f"git -C {location} status -s"
        try:
            p = subprocess.run(cmd,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               shell=True)
        except subprocess.CalledProcessError:
            return []
        return p.stdout.decode('utf-8').split('\n')

    def __get_length(array):
        """Get the max string length for an attribute in a collection."""
        max_count = int(0)
        for item in array:
            cur_len = len(item)
            if cur_len > max_count:
                max_count = cur_len
        return max_count
