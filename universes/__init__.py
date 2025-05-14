"""
Package for universe modules for the Multiverse Fugitive game.

Each universe module should:
1. Define a class that inherits from core.Universe
2. Implement all required methods: on_entry, get_choices, handle_choice, on_exit
3. Be registered with the UniverseManager in main.py
"""

# Import universes here so they can be easily imported elsewhere
from universes.peaky_blinders import PeakyBlindersUniverse
from universes.mcu import MCUUniverse
from universes.stranger_things import StrangerThingsUniverse
