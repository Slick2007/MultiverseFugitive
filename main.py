#!/usr/bin/env python3
"""
Multiverse Fugitive - A Fully Choice-Based Terminal Game

A text-based adventure where the player explores different fictional universes,
making choices that affect their journey through the multiverse.
"""

import os
import sys
import time
import random
from typing import Optional, Dict, List, Any
import colorama
from colorama import Fore, Style, Back

# Import core modules
from core import PlayerState, Choice, Universe, UniverseManager
from save_manager import save_game, load_game, show_save_slots, autosave, get_latest_save, quick_save
from utils import clear_screen, print_slow, print_title, print_story_intro, get_numeric_input, confirm_action, print_ending

# Import universes
from universes import PeakyBlindersUniverse, MCUUniverse, StrangerThingsUniverse

# Initialize colorama
colorama.init(autoreset=True)

def initialize_game() -> UniverseManager:
    """Set up the universe manager and register all available universes."""
    manager = UniverseManager()
    
    # Register universes
    manager.register_universe(PeakyBlindersUniverse)
    manager.register_universe(MCUUniverse)
    manager.register_universe(StrangerThingsUniverse)
    
    # Additional universes would be registered here
    # manager.register_universe(GTAUniverse)
    # etc.
    
    return manager

def start_new_game() -> PlayerState:
    """Initialize a new game with a fresh player state."""
    print_title()
    print_story_intro()
    
    return PlayerState()

def load_existing_game() -> Optional[PlayerState]:
    """Show save slots and let the player load a saved game."""
    clear_screen()
    print(f"{Fore.CYAN}===== LOAD GAME ====={Style.RESET_ALL}")
    
    save_info = show_save_slots()
    
    # Filter out empty slots and convert to list
    valid_slots = [slot for slot, info in save_info.items() if not info.get("empty", False)]
    
    if not valid_slots:
        print(f"{Fore.YELLOW}No save files found. Starting a new game...{Style.RESET_ALL}")
        time.sleep(2)
        return None
    
    # Check if there's an autosave
    has_autosave = "autosave" in valid_slots
    
    # Create a list of numeric slots for selection
    numeric_slots = [int(slot) for slot in valid_slots if slot != "autosave"]
    
    # Add option for autosave if it exists
    autosave_option = len(numeric_slots) + 1 if has_autosave else 0
    
    print("\nSelect a save to load:")
    if numeric_slots:
        print(f"1-{len(numeric_slots)}: Regular save slots")
    if has_autosave:
        print(f"{autosave_option}: Autosave")
    print("0: Cancel and start a new game")
    
    # Determine the maximum option number
    max_option = autosave_option if has_autosave else len(numeric_slots)
    
    # Get user selection
    selection = get_numeric_input("Option", 0, max_option)
    
    if selection == 0:
        return None
    elif has_autosave and selection == autosave_option:
        return load_game("autosave")
    else:
        # Convert selection to slot number
        slot_index = selection - 1
        if 0 <= slot_index < len(numeric_slots):
            slot = str(numeric_slots[slot_index])
            return load_game(slot)
    
    # If we get here, something went wrong
    print(f"{Fore.RED}Invalid selection. Starting a new game...{Style.RESET_ALL}")
    time.sleep(2)
    return None

def show_main_menu() -> int:
    """Display the main menu and return the player's choice."""
    clear_screen()
    print_title()
    
    print(f"\n{Fore.CYAN}===== MAIN MENU ====={Style.RESET_ALL}")
    print(f"{Fore.WHITE}1. New Game{Style.RESET_ALL}")
    print(f"{Fore.WHITE}2. Load Game{Style.RESET_ALL}")
    print(f"{Fore.WHITE}3. Continue Last Save{Style.RESET_ALL}")
    print(f"{Fore.WHITE}4. About{Style.RESET_ALL}")
    print(f"{Fore.WHITE}5. Exit{Style.RESET_ALL}")
    
    return get_numeric_input("\nSelect an option", 1, 5)

