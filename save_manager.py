"""
Save game functionality for Multiverse Fugitive.
"""

import os
import json
from typing import Optional, Dict, Any, List
import time
import colorama
from colorama import Fore, Style

from core import PlayerState

# Initialize colorama
colorama.init(autoreset=True)

SAVE_DIRECTORY = "saves"
MAX_SAVES = 3
AUTOSAVE_SLOT = "autosave"  # Special slot for autosaves

def ensure_save_directory() -> None:
    """Create the save directory if it doesn't exist."""
    if not os.path.exists(SAVE_DIRECTORY):
        try:
            os.makedirs(SAVE_DIRECTORY)
        except OSError:
            print(f"{Fore.RED}Error: Could not create save directory.{Style.RESET_ALL}")

def get_save_files() -> Dict[str, str]:
    """Get a mapping of save slots to save file paths."""
    ensure_save_directory()
    
    save_files = {}
    
    try:
        for filename in os.listdir(SAVE_DIRECTORY):
            if filename.endswith(".json"):
                if filename.startswith("save_"):
                    # Regular save slots (numbered)
                    try:
                        slot_num = int(filename.split('_')[1].split('.')[0])
                        if 1 <= slot_num <= MAX_SAVES:
                            save_files[str(slot_num)] = os.path.join(SAVE_DIRECTORY, filename)
                    except ValueError:
                        pass
                elif filename == "autosave.json":
                    # Autosave slot
                    save_files[AUTOSAVE_SLOT] = os.path.join(SAVE_DIRECTORY, filename)
    except OSError:
        print(f"{Fore.RED}Error: Could not access save directory.{Style.RESET_ALL}")
    
    return save_files

