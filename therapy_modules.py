#!/usr/bin/env python3

import random
import time
from colorama import Fore, Style, init
import json
import os
from datetime import datetime, timedelta

# Initialize colorama
init()

class TherapyModule:
    """Base class for all therapy modules."""
    
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.exercises = []
        self.progress_file = f"{name.lower().replace(' ', '_')}_progress.json"
        self.progress = self.load_progress()
    
    def load_progress(self):
        """Load progress data from file."""
        try:
            if os.path.exists(self.progress_file):
                with open(self.progress_file, 'r') as f:
                    return json.load(f)
            return {"exercises_completed": [], "last_session": None}
        except (json.JSONDecodeError, FileNotFoundError):
            return {"exercises_completed": [], "last_session": None}
    
    def save_progress(self):
        """Save progress data to file."""
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress, f)
    
    def get_exercise(self):
        """Get a random exercise from the module."""
        if not self.exercises:
            return None
        return random.choice(self.exercises)
    
    def complete_exercise(self, exercise_name):
        """Mark an exercise as completed."""
        self.progress["exercises_completed"].append({
            "exercise": exercise_name,
            "timestamp": datetime.now().isoformat()
        })
        self.progress["last_session"] = datetime.now().isoformat()
        self.save_progress()
    
    def get_progress_summary(self):
        """Get a summary of progress in this module."""
        if not self.progress["exercises_completed"]:
            return f"You haven't completed any {self.name} exercises yet."
        
        total_exercises = len(self.progress["exercises_completed"])
        unique_exercises = len(set(e["exercise"] for e in self.progress["exercises_completed"]))
        
        last_session = None
        if self.progress["last_session"]:
            try:
                last_session_dt = datetime.fromisoformat(self.progress["last_session"])
                last_session = last_session_dt.strftime("%a, %b %d at %I:%M %p")
            except ValueError:
                pass
        
        summary = [
            f"You've completed {total_exercises} {self.name} exercises.",
            f"You've tried {unique_exercises} different exercises.",
        ]
        
        if last_session:
            summary.append(f"Your last session was on {last_session}.")
        
        # Count exercises in the last week
        recent_count = 0
        week_ago = datetime.now() - timedelta(days=7)
        for entry in self.progress["exercises_completed"]:
            try:
                entry_dt = datetime.fromisoformat(entry["timestamp"])
                if entry_dt > week_ago:
                    recent_count += 1
            except ValueError:
                continue
        
        summary.append(f"You've done {recent_count} exercises in the past week.")
        
        return "\n".join(summary)

class AnxietyModule(TherapyModule):
    """Module for anxiety management."""
    
    def __init__(self):
        super().__init__("Anxiety Management", "Techniques to reduce anxiety and manage panic")
        self.exercises = [
            {
                "name": "5-4-3-2-1 Grounding",
                "description": "A sensory awareness exercise to ground yourself in the present moment.",
                "steps": [
                    "Find a comfortable position and take a deep breath.",
                    "Name 5 things you can SEE around you.",
                    "Name 4 things you can FEEL or TOUCH right now.",
                    "Name 3 things you can HEAR in this moment.",
                    "Name 2 things you can SMELL (or like the smell of).",
                    "Name 1 thing you can TASTE (or like the taste of).",
                    "Notice how your body feels now compared to when you started."
                ]
            },
            {
                "name": "Progressive Muscle Relaxation",
                "description": "Systematically tense and release muscle groups to reduce physical tension.",
                "steps": [
                    "Find a quiet, comfortable place to sit or lie down.",
                    "Take a deep breath in, and tense your feet and toes for 5 seconds.",
                    "Release the tension and notice the difference. Breathe normally.",
                    "Next, tense your calf muscles for 5 seconds.",
                    "Release and notice the sensation of relaxation.",
                    "Continue this pattern up through your body: thighs, abdomen, chest, hands, arms, shoulders, neck, and face.",
                    "Finally, take a deep breath and notice how your body feels now."
                ]
            },
            {
                "name": "Worry Time",
                "description": "Schedule a specific time to address worries, reducing their impact throughout the day.",
                "steps": [
                    "Choose a 15-minute 'worry time' each day (not right before bed).",
                    "When worries arise outside this time, write them down to address later.",
                    "During your designated worry time, review your list and address each concern.",
                    "For each worry, ask: Is this within my control? What's one small step I could take?",
                    "After your worry time ends, put the list away until tomorrow.",
                    "This practice helps contain worry to a specific time rather than all day."
                ]
            },
            {
                "name": "Thought Challenging",
                "description": "Identify and challenge anxious thoughts using evidence and alternative perspectives.",
                "steps": [
                    "Identify a specific thought that's making you anxious.",
                    "Rate how strongly you believe this thought (0-100%).",
                    "What evidence supports this thought?",
                    "What evidence contradicts this thought?",
                    "Is there an alternative explanation or perspective?",
                    "What would you tell a friend who had this thought?",
                    "How would you reframe this thought in a more balanced way?",
                    "Rate how strongly you believe the original thought now (0-100%)."
                ]
            }
        ]

