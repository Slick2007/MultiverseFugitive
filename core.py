"""
Core module containing the fundamental classes and logic for the Multiverse Fugitive game.
"""

import json
import os
from dataclasses import dataclass, field
from typing import List, Dict, Callable, Optional, Union, Any
import colorama
from colorama import Fore, Style

# Initialize colorama
colorama.init(autoreset=True)

@dataclass
class Choice:
    """Represents a choice option presented to the player."""
    id: int
    prompt: str
    consequence: Union[str, Callable]
    
    def __str__(self) -> str:
        return f"{self.id}. {self.prompt}"

@dataclass
class PlayerState:
    """Tracks the player's state across all universes."""
    morality: int = 50  # 0-100, 0 = evil, 100 = good
    memory_sync: int = 0  # 0-100, 100 = remembers true self
    fracture_key_charges: int = 5  # Number of universe jumps available
    key_fragments: set = field(default_factory=set)  # Set of collected key fragments
    reputation: Dict[str, int] = field(default_factory=dict)  # Reputation per universe
    inventory: List[str] = field(default_factory=list)  # Items collected
    visited_universes: set = field(default_factory=set)  # Universes visited
    
    def adjust_morality(self, amount: int) -> None:
        """Adjust the player's morality, keeping it within 0-100."""
        self.morality = max(0, min(100, self.morality + amount))
        
    def adjust_memory_sync(self, amount: int) -> None:
        """Adjust the player's memory sync, keeping it within 0-100."""
        self.memory_sync = max(0, min(100, self.memory_sync + amount))
        
    def add_item(self, item: str) -> None:
        """Add an item to the player's inventory."""
        self.inventory.append(item)
        
    def remove_item(self, item: str) -> bool:
        """Remove an item from the player's inventory. Returns True if successful."""
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False
        
    def adjust_reputation(self, universe: str, amount: int) -> None:
        """Adjust the player's reputation in a specific universe."""
        if universe in self.reputation:
            self.reputation[universe] += amount
        else:
            self.reputation[universe] = amount
            
    def add_key_fragment(self, universe: str) -> None:
        """Add a key fragment from a universe."""
        self.key_fragments.add(universe)
        
    def use_fracture_key_charge(self) -> bool:
        """Use a fracture key charge. Returns False if no charges left."""
        if self.fracture_key_charges <= 0:
            return False
        self.fracture_key_charges -= 1
        return True
        
    def has_completed_universe(self, universe: str) -> bool:
        """Check if a universe has been completed (key fragment collected)."""
        return universe in self.key_fragments
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert player state to a dictionary for saving."""
        return {
            "morality": self.morality,
            "memory_sync": self.memory_sync,
            "fracture_key_charges": self.fracture_key_charges,
            "key_fragments": list(self.key_fragments),
            "reputation": self.reputation,
            "inventory": self.inventory,
            "visited_universes": list(self.visited_universes)
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PlayerState':
        """Create a PlayerState from a dictionary."""
        state = cls(
            morality=data.get("morality", 50),
            memory_sync=data.get("memory_sync", 0),
            fracture_key_charges=data.get("fracture_key_charges", 5),
            reputation=data.get("reputation", {}),
            inventory=data.get("inventory", [])
        )
        state.key_fragments = set(data.get("key_fragments", []))
        state.visited_universes = set(data.get("visited_universes", []))
        return state
        
    def display_stats(self) -> None:
        """Display the player's current stats."""
        print(f"\n{Fore.CYAN}===== PLAYER STATS ====={Style.RESET_ALL}")
        
        # Display morality with color coding
        if self.morality >= 75:
            morality_color = Fore.GREEN
        elif self.morality >= 25:
            morality_color = Fore.YELLOW
        else:
            morality_color = Fore.RED
        
        print(f"Morality: {morality_color}{self.morality}/100{Style.RESET_ALL}")
        
        # Display memory sync with color coding
        if self.memory_sync >= 75:
            memory_color = Fore.CYAN
        elif self.memory_sync >= 25:
            memory_color = Fore.BLUE
        else:
            memory_color = Fore.MAGENTA
        
        print(f"Memory Sync: {memory_color}{self.memory_sync}/100{Style.RESET_ALL}")
        
        # Display remaining charges
        if self.fracture_key_charges <= 1:
            charge_color = Fore.RED
        elif self.fracture_key_charges <= 3:
            charge_color = Fore.YELLOW
        else:
            charge_color = Fore.GREEN
            
        print(f"Fracture Key Charges: {charge_color}{self.fracture_key_charges}{Style.RESET_ALL}")
        
        # Display key fragments
        print(f"Key Fragments: {Fore.YELLOW}{len(self.key_fragments)}{Style.RESET_ALL}")
        
        # Display inventory
        if self.inventory:
            print(f"\n{Fore.CYAN}Inventory:{Style.RESET_ALL}")
            for item in self.inventory:
                print(f"  • {item}")
        else:
            print(f"\n{Fore.CYAN}Inventory:{Style.RESET_ALL} Empty")
        
        # Display reputations
        if self.reputation:
            print(f"\n{Fore.CYAN}Reputation:{Style.RESET_ALL}")
            for universe, rep in self.reputation.items():
                if rep >= 50:
                    rep_color = Fore.GREEN
                elif rep >= 0:
                    rep_color = Fore.YELLOW
                else:
                    rep_color = Fore.RED
                print(f"  • {universe}: {rep_color}{rep}{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}========================{Style.RESET_ALL}")

