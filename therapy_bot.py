#!/usr/bin/env python3

import sys
import os
import site

# Add the user site-packages to the path
user_site_packages = site.getusersitepackages()
if user_site_packages not in sys.path:
    sys.path.insert(0, user_site_packages)

import questionary
from colorama import init, Fore, Style
import random
import json
import os
from datetime import datetime
import openai
import time

# Initialize colorama for cross-platform colored output
init()

# Read API key directly from .env file
def read_api_key_from_env_file():
    try:
        print(f"{Fore.YELLOW}Attempting to read .env file...{Style.RESET_ALL}")
        with open('.env', 'r') as file:
            env_content = file.read()
            print(f"{Fore.YELLOW}ENV file content length: {len(env_content)} characters{Style.RESET_ALL}")
            for line in env_content.split('\n'):
                if line.startswith('OPENAI_API_KEY='):
                    api_key = line.split('=', 1)[1].strip()
                    print(f"{Fore.YELLOW}API key found, length: {len(api_key)} characters{Style.RESET_ALL}")
                    return api_key
            print(f"{Fore.RED}No OPENAI_API_KEY found in .env file{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error reading .env file: {e}{Style.RESET_ALL}")
    return None

# Use the API key
api_key = read_api_key_from_env_file()
if api_key:
    print(f"{Fore.GREEN}Setting API key: {api_key[:5]}...{api_key[-5:]}{Style.RESET_ALL}")
    openai.api_key = api_key
    
    # Try setting organization if this is an OpenAI key with a project identifier
    if api_key.startswith('sk-proj-'):
        print(f"{Fore.YELLOW}Detected project-specific API key. Attempting to extract org ID...{Style.RESET_ALL}")
        try:
            # For some platforms, the organization ID might be embedded in the key or needed separately
            # Uncomment and set this if needed
            # openai.organization = "org-..."
            print(f"{Fore.GREEN}Set organization ID{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.YELLOW}Could not set organization ID: {e}{Style.RESET_ALL}")
    
    print(f"{Fore.GREEN}API key loaded successfully!{Style.RESET_ALL}")
else:
    print(f"{Fore.RED}Failed to load API key from .env file{Style.RESET_ALL}")

