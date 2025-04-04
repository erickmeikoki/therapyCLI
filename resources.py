#!/usr/bin/env python3

from colorama import Fore, Style, init
import json
import os
import random

# Initialize colorama
init()

class ResourceLibrary:
    def __init__(self):
        self.crisis_resources = self.load_crisis_resources()
        self.self_help_resources = self.load_self_help_resources()
        self.reading_recommendations = self.load_reading_recommendations()
        self.mental_health_facts = self.load_mental_health_facts()
    
    def load_crisis_resources(self):
        """Load crisis hotline information by country."""
        return {
            "global": {
                "name": "International Association for Suicide Prevention",
                "website": "https://www.iasp.info/resources/Crisis_Centres/",
                "description": "Directory of crisis centers around the world."
            },
            "us": {
                "hotlines": [
                    {
                        "name": "National Suicide Prevention Lifeline",
                        "number": "988 or 1-800-273-8255",
                        "website": "https://988lifeline.org/",
                        "description": "24/7, free and confidential support for people in distress."
                    },
                    {
                        "name": "Crisis Text Line",
                        "number": "Text HOME to 741741",
                        "website": "https://www.crisistextline.org/",
                        "description": "Text-based crisis support available 24/7."
                    },
                    {
                        "name": "SAMHSA's National Helpline",
                        "number": "1-800-662-4357",
                        "website": "https://www.samhsa.gov/find-help/national-helpline",
                        "description": "Treatment referral and information service for individuals facing mental health or substance use disorders."
                    }
                ]
            },
            "canada": {
                "hotlines": [
                    {
                        "name": "Canada Suicide Prevention Service",
                        "number": "1-833-456-4566",
                        "website": "https://www.crisisservicescanada.ca/",
                        "description": "Available 24/7 for anyone thinking about or affected by suicide."
                    },
                    {
                        "name": "Kids Help Phone",
                        "number": "1-800-668-6868 or text CONNECT to 686868",
                        "website": "https://kidshelpphone.ca/",
                        "description": "24/7 support service for youth."
                    }
                ]
            },
            "uk": {
                "hotlines": [
                    {
                        "name": "Samaritans",
                        "number": "116 123",
                        "website": "https://www.samaritans.org/",
                        "description": "24/7 support line for anyone in emotional distress."
                    },
                    {
                        "name": "CALM (Campaign Against Living Miserably)",
                        "number": "0800 58 58 58",
                        "website": "https://www.thecalmzone.net/",
                        "description": "Support for men in the UK, targeted at reducing male suicide."
                    }
                ]
            },
            "australia": {
                "hotlines": [
                    {
                        "name": "Lifeline Australia",
                        "number": "13 11 14",
                        "website": "https://www.lifeline.org.au/",
                        "description": "24/7 crisis support and suicide prevention services."
                    },
                    {
                        "name": "Beyond Blue",
                        "number": "1300 22 4636",
                        "website": "https://www.beyondblue.org.au/",
                        "description": "Support for anxiety, depression, and suicide prevention."
                    }
                ]
            }
        }
    
    def load_self_help_resources(self):
        """Load online self-help resources."""
        return [
            {
                "name": "Mindfulness-Based Stress Reduction (MBSR)",
                "website": "https://palousemindfulness.com/",
                "description": "Free online MBSR course with guided meditations and resources.",
                "tags": ["stress", "anxiety", "mindfulness", "meditation", "free"]
            },
            {
                "name": "MoodGYM",
                "website": "https://moodgym.com.au/",
                "description": "Interactive self-help program that teaches cognitive behavioral therapy skills for preventing and coping with depression.",
                "tags": ["depression", "CBT", "mood", "interactive"]
            },
            {
                "name": "7 Cups",
                "website": "https://www.7cups.com/",
                "description": "Online therapy and free support with trained listeners.",
                "tags": ["therapy", "support", "listening", "community", "free option"]
            },
            {
                "name": "Insight Timer",
                "website": "https://insighttimer.com/",
                "description": "Free meditation app with thousands of guided meditations.",
                "tags": ["meditation", "sleep", "anxiety", "stress", "free"]
            },
            {
                "name": "Mental Health America Screening Tools",
                "website": "https://screening.mhanational.org/screening-tools/",
                "description": "Free, anonymous, and confidential mental health screenings.",
                "tags": ["assessment", "screening", "depression", "anxiety", "free"]
            },
            {
                "name": "CBT-i Coach",
                "website": "https://mobile.va.gov/app/cbt-i-coach",
                "description": "App for insomnia management using cognitive behavioral therapy techniques.",
                "tags": ["sleep", "insomnia", "CBT", "app", "free"]
            },
            {
                "name": "ACT Coach",
                "website": "https://www.ptsd.va.gov/appvid/mobile/actcoach_app.asp",
                "description": "Learn Acceptance and Commitment Therapy (ACT) strategies for psychological flexibility.",
                "tags": ["ACT", "mindfulness", "values", "app", "free"]
            },
            {
                "name": "Breathe2Relax",
                "website": "https://telehealth.org/apps/behavioral/breathe2relax-mobile-app",
                "description": "Stress management tool that provides detailed information on the effects of stress on the body.",
                "tags": ["breathing", "stress", "anxiety", "app", "free"]
            }
        ]
    
    def load_reading_recommendations(self):
        """Load reading recommendations by category."""
        return {
            "anxiety": [
                {
                    "title": "Dare: The New Way to End Anxiety and Stop Panic Attacks",
                    "author": "Barry McDonagh",
                    "description": "A step-by-step approach to overcoming anxiety and panic attacks."
                },
                {
                    "title": "The Anxiety and Phobia Workbook",
                    "author": "Edmund J. Bourne",
                    "description": "Practical exercises and techniques to help overcome anxiety and phobias."
                },
                {
                    "title": "The Wisdom of Anxiety",
                    "author": "Sheryl Paul",
                    "description": "Explores anxiety as a messenger that can guide us toward emotional healing."
                }
            ],
            "depression": [
                {
                    "title": "Feeling Good: The New Mood Therapy",
                    "author": "David D. Burns",
                    "description": "Classic book on cognitive behavioral therapy for depression."
                },
                {
                    "title": "The Upward Spiral",
                    "author": "Alex Korb",
                    "description": "Uses neuroscience to explain how small changes can lead to better moods."
                },
                {
                    "title": "Lost Connections",
                    "author": "Johann Hari",
                    "description": "Explores social and environmental causes of depression and anxiety."
                }
            ],
            "mindfulness": [
                {
                    "title": "Wherever You Go, There You Are",
                    "author": "Jon Kabat-Zinn",
                    "description": "Practical guide to mindfulness meditation for beginners and experienced practitioners."
                },
                {
                    "title": "The Miracle of Mindfulness",
                    "author": "Thich Nhat Hanh",
                    "description": "Simple introduction to the practice of mindfulness in everyday life."
                },
                {
                    "title": "Full Catastrophe Living",
                    "author": "Jon Kabat-Zinn",
                    "description": "Comprehensive guide to mindfulness-based stress reduction (MBSR)."
                }
            ],
            "sleep": [
                {
                    "title": "Why We Sleep",
                    "author": "Matthew Walker",
                    "description": "Explores the science of sleep and offers practical advice for improving sleep quality."
                },
                {
                    "title": "Say Good Night to Insomnia",
                    "author": "Gregg D. Jacobs",
                    "description": "Six-week drug-free program to overcome insomnia."
                },
                {
                    "title": "The Sleep Solution",
                    "author": "W. Chris Winter",
                    "description": "Practical guide to solving sleep problems from a neurologist and sleep specialist."
                }
            ],
            "self_compassion": [
                {
                    "title": "Self-Compassion: The Proven Power of Being Kind to Yourself",
                    "author": "Kristin Neff",
                    "description": "Research-based approach to treating yourself with the same kindness you would offer others."
                },
                {
                    "title": "The Mindful Self-Compassion Workbook",
                    "author": "Kristin Neff and Christopher Germer",
                    "description": "Practical exercises for developing self-compassion."
                },
                {
                    "title": "The Compassionate Mind",
                    "author": "Paul Gilbert",
                    "description": "Using compassion-focused therapy to treat anxiety, depression, and shame."
                }
            ]
        }
    
    def load_mental_health_facts(self):
        """Load interesting and destigmatizing mental health facts."""
        return [
            "Mental health conditions are common. About 1 in 5 adults in the U.S. experiences mental illness each year.",
            "Treatment for mental health conditions is effective, with 70-90% of individuals reporting reduced symptoms and improved quality of life with proper care.",
            "Exercise has been shown to reduce symptoms of depression and anxiety, with some studies finding it as effective as medication for mild to moderate depression.",
            "Sleep and mental health are closely connected. Chronic sleep problems affect 50-80% of patients in a typical psychiatric practice.",
            "Practicing mindfulness for just 8 weeks can actually change the brain, increasing density in areas associated with learning, memory, emotion regulation, and empathy.",
            "Expressing gratitude has been shown to increase happiness, reduce depression, and help people sleep better.",
            "Social connection is one of the strongest protective factors against mental health challenges. Having supportive relationships reduces the risk of depression, anxiety, and other conditions.",
            "Mental health conditions are medical conditions, not character flaws or personal weaknesses.",
            "Recovery from mental health challenges is possible. People with mental health conditions can and do live fulfilling, productive lives.",
            "The relationship between a therapist and client (therapeutic alliance) is one of the strongest predictors of successful therapy outcomes, regardless of the type of therapy used.",
            "Many famous and successful people throughout history have lived with mental health conditions, including Abraham Lincoln, Vincent van Gogh, Demi Lovato, and Michael Phelps.",
            "Your brain releases endorphins when you laugh, which naturally reduces stress and increases feelings of wellbeing.",
            "Helping others has been shown to improve mental health by reducing stress and increasing feelings of purpose and satisfaction.",
            "The human brain can generate new neurons throughout life, a process called neurogenesis. This means positive change is always possible, regardless of age.",
            "Nature exposure for just 20 minutes has been shown to significantly lower stress hormone levels.",
            "Mental health conditions are treatable, and many people who receive appropriate care recover completely or learn to manage their symptoms effectively.",
            "Creative activities like art, music, writing, and dance can reduce stress and anxiety while increasing positive emotions.",
            "Deep breathing activates the parasympathetic nervous system, which counteracts the stress response and promotes relaxation.",
            "Pets can improve mental health by reducing stress, providing companionship, and encouraging physical activity and social interaction."
        ]
    
    def get_crisis_resources(self, country=None):
        """Get crisis resources, optionally filtered by country."""
        if country and country.lower() in self.crisis_resources:
            resources = {country.lower(): self.crisis_resources[country.lower()]}
            resources["global"] = self.crisis_resources["global"]
            return resources
        return self.crisis_resources
    
    def get_self_help_resources(self, tag=None, limit=5):
        """Get self-help resources, optionally filtered by tag."""
        if tag:
            filtered = [r for r in self.self_help_resources if tag.lower() in [t.lower() for t in r.get("tags", [])]]
            return filtered[:limit]
        
        # Return random selection if no tag specified
        shuffled = self.self_help_resources.copy()
        random.shuffle(shuffled)
        return shuffled[:limit]
    
    def get_reading_recommendations(self, category=None, limit=3):
        """Get reading recommendations, optionally filtered by category."""
        if category and category.lower() in self.reading_recommendations:
            return self.reading_recommendations[category.lower()][:limit]
        
        # Return random selection if no category specified
        all_books = []
        for category_books in self.reading_recommendations.values():
            all_books.extend(category_books)
        
        random.shuffle(all_books)
        return all_books[:limit]
    
    def get_random_mental_health_fact(self):
        """Get a random mental health fact."""
        return random.choice(self.mental_health_facts)
    
    def format_crisis_resources(self, resources):
        """Format crisis resources for display."""
        output = []
        
        for country, data in resources.items():
            if country == "global":
                output.append(f"\n{Fore.CYAN}Global Resources:{Style.RESET_ALL}")
                output.append(f"• {data['name']}: {data['website']}")
                output.append(f"  {data['description']}")
            else:
                output.append(f"\n{Fore.CYAN}{country.upper()} Resources:{Style.RESET_ALL}")
                for hotline in data.get('hotlines', []):
                    output.append(f"• {Fore.GREEN}{hotline['name']}{Style.RESET_ALL}: {hotline['number']}")
                    output.append(f"  {hotline['website']}")
                    output.append(f"  {hotline['description']}")
        
        return "\n".join(output)
    
    def format_self_help_resources(self, resources):
        """Format self-help resources for display."""
        if not resources:
            return "No resources found."
        
        output = [f"\n{Fore.CYAN}Self-Help Resources:{Style.RESET_ALL}"]
        
        for resource in resources:
            output.append(f"\n• {Fore.GREEN}{resource['name']}{Style.RESET_ALL}")
            output.append(f"  {resource['website']}")
            output.append(f"  {resource['description']}")
            tags = ", ".join([f"#{tag}" for tag in resource.get('tags', [])])
            if tags:
                output.append(f"  {Fore.YELLOW}{tags}{Style.RESET_ALL}")
        
        return "\n".join(output)
    
    def format_reading_recommendations(self, books):
        """Format reading recommendations for display."""
        if not books:
            return "No recommendations found."
        
        output = [f"\n{Fore.CYAN}Reading Recommendations:{Style.RESET_ALL}"]
        
        for book in books:
            output.append(f"\n• {Fore.GREEN}{book['title']}{Style.RESET_ALL} by {book['author']}")
            output.append(f"  {book['description']}")
        
        return "\n".join(output)

