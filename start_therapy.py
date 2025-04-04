#!/usr/bin/env python3
"""
Enhanced Therapy Bot Launcher

This script launches the Enhanced Therapy Bot with appropriate environment setup.

Usage:
    python start_therapy.py [options]

Options:
    --skip-greeting     Skip the initial greeting and check-in
    --module NAME       Jump directly to a specific therapy module
    --journal           Go directly to journal mode
    --reminders         Go directly to reminders
    --chat              Start in chat mode
    --version           Display version information

Examples:
    python start_therapy.py --chat
    python start_therapy.py --module anxiety
    python start_therapy.py --journal
"""

import os
import sys
import time
import platform

def check_dependencies():
    """Check if all required dependencies are installed."""
    try:
        import questionary
        import colorama
        import numpy
        import matplotlib
        return True
    except ImportError as e:
        print(f"Missing dependency: {str(e)}")
        print("Please install required dependencies with: pip3 install -r requirements.txt")
        return False

def clear_screen():
    """Clear the terminal screen."""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def display_welcome():
    """Display a welcome message with ASCII art."""
    clear_screen()
    print("\033[36m")  # Cyan color
    print("=" * 60)
    print("""
   _____ _                               ____        _   
  |_   _| |__   ___ _ __ __ _ _ __  _   | __ )  ___ | |_ 
    | | | '_ \ / _ \ '__/ _` | '_ \| | | |  _ \ / _ \| __|
    | | | | | |  __/ | | (_| | |_) | |_| | |_) | (_) | |_ 
    |_| |_| |_|\___|_|  \__,_| .__/ \__, |____/ \___/ \__|
                             |_|    |___/                
    """)
    print("=" * 60)
    print("\033[0m")  # Reset color
    
    print("Welcome to your personal therapy bot!")
    print("This bot provides a safe space for reflection and mental wellness.")
    print("\nLoading resources...")
    
    # Simulate loading for a better user experience
    for _ in range(5):
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(0.3)
    print("\n")

def main():
    """Main entry point for the therapy bot application."""
    if not check_dependencies():
        return
        
    display_welcome()
    
    print("Starting therapy session...\n")
    time.sleep(1)
    
    try:
        from enhanced_therapy_bot import EnhancedTherapyBot
        bot = EnhancedTherapyBot()
        bot.run()
    except Exception as e:
        print(f"Error starting therapy bot: {str(e)}")
        print("If this is your first time running the bot, make sure all modules are in place.")

if __name__ == "__main__":
    main() 