def show_about() -> None:
    """Display information about the game."""
    clear_screen()
    print(f"{Fore.CYAN}===== ABOUT MULTIVERSE FUGITIVE ====={Style.RESET_ALL}")
    print("\nA choice-based adventure through fictional universes.")
    print("You play as a fugitive of reality, jumping between worlds to collect key fragments.")
    print("\nGame Features:")
    print("- Explore multiple fictional universes")
    print("- Make choices that affect your character's morality and memory")
    print("- Collect items and build reputation in each universe")
    print("- Multiple ending paths based on your decisions")
    
    print(f"\n{Fore.YELLOW}Created as a modular, expandable game engine.{Style.RESET_ALL}")
    
    print("\nPress Enter to return to the main menu...")
    input()

def show_multiverse_hub(state: PlayerState, universe_manager: UniverseManager) -> str:
    """
    Display the multiverse hub (void between universes) and handle player choices.
    Returns the ID of the selected universe or special commands.
    """
    clear_screen()
    print(f"{Fore.CYAN}===== THE VOID - MULTIVERSE HUB ====={Style.RESET_ALL}")
    
    print_slow("You float in the empty space between realities, your fracture key pulsing with energy.")
    if len(state.key_fragments) > 0:
        print_slow(f"The {len(state.key_fragments)} key fragments you've collected shimmer, eager to be reunited.")
    
    # Display player stats
    state.display_stats()
    
    # List available universes
    universe_manager.list_universes(state)
    
    # Setup menu options
    options = []
    
    # Universe selection options
    for i, universe_id in enumerate(universe_manager.universes.keys(), 1):
        universe = universe_manager.get_universe(universe_id)
        if universe:
            completed = universe_id in state.key_fragments
            status = f"{Fore.GREEN}[COMPLETED]" if completed else ""
            options.append(f"{i}. Enter {universe.name} {status}")
        else:
            options.append(f"{i}. Enter Unknown Universe")
    
    # Additional options
    options.append(f"{len(universe_manager.universes) + 1}. Save Game")
    options.append(f"{len(universe_manager.universes) + 2}. Quick Save")
    options.append(f"{len(universe_manager.universes) + 3}. Exit to Main Menu")
    
    print(f"\n{Fore.CYAN}===== ACTIONS ====={Style.RESET_ALL}")
    for option in options:
        print(option)
    
    max_option = len(universe_manager.universes) + 3
    choice = get_numeric_input("\nSelect an option", 1, max_option)
    
    # Handle universe selection
    if choice <= len(universe_manager.universes):
        universe_ids = list(universe_manager.universes.keys())
        if choice <= len(universe_ids):
            selected_universe = universe_ids[choice - 1]
            
            # Check if player has enough charges
            if state.fracture_key_charges <= 0:
                print_slow(f"{Fore.RED}You don't have any fracture key charges left!{Style.RESET_ALL}")
                print_slow("You're trapped in the void, unable to enter any more universes.")
                print("\nPress Enter to continue...")
                input()
                return "no_charges"
            
            # Confirm universe entry
            universe = universe_manager.get_universe(selected_universe)
            if universe:
                print(f"\nYou're about to enter {Fore.YELLOW}{universe.name}{Style.RESET_ALL}.")
                print(f"This will use one fracture key charge. You have {state.fracture_key_charges} remaining.")
                
                if confirm_action(f"enter {universe.name}"):
                    # Autosave before entering a universe (in case something goes wrong)
                    autosave(state)
                    return selected_universe
    
    # Handle regular save game
    elif choice == len(universe_manager.universes) + 1:
        save_slot = str(get_numeric_input("Enter save slot (1-3)", 1, 3))
        save_game(state, save_slot)
        print("\nPress Enter to continue...")
        input()
    
    # Handle quick save
    elif choice == len(universe_manager.universes) + 2:
        if quick_save(state):
            print(f"{Fore.GREEN}Game quick-saved successfully.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Failed to quick-save the game.{Style.RESET_ALL}")
        print("\nPress Enter to continue...")
        input()
    
    # Exit to main menu
    elif choice == len(universe_manager.universes) + 3:
        if confirm_action("exit to the main menu"):
            # Autosave before exiting to menu
            autosave(state)
            return "exit_to_menu"
    
    # Return empty string to stay in hub
    return ""

