"""
Marvel Cinematic Universe module for Multiverse Fugitive.
"""

from typing import List, Dict, Any
import random
import time
import colorama
from colorama import Fore, Style

from core import Universe, PlayerState, Choice
from utils import print_slow, clear_screen, confirm_action

colorama.init(autoreset=True)

class MCUUniverse(Universe):
    """
    The Marvel Cinematic Universe.
    
    Players navigate the world of superheroes and villains,
    making choices that impact their standing with the Avengers and other characters.
    """
    
    name = "Marvel Cinematic Universe"
    description = "Navigate the world of superheroes, villains, and cosmic threats in the MCU."
    
    def __init__(self):
        # Track the current scene/location
        self.current_scene = "awakening"
        
        # Characters to keep track of
        self.characters = {
            "tony": {
                "name": "Tony Stark",
                "description": "Genius billionaire playboy philanthropist, also known as Iron Man."
            },
            "steve": {
                "name": "Steve Rogers",
                "description": "The first Avenger, Captain America, with an unbreakable moral compass."
            },
            "natasha": {
                "name": "Natasha Romanoff",
                "description": "Former assassin turned Avenger, the Black Widow."
            },
            "fury": {
                "name": "Nick Fury",
                "description": "The director of S.H.I.E.L.D. and the one who brought the Avengers together."
            },
            "loki": {
                "name": "Loki",
                "description": "The God of Mischief, always with his own agenda."
            }
        }
        
        # Scenes/locations in this universe
        self.scenes = {
            "awakening": {
                "description": "You wake up in New York City, but something is different. The skyline includes Stark Tower with its distinctive 'A' logo. A news broadcast on a nearby screen shows footage of the Avengers fighting aliens in the Battle of New York.",
                "first_visit": True
            },
            "stark_tower": {
                "description": "Stark Tower (now Avengers Tower) stands tall in the Manhattan skyline. The lobby is sleek and modern, with cutting-edge technology everywhere. Security is tight, with guards and AI systems monitoring all movement.",
                "first_visit": True
            },
            "shield_hq": {
                "description": "The secret headquarters of S.H.I.E.L.D. Agents move purposefully through the facility, which is filled with advanced technology and weapons. Monitors display global threats and agent deployments.",
                "first_visit": True
            },
            "central_park": {
                "description": "A quiet area of Central Park where people relax, seemingly unaware of the superhero drama that regularly unfolds in their city. There's an unusual energy in the air today.",
                "first_visit": True
            },
            "sanctum": {
                "description": "The New York Sanctum, home to the Masters of the Mystic Arts. Ancient artifacts line the walls, and there's a sense of otherworldly power permeating the building.",
                "first_visit": True
            }
        }
    
    def on_entry(self, state: PlayerState) -> None:
        """Called when the player enters the MCU universe."""
        clear_screen()
        print(f"{Fore.CYAN}===== ENTERING UNIVERSE: {self.name} ====={Style.RESET_ALL}\n")
        
        # Add to visited universes
        state.visited_universes.add("mcu")
        
        # Initialize reputation for this universe if first visit
        if "mcu" not in state.reputation:
            state.reputation["mcu"] = 0
        
        # Intro narration
        print_slow(f"{Fore.YELLOW}New York City - Present Day{Style.RESET_ALL}")
        time.sleep(0.5)
        
        # Display the awakening scene
        self._show_scene_description("awakening")
        
        # Additional intro text
        print_slow("Your fracture key pulses in your pocket, its energy somehow feeling different in this reality.")
        print_slow("A newspaper stand nearby has the headline: 'AVENGERS SAVE CITY FROM ALIEN INVASION'")
        
        # Player choice on how to react to waking up
        print("\nWhat do you do?")
        print("1. Try to remember what you know about this universe")
        print("2. Look for someone who might help you")
        print("3. Check if you have any unusual abilities in this universe")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == "1":
            print_slow("You concentrate, trying to recall information about this universe.")
            print_slow("Flashes of knowledge come to you - Iron Man, Captain America, Thor, the Infinity Stones...")
            state.adjust_memory_sync(5)
            print(f"{Fore.BLUE}Memory sync increased by 5%{Style.RESET_ALL}")
        elif choice == "2":
            print_slow("You decide to find someone who might help you understand this place.")
            print_slow("A street vendor selling Avengers merchandise eyes you curiously.")
        else:
            print_slow("You focus inward, wondering if this universe has granted you any special powers.")
            print_slow("You don't feel particularly super, but you do find a strange device in your pocket.")
            state.add_item("S.H.I.E.L.D. Communicator")
            print(f"{Fore.GREEN}Item added to inventory: S.H.I.E.L.D. Communicator{Style.RESET_ALL}")
        
        print_slow("\nThe city is bustling around you. In a world of superheroes and villains, you'll need to choose your allies carefully.")
        print("\nPress Enter to continue...")
        input()
    
    def _show_scene_description(self, scene_id: str) -> None:
        """Display the description for a scene."""
        scene = self.scenes.get(scene_id)
        if not scene:
            return
        
        print_slow(scene["description"])
        
        # Mark as visited
        if scene.get("first_visit", False):
            scene["first_visit"] = False
    
    def get_choices(self, state: PlayerState) -> List[Choice]:
        """Return the available choices based on the current scene."""
        choices = []
        
        if self.current_scene == "awakening":
            choices = [
                Choice(1, "Head to Stark Tower", self._go_to_stark_tower),
                Choice(2, "Visit Central Park", self._go_to_central_park),
                Choice(3, "Follow a person who looks like a S.H.I.E.L.D. agent", self._follow_shield_agent)
            ]
            
        elif self.current_scene == "stark_tower":
            choices = [
                Choice(1, "Try to speak with Tony Stark", self._speak_with_stark),
                Choice(2, "Explore the public areas", self._explore_stark_tower),
                Choice(3, "Listen to employee conversations", self._eavesdrop_stark_tower)
            ]
            
            # Add conditional choice if player has S.H.I.E.L.D. Communicator
            if "S.H.I.E.L.D. Communicator" in state.inventory:
                choices.append(Choice(4, "Use the S.H.I.E.L.D. Communicator", self._use_communicator))
            
        elif self.current_scene == "central_park":
            choices = [
                Choice(1, "Help a child who lost their parent", self._help_lost_child),
                Choice(2, "Investigate a strange energy signature", self._investigate_energy),
                Choice(3, "Visit the New York Sanctum nearby", self._go_to_sanctum)
            ]
            
        elif self.current_scene == "shield_hq":
            choices = [
                Choice(1, "Try to speak with Nick Fury", self._speak_with_fury),
                Choice(2, "Access a computer terminal", self._access_shield_terminal),
                Choice(3, "Return to the city streets", lambda state: self._change_scene("awakening", state))
            ]
            
            # Add conditional choice based on reputation
            if state.reputation.get("mcu", 0) >= 20:
                choices.append(Choice(4, "Request S.H.I.E.L.D. resources", self._request_resources))
            
        elif self.current_scene == "sanctum":
            choices = [
                Choice(1, "Examine the mystical artifacts", self._examine_artifacts),
                Choice(2, "Speak with a Master of the Mystic Arts", self._speak_with_master),
                Choice(3, "Return to Central Park", lambda state: self._change_scene("central_park", state))
            ]
        
        # Always add option to leave universe if not in the initial scene
        if self.current_scene != "awakening":
            choices.append(Choice(len(choices) + 1, "Use fracture key to exit universe", self._exit_universe))
        
        return choices
    
    def handle_choice(self, choice_id: int, state: PlayerState) -> str:
        """Process the player's choice and return the next scene."""
        choices = self.get_choices(state)
        
        # Find the chosen option
        chosen_choice = None
        for choice in choices:
            if choice.id == choice_id:
                chosen_choice = choice
                break
        
        if not chosen_choice:
            print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
            return self.current_scene
        
        # Execute the consequence function or print the consequence text
        if callable(chosen_choice.consequence):
            result = chosen_choice.consequence(state)
            return result if result else self.current_scene
        else:
            print_slow(chosen_choice.consequence)
            return self.current_scene
    
    def on_exit(self, state: PlayerState) -> None:
        """Called when the player exits the MCU universe."""
        clear_screen()
        print(f"{Fore.CYAN}===== EXITING UNIVERSE: {self.name} ====={Style.RESET_ALL}\n")
        
        # Add key fragment if this is the first time completing the universe
        if "mcu" not in state.key_fragments:
            print_slow("As you activate your fracture key, it seems to resonate with this universe's energy.")
            print_slow("A small fragment of reality breaks off and fuses with your key.")
            state.add_key_fragment("mcu")
            print(f"{Fore.YELLOW}Key Fragment acquired: Marvel Cinematic Universe{Style.RESET_ALL}")
        
        # Final messages based on reputation
        rep = state.reputation.get("mcu", 0)
        if rep >= 50:
            print_slow(f"Tony Stark gives you a knowing nod as you start to fade away.")
            print_slow(f"'Multiverse theory, huh? We should talk when you get back,' he says with a smirk.")
        elif rep >= 20:
            print_slow(f"You've made some connections in this universe, but also left some questions unanswered.")
            print_slow(f"Nick Fury will definitely be adding you to his list of interdimensional entities to monitor.")
        else:
            print_slow(f"You leave this universe mostly unnoticed, which is probably for the best.")
            print_slow(f"In a world of gods and monsters, sometimes staying under the radar is the wisest choice.")
        
        print("\nPress Enter to continue...")
        input()
    
    # Scene transition methods
    def _change_scene(self, new_scene: str, state: PlayerState) -> str:
        """Change to a new scene and display its description."""
        clear_screen()
        self.current_scene = new_scene
        self._show_scene_description(new_scene)
        return new_scene
    
    # Scene-specific choice consequences
    def _go_to_stark_tower(self, state: PlayerState) -> str:
        """Go to Stark Tower."""
        print_slow("You make your way through the bustling New York streets toward the iconic Stark Tower.")
        print_slow("The building dominates the skyline, a beacon of advanced technology and superhero activity.")
        return self._change_scene("stark_tower", state)
    
    def _go_to_central_park(self, state: PlayerState) -> str:
        """Visit Central Park."""
        print_slow("You decide to visit Central Park, a quiet contrast to the city's chaos.")
        print_slow("People jog, picnic, and relax, seemingly unfazed by living in a city of superheroes.")
        return self._change_scene("central_park", state)
    
    def _follow_shield_agent(self, state: PlayerState) -> str:
        """Follow a S.H.I.E.L.D. agent."""
        print_slow("You discreetly follow someone who has the bearing and subtle earpiece of a S.H.I.E.L.D. agent.")
        print_slow("They lead you to an unmarked building with unusually tight security.")
        state.adjust_morality(-5)  # Slightly questionable to follow someone
        return self._change_scene("shield_hq", state)
    
    def _speak_with_stark(self, state: PlayerState) -> str:
        """Try to speak with Tony Stark."""
        print_slow("You attempt to arrange a meeting with Tony Stark, but security is tight.")
        print_slow("'Do you have an appointment?' asks a stern-looking receptionist.")
        
        print("\nHow do you respond?")
        print("1. 'I have information about interdimensional threats.'")
        print("2. 'I'm just looking for a tour of the facility.'")
        print("3. 'I need to speak with him about the Avengers Initiative.'")
        
        subchoice = input("\nEnter your choice (1-3): ")
        
        if subchoice == "1":
            print_slow("The receptionist's expression changes slightly at your mention of interdimensional threats.")
            print_slow("'Wait here,' she says, making a phone call.")
            
            if random.random() < 0.3:  # 30% chance of success
                print_slow("\nTo your surprise, you're escorted to a private elevator.")
                print_slow("'Mr. Stark will see you briefly,' the security guard informs you.")
                state.adjust_reputation("mcu", 15)
                print(f"{Fore.GREEN}Reputation increased by 15{Style.RESET_ALL}")
                
                print_slow("\nTony Stark looks up from his holographic workstation as you enter.")
                print_slow("'So, you're the one talking about other dimensions. Make it quick, I've got a party in an hour.'")
                
                # Add memory trigger
                if random.random() < 0.4:  # 40% chance
                    print_slow("\nSomething about Stark's technology triggers a memory...")
                    print_slow("You recall fragments of your purpose across the multiverse.")
                    state.adjust_memory_sync(4)
                    print(f"{Fore.BLUE}Memory sync increased by 4%{Style.RESET_ALL}")
            else:
                print_slow("\n'I'm sorry,' she eventually says. 'Mr. Stark is unavailable.'")
                print_slow("You're politely but firmly escorted back to the lobby.")
        elif subchoice == "2":
            print_slow("'Public tours are on Tuesdays and Thursdays,' she informs you.")
            print_slow("'You can register online for the next available slot.'")
        else:
            print_slow("The receptionist narrows her eyes at your mention of the Avengers Initiative.")
            print_slow("'Security will escort you out now,' she says coldly, pressing a button.")
            state.adjust_reputation("mcu", -10)
            print(f"{Fore.RED}Reputation decreased by 10{Style.RESET_ALL}")
        
        return self.current_scene
    
    def _explore_stark_tower(self, state: PlayerState) -> str:
        """Explore the public areas of Stark Tower."""
        print_slow("You wander through the public areas of Stark Tower, admiring the futuristic design.")
        print_slow("Display cases showcase Iron Man suit prototypes and Stark Industries technology.")
        
        # Chance to find something useful
        if random.random() < 0.3:  # 30% chance
            print_slow("\nIn a less-monitored corner, you notice something unusual on a desk.")
            print_slow("It's a visitor badge that someone forgot to turn in. You pocket it discreetly.")
            state.add_item("Stark Tower Visitor Badge")
            print(f"{Fore.GREEN}Item added to inventory: Stark Tower Visitor Badge{Style.RESET_ALL}")
            state.adjust_morality(-5)
            print(f"{Fore.YELLOW}Morality decreased by 5{Style.RESET_ALL}")
        
        return self.current_scene
    
    def _eavesdrop_stark_tower(self, state: PlayerState) -> str:
        """Listen to employee conversations in Stark Tower."""
        print_slow("You find a quiet spot near the employee café and listen to conversations.")
        print_slow("You overhear talk about new security protocols, Avengers sightings, and company gossip.")
        
        # Gain some intelligence
        print_slow("\nYou learn that Tony Stark is working on a new energy project with Dr. Banner.")
        
        # Small chance to be noticed
        if random.random() < 0.2:  # 20% chance
            print_slow("\nA security guard notices your eavesdropping and approaches you.")
            print_slow("'Can I see your badge, please?' he asks firmly.")
            
            if "Stark Tower Visitor Badge" in state.inventory:
                print_slow("You show the visitor badge you found earlier. He nods and moves on.")
                print_slow("That was close!")
            else:
                print_slow("Without a badge, you're escorted to the exit.")
                print_slow("'Please don't return without proper authorization,' the guard warns.")
                state.adjust_reputation("mcu", -5)
                print(f"{Fore.RED}Reputation decreased by 5{Style.RESET_ALL}")
        else:
            state.adjust_reputation("mcu", 5)
            print(f"{Fore.GREEN}Reputation increased by 5{Style.RESET_ALL}")
        
        return self.current_scene
    
    def _help_lost_child(self, state: PlayerState) -> str:
        """Help a child who lost their parent in Central Park."""
        print_slow("You notice a small child crying near a park bench, clearly separated from their parents.")
        print_slow("You approach carefully and ask if they need help finding their family.")
        
        print_slow("\nThe child looks at you with tearful eyes and nods.")
        print_slow("You help them locate a park ranger, who uses their radio to contact the child's parents.")
        print_slow("Soon, a relieved mother arrives, thanking you profusely for your help.")
        
        state.adjust_morality(10)
        print(f"{Fore.GREEN}Morality increased by 10{Style.RESET_ALL}")
        
        # Easter egg - small chance the parent is connected to the story
        if random.random() < 0.2:  # 20% chance
            print_slow("\n'How can I repay you?' the mother asks.")
            print_slow("You notice a S.H.I.E.L.D. logo partially visible on her identification card.")
            print_slow("'I'm just happy to help,' you reply, but she slips you her card anyway.")
            print_slow("'If you ever need anything,' she whispers, 'call this number.'")
            state.add_item("S.H.I.E.L.D. Agent's Card")
            print(f"{Fore.GREEN}Item added to inventory: S.H.I.E.L.D. Agent's Card{Style.RESET_ALL}")
            state.adjust_reputation("mcu", 10)
            print(f"{Fore.GREEN}Reputation increased by 10{Style.RESET_ALL}")
        
        return self.current_scene
    
    def _investigate_energy(self, state: PlayerState) -> str:
        """Investigate a strange energy signature in Central Park."""
        print_slow("You're drawn to a secluded area of the park where the air seems to shimmer strangely.")
        print_slow("As you approach, your fracture key begins to pulse with an answering energy.")
        
        print_slow("\nYou cautiously examine the area, finding a small, glowing artifact half-buried in the ground.")
        print_slow("It seems to be of alien origin, possibly related to the Chitauri invasion.")
        
        print("\nWhat do you do with the artifact?")
        print("1. Take it with you")
        print("2. Leave it alone")
        print("3. Report it to authorities")
        
        subchoice = input("\nEnter your choice (1-3): ")
        
        if subchoice == "1":
            print_slow("You carefully pick up the artifact and pocket it.")
            print_slow("It hums with power against your fracture key.")
            state.add_item("Chitauri Energy Core")
            print(f"{Fore.GREEN}Item added to inventory: Chitauri Energy Core{Style.RESET_ALL}")
            state.adjust_morality(-5)
            print(f"{Fore.YELLOW}Morality decreased by 5{Style.RESET_ALL}")
            
            # Memory trigger from alien tech
            print_slow("As you hold the alien technology, flashes of memory surface...")
            state.adjust_memory_sync(3)
            print(f"{Fore.BLUE}Memory sync increased by 3%{Style.RESET_ALL}")
        elif subchoice == "2":
            print_slow("You decide it's safer to leave the artifact untouched.")
            print_slow("Who knows what kind of alien technology it might be?")
        else:
            print_slow("You find a police officer and report the strange object.")
            print_slow("Within minutes, a team in unmarked vehicles arrives to secure the area.")
            print_slow("A woman in a suit nods to you in thanks before asking you to move along.")
            state.adjust_morality(5)
            print(f"{Fore.GREEN}Morality increased by 5{Style.RESET_ALL}")
            state.adjust_reputation("mcu", 5)
            print(f"{Fore.GREEN}Reputation increased by 5{Style.RESET_ALL}")
        
        return self.current_scene
    
    def _go_to_sanctum(self, state: PlayerState) -> str:
        """Visit the New York Sanctum."""
        print_slow("You make your way to a peculiar building on Bleecker Street.")
        print_slow("Something tells you this is no ordinary townhouse - it's the New York Sanctum.")
        
        print_slow("\nAs you approach the door, it opens on its own, as if inviting you inside.")
        
        return self._change_scene("sanctum", state)
    
    def _speak_with_fury(self, state: PlayerState) -> str:
        """Try to speak with Nick Fury at S.H.I.E.L.D. HQ."""
        print_slow("You attempt to arrange a meeting with Director Fury, but it's not easy to get through security.")
        
        # Check if player has items that could help
        has_credentials = "S.H.I.E.L.D. Communicator" in state.inventory or "S.H.I.E.L.D. Agent's Card" in state.inventory
        
        if has_credentials:
            if "S.H.I.E.L.D. Communicator" in state.inventory:
                print_slow("You show the S.H.I.E.L.D. Communicator you found earlier.")
            else:
                print_slow("You show the S.H.I.E.L.D. Agent's card you received in the park.")
            
            print_slow("The security officer examines it carefully, then makes a call.")
            print_slow("'Director Fury will see you for five minutes,' he says, looking surprised himself.")
            
            print_slow("\nYou're escorted to a sparse office where Nick Fury stands looking out the window.")
            print_slow("'I don't know who you are,' he says without turning, 'but you've got my attention.'")
            print_slow("'I know when something doesn't belong in this universe. What's your story?'")
            
            state.adjust_reputation("mcu", 15)
            print(f"{Fore.GREEN}Reputation increased by 15{Style.RESET_ALL}")
            
            # Memory trigger from meeting a key character
            print_slow("\nSomething about Fury's perceptiveness triggers a memory...")
            state.adjust_memory_sync(5)
            print(f"{Fore.BLUE}Memory sync increased by 5%{Style.RESET_ALL}")
        else:
            print_slow("Without any credentials, you're quickly turned away from the restricted areas.")
            print_slow("'This area is off-limits to civilians,' a stern agent informs you.")
        
        return self.current_scene
    
    def _access_shield_terminal(self, state: PlayerState) -> str:
        """Try to access a S.H.I.E.L.D. computer terminal."""
        print_slow("You spot an unattended computer terminal and decide to try your luck.")
        
        # Check difficulty based on player's items
        if "S.H.I.E.L.D. Communicator" in state.inventory:
            success_chance = 0.6  # 60% chance with communicator
        else:
            success_chance = 0.3  # 30% chance without
        
        if random.random() < success_chance:
            print_slow("You manage to access the system, quickly searching for useful information.")
            print_slow("Files mention the 'Multiverse Initiative' - S.H.I.E.L.D. is aware of other realities!")
            print_slow("You download some data before logging out.")
            state.add_item("S.H.I.E.L.D. Multiverse Data")
            print(f"{Fore.GREEN}Item added to inventory: S.H.I.E.L.D. Multiverse Data{Style.RESET_ALL}")
            
            # Good for memory, bad for morality (stealing data)
            state.adjust_memory_sync(5)
            print(f"{Fore.BLUE}Memory sync increased by 5%{Style.RESET_ALL}")
            state.adjust_morality(-10)
            print(f"{Fore.YELLOW}Morality decreased by 10{Style.RESET_ALL}")
        else:
            print_slow("As you attempt to access the terminal, an alarm sounds!")
            print_slow("'Security breach in sector four!' announces a computerized voice.")
            print_slow("You quickly back away, trying to look innocent as agents rush toward the computer.")
            state.adjust_reputation("mcu", -15)
            print(f"{Fore.RED}Reputation decreased by 15{Style.RESET_ALL}")
        
        return self.current_scene
    
    def _examine_artifacts(self, state: PlayerState) -> str:
        """Examine the mystical artifacts in the Sanctum."""
        print_slow("You carefully examine the various mystical artifacts on display in the Sanctum.")
        print_slow("Strange relics from different dimensions and times line the walls and display cases.")
        
        print_slow("\nOne artifact in particular catches your eye - a small amulet that seems to shimmer between realities.")
        print_slow("As you approach it, your fracture key resonates with it, creating a harmonic hum.")
        
        print("\nWhat do you do?")
        print("1. Touch the amulet")
        print("2. Step back from it")
        print("3. Look for information about it")
        
        subchoice = input("\nEnter your choice (1-3): ")
        
        if subchoice == "1":
            print_slow("As your fingers touch the amulet, visions flood your mind!")
            print_slow("You see countless realities, timelines splitting and merging...")
            print_slow("The experience is overwhelming but enlightening.")
            
            state.adjust_memory_sync(10)
            print(f"{Fore.BLUE}Memory sync increased by 10%{Style.RESET_ALL}")
            
            print_slow("\n'The Amulet of Multiversal Awareness shows different things to different people.'")
            print_slow("An Asian man in robes has appeared beside you. 'I'm Wong. And you're not from here, are you?'")
        elif subchoice == "2":
            print_slow("You wisely step back from the amulet, sensing its power might be dangerous.")
            print_slow("'A prudent choice,' says a voice behind you. 'Not all who wander between realities have such caution.'")
            print_slow("A tall man in blue robes introduces himself as Doctor Strange, Master of the Mystic Arts.")
        else:
            print_slow("You look around for information about the amulet and find an ancient text nearby.")
            print_slow("Before you can read it, a woman in yellow robes approaches.")
            print_slow("'The Ancient One would like to speak with you, traveler between worlds,' she says.")
            state.adjust_reputation("mcu", 10)
            print(f"{Fore.GREEN}Reputation increased by 10{Style.RESET_ALL}")
        
        return self.current_scene
    
    def _speak_with_master(self, state: PlayerState) -> str:
        """Speak with a Master of the Mystic Arts."""
        print_slow("You approach one of the robed figures moving through the Sanctum.")
        print_slow("'Excuse me,' you begin, but they speak before you can continue.")
        
        print_slow("\n'We've been expecting someone like you,' they say. 'A fracture in the multiverse was detected.'")
        print_slow("They explain that the Masters of the Mystic Arts protect reality from interdimensional threats.")
        print_slow("'Your fracture key is of great interest to us. It contains power similar to the Infinity Stones.'")
        
        print("\nHow do you respond?")
        print("1. Ask for their help understanding the multiverse")
        print("2. Inquire about the Infinity Stones")
        print("3. Ask if they can help repair your fracture key")
        
        subchoice = input("\nEnter your choice (1-3): ")
        
        if subchoice == "1":
            print_slow("The master seems pleased by your question and offers some guidance.")
            print_slow("'The multiverse is infinite, with realities branching at every decision point.'")
            print_slow("'Your fracture from your home reality has created ripples we can detect.'")
            
            state.adjust_memory_sync(7)
            print(f"{Fore.BLUE}Memory sync increased by 7%{Style.RESET_ALL}")
        elif subchoice == "2":
            print_slow("'The Infinity Stones are six singularities that existed before creation itself,'")
            print_slow("the master explains. 'They each control an essential aspect of existence.'")
            print_slow("'Your fracture key seems to resonate with the Space Stone in particular.'")
            
            state.adjust_reputation("mcu", 5)
            print(f"{Fore.GREEN}Reputation increased by 5{Style.RESET_ALL}")
        else:
            print_slow("The master examines your fracture key without touching it.")
            print_slow("'Its damage is beyond our ability to repair directly,' they admit.")
            print_slow("'But collecting fragments from each reality should restore its power.'")
            print_slow("'This universe has a fragment waiting for you to claim it.'")
            
            # Help player with a hint
            print_slow("\nThey point you toward a specific display case in the main hall.")
            print_slow("Inside is a small crystalline structure that resembles a piece of your key.")
        
        return self.current_scene
    
    def _use_communicator(self, state: PlayerState) -> str:
        """Use the S.H.I.E.L.D. Communicator found earlier."""
        print_slow("You activate the S.H.I.E.L.D. Communicator, wondering who might answer.")
        print_slow("After a moment of static, a voice responds: 'This is Agent Hill. Identify yourself.'")
        
        print("\nHow do you respond?")
        print("1. 'I'm a traveler from another reality seeking information.'")
        print("2. 'I found this communicator and was curious who would answer.'")
        print("3. 'I need to speak with Director Fury about an interdimensional threat.'")
        
        subchoice = input("\nEnter your choice (1-3): ")
        
        if subchoice == "1":
            print_slow("There's a long pause before Agent Hill responds.")
            print_slow("'Stay where you are. A team will meet you shortly to discuss your... situation.'")
            print_slow("True to her word, S.H.I.E.L.D. agents arrive within minutes to escort you.")
            return self._change_scene("shield_hq", state)
        elif subchoice == "2":
            print_slow("'That's S.H.I.E.L.D. property,' Agent Hill says coldly. 'Return it immediately.'")
            print_slow("The communicator's GPS activates, and you realize they can track your location.")
            state.adjust_reputation("mcu", -5)
            print(f"{Fore.RED}Reputation decreased by 5{Style.RESET_ALL}")
        else:
            print_slow("'Another one,' sighs Agent Hill. 'What kind of interdimensional threat?'")
            print_slow("No matter what you say, she sounds skeptical but takes your information.")
            print_slow("'Director Fury will be informed. Do not leave your current location.'")
            state.adjust_reputation("mcu", 5)
            print(f"{Fore.GREEN}Reputation increased by 5{Style.RESET_ALL}")
        
        return self.current_scene
    
    def _request_resources(self, state: PlayerState) -> str:
        """Request resources from S.H.I.E.L.D. (high reputation required)."""
        print_slow("With the respect you've earned, you formally request assistance from S.H.I.E.L.D.")
        print_slow("Your request is processed and approved surprisingly quickly.")
        
        print_slow("\nAn agent provides you with a small kit of essential items.")
        state.add_item("S.H.I.E.L.D. Field Kit")
        print(f"{Fore.GREEN}Item added to inventory: S.H.I.E.L.D. Field Kit{Style.RESET_ALL}")
        
        print_slow("'Director Fury says you're to be treated as a consultant on interdimensional matters,'")
        print_slow("the agent explains. 'The kit contains standard field equipment and emergency contacts.'")
        
        state.adjust_reputation("mcu", 10)
        print(f"{Fore.GREEN}Reputation increased by 10{Style.RESET_ALL}")
        
        return self.current_scene
    
    def _exit_universe(self, state: PlayerState) -> str:
        """Use the fracture key to exit the universe."""
        print_slow("You find a quiet spot and take out your fracture key.")
        print_slow("It pulses with energy, ready to tear a hole in reality and take you back to the void.")
        
        if confirm_action("use your fracture key to exit this universe"):
            state.use_fracture_key_charge()
            return "exit"
            
        print_slow("You decide to stay a little longer in this universe.")
        return self.current_scene