#!/usr/bin/env python3

import os
import sys
import openai
from colorama import init, Fore, Style
from rich.console import Console
from rich.table import Table

# Initialize colorama for colored output
init()

console = Console()

def display_welcome():
    console.print("[bold magenta]Welcome to the Enhanced Therapy Bot![/bold magenta]")

def display_mood_table(mood_history):
    table = Table(title="Mood History")

    table.add_column("Date", justify="right", style="cyan", no_wrap=True)
    table.add_column("Mood", style="magenta")

    for entry in mood_history:
        table.add_row(entry['timestamp'], entry['mood'])

    console.print(table)

def test_api_key():
    print(f"{Fore.CYAN}Testing OpenAI API Key{Style.RESET_ALL}")
    
    # Read API key from .env file
    try:
        with open('.env', 'r') as file:
            env_content = file.read()
            api_key = None
            for line in env_content.split('\n'):
                if line.startswith('OPENAI_API_KEY='):
                    api_key = line.split('=', 1)[1].strip()
                    print(f"API key found: {api_key[:5]}...{api_key[-5:]}")
    except Exception as e:
        print(f"{Fore.RED}Could not read .env file: {e}{Style.RESET_ALL}")
        return
    
    if not api_key:
        print(f"{Fore.RED}No API key found in .env file{Style.RESET_ALL}")
        return
    
    # Set API key
    openai.api_key = api_key
    
    # Determine if this is a project key
    is_project_key = api_key.startswith('sk-proj-')
    if is_project_key:
        print(f"{Fore.YELLOW}This appears to be a project-specific API key.{Style.RESET_ALL}")
    
    # Try different models
    models_to_try = ["gpt-3.5-turbo", "text-davinci-003", "davinci", "ada"]
    
    for model in models_to_try:
        print(f"\n{Fore.CYAN}Testing model: {model}{Style.RESET_ALL}")
        try:
            if model.startswith("gpt"):
                # For chat models
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=[{"role": "user", "content": "Say hello!"}],
                    max_tokens=10
                )
                print(f"{Fore.GREEN}Success! Response: {response.choices[0].message['content']}{Style.RESET_ALL}")
            else:
                # For completion models
                response = openai.Completion.create(
                    model=model,
                    prompt="Say hello!",
                    max_tokens=10
                )
                print(f"{Fore.GREEN}Success! Response: {response.choices[0].text}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error with {model}: {str(e)}{Style.RESET_ALL}")
    
    # Check if we can list available models
    print(f"\n{Fore.CYAN}Attempting to list available models...{Style.RESET_ALL}")
    try:
        models = openai.Model.list()
        print(f"{Fore.GREEN}Available models:{Style.RESET_ALL}")
        for model in models.data[:5]:  # Show only first 5 models
            print(f"- {model.id}")
        if len(models.data) > 5:
            print(f"... and {len(models.data) - 5} more")
    except Exception as e:
        print(f"{Fore.RED}Could not list models: {str(e)}{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}API key testing complete{Style.RESET_ALL}")

if __name__ == "__main__":
    test_api_key() 