class Universe:
    """Base class for all universe modules."""
    
    name = "Abstract Universe"
    description = "This is the base universe class. It should be subclassed."
    current_scene = "default"
    
    def on_entry(self, state: PlayerState) -> None:
        """Called when the player enters this universe."""
        raise NotImplementedError("Universes must implement on_entry")
    
    def get_choices(self, state: PlayerState) -> List[Choice]:
        """Return the list of available choices for the current state."""
        raise NotImplementedError("Universes must implement get_choices")
    
    def handle_choice(self, choice_id: int, state: PlayerState) -> str:
        """Handle a player's choice and return the next scene."""
        raise NotImplementedError("Universes must implement handle_choice")
    
    def on_exit(self, state: PlayerState) -> None:
        """Called when the player exits this universe."""
        raise NotImplementedError("Universes must implement on_exit")

class UniverseManager:
    """Manages loading and access to universe modules."""
    
    def __init__(self):
        self.universes: Dict[str, Universe] = {}
    
    def register_universe(self, universe_class: type) -> None:
        """Register a universe class with the manager."""
        universe = universe_class()
        universe_id = universe_class.__name__.lower().replace('universe', '')
        self.universes[universe_id] = universe
    
    def get_universe(self, universe_id: str) -> Optional[Universe]:
        """Get a universe by ID."""
        return self.universes.get(universe_id)
    
    def get_available_universes(self, state: PlayerState) -> Dict[str, Universe]:
        """Get all available universes that haven't been completed."""
        return {k: v for k, v in self.universes.items() 
                if k not in state.key_fragments}
    
    def list_universes(self, state: PlayerState) -> None:
        """List all available universes with their status."""
        print(f"\n{Fore.CYAN}===== AVAILABLE UNIVERSES ====={Style.RESET_ALL}")
        
        for universe_id, universe in self.universes.items():
            # Determine status and color
            if universe_id in state.key_fragments:
                status = f"{Fore.GREEN}[COMPLETED]"
            elif universe_id in state.visited_universes:
                status = f"{Fore.YELLOW}[VISITED]"
            else:
                status = f"{Fore.BLUE}[NEW]"
                
            print(f"{Fore.MAGENTA}{universe_id}{Style.RESET_ALL}: {universe.name} {status}")
            print(f"  {universe.description}")
        
        print(f"\n{Fore.CYAN}============================{Style.RESET_ALL}")
