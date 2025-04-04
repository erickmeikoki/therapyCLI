#!/usr/bin/env python3

import json
from datetime import datetime, timedelta
import math
from colorama import Fore, Style
import os

# Mapping moods to numeric values
MOOD_VALUES = {
    "😊 Great": 5,
    "😌 Good": 4,
    "😐 Okay": 3,
    "😔 Not so good": 2,
    "😢 Terrible": 1
}

# Mapping numeric values back to emojis for display
VALUE_TO_EMOJI = {
    5: "😊",
    4: "😌",
    3: "😐", 
    2: "😔",
    1: "😢"
}

def load_mood_data():
    """Load mood data from user_data.json."""
    try:
        with open('user_data.json', 'r') as f:
            data = json.load(f)
            return data.get('mood_history', [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def get_date_from_iso(iso_date):
    """Convert ISO date string to datetime object."""
    try:
        return datetime.fromisoformat(iso_date)
    except ValueError:
        # Handle date format issues gracefully
        return datetime.now()

def generate_daily_mood_average(mood_history, days=7):
    """Generate daily mood averages for the last X days."""
    if not mood_history:
        return {}
    
    # Get the date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days-1)
    
    # Initialize mood data for each day
    daily_moods = {}
    current_date = start_date
    while current_date <= end_date:
        daily_moods[current_date.strftime("%Y-%m-%d")] = []
        current_date += timedelta(days=1)
    
    # Gather mood data by day
    for entry in mood_history:
        entry_date = get_date_from_iso(entry.get('timestamp', ''))
        date_key = entry_date.strftime("%Y-%m-%d")
        
        if date_key in daily_moods:
            mood = entry.get('mood', '')
            mood_value = MOOD_VALUES.get(mood, 3)  # Default to "Okay" if unknown
            daily_moods[date_key].append(mood_value)
    
    # Calculate daily averages
    daily_averages = {}
    for date, moods in daily_moods.items():
        if moods:
            daily_averages[date] = sum(moods) / len(moods)
        else:
            daily_averages[date] = None  # No mood data for this day
    
    return daily_averages

def generate_weekly_summary(mood_history):
    """Generate a text summary of weekly mood trends."""
    if not mood_history or len(mood_history) < 3:
        return "Not enough mood data collected yet for meaningful analysis."
    
    daily_averages = generate_daily_mood_average(mood_history)
    
    # Filter out days with no data
    valid_days = {k: v for k, v in daily_averages.items() if v is not None}
    
    if not valid_days:
        return "No mood data available for the past week."
    
    # Calculate overall average
    overall_avg = sum(valid_days.values()) / len(valid_days)
    
    # Get best and worst days
    if len(valid_days) >= 2:
        best_day = max(valid_days.items(), key=lambda x: x[1])
        worst_day = min(valid_days.items(), key=lambda x: x[1])
        
        best_day_name = datetime.strptime(best_day[0], "%Y-%m-%d").strftime("%A")
        worst_day_name = datetime.strptime(worst_day[0], "%Y-%m-%d").strftime("%A")
        
        # Check if there's a trend
        sorted_days = sorted(valid_days.items(), key=lambda x: datetime.strptime(x[0], "%Y-%m-%d"))
        if len(sorted_days) >= 3:
            first_half = [v for _, v in sorted_days[:len(sorted_days)//2]]
            second_half = [v for _, v in sorted_days[len(sorted_days)//2:]]
            
            first_half_avg = sum(first_half) / len(first_half)
            second_half_avg = sum(second_half) / len(second_half)
            
            trend = None
            if second_half_avg - first_half_avg > 0.5:
                trend = "improving"
            elif first_half_avg - second_half_avg > 0.5:
                trend = "declining"
            else:
                trend = "stable"
            
            summary = []
            summary.append(f"Your mood has been {trend} over the past week.")
            summary.append(f"Your best day was {best_day_name} with an average mood of {VALUE_TO_EMOJI[round(best_day[1])]}.")
            summary.append(f"Your most challenging day was {worst_day_name} with an average mood of {VALUE_TO_EMOJI[round(worst_day[1])]}.")
            
            # Add frequency analysis
            mood_counts = {}
            for entry in mood_history:
                mood = entry.get('mood', '')
                mood_counts[mood] = mood_counts.get(mood, 0) + 1
            
            most_common_mood = max(mood_counts.items(), key=lambda x: x[1])
            summary.append(f"Your most frequent mood was {most_common_mood[0]} ({most_common_mood[1]} times).")
            
            return "\n".join(summary)
    
    return "Still collecting mood data for more detailed analysis."

def generate_ascii_chart(mood_history, days=7):
    """Generate an ASCII chart of mood over time."""
    daily_averages = generate_daily_mood_average(mood_history, days)
    
    if not daily_averages:
        return "No mood data available."
    
    # Create the chart
    chart = []
    
    # Header
    chart.append(f"\n{Fore.CYAN}Your Mood Trends (Past {days} Days){Style.RESET_ALL}")
    chart.append("─" * 50)
    
    # Y-axis labels
    y_labels = [
        f"{Fore.GREEN}Great  😊{Style.RESET_ALL}",
        f"{Fore.CYAN}Good   😌{Style.RESET_ALL}",
        f"{Fore.WHITE}Okay   😐{Style.RESET_ALL}",
        f"{Fore.YELLOW}Low    😔{Style.RESET_ALL}",
        f"{Fore.RED}Bad    😢{Style.RESET_ALL}"
    ]
    
    # Sort dates
    dates = sorted(daily_averages.keys())
    
    # Generate chart rows
    for i in range(5):
        mood_value = 5 - i
        row = [y_labels[i] + " │"]
        
        for date in dates:
            avg = daily_averages.get(date)
            if avg is None:
                row.append(" ")  # No data
            elif avg >= mood_value - 0.5 and avg < mood_value + 0.5:
                if mood_value == 5:
                    row.append(f"{Fore.GREEN}●{Style.RESET_ALL}")
                elif mood_value == 4:
                    row.append(f"{Fore.CYAN}●{Style.RESET_ALL}")
                elif mood_value == 3:
                    row.append(f"{Fore.WHITE}●{Style.RESET_ALL}")
                elif mood_value == 2:
                    row.append(f"{Fore.YELLOW}●{Style.RESET_ALL}")
                else:
                    row.append(f"{Fore.RED}●{Style.RESET_ALL}")
            else:
                row.append(" ")
        
        chart.append(" ".join(row))
    
    # X-axis
    chart.append("      ├" + "─┬" * (len(dates) - 1) + "─┤")
    
    # Date labels
    x_labels = []
    for date in dates:
        day_name = datetime.strptime(date, "%Y-%m-%d").strftime("%a")
        x_labels.append(day_name[:2])
    
    chart.append("      " + " ".join(x_labels))
    
    # Add summary
    summary = generate_weekly_summary(mood_history)
    chart.append("\n" + summary)
    
    return "\n".join(chart)

if __name__ == "__main__":
    # This allows testing the visualization independently
    mood_history = load_mood_data()
    print(generate_ascii_chart(mood_history)) 