def save_game(state: PlayerState, slot: str) -> bool:
    """
    Save the game state to a file.
    
    Args:
        state: The player's state to save
        slot: Either a number (as a string) for manual saves or 'autosave' for autosaves
    
    Returns:
        bool: True if save was successful, False otherwise
    """
    ensure_save_directory()
    
    save_data = {
        "timestamp": time.time(),
        "datetime": time.strftime("%Y-%m-%d %H:%M:%S"),
        "player_state": state.to_dict()
    }
    
    if slot == AUTOSAVE_SLOT:
        filename = "autosave.json"
    else:
        try:
            slot_num = int(slot)
            filename = f"save_{slot_num}.json"
        except ValueError:
            print(f"{Fore.RED}Invalid save slot: {slot}{Style.RESET_ALL}")
            return False
    
    filepath = os.path.join(SAVE_DIRECTORY, filename)
    
    try:
        with open(filepath, 'w') as f:
            json.dump(save_data, f, indent=2)
        
        if slot != AUTOSAVE_SLOT:  # Don't show message for autosaves
            print(f"{Fore.GREEN}Game saved successfully to slot {slot}.{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"{Fore.RED}Error saving game: {str(e)}{Style.RESET_ALL}")
        return False

def autosave(state: PlayerState) -> bool:
    """
    Automatically save the game to the autosave slot.
    This function is meant to be called at key points in the game.
    
    Args:
        state: The player's state to save
        
    Returns:
        bool: True if autosave was successful, False otherwise
    """
    return save_game(state, AUTOSAVE_SLOT)

def load_game(slot: str) -> Optional[PlayerState]:
    """
    Load a game state from a file.
    
    Args:
        slot: Either a number (as a string) for manual saves or 'autosave' for autosaves
        
    Returns:
        Optional[PlayerState]: The loaded player state, or None if loading failed
    """
    save_files = get_save_files()
    
    if slot not in save_files:
        print(f"{Fore.RED}No save file found in slot {slot}.{Style.RESET_ALL}")
        return None
    
    try:
        with open(save_files[slot], 'r') as f:
            save_data = json.load(f)
            
        player_data = save_data.get("player_state", {})
        state = PlayerState.from_dict(player_data)
        
        slot_display = "autosave" if slot == AUTOSAVE_SLOT else f"slot {slot}"
        print(f"{Fore.GREEN}Game loaded successfully from {slot_display} ({save_data.get('datetime', 'unknown date')}).{Style.RESET_ALL}")
        return state
    except Exception as e:
        print(f"{Fore.RED}Error loading game: {str(e)}{Style.RESET_ALL}")
        return None

def show_save_slots() -> Dict[str, Dict[str, Any]]:
    """
    Show available save slots with their information.
    
    Returns:
        Dict[str, Dict[str, Any]]: Information about each save slot
    """
    save_files = get_save_files()
    save_info = {}
    
    print(f"\n{Fore.CYAN}===== SAVE SLOTS ====={Style.RESET_ALL}")
    
    # First display regular save slots
    for slot_num in range(1, MAX_SAVES + 1):
        slot = str(slot_num)
        if slot in save_files:
            try:
                with open(save_files[slot], 'r') as f:
                    save_data = json.load(f)
                
                datetime = save_data.get("datetime", "Unknown date")
                player_data = save_data.get("player_state", {})
                
                save_info[slot] = _extract_save_info(player_data, datetime)
                _display_save_info(slot, save_info[slot])
                
            except Exception:
                print(f"{Fore.RED}Slot {slot}: Error reading save file{Style.RESET_ALL}")
                save_info[slot] = {"error": True}
        else:
            print(f"{Fore.YELLOW}Slot {slot}: Empty{Style.RESET_ALL}")
            save_info[slot] = {"empty": True}
    
    # Then display autosave if it exists
    if AUTOSAVE_SLOT in save_files:
        try:
            with open(save_files[AUTOSAVE_SLOT], 'r') as f:
                save_data = json.load(f)
            
            datetime = save_data.get("datetime", "Unknown date")
            player_data = save_data.get("player_state", {})
            
            save_info[AUTOSAVE_SLOT] = _extract_save_info(player_data, datetime)
            
            print(f"{Fore.BLUE}Autosave: {datetime}{Style.RESET_ALL}")
            _display_save_details(save_info[AUTOSAVE_SLOT])
            
        except Exception:
            print(f"{Fore.RED}Autosave: Error reading save file{Style.RESET_ALL}")
            save_info[AUTOSAVE_SLOT] = {"error": True}
    
    print(f"{Fore.CYAN}==================={Style.RESET_ALL}")
    return save_info

def _extract_save_info(player_data: Dict[str, Any], datetime: str) -> Dict[str, Any]:
    """Extract relevant information from save data."""
    memory_sync = player_data.get("memory_sync", 0)
    morality = player_data.get("morality", 50)
    charges = player_data.get("fracture_key_charges", 0)
    fragments = player_data.get("key_fragments", [])
    visited = player_data.get("visited_universes", [])
    inventory = player_data.get("inventory", [])
    reputation = player_data.get("reputation", {})
    
    return {
        "datetime": datetime,
        "memory_sync": memory_sync,
        "morality": morality,
        "charges": charges,
        "fragments": fragments,
        "fragment_count": len(fragments),
        "visited": visited,
        "inventory": inventory,
        "reputation": reputation
    }

def _display_save_info(slot: str, info: Dict[str, Any]) -> None:
    """Display save information in a formatted way."""
    datetime = info.get("datetime", "Unknown date")
    memory_sync = info.get("memory_sync", 0)
    morality = info.get("morality", 50)
    charges = info.get("charges", 0)
    fragment_count = info.get("fragment_count", 0)
    
    print(f"{Fore.GREEN}Slot {slot}: {datetime}{Style.RESET_ALL}")
    print(f"  Memory Sync: {memory_sync}% | Morality: {morality} | Charges: {charges} | Fragments: {fragment_count}")
    
    # Display more details if available
    _display_save_details(info)

def _display_save_details(info: Dict[str, Any]) -> None:
    """Display additional save details."""
    fragments = info.get("fragments", [])
    visited = info.get("visited", [])
    
    # Show collected fragments
    if fragments:
        fragment_list = ", ".join(fragments)
        print(f"  {Fore.YELLOW}Key Fragments: {fragment_list}{Style.RESET_ALL}")
    
    # Show visited universes that aren't completed yet
    incomplete = [universe for universe in visited if universe not in fragments]
    if incomplete:
        incomplete_list = ", ".join(incomplete)
        print(f"  {Fore.BLUE}Visited but not completed: {incomplete_list}{Style.RESET_ALL}")

def delete_save(slot: str) -> bool:
    """
    Delete a save file.
    
    Args:
        slot: Either a number (as a string) for manual saves or 'autosave' for autosaves
        
    Returns:
        bool: True if deletion was successful, False otherwise
    """
    save_files = get_save_files()
    
    if slot not in save_files:
        print(f"{Fore.RED}No save file found in slot {slot}.{Style.RESET_ALL}")
        return False
    
    try:
        os.remove(save_files[slot])
        slot_display = "autosave" if slot == AUTOSAVE_SLOT else f"slot {slot}"
        print(f"{Fore.GREEN}Save in {slot_display} deleted successfully.{Style.RESET_ALL}")
        return True
    except Exception as e:
        print(f"{Fore.RED}Error deleting save: {str(e)}{Style.RESET_ALL}")
        return False

def get_latest_save() -> Optional[str]:
    """
    Find the most recent save file.
    
    Returns:
        Optional[str]: The slot of the most recent save, or None if no saves exist
    """
    save_files = get_save_files()
    if not save_files:
        return None
    
    latest_slot = None
    latest_time = 0
    
    for slot, path in save_files.items():
        try:
            with open(path, 'r') as f:
                save_data = json.load(f)
            
            timestamp = save_data.get("timestamp", 0)
            if timestamp > latest_time:
                latest_time = timestamp
                latest_slot = slot
        except Exception:
            continue
    
    return latest_slot

def quick_save(state: PlayerState) -> bool:
    """
    Quickly save the game to the first available slot.
    If all slots are full, it will overwrite the oldest save.
    
    Args:
        state: The player's state to save
        
    Returns:
        bool: True if save was successful, False otherwise
    """
    save_files = get_save_files()
    
    # Check for empty slots
    for slot_num in range(1, MAX_SAVES + 1):
        slot = str(slot_num)
        if slot not in save_files:
            return save_game(state, slot)
    
    # If no empty slots, find the oldest save
    oldest_slot = "1"  # Default to first slot
    oldest_time = float('inf')
    
    for slot, path in save_files.items():
        if slot == AUTOSAVE_SLOT:
            continue  # Skip autosave
            
        try:
            with open(path, 'r') as f:
                save_data = json.load(f)
            
            timestamp = save_data.get("timestamp", 0)
            if timestamp < oldest_time:
                oldest_time = timestamp
                oldest_slot = slot
        except Exception:
            # If there's an error reading the file, overwrite this slot
            return save_game(state, slot)
    
    # Overwrite the oldest save
    return save_game(state, oldest_slot)
