# Developer Documentation: Enhanced Therapy Bot

This document provides technical details for developers interested in contributing to or modifying the Enhanced Therapy Bot CLI application.

## Architecture Overview

The Enhanced Therapy Bot is built with a modular architecture to make it easy to extend and maintain:

```
Enhanced Therapy Bot
├── enhanced_therapy_bot.py  # Main application
├── start_therapy.py         # Launcher script
├── therapy_modules.py       # Therapeutic exercise modules
├── local_nlp.py             # Local natural language processing
├── journal_system.py        # Journal functionality
├── mood_visualization.py    # Mood tracking visualization
├── reminder_system.py       # Reminder system
├── resources.py             # Mental health resources
├── user_data.json           # User profile and mood history
└── user_preferences.json    # User preferences
```

## Core Components

### EnhancedTherapyBot (enhanced_therapy_bot.py)

The main class that orchestrates all components and manages the user experience. Handles:

- Initial greeting and check-in
- User mood tracking
- Main menu navigation
- Component initialization

### Therapy Modules (therapy_modules.py)

Defines therapeutic exercise modules including:

- Mindfulness exercises
- Breathing techniques
- Anxiety management
- Depression management
- Sleep improvement
- Physical activity

Each module contains multiple exercises with instructions, steps, and completion tracking.

### Local NLP (local_nlp.py)

Provides natural language processing capabilities without requiring external API calls:

- Basic sentiment analysis
- Pattern detection (anxiety, stress, etc.)
- Response generation
- Topic extraction
- Journal prompt suggestion

### Journal System (journal_system.py)

Manages the user's journal entries:

- Creating entries with tags
- Searching and retrieving entries
- Entry statistics
- Mood-based journal prompts
- Streak tracking

### Mood Visualization (mood_visualization.py)

Generates visualizations for mood data:

- ASCII chart generation
- Time-based mood analysis
- Mood data processing

### Reminder System (reminder_system.py)

Manages check-in reminders:

- Creating/updating reminders
- Recurring reminder logic
- Due reminder detection
- Smart scheduling suggestions

### Resource Library (resources.py)

Contains mental health resources:

- Crisis resources by country
- Self-help resources by category
- Reading recommendations
- Mental health facts

## Development Guidelines

### Adding a New Feature

1. Identify the appropriate module for your feature (or create a new one)
2. Implement the feature with appropriate test cases
3. Add any necessary UI elements to the main menu in `enhanced_therapy_bot.py`
4. Update documentation

### Adding a New Therapy Module

1. Add a new module class in `therapy_modules.py`
2. Define exercises with clear instructions
3. Register the module in the `get_all_modules()` function
4. Implement any specialized functionality needed for the exercises

### Style Guidelines

- Follow PEP 8 for Python code style
- Use docstrings for all classes and functions
- Keep UI text friendly and supportive
- Use colorama for consistent color schemes
- Favor user experience over technical complexity

### Data Storage

All user data is stored locally:

- JSON for persistent storage
- Each module should handle its own data validation
- Use `try/except` for handling file operations
- Avoid storing sensitive information in plain text

## Testing

Run the bot with different scenarios:

- First-time user experience
- Returning user with existing data
- Different mood inputs
- Various feature utilizations

## Extending the NLP Capabilities

To improve the local NLP capabilities:

1. Expand the response templates in `local_nlp.py`
2. Add more sophisticated pattern matching
3. Improve topic extraction accuracy
4. Enhance sentiment analysis accuracy

## Future Development Ideas

- Voice input/output support
- Export data to common formats
- Integration with meditation timers
- Integration with habit tracking
- Remote cloud backup of journal entries
- Multi-user support

## Troubleshooting

Common issues:

- Missing dependencies: Run `pip install -r requirements.txt`
- Data file corruption: Check JSON file integrity
- Display issues: Verify terminal supports ANSI colors
- Performance issues: Check for large data files

## Contact

For questions or suggestions, please open an issue in the GitHub repository.
