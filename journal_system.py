#!/usr/bin/env python3

import json
import os
from datetime import datetime
import random
from colorama import Fore, Style

class JournalSystem:
    def __init__(self):
        self.journal_file = "journal_entries.json"
        self.entries = self.load_entries()
        self.prompts = self.load_prompts()
    
    def load_entries(self):
        """Load journal entries from file."""
        try:
            if os.path.exists(self.journal_file):
                with open(self.journal_file, 'r') as f:
                    return json.load(f)
            return []
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def save_entries(self):
        """Save journal entries to file."""
        with open(self.journal_file, 'w') as f:
            json.dump(self.entries, f, indent=2)
    
    def load_prompts(self):
        """Load prompts for different moods."""
        return {
            "positive": [
                "What made you smile today?",
                "What are you most grateful for right now?",
                "What's something you're looking forward to?",
                "What's something that went well recently?",
                "What's a small win you've had lately?",
                "How did you take care of yourself today?",
                "What's something you're proud of accomplishing?",
                "Who had a positive impact on your day, and how?",
                "What's something beautiful you noticed today?",
                "What's something you learned recently that excited you?"
            ],
            "neutral": [
                "What's on your mind today?",
                "How would you describe your energy level right now?",
                "What are you curious about lately?",
                "What do you want to remember about today?",
                "How did today differ from your expectations?",
                "What's something you'd like to do differently tomorrow?",
                "What would make tomorrow a good day?",
                "What are you thinking about but not saying?",
                "What's something you're still figuring out?",
                "If today were a color, what would it be and why?"
            ],
            "negative": [
                "What's been challenging for you lately?",
                "What do you need right now that you're not getting?",
                "What would help you feel better in this moment?",
                "What's something that's bothering you that you could let go of?",
                "What negative thought keeps coming up, and how can you reframe it?",
                "What small step could you take to improve your situation?",
                "What's one thing you can control right now?",
                "When was the last time you felt better, and what was different?",
                "What would you tell a friend who was feeling the way you are?",
                "What have you overcome in the past that reminds you of your strength?"
            ]
        }
    
    def get_prompt_for_mood(self, mood):
        """Get a random prompt appropriate for the current mood."""
        if "Great" in mood or "Good" in mood:
            category = "positive"
        elif "Okay" in mood:
            category = "neutral"
        else:
            category = "negative"
        
        return random.choice(self.prompts[category])
    
    def add_entry(self, content, mood=None, prompt=None, tags=None):
        """Add a new journal entry."""
        entry = {
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "mood": mood,
            "prompt": prompt,
            "tags": tags or []
        }
        
        self.entries.append(entry)
        self.save_entries()
        return entry
    
    def get_entries(self, limit=5, mood=None, tag=None):
        """Get recent journal entries, optionally filtered by mood or tag."""
        filtered = self.entries
        
        if mood:
            filtered = [e for e in filtered if e.get("mood") == mood]
        
        if tag:
            filtered = [e for e in filtered if tag.lower() in [t.lower() for t in e.get("tags", [])]]
        
        # Sort by date (newest first)
        filtered.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        
        return filtered[:limit]
    
    def search_entries(self, query):
        """Search entries for a specific term."""
        query = query.lower()
        results = [
            e for e in self.entries 
            if query in e.get("content", "").lower() or 
               query in e.get("prompt", "").lower() or
               any(query in tag.lower() for tag in e.get("tags", []))
        ]
        
        # Sort by date (newest first)
        results.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        
        return results
    
    def format_entry_for_display(self, entry):
        """Format an entry for terminal display."""
        date_str = "Unknown date"
        try:
            dt = datetime.fromisoformat(entry.get("timestamp", ""))
            date_str = dt.strftime("%a, %b %d, %Y at %I:%M %p")
        except (ValueError, TypeError):
            pass
        
        mood_str = f" | Mood: {entry.get('mood', 'Not recorded')}" if entry.get("mood") else ""
        
        result = [
            f"{Fore.CYAN}Entry from {date_str}{mood_str}{Style.RESET_ALL}",
            f"{Fore.YELLOW}Prompt: {entry.get('prompt', 'No prompt')}{Style.RESET_ALL}",
            f"\n{entry.get('content', '')}\n"
        ]
        
        if entry.get("tags"):
            tags_str = ", ".join(f"#{tag}" for tag in entry.get("tags", []))
            result.append(f"{Fore.GREEN}Tags: {tags_str}{Style.RESET_ALL}")
        
        return "\n".join(result)
    
    def get_entry_stats(self):
        """Get statistics about journal entries."""
        if not self.entries:
            return "No journal entries yet."
        
        total_entries = len(self.entries)
        
        # Get date range
        dates = [datetime.fromisoformat(e.get("timestamp", datetime.now().isoformat())) 
                for e in self.entries if e.get("timestamp")]
        dates.sort()
        
        if dates:
            first_entry = dates[0].strftime("%b %d, %Y")
            streak = self.calculate_streak()
            
            mood_counts = {}
            for e in self.entries:
                mood = e.get("mood")
                if mood:
                    mood_counts[mood] = mood_counts.get(mood, 0) + 1
            
            common_mood = max(mood_counts.items(), key=lambda x: x[1]) if mood_counts else None
            
            stats = [
                f"Total entries: {total_entries}",
                f"Journaling since: {first_entry}",
                f"Current streak: {streak} days"
            ]
            
            if common_mood:
                stats.append(f"Most common mood: {common_mood[0]} ({common_mood[1]} entries)")
            
            # Find most used tags
            all_tags = []
            for e in self.entries:
                all_tags.extend(e.get("tags", []))
            
            tag_counts = {}
            for tag in all_tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
            
            if tag_counts:
                top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:3]
                tag_str = ", ".join(f"#{tag} ({count})" for tag, count in top_tags)
                stats.append(f"Top tags: {tag_str}")
            
            return "\n".join(stats)
        
        return "Journal statistics not available."
    
    def calculate_streak(self):
        """Calculate the current journaling streak in days."""
        if not self.entries:
            return 0
        
        # Get unique dates of entries
        dates = set()
        for entry in self.entries:
            try:
                dt = datetime.fromisoformat(entry.get("timestamp", ""))
                dates.add(dt.strftime("%Y-%m-%d"))
            except (ValueError, TypeError):
                continue
        
        dates = sorted(dates, reverse=True)
        
        if not dates:
            return 0
        
        # Check if there's an entry today
        today = datetime.now().strftime("%Y-%m-%d")
        if today not in dates:
            return 0
        
        # Calculate streak
        streak = 1
        current_date = datetime.strptime(today, "%Y-%m-%d")
        
        for i in range(1, len(dates)):
            prev_date = current_date - datetime.timedelta(days=1)
            prev_date_str = prev_date.strftime("%Y-%m-%d")
            
            if prev_date_str in dates:
                streak += 1
                current_date = prev_date
            else:
                break
        
        return streak

# Example usage if run directly
if __name__ == "__main__":
    journal = JournalSystem()
    
    # Add a sample entry if none exist
    if not journal.entries:
        journal.add_entry(
            "Today was a good day. I accomplished a lot and felt productive.",
            mood="😌 Good",
            prompt="What went well today?",
            tags=["productivity", "work"]
        )
    
    # Display all entries
    print(f"{Fore.CYAN}Journal Entries:{Style.RESET_ALL}\n")
    for entry in journal.get_entries(limit=3):
        print(journal.format_entry_for_display(entry))
        print("-" * 50)
    
    # Show stats
    print(f"\n{Fore.CYAN}Journal Stats:{Style.RESET_ALL}")
    print(journal.get_entry_stats()) 