class DepressionModule(TherapyModule):
    """Module for depression management."""
    
    def __init__(self):
        super().__init__("Depression Management", "Strategies to improve mood and combat depression")
        self.exercises = [
            {
                "name": "Behavioral Activation",
                "description": "Engage in meaningful activities to improve mood even when motivation is low.",
                "steps": [
                    "Make a list of activities that typically bring you joy or satisfaction.",
                    "Rate each activity by difficulty (1-10) and potential satisfaction (1-10).",
                    "Start with activities that are lower in difficulty but higher in satisfaction.",
                    "Schedule one such activity for tomorrow, being specific about when and how.",
                    "After completing the activity, note how you felt before, during, and after.",
                    "Gradually increase the number and difficulty of activities as you progress."
                ]
            },
            {
                "name": "Gratitude Practice",
                "description": "Focus on positive aspects of life to shift attention from negative thoughts.",
                "steps": [
                    "Take a few deep breaths to center yourself.",
                    "Think of three specific things you're grateful for today, no matter how small.",
                    "For each one, write down what it is and why you appreciate it.",
                    "Try to include different areas of life (people, experiences, abilities, etc.).",
                    "Notice any feelings that arise as you reflect on these positive elements."
                ]
            },
            {
                "name": "Values Reflection",
                "description": "Reconnect with your core values to find meaning and direction.",
                "steps": [
                    "Consider different life domains: relationships, work, personal growth, leisure, etc.",
                    "For each domain, ask: What matters most to me in this area?",
                    "Choose one value that feels most important to you right now.",
                    "Reflect on how you can express this value today, even in a small way.",
                    "Plan one specific action aligned with this value for tomorrow."
                ]
            },
            {
                "name": "Positive Memory Bank",
                "description": "Build a collection of positive memories to counter negative thought patterns.",
                "steps": [
                    "Recall a positive memory where you felt happy, proud, or connected.",
                    "Write down the memory in detail using all five senses.",
                    "What were you seeing, hearing, feeling, smelling, and tasting?",
                    "Notice the emotions connected to this memory.",
                    "Take a moment to fully re-experience this positive memory.",
                    "Add this to your 'memory bank' to revisit when negative thoughts arise."
                ]
            }
        ]

class StressManagementModule(TherapyModule):
    """Module for stress management."""
    
    def __init__(self):
        super().__init__("Stress Management", "Techniques to reduce and cope with stress")
        self.exercises = [
            {
                "name": "Box Breathing",
                "description": "A simple breathing technique to calm the nervous system.",
                "steps": [
                    "Find a comfortable seated position.",
                    "Breathe in through your nose for a count of 4.",
                    "Hold your breath for a count of 4.",
                    "Exhale through your mouth for a count of 4.",
                    "Hold your breath (lungs empty) for a count of 4.",
                    "Repeat this cycle 5-10 times.",
                    "Notice how your body and mind feel afterward."
                ]
            },
            {
                "name": "Body Scan",
                "description": "A mindfulness practice to release tension and increase body awareness.",
                "steps": [
                    "Lie down or sit in a comfortable position and close your eyes.",
                    "Begin by bringing awareness to your feet. Notice any sensations without judgment.",
                    "Slowly move your attention up through your body: legs, hips, abdomen, chest, etc.",
                    "For each area, notice sensations and consciously release any tension.",
                    "If you find areas of discomfort, breathe into them without trying to change anything.",
                    "When you reach the top of your head, take a moment to feel your whole body.",
                    "Take a deep breath, and when ready, gently open your eyes."
                ]
            },
            {
                "name": "Stress Diary",
                "description": "Track stress triggers and responses to identify patterns and develop strategies.",
                "steps": [
                    "Create a log with columns for: Situation, Stress Level (1-10), Physical Sensations, Thoughts, Behaviors, and Coping Strategy.",
                    "For each stressful event, record all these elements.",
                    "After a week, review your diary and look for patterns in triggers and responses.",
                    "Identify which coping strategies were most effective.",
                    "Based on your observations, create a personalized stress management plan."
                ]
            },
            {
                "name": "Priority Matrix",
                "description": "Organize tasks to reduce overwhelm and increase productivity.",
                "steps": [
                    "Draw a 2x2 grid with axes of 'Urgent' and 'Important'.",
                    "List all your current tasks and responsibilities.",
                    "Place each task in the appropriate quadrant: Urgent & Important, Important but Not Urgent, Urgent but Not Important, Neither Urgent nor Important.",
                    "Focus first on tasks that are both urgent and important.",
                    "Schedule time for important but not urgent tasks (these often prevent future stress).",
                    "Delegate or minimize time spent on urgent but not important tasks.",
                    "Eliminate or drastically reduce tasks that are neither urgent nor important."
                ]
            }
        ]

