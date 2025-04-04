#!/usr/bin/env python3

import sys
import os
import site
import argparse
import time
import json
import re
import random
from datetime import datetime, timedelta

# Add the user site-packages to the path
user_site_packages = site.getusersitepackages()
if user_site_packages not in sys.path:
    sys.path.insert(0, user_site_packages)

import questionary
from colorama import init, Fore, Style

# Import our custom modules
from local_nlp import LocalNLP
from therapy_modules import get_all_modules, run_exercise
from mood_visualization import generate_ascii_chart, load_mood_data
from journal_system import JournalSystem
from reminder_system import ReminderSystem
from resources import ResourceLibrary

# Initialize colorama for cross-platform colored output
init()

class EnhancedTherapyBot:
    def __init__(self):
        self.user_name = None
        self.mood_history = []
        self.load_user_data()
        
        # Initialize components
        self.nlp = LocalNLP()
        self.journal = JournalSystem()
        self.reminders = ReminderSystem()
        self.resources = ResourceLibrary()
        self.therapy_modules = get_all_modules()
        
        # Track user preferences
        self.preferences = self.load_preferences()
        
        # Parse command line arguments
        self.args = self.parse_arguments()

    def parse_arguments(self):
        """Parse command line arguments."""
        parser = argparse.ArgumentParser(description='Enhanced Therapy Bot CLI')
        parser.add_argument('--skip-greeting', action='store_true', 
                            help='Skip the initial greeting and check-in')
        parser.add_argument('--module', type=str, 
                            help='Jump directly to a specific therapy module')
        parser.add_argument('--journal', action='store_true',
                            help='Go directly to journal mode')
        parser.add_argument('--reminders', action='store_true',
                            help='Go directly to reminders')
        parser.add_argument('--chat', action='store_true',
                            help='Start in chat mode')
        parser.add_argument('--version', action='store_true',
                            help='Display version information')
        
        # If no arguments provided, return empty namespace
        if len(sys.argv) == 1:
            return parser.parse_args([])
        return parser.parse_args()

    def load_user_data(self):
        """Load user data from file if it exists."""
        try:
            with open('user_data.json', 'r') as f:
                data = json.load(f)
                self.user_name = data.get('name')
                self.mood_history = data.get('mood_history', [])
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    def save_user_data(self):
        """Save user data to file."""
        with open('user_data.json', 'w') as f:
            json.dump({
                'name': self.user_name,
                'mood_history': self.mood_history
            }, f)
            
    def load_preferences(self):
        """Load user preferences."""
        try:
            with open('user_preferences.json', 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Default preferences
            return {
                "favorite_activities": [],
                "therapy_module_history": [],
                "journal_frequency": 0,
                "reminder_time": None,
                "last_used_features": []
            }
            
    def save_preferences(self):
        """Save user preferences."""
        with open('user_preferences.json', 'w') as f:
            json.dump(self.preferences, f)

    def get_greeting(self):
        """Return a personalized greeting based on mood history and time of day."""
        hour = datetime.now().hour
        time_of_day = (
            "morning" if 5 <= hour < 12
            else "afternoon" if 12 <= hour < 17
            else "evening" if 17 <= hour < 22
            else "night"
        )

        # Use local NLP for a natural sounding greeting
        context = f"User's name is {self.user_name}. It's {time_of_day}."
        if self.mood_history:
            last_mood = self.mood_history[-1]['mood']
            context += f" Their last recorded mood was: {last_mood}"
            
            # Calculate days since last check-in
            try:
                last_date = datetime.fromisoformat(self.mood_history[-1]['timestamp'])
                days_since = (datetime.now() - last_date).days
                if days_since > 0:
                    context += f" It has been {days_since} days since their last check-in."
            except (ValueError, TypeError):
                pass
        
        # Check for due reminders
        due_reminders = self.reminders.get_due_reminders()
        if due_reminders:
            context += f" They have {len(due_reminders)} due reminders."
            
        # Check journal streak
        if hasattr(self.journal, 'calculate_streak'):
            streak = self.journal.calculate_streak()
            if streak > 0:
                context += f" They have a journaling streak of {streak} days."
        
        # Generate greeting template
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
        
        # Check for due reminders
        due_reminders = self.reminders.get_due_reminders()
        if due_reminders:
            print(f"\n{Fore.YELLOW}You have {len(due_reminders)} reminders due:{Style.RESET_ALL}")
            for i, reminder in enumerate(due_reminders[:3], 1):  # Show at most 3
                print(f"{i}. {self.reminders.format_reminder(reminder)}")
            
            if len(due_reminders) > 3:
                print(f"...and {len(due_reminders) - 3} more.")
            
            print()  # Add spacing

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

        # Share a mental health fact occasionally
        if random.random() < 0.3:  # 30% chance
            print(f"\n{Fore.CYAN}Did you know?{Style.RESET_ALL} {self.resources.get_random_mental_health_fact()}\n")

        if "Not so good" in mood or "Terrible" in mood:
            self.handle_negative_mood()
        else:
            self.handle_positive_mood()

        self.main_menu()
        self.save_user_data()
        self.save_preferences()

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

            # Analyze text with local NLP
            sentiment = self.nlp.analyze_sentiment(user_input)
            patterns = self.nlp.detect_patterns(user_input)
            
            # Suggest appropriate therapy module based on detected patterns
            suggested_module = None
            if "stress" in patterns or "anxiety" in patterns:
                suggested_module = next((m for m in self.therapy_modules if m.name == "Anxiety Management"), None)
            elif "mood" in patterns or sentiment["label"] == "negative":
                suggested_module = next((m for m in self.therapy_modules if m.name == "Depression Management"), None)
            elif "sleep" in patterns:
                suggested_module = next((m for m in self.therapy_modules if m.name == "Sleep Improvement"), None)
            
            # Generate response using local NLP
            response = self.nlp.get_response(user_input)
            print(f"\n{Fore.GREEN}{response}{Style.RESET_ALL}")
            
            # Add journal entry
            if questionary.confirm("\nWould you like to save this as a journal entry?").ask():
                prompt = self.nlp.suggest_journal_prompt(user_input)
                tags = []
                
                for pattern in patterns:
                    if pattern not in ["greeting", "farewell", "affirmation", "negation", "question"]:
                        tags.append(pattern)
                
                self.journal.add_entry(
                    user_input,
                    mood=self.mood_history[-1]['mood'],
                    prompt=prompt,
                    tags=tags
                )
                print(f"{Fore.GREEN}Journal entry saved!{Style.RESET_ALL}")
            
            # Suggest therapy module if relevant
            if suggested_module:
                if questionary.confirm(f"\nBased on what you shared, would you like to try a {suggested_module.name} exercise?").ask():
                    exercise = suggested_module.get_exercise()
                    if exercise:
                        completed = run_exercise(exercise, suggested_module.name)
                        if completed:
                            suggested_module.complete_exercise(exercise['name'])
                            
                            # Update preferences
                            self.preferences["therapy_module_history"].append({
                                "module": suggested_module.name,
                                "exercise": exercise['name'],
                                "timestamp": datetime.now().isoformat()
                            })
                            # Keep history manageable
                            if len(self.preferences["therapy_module_history"]) > 20:
                                self.preferences["therapy_module_history"] = self.preferences["therapy_module_history"][-20:]
            
            print("\nWould you like to try some simple exercises that might help?")

    def handle_positive_mood(self):
        """Handle when user is feeling good."""
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
            
            # Analyze with local NLP
            sentiment = self.nlp.analyze_sentiment(user_input)
            patterns = self.nlp.detect_patterns(user_input)
            
            # Generate response
            response = self.nlp.get_response(user_input)
            print(f"\n{Fore.GREEN}{response}{Style.RESET_ALL}")
            
            # Add journal entry for positive experiences too
            if questionary.confirm("\nWould you like to save this as a gratitude journal entry?").ask():
                prompt = "What are you most grateful for in this situation?"
                tags = ["gratitude"]
                
                for pattern in patterns:
                    if pattern not in ["greeting", "farewell", "affirmation", "negation", "question"]:
                        tags.append(pattern)
                
                self.journal.add_entry(
                    user_input, 
                    mood=self.mood_history[-1]['mood'],
                    prompt=prompt,
                    tags=tags
                )
                print(f"{Fore.GREEN}Gratitude journal entry saved!{Style.RESET_ALL}")
                
                # Offer to visualize mood trends
                if len(self.mood_history) >= 3:
                    if questionary.confirm("\nWould you like to see your mood trends?").ask():
                        mood_chart = generate_ascii_chart(self.mood_history)
                        print(mood_chart)

    def main_menu(self):
        """Display main menu with all available features."""
        options = [
            "🧠 Therapy Modules",
            "📔 Journal",
            "📈 Mood Tracker",
            "⏰ Reminders",
            "📚 Resources",
            "💬 Chat",
            "❌ Exit"
        ]
        
        while True:
            choice = questionary.select(
                "\nWhat would you like to do today?",
                choices=options
            ).ask()
            
            # Track feature usage
            if "Exit" not in choice:
                self.preferences["last_used_features"].append({
                    "feature": choice,
                    "timestamp": datetime.now().isoformat()
                })
                # Keep history manageable
                if len(self.preferences["last_used_features"]) > 20:
                    self.preferences["last_used_features"] = self.preferences["last_used_features"][-20:]
            
            if "Therapy Modules" in choice:
                self.show_therapy_modules()
            elif "Journal" in choice:
                self.show_journal_options()
            elif "Mood Tracker" in choice:
                self.show_mood_tracker()
            elif "Reminders" in choice:
                self.manage_reminders()
            elif "Resources" in choice:
                self.show_resources()
            elif "Chat" in choice:
                self.chat_mode()
            elif "Exit" in choice:
                # Show a farewell message
                farewells = [
                    "Take care of yourself. Remember, I'm here whenever you need me.",
                    "Goodbye for now. I'll be here next time you want to chat.",
                    "Wishing you well until we meet again. Take good care of yourself!",
                    "Until next time, be kind to yourself. I'll be here when you return.",
                    "Thank you for checking in today. I look forward to our next conversation!",
                    "Take care of yourself. Remember that each day is a new opportunity."
                ]
                print(f"\n{Fore.CYAN}{random.choice(farewells)}{Style.RESET_ALL}\n")
                break
    
    def show_therapy_modules(self):
        """Display available therapy modules."""
        print(f"\n{Fore.CYAN}Available Therapy Modules:{Style.RESET_ALL}")
        
        module_choices = []
        for i, module in enumerate(self.therapy_modules, 1):
            module_choices.append(f"{i}. {module.name} - {module.description}")
        
        module_choices.append("Back to Main Menu")
        
        choice = questionary.select(
            "Select a module:",
            choices=module_choices
        ).ask()
        
        if "Back to Main Menu" in choice:
            return
        
        # Get module index
        try:
            idx = int(choice.split(".")[0]) - 1
            selected_module = self.therapy_modules[idx]
            
            print(f"\n{Fore.CYAN}Selected: {selected_module.name}{Style.RESET_ALL}")
            print(selected_module.get_progress_summary())
            
            if questionary.confirm("\nWould you like to try an exercise?").ask():
                exercise = selected_module.get_exercise()
                if exercise:
                    completed = run_exercise(exercise, selected_module.name)
                    if completed:
                        selected_module.complete_exercise(exercise['name'])
                        
                        # Update preferences
                        self.preferences["therapy_module_history"].append({
                            "module": selected_module.name,
                            "exercise": exercise['name'],
                            "timestamp": datetime.now().isoformat()
                        })
                else:
                    print("No exercises available in this module.")
        except (ValueError, IndexError):
            print("Invalid selection.")
    
    def show_journal_options(self):
        """Display journal options."""
        print(f"\n{Fore.CYAN}Journal Options:{Style.RESET_ALL}")
        
        options = [
            "Create New Entry",
            "View Recent Entries",
            "Search Entries",
            "View Journal Stats",
            "Back to Main Menu"
        ]
        
        choice = questionary.select(
            "What would you like to do?",
            choices=options
        ).ask()
        
        if choice == "Create New Entry":
            self.create_journal_entry()
        elif choice == "View Recent Entries":
            self.view_journal_entries()
        elif choice == "Search Entries":
            self.search_journal_entries()
        elif choice == "View Journal Stats":
            stats = self.journal.get_entry_stats()
            print(f"\n{Fore.CYAN}Journal Statistics:{Style.RESET_ALL}\n{stats}")
    
    def create_journal_entry(self):
        """Create a new journal entry."""
        print(f"\n{Fore.CYAN}New Journal Entry:{Style.RESET_ALL}")
        
        # Suggest a prompt
        mood = self.mood_history[-1]['mood'] if self.mood_history else "😐 Okay"
        prompt = self.journal.get_prompt_for_mood(mood)
        
        print(f"\n{Fore.YELLOW}Prompt: {prompt}{Style.RESET_ALL}")
        
        content = questionary.text(
            "Write your entry (or type a different prompt to change):",
            multiline=True
        ).ask()
        
        # Check if the user entered a different prompt
        if len(content.split()) <= 7 and "?" in content:
            prompt = content
            content = questionary.text(
                f"{Fore.YELLOW}New Prompt: {prompt}{Style.RESET_ALL}\nWrite your entry:",
                multiline=True
            ).ask()
        
        # Get tags
        tags_input = questionary.text(
            "Add tags (comma separated, optional):"
        ).ask()
        
        tags = []
        if tags_input.strip():
            tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
        
        # Add entry
        entry = self.journal.add_entry(
            content,
            mood=mood,
            prompt=prompt,
            tags=tags
        )
        
        print(f"\n{Fore.GREEN}Journal entry saved!{Style.RESET_ALL}")
        print(self.journal.format_entry_for_display(entry))
        
        # Update preferences
        self.preferences["journal_frequency"] = self.preferences.get("journal_frequency", 0) + 1
    
    def view_journal_entries(self):
        """View recent journal entries."""
        entries = self.journal.get_entries(limit=5)
        
        if not entries:
            print(f"\n{Fore.YELLOW}No journal entries found.{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}Recent Journal Entries:{Style.RESET_ALL}")
        
        for i, entry in enumerate(entries, 1):
            print(f"\n{i}. {self.journal.format_entry_for_display(entry)}")
            print("-" * 50)
    
    def search_journal_entries(self):
        """Search journal entries."""
        query = questionary.text(
            "Enter search term:"
        ).ask()
        
        if not query.strip():
            return
        
        results = self.journal.search_entries(query)
        
        if not results:
            print(f"\n{Fore.YELLOW}No entries found matching '{query}'.{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}Found {len(results)} entries matching '{query}':{Style.RESET_ALL}")
        
        for i, entry in enumerate(results[:5], 1):  # Show up to 5 results
            print(f"\n{i}. {self.journal.format_entry_for_display(entry)}")
            print("-" * 50)
        
        if len(results) > 5:
            print(f"\n...and {len(results) - 5} more.")
    
    def show_mood_tracker(self):
        """Display mood tracking visualization."""
        if len(self.mood_history) < 3:
            print(f"\n{Fore.YELLOW}Not enough mood data collected yet. Check in more often to see your trends.{Style.RESET_ALL}")
            return
        
        # Generate and display chart
        mood_chart = generate_ascii_chart(self.mood_history)
        print(mood_chart)
        
        # Offer to download mood data
        if questionary.confirm("\nWould you like to export your mood data as JSON?").ask():
            export_path = "mood_export.json"
            with open(export_path, 'w') as f:
                json.dump(self.mood_history, f, indent=2)
            print(f"\n{Fore.GREEN}Mood data exported to {export_path}{Style.RESET_ALL}")
    
    def manage_reminders(self):
        """Manage reminders."""
        print(f"\n{Fore.CYAN}Reminder System{Style.RESET_ALL}")
        
        options = [
            "View Upcoming Reminders",
            "Add New Reminder",
            "Get Suggestions",
            "Mark Reminder Complete",
            "Back to Main Menu"
        ]
        
        choice = questionary.select(
            "What would you like to do?",
            choices=options
        ).ask()
        
        if choice == "View Upcoming Reminders":
            upcoming = self.reminders.get_upcoming_reminders()
            if upcoming:
                print(f"\n{Fore.CYAN}Upcoming Reminders:{Style.RESET_ALL}")
                for i, reminder in enumerate(upcoming, 1):
                    print(f"\n{i}. {self.reminders.format_reminder(reminder)}")
            else:
                print("\nNo upcoming reminders found.")
                
        elif choice == "Add New Reminder":
            title = questionary.text("Enter reminder title:").ask()
            if not title.strip():
                return
                
            suggested_time = self.reminders.suggest_check_in_time()
            datetime_str = questionary.text(
                f"Enter date and time (YYYY-MM-DD HH:MM) [suggested: {suggested_time}]:"
            ).ask()
            
            if not datetime_str.strip():
                datetime_str = suggested_time
            
            description = questionary.text("Enter description (optional):").ask()
            
            recurring_options = ["none", "daily", "weekly", "monthly"]
            recurring_choice = questionary.select(
                "How often should this repeat?",
                choices=recurring_options
            ).ask()
            
            recurring = recurring_choice if recurring_choice != "none" else None
            
            success, message = self.reminders.add_reminder(title, datetime_str, description, recurring)
            print(f"\n{message}")
            
        elif choice == "Get Suggestions":
            suggestions = self.reminders.generate_check_in_suggestions()
            print(f"\n{Fore.CYAN}Suggested Check-ins:{Style.RESET_ALL}")
            
            for i, suggestion in enumerate(suggestions, 1):
                print(f"\n{i}. {Fore.GREEN}{suggestion['title']}{Style.RESET_ALL}")
                print(f"   Description: {suggestion['description']}")
                print(f"   Recurring: {suggestion['recurring']}")
            
            add_choice = questionary.text(
                "\nEnter number to add (or leave blank to skip):"
            ).ask()
            
            try:
                idx = int(add_choice) - 1
                if 0 <= idx < len(suggestions):
                    suggestion = suggestions[idx]
                    suggested_time = self.reminders.suggest_check_in_time()
                    datetime_str = questionary.text(
                        f"Enter date and time (YYYY-MM-DD HH:MM) [suggested: {suggested_time}]:"
                    ).ask()
                    
                    if not datetime_str.strip():
                        datetime_str = suggested_time
                    
                    success, message = self.reminders.add_reminder(
                        suggestion["title"], 
                        datetime_str, 
                        suggestion["description"], 
                        suggestion["recurring"]
                    )
                    print(f"\n{message}")
            except (ValueError, IndexError):
                pass
                
        elif choice == "Mark Reminder Complete":
            reminders = self.reminders.get_due_reminders()
            if not reminders:
                print("\nNo due reminders found.")
                return
                
            print(f"\n{Fore.CYAN}Due Reminders:{Style.RESET_ALL}")
            for i, reminder in enumerate(reminders, 1):
                print(f"\n{i}. {self.reminders.format_reminder(reminder)}")
                
            complete_choice = questionary.text(
                "\nEnter number to mark as complete (or leave blank to cancel):"
            ).ask()
            
            try:
                idx = int(complete_choice) - 1
                if 0 <= idx < len(reminders):
                    reminder_id = reminders[idx].get("id")
                    success, message = self.reminders.mark_reminder_completed(reminder_id)
                    print(f"\n{message}")
            except (ValueError, IndexError):
                pass
    
    def show_resources(self):
        """Display mental health resources."""
        print(f"\n{Fore.CYAN}Mental Health Resources{Style.RESET_ALL}")
        
        options = [
            "Crisis Resources",
            "Self-Help Resources",
            "Reading Recommendations",
            "Mental Health Fact",
            "Back to Main Menu"
        ]
        
        choice = questionary.select(
            "What type of resources would you like?",
            choices=options
        ).ask()
        
        if choice == "Crisis Resources":
            country = questionary.text(
                "Enter country code (us, canada, uk, australia) or leave blank for all:"
            ).ask()
            
            resources = self.resources.get_crisis_resources(country if country.strip() else None)
            print(self.resources.format_crisis_resources(resources))
            
        elif choice == "Self-Help Resources":
            tag = questionary.text(
                "Enter a tag (e.g., anxiety, depression, sleep) or leave blank:"
            ).ask()
            
            resources = self.resources.get_self_help_resources(tag if tag.strip() else None)
            print(self.resources.format_self_help_resources(resources))
            
        elif choice == "Reading Recommendations":
            categories = ", ".join(self.resources.reading_recommendations.keys())
            category = questionary.text(
                f"Enter a category ({categories}) or leave blank:"
            ).ask()
            
            books = self.resources.get_reading_recommendations(category if category.strip() else None)
            print(self.resources.format_reading_recommendations(books))
            
        elif choice == "Mental Health Fact":
            fact = self.resources.get_random_mental_health_fact()
            print(f"\n{Fore.CYAN}Did you know?{Style.RESET_ALL}\n{fact}")
    
    def chat_mode(self):
        """Open-ended chat mode using local NLP."""
        print(f"\n{Fore.CYAN}Chat Mode - Type 'exit' to return to main menu{Style.RESET_ALL}")
        
        while True:
            user_input = questionary.text("You:").ask()
            
            if user_input.lower() in ['exit', 'quit', 'back', 'menu']:
                break
                
            # Analyze the input
            sentiment = self.nlp.analyze_sentiment(user_input)
            patterns = self.nlp.detect_patterns(user_input)
            topics = self.nlp.extract_topics(user_input)
            
            # Generate a response
            response = self.nlp.get_response(user_input)
            print(f"\nTherapy Bot: {response}")
            
            # Occasionally suggest a journal prompt
            if random.random() < 0.2:  # 20% chance
                prompt = self.nlp.suggest_journal_prompt(user_input)
                print(f"\n{Fore.YELLOW}Journal Prompt: {prompt}{Style.RESET_ALL}")
                
                if questionary.confirm("Would you like to respond to this prompt now?").ask():
                    content = questionary.text(
                        prompt,
                        multiline=True
                    ).ask()
                    
                    tags = []
                    for pattern in patterns:
                        if pattern not in ["greeting", "farewell", "affirmation", "negation", "question"]:
                            tags.append(pattern)
                    
                    # Add topics as tags
                    tags.extend(topics[:2])  # Add up to 2 topics as tags
                    
                    self.journal.add_entry(
                        content,
                        mood=self.mood_history[-1]['mood'] if self.mood_history else None,
                        prompt=prompt,
                        tags=tags
                    )
                    print(f"\n{Fore.GREEN}Journal entry saved!{Style.RESET_ALL}")

    def run(self):
        """Main entry point that handles command line arguments."""
        if self.args.version:
            print("Enhanced Therapy Bot v1.0.0")
            return
            
        if not self.args.skip_greeting:
            self.check_in()
        else:
            # If skipping greeting but we don't have a name, ask for it
            if not self.user_name:
                self.user_name = questionary.text(
                    "First, could you tell me your name?",
                    validate=lambda text: len(text) > 0
                ).ask()
                self.save_user_data()
                
        # Handle direct navigation to specific features
        if self.args.module:
            module_name = self.args.module.lower()
            for module in self.therapy_modules:
                if module_name in module.name.lower():
                    print(f"\n{Fore.CYAN}Going directly to {module.name}{Style.RESET_ALL}")
                    time.sleep(1)
                    
                    print(f"\n{Fore.CYAN}Selected: {module.name}{Style.RESET_ALL}")
                    print(module.get_progress_summary())
                    
                    if questionary.confirm("\nWould you like to try an exercise?").ask():
                        exercise = module.get_exercise()
                        if exercise:
                            completed = run_exercise(exercise, module.name)
                            if completed:
                                module.complete_exercise(exercise['name'])
                    
                    self.main_menu()
                    return
            
            print(f"\n{Fore.YELLOW}Module '{self.args.module}' not found.{Style.RESET_ALL}")
            
        elif self.args.journal:
            print(f"\n{Fore.CYAN}Going directly to Journal{Style.RESET_ALL}")
            time.sleep(1)
            self.show_journal_options()
            self.main_menu()
            
        elif self.args.reminders:
            print(f"\n{Fore.CYAN}Going directly to Reminders{Style.RESET_ALL}")
            time.sleep(1)
            self.manage_reminders()
            self.main_menu()
            
        elif self.args.chat:
            print(f"\n{Fore.CYAN}Going directly to Chat Mode{Style.RESET_ALL}")
            time.sleep(1)
            self.chat_mode()
            self.main_menu()
            
        else:
            # If no specific destination and we skipped greeting, show main menu
            if self.args.skip_greeting:
                self.main_menu()

if __name__ == "__main__":
    bot = EnhancedTherapyBot()
    bot.run() 