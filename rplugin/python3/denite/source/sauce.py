"""A Denite source for Denite sources."""
# ==============================================================================
#  FILE: sauce.py
#  AUTHOR: Clay Dunston <dunstontc@gmail.com>
#  License: MIT License
#  Last Modified: 2017-12-30
# ==============================================================================


from .base import Base


class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'sauce'
        self.kind = 'command'
        self.vars = {}

    def on_init(self, context):
        context['__sauces'] = self.vim.call('projectile#CommandCompletion', 'Denite ')

    def gather_candidates(self, context):
        candidates = []

        for sauce in context['__sauces']:
            if sauce != 'Denite':
                candidates.append({
                    'word': sauce,
                    'action__command': 'Denite ' + sauce,
                })

        return candidates