class SleepImprovementModule(TherapyModule):
    """Module for sleep improvement."""
    
    def __init__(self):
        super().__init__("Sleep Improvement", "Strategies for better sleep quality and quantity")
        self.exercises = [
            {
                "name": "Sleep Hygiene Assessment",
                "description": "Evaluate and improve your sleep environment and routines.",
                "steps": [
                    "Assess your bedroom: Is it dark, quiet, cool, and comfortable?",
                    "Review your bedtime routine: Do you wind down for 30-60 minutes before sleep?",
                    "Check your daytime habits: Exercise timing, caffeine, alcohol, and screen use.",
                    "Evaluate your sleep schedule: Are you consistent with sleep and wake times?",
                    "For each area, identify one improvement you can make tonight.",
                    "Implement these changes and track their impact on your sleep quality."
                ]
            },
            {
                "name": "Progressive Relaxation for Sleep",
                "description": "A body relaxation technique specifically for bedtime.",
                "steps": [
                    "Lie in bed in a comfortable position for sleep.",
                    "Take three deep breaths, exhaling slowly each time.",
                    "Beginning with your toes, tense and then completely relax each muscle group.",
                    "Work your way up through your body: feet, legs, hips, abdomen, chest, hands, arms, shoulders, neck, and face.",
                    "After completing the full body, imagine a wave of relaxation flowing from your head to your toes.",
                    "Now allow yourself to drift toward sleep, returning to the breath if your mind wanders."
                ]
            },
            {
                "name": "Worry Download",
                "description": "Clear your mind of concerns before bedtime to prevent racing thoughts.",
                "steps": [
                    "30-60 minutes before bedtime, take out a piece of paper.",
                    "Write down everything that's on your mind or worrying you.",
                    "For each item, briefly note one step you can take tomorrow (or when appropriate).",
                    "Symbolically 'put away' these concerns by folding the paper and setting it aside until morning.",
                    "During your bedtime routine, if worries return, remind yourself they're written down and can be addressed tomorrow."
                ]
            },
            {
                "name": "Sleep Restriction",
                "description": "Temporarily limit time in bed to build stronger sleep drive and consolidate sleep.",
                "steps": [
                    "Track your actual sleep time (not just time in bed) for one week.",
                    "Calculate your average sleep time (e.g., 6 hours).",
                    "Set a consistent wake-up time every day of the week.",
                    "Count backward from your wake time to set your bedtime (e.g., if wake at 7am and average 6 hours, bedtime is 1am).",
                    "Only go to bed when sleepy, and get out of bed if you can't sleep after 20 minutes.",
                    "Maintain this schedule for a week, then increase time in bed by 15-30 minutes if sleep efficiency is over 85%.",
                    "Continue until you reach your optimal sleep duration."
                ]
            }
        ]

def get_all_modules():
    """Return all available therapy modules."""
    return [
        AnxietyModule(),
        DepressionModule(),
        StressManagementModule(),
        SleepImprovementModule()
    ]

def run_exercise(exercise, module_name):
    """Run a therapeutic exercise with user interaction."""
    print(f"\n{Fore.CYAN}=== {module_name}: {exercise['name']} ==={Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{exercise['description']}{Style.RESET_ALL}\n")
    
    input("Press Enter when you're ready to begin...")
    
    for i, step in enumerate(exercise['steps'], 1):
        print(f"\n{Fore.GREEN}Step {i}: {step}{Style.RESET_ALL}")
        if i < len(exercise['steps']):
            input("\nPress Enter to continue to the next step...")
        else:
            input("\nPress Enter when you've completed this step...")
    
    print(f"\n{Fore.CYAN}Exercise complete! How do you feel?{Style.RESET_ALL}")
    return True

# Example usage if run directly
if __name__ == "__main__":
    print(f"{Fore.CYAN}Available Therapy Modules:{Style.RESET_ALL}\n")
    
    modules = get_all_modules()
    for i, module in enumerate(modules, 1):
        print(f"{i}. {Fore.GREEN}{module.name}{Style.RESET_ALL} - {module.description}")
    
    try:
        choice = int(input("\nSelect a module (1-4): ")) - 1
        if 0 <= choice < len(modules):
            selected_module = modules[choice]
            print(f"\n{Fore.CYAN}Selected: {selected_module.name}{Style.RESET_ALL}")
            
            exercise = selected_module.get_exercise()
            if exercise:
                completed = run_exercise(exercise, selected_module.name)
                if completed:
                    selected_module.complete_exercise(exercise['name'])
                    print(f"\n{Fore.YELLOW}Progress Updated:{Style.RESET_ALL}")
                    print(selected_module.get_progress_summary())
            else:
                print("No exercises available in this module.")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Please enter a valid number.") 