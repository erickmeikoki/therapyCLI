#!/usr/bin/env python3

import json
import os
from datetime import datetime, timedelta
import time
from colorama import Fore, Style
import random

class ReminderSystem:
    def __init__(self):
        self.reminders_file = "reminders.json"
        self.reminders = self.load_reminders()
    
    def load_reminders(self):
        """Load reminders from file."""
        try:
            if os.path.exists(self.reminders_file):
                with open(self.reminders_file, 'r') as f:
                    return json.load(f)
            return []
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def save_reminders(self):
        """Save reminders to file."""
        with open(self.reminders_file, 'w') as f:
            json.dump(self.reminders, f, indent=2)
    
    def add_reminder(self, title, datetime_str, description="", recurring=None):
        """Add a new reminder.
        
        Args:
            title: Title of the reminder
            datetime_str: Datetime string in format 'YYYY-MM-DD HH:MM'
            description: Optional description
            recurring: Optional, one of 'daily', 'weekly', 'monthly', or None
        """
        try:
            reminder_time = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
            
            reminder = {
                "id": str(int(time.time())),  # Unix timestamp as ID
                "title": title,
                "datetime": reminder_time.isoformat(),
                "description": description,
                "recurring": recurring,
                "completed": False,
                "created_at": datetime.now().isoformat()
            }
            
            self.reminders.append(reminder)
            self.save_reminders()
            return True, "Reminder added successfully."
        except ValueError:
            return False, "Invalid date format. Please use YYYY-MM-DD HH:MM format."
    
    def remove_reminder(self, reminder_id):
        """Remove a reminder by ID."""
        initial_count = len(self.reminders)
        self.reminders = [r for r in self.reminders if r.get("id") != reminder_id]
        
        if len(self.reminders) < initial_count:
            self.save_reminders()
            return True, "Reminder removed successfully."
        else:
            return False, "Reminder not found."
    
    def mark_reminder_completed(self, reminder_id):
        """Mark a reminder as completed."""
        for reminder in self.reminders:
            if reminder.get("id") == reminder_id:
                reminder["completed"] = True
                
                # If it's recurring, create the next instance
                if reminder.get("recurring"):
                    self._create_next_recurring_reminder(reminder)
                
                self.save_reminders()
                return True, "Reminder marked as completed."
        
        return False, "Reminder not found."
    
    def _create_next_recurring_reminder(self, reminder):
        """Create the next instance of a recurring reminder."""
        try:
            current_time = datetime.fromisoformat(reminder.get("datetime"))
            recurring_type = reminder.get("recurring")
            
            if recurring_type == "daily":
                next_time = current_time + timedelta(days=1)
            elif recurring_type == "weekly":
                next_time = current_time + timedelta(weeks=1)
            elif recurring_type == "monthly":
                # Approximate a month as 30 days
                next_time = current_time + timedelta(days=30)
            else:
                return
            
            new_reminder = reminder.copy()
            new_reminder["id"] = str(int(time.time()))
            new_reminder["datetime"] = next_time.isoformat()
            new_reminder["completed"] = False
            new_reminder["created_at"] = datetime.now().isoformat()
            
            self.reminders.append(new_reminder)
        except (ValueError, TypeError):
            pass
    
    def get_due_reminders(self, include_completed=False):
        """Get reminders that are due (datetime <= now)."""
        now = datetime.now()
        due = []
        
        for reminder in self.reminders:
            try:
                reminder_time = datetime.fromisoformat(reminder.get("datetime"))
                if reminder_time <= now and (include_completed or not reminder.get("completed", False)):
                    due.append(reminder)
            except (ValueError, TypeError):
                continue
        
        return due
    
    def get_upcoming_reminders(self, days=7, include_completed=False):
        """Get reminders coming up in the next X days."""
        now = datetime.now()
        future = now + timedelta(days=days)
        upcoming = []
        
        for reminder in self.reminders:
            try:
                reminder_time = datetime.fromisoformat(reminder.get("datetime"))
                if now <= reminder_time <= future and (include_completed or not reminder.get("completed", False)):
                    upcoming.append(reminder)
            except (ValueError, TypeError):
                continue
        
        # Sort by datetime
        upcoming.sort(key=lambda x: datetime.fromisoformat(x.get("datetime")))
        return upcoming
    
    def get_all_reminders(self, include_completed=False):
        """Get all reminders, optionally including completed ones."""
        if include_completed:
            return sorted(self.reminders, key=lambda x: datetime.fromisoformat(x.get("datetime")))
        else:
            return sorted([r for r in self.reminders if not r.get("completed", False)], 
                         key=lambda x: datetime.fromisoformat(x.get("datetime")))
    
    def format_reminder(self, reminder):
        """Format a reminder for display."""
        try:
            reminder_time = datetime.fromisoformat(reminder.get("datetime"))
            time_str = reminder_time.strftime("%a, %b %d at %I:%M %p")
            
            recurring_str = ""
            if reminder.get("recurring"):
                recurring_str = f" (Recurring: {reminder.get('recurring')})"
            
            status = f"{Fore.GREEN}Completed{Style.RESET_ALL}" if reminder.get("completed") else f"{Fore.YELLOW}Pending{Style.RESET_ALL}"
            
            result = [
                f"{Fore.CYAN}{reminder.get('title')}{Style.RESET_ALL}{recurring_str}",
                f"When: {time_str}",
                f"Status: {status}"
            ]
            
            if reminder.get("description"):
                result.append(f"Details: {reminder.get('description')}")
            
            return "\n".join(result)
        except (ValueError, TypeError):
            return f"Invalid reminder format: {reminder.get('title', 'Unknown')}"
    
    def suggest_check_in_time(self):
        """Suggest a good time for the next check-in based on patterns."""
        suggestions = []
        
        # Suggest tomorrow morning
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_morning = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 9, 0)
        suggestions.append(tomorrow_morning)
        
        # Suggest tomorrow evening
        tomorrow_evening = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 19, 0)
        suggestions.append(tomorrow_evening)
        
        # If we have existing reminders, suggest a similar time
        if self.reminders:
            try:
                times = []
                for reminder in self.reminders:
                    dt = datetime.fromisoformat(reminder.get("datetime"))
                    times.append(dt.time())
                
                if times:
                    # Find the most common hour
                    hours = [t.hour for t in times]
                    common_hour = max(set(hours), key=hours.count)
                    
                    # Use that hour tomorrow
                    similar_time = datetime(tomorrow.year, tomorrow.month, tomorrow.day, common_hour, 0)
                    suggestions.append(similar_time)
            except (ValueError, TypeError):
                pass
        
        # Return a random suggestion
        suggestion = random.choice(suggestions)
        return suggestion.strftime("%Y-%m-%d %H:%M")
    
    def generate_check_in_suggestions(self):
        """Generate suggestions for check-in reminders."""
        suggestions = [
            {
                "title": "Daily Mood Check-in",
                "description": "Take a moment to reflect on your mood and log it in your therapy bot.",
                "recurring": "daily"
            },
            {
                "title": "Weekly Journal Session",
                "description": "Spend 15 minutes journaling about your week.",
                "recurring": "weekly"
            },
            {
                "title": "Anxiety Management Exercise",
                "description": "Practice a technique from the Anxiety Management module.",
                "recurring": "daily"
            },
            {
                "title": "Evening Reflection",
                "description": "Reflect on three good things that happened today.",
                "recurring": "daily"
            },
            {
                "title": "Stress Check",
                "description": "Check your stress levels and practice a relaxation technique if needed.",
                "recurring": "daily"
            }
        ]
        
        return suggestions

