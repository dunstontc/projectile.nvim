"""A Denite source for Denite sources."""
# ==============================================================================
#  FILE: sauce.py
#  AUTHOR: Clay Dunston <dunstontc@gmail.com>
#  License: MIT License
#  Last Modified: 2017-12-30
# ==============================================================================


from .base import Base


class Source(Base):
    """I wanna be the very best, like no one ever was."""

    def __init__(self, vim):
        """To catch them is my real test, to train them is my cause."""
        super().__init__(vim)

        self.name = 'sauce'
        self.kind = 'command'
        self.vars = {}

    def on_init(self, context):
        """I will travel across the land, searching far and wide."""
        context['__sauces'] = self.vim.call('projectile#GetCommandCompletion', 'Denite ')

    def gather_candidates(self, context):
        """Each Denite source, to understand, the power that's insiiide."""
        candidates = []

        for sauce in context['__sauces']:
            candidates.append({
                'word': sauce,
                'action__command': 'Denite ' + sauce,
            })

        return candidates

