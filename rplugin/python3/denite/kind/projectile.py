"""Kind using JSON to persist data for projects."""
#  =============================================================================
#  FILE: projectile.py
#  AUTHOR: Clay Dunston <dunstontc@gmail.com>
#  License: MIT
#  Last Modified: 2017-12-29
#  =============================================================================

import json
import datetime
from os.path import basename, isdir, normpath

from ..kind.directory import Kind as Directory
from denite.util import expand, input, path2project


class Kind(Directory):
    """Kind using JSON to persist data for projects."""

    def __init__(self, vim):
        """Initialize thyself."""
        super().__init__(vim)
        self.name             = 'projectile'
        self.default_action   = 'open'
        self.persist_actions += ['delete']
        self.redraw_actions  += ['delete']
        self.vars = {
            'exclude_filetypes': ['denite'],
            'date_format':       '%d %b %Y %H:%M:%S',
            'data_dir':          vim.vars.get('projectile#data_dir', '~/.cache/projectile'),
            'user_cmd':          vim.vars.get('projectile#directory_command'),
        }

    def action_add(self, context):
        """Add a project to ``projectile#data_dir``/projects.json."""
        data_file = expand(self.vars['data_dir'] + '/projects.json')
        root_dir  = self.vim.call('getcwd')
        boofer    = self.vim.current.buffer.name
        pj_root   = path2project(self.vim, boofer, '.git')
        pj_name   = basename(normpath(pj_root))
        new_data  = {}

        project_root = input(self.vim, context, 'Project Root: ', pj_root)
        if not len(project_root):
            project_root = pj_root

        project_name = input(self.vim, context, 'Project Name: ', pj_name)
        if not len(project_name):
            project_name = pj_name

        new_data = {
            'name':        project_name,
            'root':        project_root,
            'timestamp':   str(datetime.datetime.now().isoformat()),
            'description': '',
            'vcs':         isdir(f"{root_dir}/.git")  # TODO: Also check for .hg/ and .svn
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
        data_file    = expand(self.vars['data_dir'] + '/projects.json')
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

    def action_custom(self, context):
        """Execute a custom action defined by ``g:projectile#directory_command``."""
        target   = context['targets'][0]
        user_cmd = self.vim.vars.get('projectile#directory_command')
        if not isdir(target['action__path']):
            return
        destination = expand(target['action__path'])
        self.vim.call('execute', f'{user_cmd} {destination}')


