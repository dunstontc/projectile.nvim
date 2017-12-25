"""Grep for TODOS."""
# ==============================================================================
#  FILE: todo.py
#  AUTHOR: Clay Dunston <dunstontc@gmail.com>
#  License: MIT license
#  Last Modified: 2017-12-20
# ==============================================================================

import re
import subprocess
from .base import Base
# from denite import util


# Based off of a script by @chemzqm in denite-git
def run_search(command, options, pattern, location):
    try:
        p = subprocess.run(f"{command} {' '.join(options)} \"{pattern}\" {location}",
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT,
                           shell=True)
    except subprocess.CalledProcessError:
        return []
    return p.stdout.decode('utf-8').split('\n')


class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)
        self.name        = 'todo'
        self.kind        = 'file'
        self.matchers    = ['matcher_fuzzy']
        self.vars = {
            'data_dir':    vim.vars.get('projectile#data_dir', '~/.cache/projectile'),
            'todo_terms':  vim.vars.get('projectile#todo_terms'),
            'search_prog': vim.vars.get('projectile#search_prog'),
            'encoding':    'utf-8',

            'command' : 'ag',
            'options' : ['-s', '--nocolor', '--nogroup', '--vimgrep'],

            'ack_options'  : ['-r'],
            'ag_options'   : ['-s', '--nocolor', '--nogroup', '--vimgrep'],
            'grep_options' : ['-E', '-r', '-n'],
            'pt_options'   : ['--nogroup', '--nocolor', '--column'],
        }

    def on_init(self, context):
        # context['is_async'] = True
        context['path_pattern']    = re.compile(r'(^.*?)(?:\:.*$)', re.M)
        context['line_pattern']    = re.compile(r'(?:\:)(\d*)(?:\:)(\d*)', re.M)
        context['content_pattern'] = re.compile(r'(BUG|FIXME|HACK|NOTE|OPTIMIZE|TODO|XXX)+(.*$)', re.M)
        context['terms'] = '|'.join(self.vars.get('todo_terms'))
        # context['terms'] = self.vars.get('todo_terms')

        a = self.vars['command']
        b = self.vars['options']
        # c = self.vars['input']
        c = f"\s({context['terms']})\:\s"
        d = self.vim.call('getcwd')

        context['todos'] = run_search(a, b, c, d)

    def gather_candidates(self, context):
        cur_dir_len = len(self.vim.call('getcwd'))
        candidates  = []
        max_count   = int(0)

        for item in context['todos']:
            try:
                comp_path = context['path_pattern'].search(item).group(1)[cur_dir_len:]
            except AttributeError:
                comp_path = ' '
            cur_len = len(comp_path)
            if cur_len > max_count:
                max_count = cur_len

        for item in context['todos']:
            try:
                todo_path = context['path_pattern'].search(item).group(1)
            except AttributeError:
                todo_path = ''

            try:
                todo_line = context['line_pattern'].search(item).group(1)
                todo_col  = context['line_pattern'].search(item).group(2)
                todo_pos  = f'{todo_path[cur_dir_len:]} [{todo_line}:{todo_col}]'
            except AttributeError:
                todo_line = ''
                todo_pos  = ''

            try:
                todo_content = context['content_pattern'].search(item).group(0)
            except AttributeError:
                todo_content = ''

            if item:
                candidates.append({
                    'word': item,
                    'abbr': '{0:>{width}} -- {1:>}'.format(todo_pos,
                                                           todo_content,
                                                           width=(max_count + 8)  # + 8 for the line & column info
                                                           ),
                    'action__path': todo_path,
                    'action__line': todo_line,
                    'action__col':  todo_col,
                })

        return candidates

    def define_syntax(self):
        self.vim.command(r'syntax match deniteSource_Todo /^.*$/ containedin=' + self.syntax_name + ' '
                         r'contains=deniteSource_Todo_Path,deniteSource_Todo_Noise,deniteSource_Todo_Pos,deniteSource_Todo_Word,deniteSource_Todo_String')
        self.vim.command(r'syntax match deniteSource_Todo_Word   /\v(BUG|FIXME|HACK|NOTE|OPTIMIZE|TODO|XXX)\:/ contained ')
        self.vim.command(r'syntax match deniteSource_Todo_Path   /\%(^\s\)\@<=\(.*\)\%(\[\)\@=/                contained ')
        self.vim.command(r'syntax match deniteSource_Todo_Noise  /\S*\%\(--\)\s/                               contained ')
        self.vim.command(r'syntax match deniteSource_Todo_Noise  /\[\|\]/                                      contained ')
        self.vim.command(r'syntax match deniteSource_Todo_Pos    /\d\+\(:\d\+\)\?/                             contained ')
        self.vim.command(r'syntax match deniteSource_Todo_String /\s`\S\+`/                                    contained ')

    def highlight(self):
        self.vim.command('highlight default link deniteSource_Todo        Normal')
        self.vim.command('highlight default link deniteSource_Todo_Noise  Comment')
        self.vim.command('highlight default link deniteSource_Todo_Path   Directory')
        self.vim.command('highlight default link deniteSource_Todo_Pos    Number')
        self.vim.command('highlight default link deniteSource_Todo_Word   Type')
        self.vim.command('highlight default link deniteSource_Todo_String String')


