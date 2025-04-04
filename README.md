# Enhanced Therapy Bot CLI

A feature-rich command-line therapy bot that supports your mental wellbeing through personalized check-ins, mood tracking, journaling, and guided therapeutic exercises.

## Features

- 🧠 **Therapy Modules**: Access a variety of therapeutic exercises including breathing techniques, mindfulness, anxiety management, and more
- 📔 **Journaling System**: Record your thoughts with prompted journal entries and search/review past entries
- 📈 **Mood Tracking**: Visualize your mood patterns over time with ASCII charts
- ⏰ **Reminders**: Set personalized check-in reminders for consistent mental health practice
- 📚 **Resource Library**: Access crisis resources, self-help tools, and reading recommendations
- 💬 **Smart Chat**: Have open-ended conversations with local NLP-powered responses
- 🎨 **Colorful Interface**: Enjoy a welcoming, colorful command-line experience

## Installation

1. Make sure you have Python 3.7+ installed on your system
2. Clone this repository
3. Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

Start the enhanced therapy bot by executing:

```bash
python start_therapy.py
```

Or run the bot directly:

```bash
python enhanced_therapy_bot.py
```

The bot will:

1. Greet you and ask for your name (first time only)
2. Check in on your current mood
3. Display any due reminders
4. Offer support and activities based on your responses
5. Present a main menu with all available features
6. Save your progress and preferences for future sessions

## Privacy & Data

All your data is stored locally:

- Mood history and user info in `user_data.json`
- Preferences in `user_preferences.json`
- Journal entries in a local journal file
- Reminders in a local reminders file

No data is sent to external servers.

## Command-line Arguments

You can use the following command-line arguments with the bot:

```bash
# Skip the initial greeting and check-in
python start_therapy.py --skip-greeting

# Jump directly to a specific therapy module
python start_therapy.py --module anxiety

# Go directly to journal mode
python start_therapy.py --journal

# Go directly to reminders management
python start_therapy.py --reminders

# Start in chat mode
python start_therapy.py --chat

# Display version information
python start_therapy.py --version
```

## Contributing

Contributions are welcome! Feel free to submit issues and enhancement requests.

## License

MIT