# Example usage if run directly
if __name__ == "__main__":
    reminder_system = ReminderSystem()
    
    print(f"{Fore.CYAN}Reminder System{Style.RESET_ALL}")
    print("1. Show upcoming reminders")
    print("2. Add a new reminder")
    print("3. Get suggestions")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ")
    
    if choice == "1":
        upcoming = reminder_system.get_upcoming_reminders()
        if upcoming:
            print(f"\n{Fore.CYAN}Upcoming Reminders:{Style.RESET_ALL}")
            for i, reminder in enumerate(upcoming, 1):
                print(f"\n{i}. {reminder_system.format_reminder(reminder)}")
        else:
            print("\nNo upcoming reminders found.")
    
    elif choice == "2":
        title = input("Enter reminder title: ")
        suggested_time = reminder_system.suggest_check_in_time()
        datetime_str = input(f"Enter date and time (YYYY-MM-DD HH:MM) [suggested: {suggested_time}]: ")
        if not datetime_str.strip():
            datetime_str = suggested_time
        
        description = input("Enter description (optional): ")
        
        recurring_options = ["none", "daily", "weekly", "monthly"]
        print("Recurring options:")
        for i, option in enumerate(recurring_options):
            print(f"{i+1}. {option}")
        
        recurring_choice = input("Select recurring option (1-4): ")
        try:
            recurring = recurring_options[int(recurring_choice) - 1]
            if recurring == "none":
                recurring = None
        except (ValueError, IndexError):
            recurring = None
        
        success, message = reminder_system.add_reminder(title, datetime_str, description, recurring)
        print(f"\n{message}")
    
    elif choice == "3":
        suggestions = reminder_system.generate_check_in_suggestions()
        print(f"\n{Fore.CYAN}Suggested Check-ins:{Style.RESET_ALL}")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"\n{i}. {Fore.GREEN}{suggestion['title']}{Style.RESET_ALL}")
            print(f"   Description: {suggestion['description']}")
            print(f"   Recurring: {suggestion['recurring']}")
        
        add_choice = input("\nWould you like to add any of these? (Enter number or 'n' to skip): ")
        try:
            idx = int(add_choice) - 1
            if 0 <= idx < len(suggestions):
                suggestion = suggestions[idx]
                suggested_time = reminder_system.suggest_check_in_time()
                datetime_str = input(f"Enter date and time (YYYY-MM-DD HH:MM) [suggested: {suggested_time}]: ")
                if not datetime_str.strip():
                    datetime_str = suggested_time
                
                success, message = reminder_system.add_reminder(
                    suggestion["title"], 
                    datetime_str, 
                    suggestion["description"], 
                    suggestion["recurring"]
                )
                print(f"\n{message}")
        except (ValueError, IndexError):
            print("No reminder added.")
    
    elif choice == "4":
        print("Exiting reminder system.") 