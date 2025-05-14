"""
Utility functions for the Multiverse Fugitive game.
"""

import os
import sys
import time
import random
from typing import List, Optional
import colorama
from colorama import Fore, Style, Back

# Initialize colorama for colored terminal output
colorama.init(autoreset=True)

def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_slow(text: str, delay: float = 0.03) -> None:
    """Print text slowly, character by character."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def print_title() -> None:
    """Print the game's title in a stylized way."""
    clear_screen()
    
    title = """
    ███╗   ███╗██╗   ██╗██╗  ████████╗██╗██╗   ██╗███████╗██████╗ ███████╗███████╗
    ████╗ ████║██║   ██║██║  ╚══██╔══╝██║██║   ██║██╔════╝██╔══██╗██╔════╝██╔════╝
    ██╔████╔██║██║   ██║██║     ██║   ██║██║   ██║█████╗  ██████╔╝███████╗█████╗  
    ██║╚██╔╝██║██║   ██║██║     ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗╚════██║██╔══╝  
    ██║ ╚═╝ ██║╚██████╔╝███████╗██║   ██║ ╚████╔╝ ███████╗██║  ██║███████║███████╗
    ╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═╝   ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝
                                                                                 
    ███████╗██╗   ██╗ ██████╗ ██╗████████╗██╗██╗   ██╗███████╗                     
    ██╔════╝██║   ██║██╔════╝ ██║╚══██╔══╝██║██║   ██║██╔════╝                     
    █████╗  ██║   ██║██║  ███╗██║   ██║   ██║██║   ██║█████╗                       
    ██╔══╝  ██║   ██║██║   ██║██║   ██║   ██║╚██╗ ██╔╝██╔══╝                       
    ██║     ╚██████╔╝╚██████╔╝██║   ██║   ██║ ╚████╔╝ ███████╗                     
    ╚═╝      ╚═════╝  ╚═════╝ ╚═╝   ╚═╝   ╚═╝  ╚═══╝  ╚══════╝                     
    """
    
    print(f"{Fore.CYAN}{title}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}A journey across fictional universes{Style.RESET_ALL}")
    print(f"{Fore.RED}You are a fugitive of reality, jumping through the multiverse to find your way home.{Style.RESET_ALL}")
    print("\n")

def print_story_intro() -> None:
    """Print the game's story introduction."""
    clear_screen()
    print(f"{Fore.CYAN}===== THE STORY SO FAR ====={Style.RESET_ALL}\n")
    
    intro = [
        "You wake up in a void between realities, disoriented and confused.",
        "A voice echoes in the darkness: 'You've been fractured from your timeline.'",
        "'The only way back is to collect key fragments from different universes.'",
        "'But be warned: each jump weakens your connection to reality.'",
        "'You must maintain your memory sync or risk losing yourself forever.'",
        "'Your choices in each world will shape your morality and determine your ultimate fate.'",
        "'You have a limited number of jumps before your fracture key is depleted.'",
        "'Choose wisely, traveler...'",
    ]
    
    for line in intro:
        print_slow(f"{Fore.WHITE}{line}{Style.RESET_ALL}")
        time.sleep(0.5)
    
    print("\nPress Enter to continue...")
    input()

def get_valid_input(prompt: str, valid_options: List[str], case_sensitive: bool = False) -> str:
    """Get user input that matches one of the valid options."""
    while True:
        user_input = input(f"{prompt}: ")
        
        if not case_sensitive:
            user_input = user_input.lower()
            valid_options = [opt.lower() for opt in valid_options]
            
        if user_input in valid_options:
            return user_input
        
        print(f"{Fore.RED}Invalid option. Please try again.{Style.RESET_ALL}")

def get_numeric_input(prompt: str, min_val: int, max_val: int) -> int:
    """Get a numeric input within a specified range."""
    while True:
        try:
            value = int(input(f"{prompt}: "))
            if min_val <= value <= max_val:
                return value
            print(f"{Fore.RED}Please enter a number between {min_val} and {max_val}.{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number.{Style.RESET_ALL}")

def confirm_action(action: str) -> bool:
    """Ask the player to confirm an action."""
    response = get_valid_input(
        f"{Fore.YELLOW}Are you sure you want to {action}? (y/n){Style.RESET_ALL}",
        ["y", "n"]
    )
    return response == "y"

def print_ending(ending_type: str) -> None:
    """Print one of the possible game endings."""
    clear_screen()
    
    if ending_type == "key_fragments":
        # Player collected all key fragments
        print(f"\n{Fore.CYAN}===== THE MULTIVERSE KEEPER ====={Style.RESET_ALL}\n")
        print_slow(f"{Fore.GREEN}You've collected all the key fragments and repaired the fracture key.{Style.RESET_ALL}")
        print_slow("The multiverse stabilizes around you, and you feel yourself being pulled back.")
        print_slow("Your true timeline welcomes you back, but you'll never forget the worlds you visited.")
        print_slow(f"{Fore.YELLOW}Congratulations! You've completed the main objective.{Style.RESET_ALL}")
        
    elif ending_type == "charges":
        # Player ran out of charges
        print(f"\n{Fore.RED}===== LOST IN THE VOID ====={Style.RESET_ALL}\n")
        print_slow(f"{Fore.RED}Your fracture key has depleted its last charge.{Style.RESET_ALL}")
        print_slow("You find yourself stranded between universes, a ghost in the void.")
        print_slow("Perhaps in another lifetime, you'll find your way home...")
        print_slow(f"{Fore.YELLOW}GAME OVER: You've run out of fracture key charges.{Style.RESET_ALL}")
        
    elif ending_type == "memory_sync":
        # Player reached 100% memory sync
        print(f"\n{Fore.BLUE}===== TRUE SELF AWAKENED ====={Style.RESET_ALL}\n")
        print_slow(f"{Fore.CYAN}Your memory sync has reached 100%.{Style.RESET_ALL}")
        print_slow("The truth floods back - you weren't a victim of circumstance...")
        print_slow("You were the Keeper of Realities who chose to experience life in each universe.")
        print_slow("With your full power restored, you can now travel the multiverse at will.")
        print_slow(f"{Fore.YELLOW}SPECIAL ENDING: You've unlocked your true identity.{Style.RESET_ALL}")
        
    print("\nThank you for playing Multiverse Fugitive!")
    print("Press Enter to exit...")
    input()
