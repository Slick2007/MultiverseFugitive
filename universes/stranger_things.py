"""
Stranger Things universe module for Multiverse Fugitive.
"""

from typing import List, Dict, Any
import random
import time
import colorama
from colorama import Fore, Style

from core import Universe, PlayerState, Choice
from utils import print_slow, clear_screen, confirm_action

colorama.init(autoreset=True)

class StrangerThingsUniverse(Universe):
    """
    The Stranger Things universe set in Hawkins, Indiana during the 1980s.
    
    Players navigate the mysterious town where supernatural events and
    government conspiracies threaten the residents.
    """
    
    name = "Stranger Things"
    description = "Explore the mysterious town of Hawkins, Indiana in the 1980s, where supernatural forces lurk."
    
    def __init__(self):
        # Track the current scene/location
        self.current_scene = "awakening"
        
        # Characters to keep track of
        self.characters = {
            "eleven": {
                "name": "Eleven",
                "description": "A young girl with psychokinetic abilities who escaped from Hawkins Lab."
            },
            "hopper": {
                "name": "Jim Hopper",
                "description": "Hawkins Chief of Police investigating the strange occurrences."
            },
            "joyce": {
                "name": "Joyce Byers",
                "description": "A determined mother searching for her missing son."
            },
            "mike": {
                "name": "Mike Wheeler",
                "description": "Leader of a group of friends who call themselves 'The Party'."
            },
            "brenner": {
                "name": "Dr. Martin Brenner",
                "description": "The scientist in charge of Hawkins Lab, referred to as 'Papa' by Eleven."
            }
        }
        
        # Scenes/locations in this universe
        self.scenes = {
            "awakening": {
                "description": "You wake up on the outskirts of Hawkins, Indiana. It's 1983, and the air is thick with summer heat. In the distance, you can see the small town nestled among trees, and further away, the imposing silhouette of Hawkins National Laboratory.",
                "first_visit": True
            },
            "hawkins_town": {
                "description": "The small town of Hawkins has a quaint, 80s charm. The streets are lined with local shops, there's a movie theater playing 'Back to the Future', and kids ride bikes freely. Despite the seeming normalcy, there's a tension in the air.",
                "first_visit": True
            },
            "hawkins_lab": {
                "description": "Hawkins National Laboratory looms behind tall fences topped with barbed wire. The facility is guarded by men in uniforms, and 'Restricted Area' signs are posted prominently. Whatever happens inside is meant to stay secret.",
                "first_visit": True
            },
            "the_upside_down": {
                "description": "A dark, twisted reflection of the real world. Ash-like particles float in the air, strange vines cover surfaces, and an eerie blue glow permeates everything. The atmosphere is toxic, and strange sounds echo in the distance.",
                "first_visit": True
            },
            "byers_house": {
                "description": "The Byers family home sits at the edge of town. Christmas lights are strung up throughout the house, and the walls are covered in hand-drawn maps and pictures. An atmosphere of desperation and determination fills the air.",
                "first_visit": True
            }
        }
    
    def on_entry(self, state: PlayerState) -> None:
        """Called when the player enters the Stranger Things universe."""
        clear_screen()
        print(f"{Fore.CYAN}===== ENTERING UNIVERSE: {self.name} ====={Style.RESET_ALL}\n")
        
        # Add to visited universes
        state.visited_universes.add("stranger_things")
        
        # Initialize reputation for this universe if first visit
        if "stranger_things" not in state.reputation:
            state.reputation["stranger_things"] = 0
        
        # Intro narration
        print_slow(f"{Fore.YELLOW}Hawkins, Indiana - Summer 1983{Style.RESET_ALL}")
        time.sleep(0.5)
        
        # Display the awakening scene
        self._show_scene_description("awakening")
        
        # Additional intro text
        print_slow("Your fracture key pulses with a strange energy, almost as if responding to something in this world.")
        print_slow("In the distance, you hear the sound of sirens, and a voice on a loudspeaker making an announcement.")
        
        # Player choice on how to react to waking up
        print("\nWhat do you do?")
        print("1. Try to remember what you know about this place")
        print("2. Head toward the town of Hawkins")
        print("3. Investigate the source of the sirens")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == "1":
            print_slow("You concentrate, trying to recall information about this universe.")
            print_slow("Images flash in your mind: a girl with a shaved head, a creature with no face, christmas lights blinking with messages...")
            state.adjust_memory_sync(5)
            print(f"{Fore.BLUE}Memory sync increased by 5%{Style.RESET_ALL}")
        elif choice == "2":
            print_slow("You decide to head toward the town to orient yourself and gather information.")
            print_slow("As you walk, you notice a discarded 'Hawkins Lab' ID badge in the grass.")
            state.add_item("Hawkins Lab ID Badge")
            print(f"{Fore.GREEN}Item added to inventory: Hawkins Lab ID Badge{Style.RESET_ALL}")
        else:
            print_slow("You follow the sound of the sirens toward Hawkins National Laboratory.")
            print_slow("From behind a tree, you observe men in hazmat suits entering the facility.")
            print_slow("Something has gone very wrong there...")
            state.adjust_morality(-5)  # Slight moral ambiguity in spying
            print(f"{Fore.YELLOW}Morality decreased by 5{Style.RESET_ALL}")
        
        print_slow("\nThe air in Hawkins feels charged with an unnatural energy. Something is happening in this town, something beyond normal understanding.")
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
                Choice(1, "Head to Hawkins town center", self._go_to_hawkins_town),
                Choice(2, "Investigate Hawkins National Laboratory", self._go_to_hawkins_lab),
                Choice(3, "Follow the train tracks through the woods", self._follow_tracks)
            ]
            
        elif self.current_scene == "hawkins_town":
            choices = [
                Choice(1, "Visit the local police station", self._visit_police_station),
                Choice(2, "Check out the arcade where kids hang out", self._visit_arcade),
                Choice(3, "Look for unusual news in the local newspaper", self._read_newspaper)
            ]
            
            # Add conditional choice if player knows about the Byers
            if "Joyce's Address" in state.inventory:
                choices.append(Choice(4, "Visit the Byers family home", self._go_to_byers_house))
            
        elif self.current_scene == "hawkins_lab":
            choices = [
                Choice(1, "Try to gain access to the lab", self._enter_lab),
                Choice(2, "Monitor the employees coming and going", self._monitor_lab),
                Choice(3, "Look for unusual phenomena around the perimeter", self._investigate_perimeter)
            ]
            
            # Add conditional choice if player has lab badge
            if "Hawkins Lab ID Badge" in state.inventory:
                choices.append(Choice(4, "Use the ID badge to enter the facility", self._use_lab_badge))
            
        elif self.current_scene == "the_upside_down":
            choices = [
                Choice(1, "Look for a way back to the normal world", self._find_exit_portal),
                Choice(2, "Search for signs of other humans", self._search_for_people),
                Choice(3, "Collect a sample from the environment", self._collect_sample)
            ]
            
            # Add conditional choice based on items
            if "Compass" in state.inventory:
                choices.append(Choice(4, "Use the compass to navigate", self._use_compass))
            
        elif self.current_scene == "byers_house":
            choices = [
                Choice(1, "Speak with Joyce Byers", self._speak_with_joyce),
                Choice(2, "Examine the Christmas light communication system", self._examine_lights),
                Choice(3, "Look at Will's drawings of the shadow monster", self._examine_drawings)
            ]
            
            # Add conditional choice based on reputation
            if state.reputation.get("stranger_things", 0) >= 20:
                choices.append(Choice(4, "Offer to help find Will", self._offer_help))
        
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
        """Called when the player exits the Stranger Things universe."""
        clear_screen()
        print(f"{Fore.CYAN}===== EXITING UNIVERSE: {self.name} ====={Style.RESET_ALL}\n")
        
        # Add key fragment if this is the first time completing the universe
        if "stranger_things" not in state.key_fragments:
            print_slow("As you activate your fracture key, it interacts with the thin barrier between dimensions in this reality.")
            print_slow("A spark of energy from the Upside Down attaches to your key, forming a new fragment.")
            state.add_key_fragment("stranger_things")
            print(f"{Fore.YELLOW}Key Fragment acquired: Stranger Things{Style.RESET_ALL}")
        
        # Final messages based on reputation
        rep = state.reputation.get("stranger_things", 0)
        if rep >= 50:
            print_slow(f"Chief Hopper nods at you as you prepare to leave.")
            print_slow(f"'I don't know who or what you are,' he says, 'but Hawkins is a little safer because of you.'")
            print_slow(f"Eleven reaches out and touches your hand. 'Friend,' she says simply.")
        elif rep >= 20:
            print_slow(f"You've made some allies in Hawkins, but many questions remain unanswered.")
            print_slow(f"The mysteries of the Upside Down and Hawkins Lab will continue without you.")
        else:
            print_slow(f"You leave Hawkins largely as you found it - full of secrets and dangers.")
            print_slow(f"The boundary between worlds remains thin here, a perfect reflection of your own journey.")
        
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
    def _go_to_hawkins_town(self, state: PlayerState) -> str:
        """Go to Hawkins town center."""
        print_slow("You make your way toward the small town of Hawkins.")
        print_slow("The streets are lined with shops, and 80s music plays from car radios.")
        return self._change_scene("hawkins_town", state)
    
    def _go_to_hawkins_lab(self, state: PlayerState) -> str:
        """Go to Hawkins National Laboratory."""
        print_slow("You approach the imposing facility of Hawkins National Laboratory.")
        print_slow("The tall fences and armed guards speak of government secrets and danger.")
        return self._change_scene("hawkins_lab", state)
    
    def _follow_tracks(self, state: PlayerState) -> str:
        """Follow the train tracks through the woods."""
        print_slow("You follow the abandoned train tracks that run through the woods.")
        print_slow("After walking for a while, you come to a clearing where the tracks diverge.")
        
        print("\nWhich way do you go?")
        print("1. Follow the tracks toward town")
        print("2. Follow the tracks deeper into the woods")
        print("3. Investigate a strange sound nearby")
        
        subchoice = input("\nEnter your choice (1-3): ")
        
        if subchoice == "1":
            print_slow("You follow the tracks toward civilization and soon reach Hawkins town.")
            return self._change_scene("hawkins_town", state)
        elif subchoice == "2":
            print_slow("The tracks lead deeper into the increasingly dark and misty woods.")
            print_slow("You begin to feel a strange sensation, as if reality is thinning around you.")
            
            # Small chance to slip into the Upside Down
            if random.random() < 0.3:  # 30% chance
                print_slow("\nSuddenly, the world seems to flicker and distort around you.")
                print_slow("The trees become twisted, covered in strange vines, and ash floats in the air.")
                print_slow("You've somehow crossed into the Upside Down!")
                
                # Memory trigger from other dimension
                print_slow("\nBeing in this twisted mirror world triggers memories of other realities you've visited...")
                state.adjust_memory_sync(7)
                print(f"{Fore.BLUE}Memory sync increased by 7%{Style.RESET_ALL}")
                
                return self._change_scene("the_upside_down", state)
            else:
                print_slow("\nEventually, you reach a junkyard where a group of kids have built a fortress.")
                print_slow("They're talking about something called 'the Demogorgon' and 'the Upside Down'.")
                state.adjust_reputation("stranger_things", 5)
                print(f"{Fore.GREEN}Reputation increased by 5{Style.RESET_ALL}")
                return self._change_scene("hawkins_town", state)
        else:
            print_slow("You venture off the tracks to investigate a strange sound.")
            print_slow("You find a broken compass spinning wildly, as if affected by a strong magnetic field.")
            state.add_item("Compass")
            print(f"{Fore.GREEN}Item added to inventory: Compass{Style.RESET_ALL}")
            print_slow("\nReturning to the tracks, you decide to head toward town.")
            return self._change_scene("hawkins_town", state)
    
    def _visit_police_station(self, state: PlayerState) -> str:
        """Visit the Hawkins Police Station."""
        print_slow("You enter the Hawkins Police Station, a small building with only a few officers on duty.")
        print_slow("Chief Jim Hopper is hunched over maps, looking stressed and tired.")
        
        print("\nWhat do you do?")
        print("1. Approach Hopper directly")
        print("2. Listen to the police radio chatter")
        print("3. Look at the missing persons bulletin board")
        
        subchoice = input("\nEnter your choice (1-3): ")
        
        if subchoice == "1":
            print_slow("You approach Chief Hopper, who eyes you suspiciously.")
            print_slow("'Can I help you?' he asks gruffly, clearly overworked and irritable.")
            
            print("\nHow do you respond?")
            print("1. 'I've noticed strange things happening in town.'")
            print("2. 'I'm new in town and wanted to introduce myself.'")
            print("3. 'I might have information about Hawkins Lab.'")
            
            response = input("\nEnter your choice (1-3): ")
            
            if response == "1":
                print_slow("Hopper's expression changes, becoming more alert.")
                print_slow("'What kind of strange things?' he asks, lowering his voice.")
                print_slow("You describe some of the unusual energy and phenomena you've noticed.")
                print_slow("He studies you for a moment. 'Come back if you see anything specific.'")
                state.adjust_reputation("stranger_things", 10)
                print(f"{Fore.GREEN}Reputation increased by 10{Style.RESET_ALL}")
            elif response == "2":
                print_slow("'Welcome to Hawkins,' he says flatly. 'Try to stay out of trouble.'")
                print_slow("It's clear he has more important things on his mind than new residents.")
            else:
                print_slow("Hopper immediately pulls you into his office and closes the door.")
                print_slow("'What do you know about the lab?' he demands, suddenly intense.")
                print_slow("Your conversation is brief but meaningful. He's clearly investigating them too.")
                state.adjust_reputation("stranger_things", 15)
                print(f"{Fore.GREEN}Reputation increased by 15{Style.RESET_ALL}")
        elif subchoice == "2":
            print_slow("You linger near the police radio, listening to the chatter.")
            print_slow("There are reports of power fluctuations, magnetic anomalies, and missing pets.")
            print_slow("One officer mentions 'another incident at the Byers house' with concern.")
            
            # Note Joyce's address
            state.add_item("Joyce's Address")
            print(f"{Fore.GREEN}Item added to inventory: Joyce's Address{Style.RESET_ALL}")
        else:
            print_slow("You examine the missing persons board, which has several recent additions.")
            print_slow("Most prominent is the case of Will Byers, a young boy who vanished recently.")
            print_slow("There's something odd about the case - the report mentions his body was found, but the poster hasn't been taken down.")
            
            # Memory trigger from anomaly
            if random.random() < 0.4:  # 40% chance
                print_slow("\nSomething about the contradictory information triggers a memory...")
                print_slow("You recall fragments of knowledge about reality distortions and parallel dimensions.")
                state.adjust_memory_sync(3)
                print(f"{Fore.BLUE}Memory sync increased by 3%{Style.RESET_ALL}")
        
        return self.current_scene
    
    def _visit_arcade(self, state: PlayerState) -> str:
        """Visit the arcade where kids hang out."""
        print_slow("You enter the Palace Arcade, filled with the sounds of video games and excited kids.")
        print_slow("A group of boys are arguing intensely over a game of Dig Dug.")
        
        print_slow("\nAs you watch, you realize these must be Mike, Lucas, and Dustin - the friends of the missing Will Byers.")
        print_slow("Their conversation occasionally drops references to 'the Vale of Shadows' and 'campaign strategies'.")
        
        print("\nWhat do you do?")
        print("1. Approach the kids and talk to them")
        print("2. Play some arcade games nearby to listen")
        print("3. Follow them when they leave")
        
        subchoice = input("\nEnter your choice (1-3): ")
        
        if subchoice == "1":
            print_slow("You approach the kids, who immediately go quiet and eye you suspiciously.")
            print_slow("'Are you from the lab?' the one wearing a baseball cap asks directly.")
            
            print("\nHow do you respond?")
            print("1. 'No, I'm just new in town.'")
            print("2. 'I'm looking for answers about strange things happening here.'")
            print("3. 'What lab are you talking about?'")
            
            response = input("\nEnter your choice (1-3): ")
            
            if response == "1":
                print_slow("They relax slightly but remain guarded.")
                print_slow("'Well, welcome to Hawkins,' says the boy with curly hair. 'Nothing interesting ever happens here.'")
                print_slow("Their forced smiles make it clear they're hiding something.")
            elif response == "2":
                print_slow("The boys exchange significant looks.")
                print_slow("'We might know some things,' the boy in the baseball cap says cautiously.")
                print_slow("'But we need to know we can trust you first.'")
                state.adjust_reputation("stranger_things", 10)
                print(f"{Fore.GREEN}Reputation increased by 10{Style.RESET_ALL}")
            else:
                print_slow("'Never mind,' says the boy with the baseball cap, and they quickly gather their things.")
                print_slow("As they leave, you hear one whisper, 'Do you think they sent another spy?'")
                state.adjust_reputation("stranger_things", -5)
                print(f"{Fore.RED}Reputation decreased by 5{Style.RESET_ALL}")
        elif subchoice == "2":
            print_slow("You insert a quarter into Dig Dug and pretend to play while listening.")
            print_slow("Their conversation reveals they're searching for their friend Will, who they believe isn't really dead.")
            print_slow("They mention someone named 'Eleven' with special powers who might help them.")
            
            # Find a useful item
            print_slow("\nWhen the boys leave, you notice they dropped a hand-drawn map of Hawkins.")
            state.add_item("Kids' Map of Hawkins")
            print(f"{Fore.GREEN}Item added to inventory: Kids' Map of Hawkins{Style.RESET_ALL}")
        else:
            print_slow("You discreetly follow the boys as they leave the arcade on their bikes.")
            print_slow("They head to a junkyard where they've built some kind of communication device.")
            print_slow("You overhear them discussing 'the gate' and 'the Upside Down' before you have to back away to avoid detection.")
            
            state.adjust_morality(-10)  # Following kids is definitely questionable
            print(f"{Fore.YELLOW}Morality decreased by 10{Style.RESET_ALL}")
            state.adjust_reputation("stranger_things", 5)  # But you learned valuable info
            print(f"{Fore.GREEN}Reputation increased by 5{Style.RESET_ALL}")
        
        return self.current_scene
    
    def _read_newspaper(self, state: PlayerState) -> str:
        """Check the local newspaper for unusual news."""
        print_slow("You pick up a copy of the Hawkins Post from a newspaper box.")
        print_slow("The front page features a story about 'toxic chemical leaks' from Hawkins Lab.")
        print_slow("There's also an obituary for Will Byers, alongside reports of unusual power outages.")
        
        # Memory trigger
        if random.random() < 0.3:  # 30% chance
            print_slow("\nSomething about the contradictory reports triggers a memory...")
            print_slow("You recall how governments often use cover stories to hide supernatural events.")
            state.adjust_memory_sync(3)
            print(f"{Fore.BLUE}Memory sync increased by 3%{Style.RESET_ALL}")
        
        return self.current_scene
    
    def _enter_lab(self, state: PlayerState) -> str:
        """Try to gain access to Hawkins Lab."""
        print_slow("You approach the main entrance of Hawkins Lab, trying to look like you belong.")
        print_slow("A stern-faced guard stops you. 'ID badge?' he demands.")
        
        if "Hawkins Lab ID Badge" in state.inventory:
            print_slow("You show the ID badge you found earlier. The guard scrutinizes it carefully.")
            
            # Success chance based on reputation
            success_chance = 0.3 + (state.reputation.get("stranger_things", 0) / 200)  # Base 30% + up to 25% from reputation
            
            if random.random() < success_chance:
                print_slow("He nods and waves you through. 'New transfer?' he asks casually.")
                print_slow("You mumble an affirmative response and hurry inside before he can ask more questions.")
                
                print_slow("\nInside, the lab is sterile and intimidating. Scientists in white coats move purposefully.")
                print_slow("Signs point to different departments: 'Biomedical Research', 'Energy Project', and most intriguingly, 'Special Subjects'.")
                
                # Reputation boost for infiltrating the lab
                state.adjust_reputation("stranger_things", 15)
                print(f"{Fore.GREEN}Reputation increased by 15{Style.RESET_ALL}")
                
                # Memory trigger from government facility
                print_slow("\nThe clinical environment and secretive atmosphere trigger a memory...")
                print_slow("You've been in places like this before, in other universes.")
                state.adjust_memory_sync(5)
                print(f"{Fore.BLUE}Memory sync increased by 5%{Style.RESET_ALL}")
            else:
                print_slow("'This badge is for maintenance. You need an escort,' he says suspiciously.")
                print_slow("'Wait here while I call this in.'")
                print_slow("You decide it's best to retreat before things get worse.")
                state.adjust_reputation("stranger_things", -5)
                print(f"{Fore.RED}Reputation decreased by 5{Style.RESET_ALL}")
        else:
            print_slow("Without an ID badge, there's no way past the guard.")
            print_slow("'No unauthorized personnel,' he states firmly. 'Please leave the premises.'")
        
        return self.current_scene
    
    def _monitor_lab(self, state: PlayerState) -> str:
        """Monitor the employees coming and going from the lab."""
        print_slow("You find a concealed spot with a good view of the lab entrance and settle in to watch.")
        print_slow("Throughout the day, you observe scientists, military personnel, and maintenance workers.")
        
        print_slow("\nAs evening approaches, you notice something odd - a delivery van arrives, but when it leaves, it sits lower on its suspension.")
        print_slow("Whatever they're bringing out of the lab, it's heavy and they're trying to be discreet about it.")
        
        # Possible reward for patience
        if random.random() < 0.4:  # 40% chance
            print_slow("\nAs you're about to leave, you notice a researcher drop something while rushing to their car.")
            print_slow("After they drive away, you investigate and find a security keycard.")
            state.add_item("Hawkins Lab Keycard")
            print(f"{Fore.GREEN}Item added to inventory: Hawkins Lab Keycard{Style.RESET_ALL}")
        
        return self.current_scene
    
    def _investigate_perimeter(self, state: PlayerState) -> str:
        """Look for unusual phenomena around the lab perimeter."""
        print_slow("You carefully circle the perimeter of the lab facility, staying hidden in the treeline.")
        print_slow("In several spots, the vegetation is dying in unusual patterns. Your fracture key pulses in response.")
        
        print_slow("\nBehind the facility, you discover a drainage pipe leading from the lab into the woods.")
        print_slow("The area around it feels wrong somehow - the air shimmers slightly, and there's an electric feeling.")
        
        print("\nWhat do you do?")
        print("1. Enter the drainage pipe")
        print("2. Take a sample of the affected soil")
        print("3. Continue observing from a safe distance")
        
        subchoice = input("\nEnter your choice (1-3): ")
        
        if subchoice == "1":
            print_slow("You crawl into the rusted drainage pipe, moving carefully to avoid making noise.")
            print_slow("The pipe is damp and slimy, but large enough to navigate while crouching.")
            
            # Risk of entering the Upside Down
            if random.random() < 0.4:  # 40% chance
                print_slow("\nAs you move deeper, the pipe seems to change. The metal becomes covered in strange growth.")
                print_slow("The air grows thick with floating particles, and you realize with a shock that you've crossed over into the Upside Down.")
                
                # Memory trigger from dimensional shift
                print_slow("\nThe transition between dimensions feels disturbingly familiar...")
                state.adjust_memory_sync(8)
                print(f"{Fore.BLUE}Memory sync increased by 8%{Style.RESET_ALL}")
                
                return self._change_scene("the_upside_down", state)
            else:
                print_slow("\nThe pipe eventually leads to a grate inside the lab's lower level.")
                print_slow("Through it, you can see a high-security area with armed guards and scientists in hazmat suits.")
                print_slow("They appear to be monitoring some kind of containment breach.")
                
                state.adjust_reputation("stranger_things", 10)
                print(f"{Fore.GREEN}Reputation increased by 10{Style.RESET_ALL}")
            
        elif subchoice == "2":
            print_slow("You collect a sample of the strange soil in an empty candy wrapper from your pocket.")
            print_slow("The dirt glitters with an unnatural residue and seems to move slightly when touched.")
            state.add_item("Contaminated Soil Sample")
            print(f"{Fore.GREEN}Item added to inventory: Contaminated Soil Sample{Style.RESET_ALL}")
        else:
            print_slow("You continue observing from a safe distance, taking mental notes of the patterns.")
            print_slow("Eventually, you see a group of hazmat-suited scientists emerge, carrying collection equipment.")
            print_slow("They take samples from the same areas you found suspicious, confirming your instincts.")
        
        return self.current_scene
    
    def _use_lab_badge(self, state: PlayerState) -> str:
        """Use the ID badge to enter Hawkins Lab."""
        print_slow("With the Hawkins Lab ID badge in hand, you approach the security checkpoint confidently.")
        print_slow("The guard glances at your badge and waves you through with minimal scrutiny.")
        
        print_slow("\nInside, the facility is a maze of sterile corridors and restricted areas.")
        print_slow("You navigate carefully, trying to avoid drawing attention to yourself.")
        
        print("\nWhich area do you investigate?")
        print("1. The research laboratories")
        print("2. The secure lower levels")
        print("3. The administrative offices")
        
        subchoice = input("\nEnter your choice (1-3): ")
        
        if subchoice == "1":
            print_slow("You make your way to the research labs, where scientists are studying unusual biological samples.")
            print_slow("Through a window, you observe a particular specimen that resembles a small piece of the Upside Down.")
            print_slow("The scientists are wearing hazmat suits and handling it with extreme caution.")
            
            state.adjust_reputation("stranger_things", 10)
            print(f"{Fore.GREEN}Reputation increased by 10{Style.RESET_ALL}")
        elif subchoice == "2":
            print_slow("You take an elevator to the secure lower levels, using the badge to gain access.")
            print_slow("As the doors open, you're shocked to see a massive reinforced door - likely the gate to the Upside Down.")
            print_slow("Armed guards patrol the area, and scientists monitor readings on complex equipment.")
            
            # Risk of discovery
            if random.random() < 0.3:  # 30% chance
                print_slow("\nA scientist looks at you with suspicion. 'Who authorized you for this level?' he demands.")
                print_slow("Before you can answer, alarms begin to blare. Your presence has been detected!")
                print_slow("You flee back to the elevator as security personnel begin to mobilize.")
                
                state.adjust_reputation("stranger_things", -10)
                print(f"{Fore.RED}Reputation decreased by 10{Style.RESET_ALL}")
            else:
                print_slow("\nYou observe undetected for several minutes, gathering valuable intelligence about the gate.")
                print_slow("The scientists' conversations reveal they've lost contact with someone on 'the other side'.")
                
                state.adjust_reputation("stranger_things", 15)
                print(f"{Fore.GREEN}Reputation increased by 15{Style.RESET_ALL}")
                
                # Memory trigger from interdimensional science
                print_slow("\nThe scientific discussion of interdimensional travel triggers a memory...")
                print_slow("You recall more about your own journey and purpose across the multiverse.")
                state.adjust_memory_sync(6)
                print(f"{Fore.BLUE}Memory sync increased by 6%{Style.RESET_ALL}")
        else:
            print_slow("You slip into the administrative offices, finding them largely empty during the workday.")
            print_slow("You quickly search through files and find classified documents about 'Project MKUltra' and 'Subject 011'.")
            print_slow("The papers detail experiments on children with psychic abilities, particularly a girl called Eleven.")
            
            state.adjust_morality(5)  # Exposing unethical experiments
            print(f"{Fore.GREEN}Morality increased by 5{Style.RESET_ALL}")
            state.adjust_reputation("stranger_things", 10)
            print(f"{Fore.GREEN}Reputation increased by 10{Style.RESET_ALL}")
        
        print_slow("\nYou exit the lab before your unauthorized exploration is discovered.")
        return self.current_scene
    
    def _find_exit_portal(self, state: PlayerState) -> str:
        """Look for a way back from the Upside Down."""
        print_slow("You search the twisted landscape of the Upside Down for any way back to the normal world.")
        print_slow("Your fracture key pulses erratically, as if confused by this in-between dimension.")
        
        print_slow("\nAfter hours of searching, you find an area where the barrier seems thinner.")
        print_slow("The air shimmers and occasionally you can see glimpses of the real world through it.")
        
        print("\nWhat do you do?")
        print("1. Try to force your way through the thin spot")
        print("2. Use your fracture key to enhance the natural portal")
        print("3. Look for another way out")
        
        subchoice = input("\nEnter your choice (1-3): ")
        
        if subchoice == "1":
            print_slow("You push against the thin spot with all your strength, feeling resistance like a thick membrane.")
            print_slow("Gradually, it gives way, and you slip through back into the normal world.")
            print_slow("You find yourself in the woods near Hawkins, disoriented but relieved to be back.")
            
            # Physical toll
            print_slow("\nThe journey between dimensions has taken a physical toll on you.")
            print_slow("But it also crystallized something in your memory...")
            state.adjust_memory_sync(10)
            print(f"{Fore.BLUE}Memory sync increased by 10%{Style.RESET_ALL}")
            
            return self._change_scene("hawkins_town", state)
        elif subchoice == "2":
            print_slow("You hold your fracture key toward the thin spot, and it begins to glow intensely.")
            print_slow("The key's energy interacts with the dimensional boundary, creating a stable portal.")
            print_slow("You step through effortlessly, emerging near Hawkins Lab in the normal world.")
            
            # Key gets stronger from the dimensional energy
            print_slow("\nYour fracture key absorbs some energy from the Upside Down, growing slightly stronger.")
            print_slow("You gain an additional fracture key charge.")
            state.fracture_key_charges += 1
            print(f"{Fore.GREEN}Fracture key charges increased by 1{Style.RESET_ALL}")
            
            return self._change_scene("hawkins_lab", state)
        else:
            print_slow("You decide to search for another exit, moving deeper into the Upside Down.")
            print_slow("The environment becomes increasingly hostile, with strange creatures skittering in the distance.")
            
            print_slow("\nEventually, you encounter a young girl with a shaved head - Eleven.")
            print_slow("She regards you with cautious curiosity. 'You... not from here,' she says simply.")
            print_slow("With a gesture, she opens a portal for you to return through.")
            
            state.adjust_reputation("stranger_things", 15)
            print(f"{Fore.GREEN}Reputation increased by 15{Style.RESET_ALL}")
            
            return self._change_scene("hawkins_town", state)
        
        return self.current_scene
    
    def _search_for_people(self, state: PlayerState) -> str:
        """Search for signs of other humans in the Upside Down."""
        print_slow("You explore the twisted reflection of Hawkins, looking for any signs of human presence.")
        print_slow("The environment is hostile - toxic air, strange vines that seem almost alive, and distant inhuman sounds.")
        
        print_slow("\nEventually, you find what looks like a makeshift fort built from scavenged materials.")
        print_slow("Inside are drawings that could only have been made by a child - Will Byers, trapped in this dimension.")
        
        print("\nWhat do you do with this information?")
        print("1. Try to find Will")
        print("2. Leave a message for Will")
        print("3. Return to the normal world to tell his family")
        
        subchoice = input("\nEnter your choice (1-3): ")
        
        if subchoice == "1":
            print_slow("You search the area calling softly for Will, careful not to attract the attention of predators.")
            print_slow("There's no sign of the boy, but you do find a torn piece of clothing caught on a vine.")
            state.add_item("Will's Jacket Scrap")
            print(f"{Fore.GREEN}Item added to inventory: Will's Jacket Scrap{Style.RESET_ALL}")
            
            state.adjust_morality(10)  # Attempting rescue is morally good
            print(f"{Fore.GREEN}Morality increased by 10{Style.RESET_ALL}")
        elif subchoice == "2":
            print_slow("Using a stick, you scratch a message in the dirt floor of the fort: 'NOT ALONE. HELP COMING.'")
            print_slow("You also leave a small light from your pocket, hoping it might provide some comfort.")
            
            state.adjust_morality(5)
            print(f"{Fore.GREEN}Morality increased by 5{Style.RESET_ALL}")
        else:
            print_slow("You memorize the location of the fort relative to landmarks you can identify.")
            print_slow("With this information, you might be able to help Will's family find him.")
            print_slow("You head back toward the thin spot you found earlier to return to the normal world.")
            
            # Return to normal Hawkins
            return self._change_scene("hawkins_town", state)
        
        return self.current_scene
    
    def _collect_sample(self, state: PlayerState) -> str:
        """Collect a sample from the Upside Down environment."""
        print_slow("You carefully collect samples from the strange environment of the Upside Down.")
        print_slow("The vines seem to recoil from your touch, and the particles floating in the air stick to your skin.")
        
        print_slow("\nYou gather a small piece of the luminescent fungus that grows on surfaces here.")
        state.add_item("Upside Down Fungus")
        print(f"{Fore.GREEN}Item added to inventory: Upside Down Fungus{Style.RESET_ALL}")
        
        # Risk of attention from predators
        if random.random() < 0.3:  # 30% chance
            print_slow("\nA distant shriek echoes through the twisted landscape. Something has noticed your activity.")
            print_slow("You glimpse a humanoid creature with no face moving in your direction.")
            print_slow("The Demogorgon is hunting, and you need to leave immediately.")
            
            print("\nHow do you escape?")
            print("1. Run for the thin spot in reality you found earlier")
            print("2. Hide and hope it passes by")
            print("3. Use your fracture key to create a distraction")
            
            escape_choice = input("\nEnter your choice (1-3): ")
            
            if escape_choice == "1":
                print_slow("You sprint through the toxic environment, lungs burning, toward where you found the thin spot.")
                print_slow("The creature follows, gaining ground with each moment.")
                print_slow("At the last second, you dive through the membrane, tumbling back into normal Hawkins.")
                
                return self._change_scene("hawkins_town", state)
            elif escape_choice == "2":
                print_slow("You find a crevice to hide in, making yourself as small and quiet as possible.")
                print_slow("The creature stalks past, its flower-like head opening and closing as it searches.")
                print_slow("After what feels like hours, it moves on, and you breathe a sigh of relief.")
            else:
                print_slow("You activate your fracture key, causing it to emit a bright pulse of energy.")
                print_slow("The creature is drawn to the disturbance in another direction, giving you time to escape.")
                print_slow("You use the opportunity to make your way back to the thin spot and return to normal Hawkins.")
                
                return self._change_scene("hawkins_town", state)
        
        return self.current_scene
    
    def _use_compass(self, state: PlayerState) -> str:
        """Use the compass to navigate the Upside Down."""
        print_slow("You take out the compass, hoping it might help you navigate this twisted dimension.")
        print_slow("Instead of pointing north, the needle spins wildly, then suddenly stops, pointing in a specific direction.")
        
        print_slow("\nCurious, you follow where it leads, moving carefully through the hostile environment.")
        print_slow("The compass guides you to a large structure that resembles Hawkins Lab in the normal world.")
        print_slow("Here, the boundary between dimensions seems especially thin - this must be near the main gate.")
        
        print("\nWhat do you do?")
        print("1. Try to pass through to the lab")
        print("2. Explore the Upside Down version of the lab")
        print("3. Look for other thin spots nearby")
        
        subchoice = input("\nEnter your choice (1-3): ")
        
        if subchoice == "1":
            print_slow("You approach the area where the gate should be in the normal world.")
            print_slow("The air shimmers and parts like a curtain, allowing you to step through into Hawkins Lab.")
            print_slow("You emerge in a quarantined area, setting off immediate alarms!")
            
            print_slow("\nSecurity personnel rush in as you flee the facility, barely escaping capture.")
            
            return self._change_scene("hawkins_lab", state)
        elif subchoice == "2":
            print_slow("You explore the twisted mirror of Hawkins Lab, finding disturbing evidence of experiments.")
            print_slow("In what would be the main research area, you discover a nest-like structure, organic and pulsing.")
            print_slow("It seems the Upside Down is using the lab as a point of expansion into your world.")
            
            # Memory trigger from dimensional anomaly
            print_slow("\nThe sight of dimensions bleeding together triggers a vivid memory...")
            print_slow("You recall more about how reality fractures and how dimensions interact.")
            state.adjust_memory_sync(7)
            print(f"{Fore.BLUE}Memory sync increased by 7%{Style.RESET_ALL}")
        else:
            print_slow("You search the area for other thin spots in the dimensional boundary.")
            print_slow("The compass leads you to several potential exit points scattered around Hawkins.")
            print_slow("You memorize their locations, which could be useful knowledge to share.")
            
            # Return to normal Hawkins through one of the thin spots
            print_slow("\nYou use one of the weak points to slip back into the normal dimension.")
            
            return self._change_scene("hawkins_town", state)
        
        return self.current_scene
    
    def _go_to_byers_house(self, state: PlayerState) -> str:
        """Visit the Byers family home."""
        print_slow("Using the address you obtained, you make your way to the Byers family home on the outskirts of town.")
        print_slow("The modest house looks disheveled, with Christmas lights strung everywhere and the windows covered in drawings.")
        
        return self._change_scene("byers_house", state)
    
    def _speak_with_joyce(self, state: PlayerState) -> str:
        """Speak with Joyce Byers at her home."""
        print_slow("You knock on the door of the Byers home, and after a moment, Joyce answers.")
        print_slow("She looks exhausted and suspicious, eyes darting past you to check for followers.")
        
        print("\nWhat do you say to her?")
        print("1. 'I'm here about your son, Will.'")
        print("2. 'I know about the Upside Down.'")
        print("3. 'I think I can help you.'")
        
        subchoice = input("\nEnter your choice (1-3): ")
        
        if subchoice == "1":
            print_slow("Joyce's expression hardens. 'Are you from the lab? Or the government?'")
            print_slow("'Because if you are,' she continues, voice shaking with emotion, 'you can tell them I know my son is alive.'")
            
            # If you have evidence from the Upside Down
            if "Will's Jacket Scrap" in state.inventory:
                print_slow("\nYou show her the piece of Will's jacket you found in the Upside Down.")
                print_slow("Joyce's eyes widen in recognition and hope. 'You've seen him? You've been there?'")
                print_slow("She pulls you inside, suddenly trusting and desperate for information.")
                
                state.adjust_reputation("stranger_things", 20)
                print(f"{Fore.GREEN}Reputation increased by 20{Style.RESET_ALL}")
            else:
                print_slow("\nWithout concrete evidence, Joyce remains suspicious but allows you inside to explain yourself.")
                print_slow("'Talk,' she demands. 'But know that I'll do anything to protect my family.'")
        elif subchoice == "2":
            print_slow("At the mention of the Upside Down, Joyce pulls you inside and slams the door.")
            print_slow("'How do you know about that?' she demands, fear and hope mingling in her expression.")
            print_slow("You explain your understanding of the parallel dimension and how it connects to Will's disappearance.")
            
            state.adjust_reputation("stranger_things", 15)
            print(f"{Fore.GREEN}Reputation increased by 15{Style.RESET_ALL}")
        else:
            print_slow("Joyce eyes you warily. 'How could you possibly help me?'")
            print_slow("You explain that you've encountered strange phenomena and want to assist her.")
            print_slow("She's skeptical but desperate enough to let you in and hear you out.")
            
            state.adjust_reputation("stranger_things", 5)
            print(f"{Fore.GREEN}Reputation increased by 5{Style.RESET_ALL}")
        
        print_slow("\nInside the house, Joyce shows you her elaborate communication system - Christmas lights strung everywhere.")
        print_slow("'Will talks to me through the electricity,' she explains. 'I know how it sounds, but it's real.'")
        
        return self.current_scene
    
    def _examine_lights(self, state: PlayerState) -> str:
        """Examine the Christmas light communication system."""
        print_slow("You study the elaborate system of Christmas lights strung throughout the house.")
        print_slow("Joyce has painted letters on the wall beneath them, creating a makeshift Ouija board.")
        print_slow("'He blinks the lights to spell words,' she explains. 'To talk to me from the other side.'")
        
        print_slow("\nAs if on cue, the lights begin to flicker in sequence, moving across the alphabet on the wall.")
        print_slow("It spells out: 'H-E-R-E'")
        print_slow("Joyce gasps. 'Will? Are you here now?'")
        
        print("\nWhat do you do?")
        print("1. Watch silently to see what happens")
        print("2. Ask a question through Joyce")
        print("3. Use your fracture key near the lights")
        
        subchoice = input("\nEnter your choice (1-3): ")
        
        if subchoice == "1":
            print_slow("You observe as Joyce communicates with what appears to be her son in the Upside Down.")
            print_slow("The lights spell out 'R-U-N' and then begin flickering erratically.")
            print_slow("'Something's coming,' Joyce whispers, terror in her voice. 'It's found him again.'")
        elif subchoice == "2":
            print_slow("You ask Joyce to ask Will if he's seen others in the Upside Down.")
            print_slow("The lights flicker in response: 'G-I-R-L'")
            print_slow("'A girl?' Joyce asks. 'Do you mean Eleven?'")
            print_slow("The lights flash once brightly - apparently meaning 'yes'.")
            
            # Memory trigger about dimensional travel
            print_slow("\nThis strange, technology-free method of interdimensional communication triggers a memory...")
            state.adjust_memory_sync(4)
            print(f"{Fore.BLUE}Memory sync increased by 4%{Style.RESET_ALL}")
        else:
            print_slow("You take out your fracture key and hold it near the flickering lights.")
            print_slow("The key glows in response, and the lights suddenly become much brighter.")
            print_slow("For a brief moment, a ghostly image of Will appears, trapped in a mirror dimension.")
            
            print_slow("\nJoyce cries out, reaching toward the apparition before it fades.")
            print_slow("'What did you do? What was that?' she demands, both grateful and frightened.")
            
            state.adjust_reputation("stranger_things", 15)
            print(f"{Fore.GREEN}Reputation increased by 15{Style.RESET_ALL}")
        
        return self.current_scene
    
    def _examine_drawings(self, state: PlayerState) -> str:
        """Look at Will's drawings of the shadow monster."""
        print_slow("You examine the drawings that cover the walls of the house - obviously made by Will.")
        print_slow("They depict a shadowy, many-limbed creature looming over a landscape that resembles Hawkins.")
        print_slow("'He calls it the shadow monster,' Joyce explains. 'It's hunting him in the Upside Down.'")
        
        # Memory trigger from the imagery
        if random.random() < 0.5:  # 50% chance
            print_slow("\nSomething about the ancient, malevolent entity triggers a deep memory...")
            print_slow("You recall encountering similar beings in other dimensions, ancient evils that exist between worlds.")
            state.adjust_memory_sync(6)
            print(f"{Fore.BLUE}Memory sync increased by 6%{Style.RESET_ALL}")
        
        return self.current_scene
    
    def _offer_help(self, state: PlayerState) -> str:
        """Offer to help find Will (high reputation required)."""
        print_slow("Having earned the trust of Joyce and others in Hawkins, you offer concrete help to find Will.")
        print_slow("'I know how to access the Upside Down,' you explain. 'And I might be able to bring him back.'")
        
        print_slow("\nJoyce looks at you with desperate hope. 'What do you need from me?'")
        print_slow("You explain that you'll need to find a thin spot in reality, and that Will's connection to her might help.")
        
        print_slow("\nTogether with Chief Hopper and Joyce, you create a plan to rescue Will from the Upside Down.")
        print_slow("Using your unique knowledge and their determination, you manage to open a temporary portal.")
        print_slow("Though you can't stay to see the rescue through, you've given them what they need to succeed.")
        
        state.adjust_morality(15)  # Significantly good moral act
        print(f"{Fore.GREEN}Morality increased by 15{Style.RESET_ALL}")
        state.adjust_reputation("stranger_things", 25)
        print(f"{Fore.GREEN}Reputation increased by 25{Style.RESET_ALL}")
        
        print_slow("\nYou know it's time for you to move on to another universe, but you'll be remembered in Hawkins.")
        
        return self.current_scene
    
    def _exit_universe(self, state: PlayerState) -> str:
        """Use the fracture key to exit the universe."""
        print_slow("You find a quiet moment to take out your fracture key.")
        print_slow("It pulses strongly in this reality, perhaps responding to the already thin dimensional barriers of Hawkins.")
        
        if confirm_action("use your fracture key to exit this universe"):
            state.use_fracture_key_charge()
            return "exit"
            
        print_slow("You decide to stay a little longer in this universe.")
        return self.current_scene