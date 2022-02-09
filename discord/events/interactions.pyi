from ..interactions import Interaction as Interaction
from .core import Event as Event

class OnInteraction(Event):
    def process(self) -> None: ...
