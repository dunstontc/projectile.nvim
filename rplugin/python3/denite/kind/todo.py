"""Extend denite-kind-file + qflist/loclist interaction."""
#  =============================================================================
#  FILE: todo.py
#  AUTHOR: Clay Dunston <dunstontc@gmail.com>
#  License: MIT
#  Last Modified: 2017-12-31
#  =============================================================================

# import os
# import re
# import json
# import datetime

# from denite import util
from ..kind.file import Kind as File


class Kind(File):
    """Todo kind, extends File kind."""

    def __init__(self, vim):
        """Initialize thyself."""
        super().__init__(vim)
        self.name             = 'todo'
        self.default_action   = 'append'
        self.persist_actions += ['preview', 'highlight', 'delete']
        self.redraw_actions  += ['delete']
        self._previewed_target  = {}
        self._previewed_buffers = {}
        self.vars = {
            'exclude_filetypes': ['denite'],
            'data_dir':          vim.vars.get('projectile#data_dir', '~/.cache/projectile'),
            'has_devicons':      vim.vars.get('loaded_devicons'),
        }

    def action_append(self, context):
        """Append todos to the quickfix or location list."""
        context['current_qf'] = self.vim.call('')
        target = context['targets'][0]
        path = target['action__path']
        self.vim.call('echo', path)