def check_game_end_conditions(state: PlayerState, universe_manager: UniverseManager) -> Optional[str]:
    """
    Check if any game ending conditions have been met.
    Returns the ending type if the game should end, None otherwise.
    """
    # Check if player has collected all key fragments
    if len(state.key_fragments) >= len(universe_manager.universes):
        return "key_fragments"
    
    # Check if player has run out of charges
    if state.fracture_key_charges <= 0:
        return "charges"
    
    # Check if player has reached 100% memory sync
    if state.memory_sync >= 100:
        return "memory_sync"
    
    return None

def enter_universe(universe_id: str, state: PlayerState, universe_manager: UniverseManager) -> None:
    """Handle the player's journey through a specific universe."""
    universe = universe_manager.get_universe(universe_id)
    if not universe:
        print(f"{Fore.RED}Error: Universe {universe_id} not found.{Style.RESET_ALL}")
        return
    
    # Enter the universe
    universe.on_entry(state)
    
    # Autosave after entering universe
    autosave(state)
    
    # Main universe gameplay loop
    while True:
        clear_screen()
        print(f"{Fore.CYAN}===== {universe.name.upper()} ====={Style.RESET_ALL}")
        print(f"{Fore.WHITE}Current Location: {universe.current_scene.replace('_', ' ').title()}{Style.RESET_ALL}")
        
        # Get available choices
        choices = universe.get_choices(state)
        
        # Display choices
        print(f"\n{Fore.CYAN}What will you do?{Style.RESET_ALL}")
        for choice in choices:
            print(f"{choice.id}. {choice.prompt}")
        
        # Get player input
        choice_id = get_numeric_input("\nYour choice", 1, len(choices))
        
        # Handle the choice
        result = universe.handle_choice(choice_id, state)
        
        # Check if player is exiting the universe
        if result == "exit":
            # Perform exit actions
            universe.on_exit(state)
            # Autosave after exiting universe (key point in game progression)
            autosave(state)
            break
        
        # Autosave after significant choices (20% chance to avoid too frequent saves)
        if random.random() < 0.2:
            autosave(state)
        
        # Pause to let player read
        print("\nPress Enter to continue...")
        input()

def main() -> None:
    """Main game function."""
    # Initialize the universe manager
    universe_manager = initialize_game()
    
    # Main game loop
    while True:
        # Show main menu
        menu_choice = show_main_menu()
        
        if menu_choice == 1:  # New Game
            state = start_new_game()
            # Create initial autosave
            autosave(state)
        elif menu_choice == 2:  # Load Game
            state = load_existing_game()
            if not state:
                state = start_new_game()
                # Create initial autosave for new game
                autosave(state)
        elif menu_choice == 3:  # Continue Last Save
            # Get the most recent save
            latest_slot = get_latest_save()
            if latest_slot:
                state = load_game(latest_slot)
                if not state:
                    print(f"{Fore.RED}Error loading the latest save. Starting a new game...{Style.RESET_ALL}")
                    time.sleep(2)
                    state = start_new_game()
                    autosave(state)
            else:
                print(f"{Fore.YELLOW}No saves found. Starting a new game...{Style.RESET_ALL}")
                time.sleep(2)
                state = start_new_game()
                autosave(state)
        elif menu_choice == 4:  # About
            show_about()
            continue
        elif menu_choice == 5:  # Exit
            print(f"{Fore.YELLOW}Thank you for playing Multiverse Fugitive!{Style.RESET_ALL}")
            sys.exit(0)
        
        # Game session loop
        game_running = True
        while game_running:
            # Show the multiverse hub
            selected_universe = show_multiverse_hub(state, universe_manager)
            
            # Handle hub choices
            if selected_universe == "exit_to_menu":
                # Autosave before returning to menu
                autosave(state)
                game_running = False
            elif selected_universe == "no_charges":
                # Player has no charges left - game over
                # Autosave for potential future "continue from death" feature
                autosave(state)
                print_ending("charges")
                game_running = False
            elif selected_universe:
                # Enter the selected universe
                enter_universe(selected_universe, state, universe_manager)
                
                # Check if any ending conditions are met
                ending = check_game_end_conditions(state, universe_manager)
                if ending:
                    # Final autosave before ending the game
                    autosave(state)
                    print_ending(ending)
                    game_running = False

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Game interrupted. Thanks for playing!{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}An error occurred: {str(e)}{Style.RESET_ALL}")
        print("If this issue persists, please report it.")
    finally:
        # Ensure proper cleanup of colorama
        colorama.deinit()