class TherapyBot:
    def __init__(self):
        self.user_name = None
        self.mood_history = []
        
        self.load_user_data()
        self.setup_ai()
        self.conversation_history = []

    def setup_ai(self):
        """Initialize OpenAI client and set up system prompt."""
        try:
            if not openai.api_key:
                raise ValueError("OPENAI_API_KEY not found in environment")
            
            # For project-specific API keys, we might need to use a different endpoint
            if openai.api_key.startswith('sk-proj-'):
                try:
                    # Try Azure OpenAI endpoint (this is just an example, you might need a different one)
                    print(f"{Fore.YELLOW}Trying with Azure OpenAI compatible endpoint...{Style.RESET_ALL}")
                    # Uncomment if needed:
                    # openai.api_base = "https://your-resource-name.openai.azure.com/"
                    # openai.api_type = "azure"
                    # openai.api_version = "2023-07-01-preview"
                except Exception as e:
                    print(f"{Fore.YELLOW}Could not set up alternative endpoint: {e}{Style.RESET_ALL}")
            
            self.ai_enabled = True
            self.conversation_history = [{
                "role": "system",
                "content": """You are a compassionate and understanding AI therapist. Your responses should be:
                1. Empathetic and warm
                2. Professional but conversational
                3. Focused on active listening and validation
                4. Encouraging but not dismissive of feelings
                5. Safety-conscious (refer to professional help for serious issues)
                
                Keep responses concise (2-3 sentences) unless deep elaboration is needed."""
            }]
        except Exception as e:
            print(f"{Fore.RED}Warning: Could not initialize OpenAI ({str(e)}). Running in basic mode.{Style.RESET_ALL}")
            self.ai_enabled = False

    def get_ai_response(self, user_input, context=""):
        """Get AI-generated response based on user input and context."""
        if not self.ai_enabled:
            return None

        # Add context and user message to conversation
        if context:
            self.conversation_history.append({
                "role": "system",
                "content": f"Context: {context}"
            })
        
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })

        try:
            # Print detailed debug info
            print(f"{Fore.YELLOW}Making API request with token: {openai.api_key[:5]}...{openai.api_key[-5:]} (length: {len(openai.api_key)}){Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Trying to use model: gpt-3.5-turbo{Style.RESET_ALL}")
            
            # Get AI response
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.conversation_history,
                max_tokens=150,
                temperature=0.7
            )

            ai_response = response.choices[0].message['content']
            
            # Add AI response to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": ai_response
            })

            # Keep conversation history manageable
            if len(self.conversation_history) > 10:
                # Keep system message and last 4 exchanges
                self.conversation_history = [self.conversation_history[0]] + self.conversation_history[-8:]

            return ai_response

        except Exception as e:
            print(f"\n{Fore.RED}AI response error: {str(e)}{Style.RESET_ALL}")
            print(f"\n{Fore.RED}Full error details: {repr(e)}{Style.RESET_ALL}")
            return None

    def load_user_data(self):
        """Load user data from file if it exists."""
        try:
            with open('user_data.json', 'r') as f:
                data = json.load(f)
                self.user_name = data.get('name')
                self.mood_history = data.get('mood_history', [])
        except FileNotFoundError:
            pass

    def save_user_data(self):
        """Save user data to file."""
        with open('user_data.json', 'w') as f:
            json.dump({
                'name': self.user_name,
                'mood_history': self.mood_history
            }, f)

    def get_greeting(self):
        """Return a personalized greeting based on mood history and time of day."""
        hour = datetime.now().hour
        time_of_day = (
            "morning" if 5 <= hour < 12
            else "afternoon" if 12 <= hour < 17
            else "evening" if 17 <= hour < 22
            else "night"
        )

        if self.ai_enabled:
            context = f"User's name is {self.user_name}. It's {time_of_day}."
            if self.mood_history:
                last_mood = self.mood_history[-1]['mood']
                context += f" Their last recorded mood was: {last_mood}"
            
            greeting = self.get_ai_response("Generate a warm, personal greeting.", context)
            if greeting:
                return greeting

        # Fallback greetings if AI is not available
        name_part = f", {self.user_name}" if self.user_name else ""
        
        greetings = [
            f"Good {time_of_day}{name_part}! I'm here to listen and support you today.",
            f"Welcome back{name_part}! How are you feeling this {time_of_day}?",
            f"Hi{name_part}! I'm glad you're here this {time_of_day}. How can I help?",
            f"Hey there{name_part}! Ready for a thoughtful chat this {time_of_day}?",
            f"It's good to see you this {time_of_day}{name_part}. Let's take a moment for your wellbeing.",
            f"Greetings{name_part}! I hope your {time_of_day} is going well so far.",
            f"{time_of_day.capitalize()} is a great time to check in with yourself{name_part}.",
            f"Welcome to our {time_of_day} session{name_part}. I'm here for you.",
        ]
        return random.choice(greetings)

    def check_in(self):
        """Main function to check in with the user."""
        print(f"\n{Fore.CYAN}{self.get_greeting()}{Style.RESET_ALL}\n")

        if not self.user_name:
            self.user_name = questionary.text(
                "First, could you tell me your name?",
                validate=lambda text: len(text) > 0
            ).ask()

        mood = questionary.select(
            "How are you feeling right now?",
            choices=[
                "😊 Great",
                "😌 Good",
                "😐 Okay",
                "😔 Not so good",
                "😢 Terrible"
            ]
        ).ask()

        self.mood_history.append({
            'mood': mood,
            'timestamp': datetime.now().isoformat()
        })

        if "Not so good" in mood or "Terrible" in mood:
            self.handle_negative_mood()
        else:
            self.handle_positive_mood()

        self.offer_activities()
        self.save_user_data()

    def handle_negative_mood(self):
        """Handle when user is feeling down."""
        responses = [
            "I'm sorry you're not feeling your best right now.",
            "That sounds difficult. Thank you for sharing how you're feeling.",
            "I'm here for you during this challenging time.",
            "It takes courage to acknowledge when you're not feeling great.",
            "Your feelings are valid, and it's okay to have tough moments."
        ]
        
        print(f"\n{Fore.YELLOW}{random.choice(responses)}{Style.RESET_ALL}")
        
        want_to_talk = questionary.confirm(
            "Would you like to talk about what's bothering you?"
        ).ask()

        if want_to_talk:
            user_input = questionary.text(
                "I'm here to listen. What's on your mind?",
                multiline=True
            ).ask()

            if self.ai_enabled:
                context = f"User ({self.user_name}) is feeling down and shared their thoughts. Provide empathetic support."
                ai_response = self.get_ai_response(user_input, context)
                if ai_response:
                    print(f"\n{Fore.GREEN}{ai_response}{Style.RESET_ALL}")
            else:
                supportive_responses = [
                    "Thank you for sharing. Remember that it's okay to not be okay sometimes.",
                    "I appreciate you opening up. These feelings won't last forever, even when it seems like they will.",
                    "Thank you for trusting me with your thoughts. Everyone struggles sometimes, and that's completely normal.",
                    "I'm glad you were able to express that. Acknowledging our feelings is the first step toward managing them.",
                    "That sounds really challenging. Be gentle with yourself as you navigate through this.",
                    "Thank you for sharing something so personal. Your resilience in difficult times is admirable."
                ]
                print(f"\n{Fore.GREEN}{random.choice(supportive_responses)}{Style.RESET_ALL}")
            
            print("\nWould you like to try some simple exercises that might help?")

    def handle_positive_mood(self):
        """Handle when user is feeling good."""
        if self.ai_enabled:
            context = f"User ({self.user_name}) is feeling good. Respond positively and encourage sharing."
            ai_response = self.get_ai_response("The user is feeling good today.", context)
            if ai_response:
                print(f"\n{Fore.GREEN}{ai_response}{Style.RESET_ALL}")
        else:
            positive_responses = [
                "I'm glad you're feeling good!",
                "That's wonderful to hear!",
                "It's great that you're in a positive space today.",
                "I'm happy to hear you're doing well!",
                "That's excellent news! Positive moments are worth celebrating.",
                "I'm really glad to hear that! Your good mood brightens our conversation."
            ]
            print(f"\n{Fore.GREEN}{random.choice(positive_responses)}{Style.RESET_ALL}")
        
        if questionary.confirm("Would you like to share what's making you feel this way?").ask():
            user_input = questionary.text(
                "I'd love to hear about it!",
                multiline=True
            ).ask()
            
            if self.ai_enabled:
                context = f"User shared something positive. Respond with enthusiasm and encouragement."
                ai_response = self.get_ai_response(user_input, context)
                if ai_response:
                    print(f"\n{Fore.GREEN}{ai_response}{Style.RESET_ALL}")
            else:
                encouragement_responses = [
                    "That's really wonderful! It's great that you're experiencing these positive moments.",
                    "Thank you for sharing something so positive! These good experiences are so important.",
                    "I'm happy to hear that! Recognizing and appreciating good moments helps build resilience.",
                    "That sounds like a really meaningful experience. Thanks for sharing it with me.",
                    "It's terrific that you're having these positive feelings. You deserve these good moments!",
                    "What a great experience! Holding onto these positive moments can help during challenging times."
                ]
                print(f"\n{Fore.GREEN}{random.choice(encouragement_responses)}{Style.RESET_ALL}")

    def offer_activities(self):
        """Offer various activities to the user."""
        activities = [
            "Practice deep breathing",
            "Write in a journal",
            "Take a short walk",
            "Listen to calming music",
            "Do some stretching",
            "Practice gratitude",
            "Try mindfulness",
            "Chat more",
            "Exit"
        ]

        while True:
            choice = questionary.select(
                "\nWould you like to try any of these activities?",
                choices=activities
            ).ask()

            if choice == "Exit":
                if self.ai_enabled:
                    farewell = self.get_ai_response("Generate a warm farewell message.", 
                                                  f"User ({self.user_name}) is leaving the session.")
                    if farewell:
                        print(f"\n{Fore.CYAN}{farewell}{Style.RESET_ALL}\n")
                    else:
                        print(f"\n{Fore.CYAN}Take care! Remember, I'm here whenever you need me.{Style.RESET_ALL}\n")
                else:
                    farewells = [
                        "Take care! Remember, I'm here whenever you need me.",
                        "Goodbye for now. I'll be here next time you want to chat.",
                        "Wishing you well until we meet again. Take good care of yourself!",
                        "Until next time, be kind to yourself. I'll be here when you return.",
                        "Thank you for checking in today. I look forward to our next conversation!",
                        "Take care of yourself. Remember that each day is a new opportunity."
                    ]
                    print(f"\n{Fore.CYAN}{random.choice(farewells)}{Style.RESET_ALL}\n")
                break
            elif choice == "Chat more":
                user_input = questionary.text(
                    "What would you like to talk about?",
                    multiline=True
                ).ask()
                
                if self.ai_enabled:
                    ai_response = self.get_ai_response(user_input)
                    if ai_response:
                        print(f"\n{Fore.GREEN}{ai_response}{Style.RESET_ALL}")
                else:
                    chat_responses = [
                        "Thank you for sharing. Would you like to talk more about that?",
                        "That's really interesting. How does that make you feel?",
                        "I appreciate you opening up. Would you like to explore this topic further?",
                        "Thank you for sharing your thoughts. Is there anything else on your mind?",
                        "I'm glad you brought that up. Would you like to try an activity that might help with that?",
                        "That's a thoughtful reflection. Is there a specific aspect of this you'd like to focus on?"
                    ]
                    print(f"\n{Fore.GREEN}{random.choice(chat_responses)}{Style.RESET_ALL}")
            elif choice == "Practice deep breathing":
                self.guide_breathing()
            elif choice == "Practice gratitude":
                self.guide_gratitude()
            elif choice == "Try mindfulness":
                self.guide_mindfulness()
            else:
                if self.ai_enabled:
                    context = f"User selected activity: {choice}. Provide encouraging guidance."
                    guidance = self.get_ai_response(f"Provide guidance for {choice}", context)
                    if guidance:
                        print(f"\n{Fore.GREEN}{guidance}{Style.RESET_ALL}")
                else:
                    activity_guidance = {
                        "Write in a journal": [
                            "Writing down your thoughts can be very therapeutic. Try spending 5-10 minutes writing whatever comes to mind.",
                            "For journal writing, try starting with 'Today I feel...' and see where your thoughts take you.",
                            "Consider writing about something you're grateful for, a challenge you're facing, or a goal you have."
                        ],
                        "Take a short walk": [
                            "A short walk can clear your mind and energize your body. Even 5-10 minutes can make a difference.",
                            "While walking, try to notice the details around you - the colors, sounds, and sensations.",
                            "Walking outdoors can boost your mood through natural light and gentle exercise."
                        ],
                        "Listen to calming music": [
                            "Music can have a powerful effect on our emotions. Find something soothing that helps you relax.",
                            "Try closing your eyes while listening and focus solely on the sounds and how they make you feel.",
                            "Classical, ambient, or nature sounds often work well for relaxation."
                        ],
                        "Do some stretching": [
                            "Gentle stretching can release physical tension that often accompanies stress.",
                            "Focus on your breathing as you stretch, and don't push beyond what feels comfortable.",
                            "Even 5 minutes of stretching can help reconnect your mind and body."
                        ]
                    }
                    
                    guidance = activity_guidance.get(choice, ["That's a great choice! Take your time with this activity."])
                    print(f"\n{Fore.GREEN}{random.choice(guidance)}{Style.RESET_ALL}")
                input("\nPress Enter when you're ready to continue...")

    def guide_breathing(self):
        """Guide the user through a breathing exercise."""
        if self.ai_enabled:
            intro = self.get_ai_response("Introduce a breathing exercise in a calm, guiding way.")
            if intro:
                print(f"\n{Fore.CYAN}{intro}{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.CYAN}Let's do a simple breathing exercise together.{Style.RESET_ALL}")
        else:
            breathing_intros = [
                "Let's do a simple breathing exercise together.",
                "Let's take a moment to focus on our breath and find some calm.",
                "Breathing exercises can help calm your nervous system. Let's try one together.",
                "Let's practice a breathing technique that can help reduce stress and bring focus.",
                "Taking control of your breath is a powerful way to influence how you feel. Let's practice."
            ]
            print(f"\n{Fore.CYAN}{random.choice(breathing_intros)}{Style.RESET_ALL}")
        
        print("Follow my lead for 3 cycles...")
        
        for i in range(3):
            input("\nPress Enter to begin cycle {}...".format(i + 1))
            print("Breathe in deeply... 2... 3... 4...")
            time.sleep(4)
            print("Hold... 2... 3... 4...")
            time.sleep(4)
            print("Breathe out slowly... 2... 3... 4... 5... 6...")
            time.sleep(6)

        if self.ai_enabled:
            closing = self.get_ai_response("Provide a calming closing message after breathing exercise.")
            if closing:
                print(f"\n{Fore.GREEN}{closing}{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.GREEN}Great job! How do you feel?{Style.RESET_ALL}")
        else:
            breathing_closings = [
                "Great job! How do you feel?",
                "Well done. Notice how your body feels more relaxed now.",
                "Excellent! You can return to this exercise anytime you need a moment of calm.",
                "Wonderful work. Your breath is always there as a tool to help center yourself.",
                "That's perfect. Remember you can use this technique anywhere, anytime you feel stressed."
            ]
            print(f"\n{Fore.GREEN}{random.choice(breathing_closings)}{Style.RESET_ALL}")
            
    def guide_gratitude(self):
        """Guide the user through a gratitude practice."""
        gratitude_intros = [
            "Let's practice gratitude, which can help shift your focus to positive aspects of life.",
            "Gratitude practice can boost your mood and wellbeing. Let's try a simple exercise.",
            "Taking time to appreciate the good things in life, big or small, can be very powerful.",
            "Gratitude helps us notice the positive things we might otherwise take for granted."
        ]
        print(f"\n{Fore.CYAN}{random.choice(gratitude_intros)}{Style.RESET_ALL}")
        
        prompts = [
            "What's something small that brought you joy recently?",
            "Who is someone you're grateful to have in your life, and why?",
            "What's something your body has done for you today that you're thankful for?",
            "What's something in nature that you appreciate?",
            "What's a skill or ability you have that you're grateful for?"
        ]
        
        for i in range(2):
            prompt = random.choice(prompts)
            prompts.remove(prompt)  # Ensure we don't repeat prompts
            
            print(f"\n{prompt}")
            input("Take a moment to reflect, then press Enter when you're ready to share or move on...")
            
            response = questionary.text(
                "If you'd like to share your reflection (or skip with Enter):",
                multiline=True
            ).ask()
            
            if response.strip():
                gratitude_responses = [
                    "That's beautiful to reflect on. Gratitude for these moments can build resilience.",
                    "Thank you for sharing. Recognizing these positive elements is powerful.",
                    "What a wonderful reflection. Carrying this gratitude with you can brighten difficult days.",
                    "I appreciate you sharing that. Gratitude practice becomes more powerful with regularity."
                ]
                print(f"\n{Fore.GREEN}{random.choice(gratitude_responses)}{Style.RESET_ALL}")
        
        gratitude_closings = [
            "This practice is most effective when done regularly. Even just noting 3 things daily can make a difference.",
            "You can continue this practice by keeping a gratitude journal or simply taking moments throughout your day to notice the good.",
            "Remember, gratitude isn't about ignoring difficulties, but about also acknowledging the positive alongside them.",
            "The more we practice gratitude, the more our brains become attuned to noticing the positive in our lives."
        ]
        print(f"\n{Fore.GREEN}{random.choice(gratitude_closings)}{Style.RESET_ALL}")
    
    def guide_mindfulness(self):
        """Guide the user through a brief mindfulness exercise."""
        mindfulness_intros = [
            "Let's practice a brief mindfulness exercise to help you connect with the present moment.",
            "Mindfulness helps us observe our thoughts and feelings without judgment. Let's try a simple practice.",
            "Taking even a short mindful pause can help reset your nervous system. Let's try one now.",
            "Mindfulness is about being fully present. Let's practice together for a few moments."
        ]
        print(f"\n{Fore.CYAN}{random.choice(mindfulness_intros)}{Style.RESET_ALL}")
        
        print("\nFind a comfortable position and, if you're comfortable doing so, gently close your eyes or soften your gaze.")
        time.sleep(3)
        
        steps = [
            "First, bring your attention to your breath. Don't try to change it, just notice how it feels...",
            "Now, notice any sensations in your body. Maybe there's tension, warmth, or tingling somewhere...",
            "If your mind wanders, that's completely normal. Just gently bring your focus back to the present...",
            "Now, notice any sounds in your environment, near or far...",
            "Finally, bring awareness to your thoughts and emotions, observing them without judgment..."
        ]
        
        for step in steps:
            print(f"\n{step}")
            time.sleep(8)
        
        print("\nWhen you're ready, if your eyes are closed, gently open them.")
        time.sleep(3)
        
        mindfulness_closings = [
            "You can bring this kind of mindful awareness to any moment in your day, not just during formal practice.",
            "Even brief moments of mindfulness like this can help create space between your thoughts and reactions.",
            "Regular mindfulness practice can help build the skill of present-moment awareness, which supports overall wellbeing.",
            "Mindfulness isn't about eliminating thoughts, but about changing your relationship with them."
        ]
        print(f"\n{Fore.GREEN}{random.choice(mindfulness_closings)}{Style.RESET_ALL}")

if __name__ == "__main__":
    bot = TherapyBot()
    bot.check_in() 