# Example usage if run directly
if __name__ == "__main__":
    library = ResourceLibrary()
    
    print(f"{Fore.CYAN}Mental Health Resources{Style.RESET_ALL}")
    print("1. Crisis Resources")
    print("2. Self-Help Resources")
    print("3. Reading Recommendations")
    print("4. Mental Health Fact")
    print("5. Exit")
    
    choice = input("\nEnter your choice (1-5): ")
    
    if choice == "1":
        country = input("Enter country code (us, canada, uk, australia) or leave blank for all: ")
        resources = library.get_crisis_resources(country if country else None)
        print(library.format_crisis_resources(resources))
    
    elif choice == "2":
        tag = input("Enter a tag (e.g., anxiety, depression, sleep) or leave blank: ")
        resources = library.get_self_help_resources(tag if tag else None)
        print(library.format_self_help_resources(resources))
    
    elif choice == "3":
        categories = ", ".join(library.reading_recommendations.keys())
        category = input(f"Enter a category ({categories}) or leave blank: ")
        books = library.get_reading_recommendations(category if category else None)
        print(library.format_reading_recommendations(books))
    
    elif choice == "4":
        fact = library.get_random_mental_health_fact()
        print(f"\n{Fore.CYAN}Did you know?{Style.RESET_ALL}\n{fact}")
    
    elif choice == "5":
        print("Exiting resource library.") 