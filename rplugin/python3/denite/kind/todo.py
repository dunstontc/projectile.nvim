"""Extend denite-kind-file + qflist/loclist interaction."""
#  =============================================================================
#  FILE: todo.py
#  AUTHOR: Clay Dunston <dunstontc@gmail.com>
#  License: MIT
#  Last Modified: 2018-01-08
#  =============================================================================

from ..kind.file import Kind as File


class Kind(File):
    """Todo kind, extends File kind."""

    def __init__(self, vim):
        """Initialize thyself."""
        super().__init__(vim)
        self.name             = 'todo'
        self.default_action   = 'open'
        self.persist_actions += ['preview', 'highlight']
        # self.redraw_actions  += ['delete']
        self._previewed_target  = {}
        self._previewed_buffers = {}
        self.vars = {
            'exclude_filetypes': ['denite'],
            'data_dir':          vim.vars.get('projectile#data_dir', '~/.cache/projectile'),
        }

    def action_add_to_quickfix(self, context):
        """Append selected todos to the quickfix list."""
        qf_list = self.vim.eval('getqflist()')

        todos = [{
            'filename': x['action__path'],
            'lnum':     x['action__line'],
            'text':     x['action__text'],
        } for x in context['targets']
            if 'action__line' in x and 'action__text' in x]

        for item in todos:
            qf_list.append(item)

        self.vim.call('setqflist', qf_list)

    # def action_add_to_loclist(self, context):
    #     """Append todos to the quickfix or location list."""
    #     # winnr    = self.vim.eval(f'bufwinnr(\"{context["__bufname"]}\")')
    #     loc_list = self.vim.eval(f'getloclist({context["__winnr"]})')
    #
    #     todos = [{
    #         'filename': x['action__path'],
    #         'lnum':     x['action__line'],
    #         'text':     x['action__text'],
    #     } for x in context['targets']
    #         if 'action__line' in x and 'action__text' in x]
    #
    #     for item in todos:
    #         loc_list.append(item)
    #
    #
    #     self.vim.call('setloclist', loc_list)


