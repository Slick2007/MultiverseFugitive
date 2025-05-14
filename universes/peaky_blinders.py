"""
Peaky Blinders universe module for Multiverse Fugitive.
"""

from typing import List, Dict, Any
import random
import time
import colorama
from colorama import Fore, Style

from core import Universe, PlayerState, Choice
from utils import print_slow, clear_screen

colorama.init(autoreset=True)

class PeakyBlindersUniverse(Universe):
    """
    The Peaky Blinders universe based in 1920s Birmingham, England.
    
    Players navigate the dangerous world of the Shelby crime family,
    making choices that impact their standing with Tommy Shelby and other characters.
    """
    
    name = "Peaky Blinders"
    description = "Navigate the dangerous criminal underworld of 1920s Birmingham, England."
    
    def __init__(self):
        # Track the current scene/location
        self.current_scene = "awakening"
        
        # Characters to keep track of
        self.characters = {
            "tommy": {
                "name": "Tommy Shelby",
                "description": "The calculating leader of the Peaky Blinders."
            },
            "arthur": {
                "name": "Arthur Shelby",
                "description": "Tommy's older, volatile brother with a violent streak."
            },
            "polly": {
                "name": "Polly Gray",
                "description": "The matriarch of the Shelby family and treasurer of the company."
            },
            "grace": {
                "name": "Grace Burgess",
                "description": "A barmaid at The Garrison pub with mysterious intentions."
            },
            "campbell": {
                "name": "Inspector Campbell",
                "description": "A ruthless policeman sent from Belfast to clean up Birmingham."
            }
        }
        
        # Scenes/locations in this universe
        self.scenes = {
            "awakening": {
                "description": "You wake up in a muddy alleyway in Birmingham. The air is thick with coal smoke. Your head pounds and your clothes are strange to you - a wool suit and flat cap, typical of the 1920s. Distant shouting and the clop of horse hooves fill the air.",
                "first_visit": True
            },
            "garrison_pub": {
                "description": "The Garrison pub is the heart of Small Heath and the unofficial headquarters of the Peaky Blinders. The smell of whiskey and cigarette smoke fills the air. Men in flat caps eye you suspiciously as you enter.",
                "first_visit": True
            },
            "shelby_office": {
                "description": "The Shelby Company Limited operates from a small office adorned with dark wood and green wallpaper. Betting slips are organized in neat piles, and a portrait of King George V hangs on the wall.",
                "first_visit": True
            },
            "small_heath": {
                "description": "The streets of Small Heath are bustling with workers, street vendors, and children playing. Industrial smog hangs in the air, and the canal runs black with factory waste.",
                "first_visit": True
            },
            "warehouse": {
                "description": "An abandoned warehouse near the canal. The perfect place for illicit activities or for hiding something valuable... or dangerous.",
                "first_visit": True
            }
        }
    
    def on_entry(self, state: PlayerState) -> None:
        """Called when the player enters the Peaky Blinders universe."""
        clear_screen()
        print(f"{Fore.CYAN}===== ENTERING UNIVERSE: {self.name} ====={Style.RESET_ALL}\n")
        
        # Add to visited universes
        state.visited_universes.add("peaky_blinders")
        
        # Initialize reputation for this universe if first visit
        if "peaky_blinders" not in state.reputation:
            state.reputation["peaky_blinders"] = 0
        
        # Intro narration
        print_slow(f"{Fore.YELLOW}Birmingham, England - 1922{Style.RESET_ALL}")
        time.sleep(0.5)
        
        # Display the awakening scene
        self._show_scene_description("awakening")
        
        # Additional intro text
        print_slow("You pat your pockets and find a strange artifact - your fracture key, glowing faintly beneath your hand.")
        print_slow("As you stand up, you notice a newspaper. The headline reads: 'SHELBY FAMILY EXPANDS BUSINESS EMPIRE'")
        
        # Player choice on how to react to waking up
        print("\nWhat do you do?")
        print("1. Try to remember who you are")
        print("2. Look for someone to help you")
        print("3. Check your pockets more thoroughly")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == "1":
            print_slow("You concentrate, trying to recall your identity. Fragments of memory return...")
            print_slow("You remember jumping between realities, searching for key fragments.")
            state.adjust_memory_sync(5)
            print(f"{Fore.BLUE}Memory sync increased by 5%{Style.RESET_ALL}")
        elif choice == "2":
            print_slow("You decide to find someone who might help you understand this place.")
            print_slow("A young boy in tattered clothes watches you curiously from across the street.")
        else:
            print_slow("You search your pockets and find a few shillings and a folded note.")
            print_slow("The note reads: 'Meet at the Garrison. Come alone. - T.S.'")
            state.add_item("Tommy's Note")
            print(f"{Fore.GREEN}Item added to inventory: Tommy's Note{Style.RESET_ALL}")
        
        print_slow("\nAs you gather your wits, you hear shouting in the distance. This city feels dangerous and unfamiliar.")
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
                Choice(1, "Head to the Garrison Pub", self._go_to_garrison),
                Choice(2, "Explore Small Heath", self._go_to_small_heath),
                Choice(3, "Follow a group of men in flat caps", self._follow_peaky_blinders)
            ]
            
        elif self.current_scene == "garrison_pub":
            choices = [
                Choice(1, "Approach the bar and order a drink", self._order_drink),
                Choice(2, "Listen to conversations around you", self._eavesdrop_garrison),
                Choice(3, "Look for Tommy Shelby", self._look_for_tommy)
            ]
            
            # Add conditional choice if player has Tommy's note
            if "Tommy's Note" in state.inventory:
                choices.append(Choice(4, "Show the note from Tommy", self._show_tommy_note))
            
        elif self.current_scene == "small_heath":
            choices = [
                Choice(1, "Help a local kid being bullied", self._help_local_kid),
                Choice(2, "Visit the Shelby Company office", self._go_to_shelby_office),
                Choice(3, "Investigate a suspicious warehouse", self._go_to_warehouse)
            ]
            
        elif self.current_scene == "shelby_office":
            choices = [
                Choice(1, "Try to speak with Polly Gray", self._speak_with_polly),
                Choice(2, "Offer information about Inspector Campbell", self._offer_campbell_info),
                Choice(3, "Return to Small Heath", lambda state: self._change_scene("small_heath", state))
            ]
            
            # Add conditional choice based on reputation
            if state.reputation.get("peaky_blinders", 0) >= 20:
                choices.append(Choice(4, "Ask about hidden opportunities", self._ask_about_opportunities))
            
        elif self.current_scene == "warehouse":
            choices = [
                Choice(1, "Search for valuable items", self._search_warehouse),
                Choice(2, "Hide and observe who comes here", self._hide_in_warehouse),
                Choice(3, "Return to Small Heath", lambda state: self._change_scene("small_heath", state))
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
        """Called when the player exits the Peaky Blinders universe."""
        clear_screen()
        print(f"{Fore.CYAN}===== EXITING UNIVERSE: {self.name} ====={Style.RESET_ALL}\n")
        
        # Add key fragment if this is the first time completing the universe
        if "peaky_blinders" not in state.key_fragments:
            print_slow("As you activate your fracture key, you notice a small fragment break off from this reality.")
            print_slow("It attaches itself to your key, becoming a permanent part of it.")
            state.add_key_fragment("peaky_blinders")
            print(f"{Fore.YELLOW}Key Fragment acquired: Peaky Blinders{Style.RESET_ALL}")
        
        # Final messages based on reputation
        rep = state.reputation.get("peaky_blinders", 0)
        if rep >= 50:
            print_slow(f"Tommy Shelby nods at you with respect as you fade from his reality.")
            print_slow(f"'If you ever find your way back,' he says, 'there's a place for you here.'")
        elif rep >= 20:
            print_slow(f"You've made some allies in Birmingham, but also some enemies.")
            print_slow(f"The Shelby family will remember your actions, for better or worse.")
        else:
            print_slow(f"You leave Birmingham largely unnoticed, another ghost passing through.")
            print_slow(f"Perhaps it's better this way - the Peaky Blinders are dangerous allies and worse enemies.")
        
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
    def _go_to_garrison(self, state: PlayerState) -> str:
        """Go to the Garrison Pub."""
        print_slow("You make your way through the grimy streets toward The Garrison pub.")
        print_slow("People step aside as you walk, eyeing your clothes suspiciously.")
        return self._change_scene("garrison_pub", state)
    
    def _go_to_small_heath(self, state: PlayerState) -> str:
        """Explore the Small Heath area."""
        print_slow("You wander through Small Heath, taking in the industrial landscape.")
        print_slow("Factory workers, market sellers, and street children bustle around you.")
        return self._change_scene("small_heath", state)
    
    def _follow_peaky_blinders(self, state: PlayerState) -> str:
        """Follow the Peaky Blinders gang members."""
        print_slow("You discreetly follow a group of men wearing flat caps with razor blades sewn in.")
        print_slow("They lead you to The Garrison pub, entering through a side door.")
        state.adjust_morality(-5)  # Slightly morally questionable to follow people
        return self._change_scene("garrison_pub", state)
    
    def _order_drink(self, state: PlayerState) -> str:
        """Order a drink at the Garrison Pub."""
        print_slow("You approach the bar where a woman with blonde hair is serving drinks.")
        print_slow("'What will it be?' she asks. You recognize her as Grace Burgess.")
        
        if random.random() < 0.3:  # 30% chance of memory trigger
            print_slow("Something about her triggers a memory from another universe...")
            print_slow("A flash of recognition - not of her, but of your purpose here.")
            state.adjust_memory_sync(3)
            print(f"{Fore.BLUE}Memory sync increased by 3%{Style.RESET_ALL}")
        
        print_slow("You order a whiskey, and Grace serves you with a curious glance.")
        print_slow("'You're not from around here, are you?' she asks.")
        return self.current_scene
    
    def _eavesdrop_garrison(self, state: PlayerState) -> str:
        """Listen to conversations in the Garrison."""
        print_slow("You find a quiet corner and listen to the conversations around you.")
        print_slow("You overhear talk about a shipment of guns, a police inspector from Belfast, and horse races.")
        
        # Gain some intelligence
        print_slow("You learn that Inspector Campbell is cracking down on the Blinders.")
        
        # Small chance to be noticed
        if random.random() < 0.2:  # 20% chance
            print_slow("A man at the next table notices your eavesdropping and glares at you.")
            print_slow("'What are you looking at?' he growls. It might be best to move on.")
            state.adjust_reputation("peaky_blinders", -5)
            print(f"{Fore.RED}Reputation decreased by 5{Style.RESET_ALL}")
        else:
            state.adjust_reputation("peaky_blinders", 5)
            print(f"{Fore.GREEN}Reputation increased by 5{Style.RESET_ALL}")
        
        return self.current_scene
    
    def _look_for_tommy(self, state: PlayerState) -> str:
        """Look for Tommy Shelby in the pub."""
        print_slow("You scan the pub for Tommy Shelby, the leader of the Peaky Blinders.")
        print_slow("A burly man steps in front of you. 'What's your business with Mr. Shelby?'")
        
        print("\nHow do you respond?")
        print("1. 'I have information he might find valuable.'")
        print("2. 'I'm just looking for work.'")
        print("3. 'That's between me and him.'")
        
        subchoice = input("\nEnter your choice (1-3): ")
        
        if subchoice == "1":
            print_slow("'Information, eh? And what kind of information would that be?'")
            print_slow("You mention something about Inspector Campbell's movements.")
            print_slow("The man eyes you suspiciously but nods. 'Wait here.'")
            state.adjust_reputation("peaky_blinders", 10)
            print(f"{Fore.GREEN}Reputation increased by 10{Style.RESET_ALL}")
            
            print_slow("\nA few minutes later, a stern man with piercing blue eyes approaches.")
            print_slow("'I'm Thomas Shelby. I hear you have something to tell me.'")
            
        elif subchoice == "2":
            print_slow("'Work?' The man smirks. 'We've got enough hands. Unless you have a special skill?'")
            print_slow("You mention you're good at solving problems and staying discreet.")
            print_slow("He seems unimpressed but gestures to a table. 'Wait there. Arthur might have use for you.'")
            
        else:
            print_slow("The man's expression darkens. 'Wrong answer, friend.'")
            print_slow("'In Small Heath, there's nothing between a man and Thomas Shelby that doesn't become everyone's business.'")
            print_slow("'I suggest you leave before there's trouble.'")
            state.adjust_reputation("peaky_blinders", -10)
            print(f"{Fore.RED}Reputation decreased by 10{Style.RESET_ALL}")
        
        return self.current_scene
    
    def _show_tommy_note(self, state: PlayerState) -> str:
        """Show Tommy's note to get a meeting with him."""
        print_slow("You show the note signed 'T.S.' to the barkeeper.")
        print_slow("Her eyes widen slightly. 'Wait here,' she says, disappearing into a back room.")
        
        print_slow("\nMoments later, a door opens, and you're ushered into a private room.")
        print_slow("Thomas Shelby sits at a table, smoking a cigarette, his cap on the table beside him.")
        print_slow("'You found my note. Good. I have a job that requires someone... not from around here.'")
        
        state.adjust_reputation("peaky_blinders", 15)
        print(f"{Fore.GREEN}Reputation increased by 15{Style.RESET_ALL}")
        
        # Add a special item
        state.add_item("Tommy's Trust")
        print(f"{Fore.GREEN}Special status gained: Tommy's Trust{Style.RESET_ALL}")
        
        return self.current_scene
    
    def _help_local_kid(self, state: PlayerState) -> str:
        """Help a local kid being bullied."""
        print_slow("You see a group of older boys harassing a younger child, trying to steal what looks like his lunch.")
        print_slow("You intervene, stepping between them and standing tall.")
        
        print_slow("'Leave him be,' you say with authority.")
        print_slow("The bullies size you up, then reluctantly back away, muttering threats.")
        
        print_slow("\nThe boy looks at you with gratitude. 'Thank you, mister. Not many would help around here.'")
        print_slow("He introduces himself as Finn Shelby, the youngest of the Shelby brothers.")
        
        state.adjust_morality(10)
        print(f"{Fore.GREEN}Morality increased by 10{Style.RESET_ALL}")
        
        state.adjust_reputation("peaky_blinders", 20)
        print(f"{Fore.GREEN}Reputation increased by 20{Style.RESET_ALL}")
        
        print_slow("\n'My brother Tommy runs things around here,' Finn says. 'He'd want to thank you properly.'")
        print_slow("Finn offers to take you to the Shelby Company office.")
        
        print("\nDo you go with him?")
        print("1. Yes, go to the Shelby office")
        print("2. No, continue exploring Small Heath")
        
        subchoice = input("\nEnter your choice (1-2): ")
        
        if subchoice == "1":
            print_slow("You decide to go with Finn to meet his brother.")
            return self._change_scene("shelby_office", state)
        else:
            print_slow("You thank Finn but decide to continue exploring on your own.")
            print_slow("'Suit yourself,' Finn says. 'But if you need anything, ask for the Shelbys.'")
            return self.current_scene
    
    def _go_to_shelby_office(self, state: PlayerState) -> str:
        """Go to the Shelby Company office."""
        print_slow("You make your way to the Shelby Company Limited office.")
        print_slow("The clerk at the front desk looks at you suspiciously.")
        
        # Different reception based on reputation
        rep = state.reputation.get("peaky_blinders", 0)
        if rep >= 20 or "Tommy's Trust" in state.inventory:
            print_slow("'Go right in,' he says, recognizing you. 'They're expecting you.'")
        else:
            print_slow("'Do you have an appointment?' he asks coldly.")
            print_slow("You make up an excuse about having information for Mr. Shelby.")
            print_slow("He reluctantly lets you wait, but you can tell you're not welcome.")
        
        return self._change_scene("shelby_office", state)
    
    def _go_to_warehouse(self, state: PlayerState) -> str:
        """Go to the suspicious warehouse."""
        print_slow("You follow rumors of illegal activities to an abandoned warehouse by the canal.")
        print_slow("The building is quiet, but you notice subtle signs of occupation - fresh footprints, a recently oiled lock.")
        
        return self._change_scene("warehouse", state)
    
    def _speak_with_polly(self, state: PlayerState) -> str:
        """Speak with Polly Gray at the Shelby office."""
        print_slow("You approach Polly Gray, who's reviewing ledgers at a large desk.")
        print_slow("She looks up at you with sharp, evaluating eyes. 'Yes? What can I do for you?'")
        
        print("\nWhat do you say to Polly?")
        print("1. 'I'm looking for work with the Shelby Company.'")
        print("2. 'I need to speak with Tommy about something important.'")
        print("3. 'I helped Finn earlier. He suggested I come by.'")
        
        subchoice = input("\nEnter your choice (1-3): ")
        
        if subchoice == "1":
            print_slow("Polly raises an eyebrow. 'Are you now? And what skills do you bring?'")
            print_slow("You mention your ability to adapt quickly to new situations.")
            print_slow("'Hmm. We'll see about that. Leave your name with the clerk.'")
            
        elif subchoice == "2":
            print_slow("'Everyone needs to speak to Tommy,' Polly says dryly. 'What makes your business so special?'")
            print_slow("You hint at knowledge from beyond this world, careful not to sound mad.")
            print_slow("Polly studies you carefully. 'You're... different, aren't you? Wait here.'")
            state.adjust_memory_sync(5)
            print(f"{Fore.BLUE}Memory sync increased by 5%{Style.RESET_ALL}")
            
        else:
            if "Tommy's Trust" in state.inventory or state.reputation.get("peaky_blinders", 0) >= 20:
                print_slow("Polly's expression softens slightly. 'Ah, you're the one who helped Finn. Thank you for that.'")
                print_slow("'Family is everything to us. Tommy will want to meet you.'")
                state.adjust_reputation("peaky_blinders", 5)
                print(f"{Fore.GREEN}Reputation increased by 5{Style.RESET_ALL}")
            else:
                print_slow("Polly looks skeptical. 'Is that so? Finn hasn't mentioned anyone to me.'")
                print_slow("You can tell she doesn't believe you. Perhaps you should come back with proof.")
                state.adjust_reputation("peaky_blinders", -5)
                print(f"{Fore.RED}Reputation decreased by 5{Style.RESET_ALL}")
        
        return self.current_scene
    
    def _offer_campbell_info(self, state: PlayerState) -> str:
        """Offer information about Inspector Campbell."""
        print_slow("You mention to a Shelby associate that you have information about Inspector Campbell's plans.")
        print_slow("The room goes quiet. Everyone looks at you with suspicion.")
        
        print_slow("\nArthur Shelby approaches, his expression menacing. 'And how would you know about Campbell?'")
        
        print("\nHow do you explain yourself?")
        print("1. 'I overheard his men talking at the pub.'")
        print("2. 'I have ways of knowing things others don't.'")
        print("3. 'I used to work for him but he betrayed me.'")
        
        subchoice = input("\nEnter your choice (1-3): ")
        
        if subchoice == "1":
            print_slow("Arthur seems doubtful but interested. 'And what exactly did you hear?'")
            print_slow("You invent some details about a planned raid, being vague but convincing.")
            print_slow("'If this checks out, you'll have earned your place. If not...' He leaves the threat hanging.")
            
        elif subchoice == "2":
            print_slow("'Is that right?' Arthur laughs. 'A fortune teller in our midst, Tommy!'")
            print_slow("Tommy Shelby appears from a back room, eyeing you carefully.")
            print_slow("'Let's hear what our visitor has to say,' he says quietly.")
            state.adjust_memory_sync(3)
            print(f"{Fore.BLUE}Memory sync increased by 3%{Style.RESET_ALL}")
            
        else:
            print_slow("Arthur's expression darkens further. 'A turncoat, eh? And why should we trust you?'")
            print_slow("You explain that Campbell's betrayal left you seeking revenge.")
            print_slow("'Revenge is something we understand,' Arthur says, nodding slowly.")
            state.adjust_morality(-5)
            print(f"{Fore.RED}Morality decreased by 5{Style.RESET_ALL}")
        
        return self.current_scene
    
    def _ask_about_opportunities(self, state: PlayerState) -> str:
        """Ask about hidden opportunities (high reputation required)."""
        print_slow("With the trust you've built, you carefully inquire about 'special opportunities' with the Shelbys.")
        print_slow("Tommy himself takes you aside to a private office.")
        
        print_slow("\n'Not many outsiders earn a place at our table,' he says, lighting a cigarette.")
        print_slow("'But you've proven yourself different. I have something that might interest you.'")
        
        print_slow("\nTommy explains about a hidden vault with valuable artifacts beneath the warehouse.")
        print_slow("'We've been unable to open it. The lock mechanism is... unusual. Perhaps you might have better luck.'")
        
        # Add quest item
        state.add_item("Warehouse Key")
        print(f"{Fore.GREEN}Item added to inventory: Warehouse Key{Style.RESET_ALL}")
        
        print_slow("\n'Be careful,' Tommy warns. 'We're not the only ones interested in what's down there.'")
        
        return self.current_scene
    
    def _search_warehouse(self, state: PlayerState) -> str:
        """Search the warehouse for valuable items."""
        print_slow("You search through the warehouse, looking for anything valuable or unusual.")
        
        if "Warehouse Key" in state.inventory:
            print_slow("Using the key Tommy gave you, you locate a hidden trapdoor beneath some crates.")
            print_slow("It leads to a small underground chamber with a strange, glowing device.")
            
            print_slow("\nThe device seems to respond to your fracture key, humming when you bring it near.")
            print_slow("You realize this is a fragment of technology from your own reality, somehow lost here.")
            
            # Major memory boost
            state.adjust_memory_sync(15)
            print(f"{Fore.BLUE}Memory sync increased by 15%{Style.RESET_ALL}")
            
            # Add important item
            state.add_item("Reality Stabilizer")
            print(f"{Fore.GREEN}Item added to inventory: Reality Stabilizer{Style.RESET_ALL}")
            
            print_slow("\nWith this technology, you might be able to better control your jumps between universes.")
            
        else:
            # Random find based on luck
            items = ["Old Pocket Watch", "Rusted Key", "Strange Coin", "Torn Photograph"]
            found_item = random.choice(items)
            
            print_slow(f"After searching for a while, you find a {found_item} hidden behind some crates.")
            state.add_item(found_item)
            print(f"{Fore.GREEN}Item added to inventory: {found_item}{Style.RESET_ALL}")
            
            # Small chance of being caught
            if random.random() < 0.3:  # 30% chance
                print_slow("\nSuddenly, you hear voices approaching the warehouse.")
                print_slow("You hide quickly as several Blinders enter, discussing shipments of illegal goods.")
                print_slow("You'll need to be more careful next time.")
        
        return self.current_scene
    
    def _hide_in_warehouse(self, state: PlayerState) -> str:
        """Hide and observe who comes to the warehouse."""
        print_slow("You find a hiding spot among the crates and wait patiently.")
        print_slow("After some time, you hear footsteps and voices approaching.")
        
        print_slow("\nThrough a crack, you see Tommy Shelby meeting with Inspector Campbell himself.")
        print_slow("Their conversation reveals a complex game of betrayal and counter-betrayal.")
        
        print_slow("\n'I know about your operation in London,' Campbell says. 'I could close it down tomorrow.'")
        print_slow("'But you won't,' Tommy replies calmly. 'Because you need what I found in the vault.'")
        
        # Memory trigger from the conversation
        print_slow("\nSomething about the 'vault' triggers a memory in you...")
        state.adjust_memory_sync(10)
        print(f"{Fore.BLUE}Memory sync increased by 10%{Style.RESET_ALL}")
        
        print("\nDo you continue hiding or reveal yourself?")
        print("1. Continue hiding and listening")
        print("2. Accidentally make a noise, revealing your presence")
        print("3. Slip away quietly while they're distracted")
        
        subchoice = input("\nEnter your choice (1-3): ")
        
        if subchoice == "1":
            print_slow("You remain hidden, gathering more valuable information.")
            print_slow("You learn that the 'vault' contains an artifact of unknown origin - possibly from another universe.")
            state.adjust_morality(-5)  # Morally questionable to eavesdrop
            print(f"{Fore.RED}Morality decreased by 5{Style.RESET_ALL}")
            
        elif subchoice == "2":
            print_slow("You shift position and accidentally knock over a small crate.")
            print_slow("The conversation stops immediately. 'We have company,' Tommy says coldly.")
            print_slow("You're discovered and brought before them, trying to explain your presence.")
            
            # High risk, high reward
            if random.random() < 0.4 or "Tommy's Trust" in state.inventory:  # 40% chance of success, guaranteed with Tommy's Trust
                print_slow("Tommy recognizes you and after a tense moment, waves off his men.")
                print_slow("'This one's with me,' he tells Campbell, giving you a look that demands silence.")
                state.adjust_reputation("peaky_blinders", 10)
                print(f"{Fore.GREEN}Reputation increased by 10{Style.RESET_ALL}")
            else:
                print_slow("'Search him,' Tommy orders. Your fracture key remains hidden, but you're roughed up.")
                print_slow("'Next time I catch you snooping, it'll be your last,' Tommy warns before letting you go.")
                state.adjust_reputation("peaky_blinders", -15)
                print(f"{Fore.RED}Reputation decreased by 15{Style.RESET_ALL}")
            
        else:
            print_slow("You carefully back away while they're engrossed in their tense negotiation.")
            print_slow("You slip out of the warehouse undetected, but wonder what artifact they were discussing.")
        
        return self.current_scene
    
    def _exit_universe(self, state: PlayerState) -> str:
        """Use the fracture key to exit the universe."""
        if not state.use_fracture_key_charge():
            print_slow(f"{Fore.RED}You don't have any fracture key charges left!{Style.RESET_ALL}")
            print_slow("You're trapped in this universe until you can find another way out.")
            return self.current_scene
        
        print_slow("You find a quiet moment alone and take out your fracture key.")
        print_slow("It glows with an otherworldly light as you activate it.")
        print_slow("The world around you begins to fade as you prepare to return to the void...")
        
        self.on_exit(state)
        return "exit"  # Special return value to trigger universe exit
