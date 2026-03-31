import psutil
import os
import time
from datetime import datetime
import json
from urllib.request import urlopen
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
import threading
import subprocess
import platform
import math
import random
import webbrowser
from zoneinfo import ZoneInfo


class IntermatiumApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Intermatium BETA - AI Assistant")
        self.root.geometry("800x700")

        # Theme dictionary
        self.themes = {
            "dark": {
                "bg_color": "#000000",
                "fg_color": "#ffffff",
                "header_bg": "#1a1a1a",
                "entry_bg": "#2a2a2a",
                "entry_fg": "#ffffff",
                "chat_bg": "#1a1a1a",
                "chat_fg": "#ffffff",
                "accent_purple": "#7c3aed",
                "accent_orange": "#ff8c42",
                "name": "Dark"
            },
            "white": {
                "bg_color": "#ffffff",
                "fg_color": "#000000",
                "header_bg": "#f0f0f0",
                "entry_bg": "#ffffff",
                "entry_fg": "#000000",
                "chat_bg": "#ffffff",
                "chat_fg": "#000000",
                "accent_purple": "#7c3aed",
                "accent_orange": "#ff8c42",
                "name": "White"
            },
            "blue": {
                "bg_color": "#0d1b2a",
                "fg_color": "#e0f2fe",
                "header_bg": "#1e3a5f",
                "entry_bg": "#1e3a5f",
                "entry_fg": "#e0f2fe",
                "chat_bg": "#1e3a5f",
                "chat_fg": "#e0f2fe",
                "accent_purple": "#60a5fa",
                "accent_orange": "#f97316",
                "name": "Blue"
            },
            "grey": {
                "bg_color": "#2a2a2a",
                "fg_color": "#e8e8e8",
                "header_bg": "#1f1f1f",
                "entry_bg": "#3a3a3a",
                "entry_fg": "#e8e8e8",
                "chat_bg": "#1f1f1f",
                "chat_fg": "#e8e8e8",
                "accent_purple": "#a78bfa",
                "accent_orange": "#fbbf24",
                "name": "Grey"
            }
        }

        self.current_theme = "dark"
        self.apply_theme(self.current_theme)

        # Fonts
        self.title_font = ("Arial", 16, "bold")
        self.button_font = ("Arial", 9)
        self.chat_font = ("Courier", 10)
        self.label_font = ("Arial", 9)
        self.input_font = ("Arial", 11)

        self.name = "Intermatium BETA"
        self.user_name = "User"
        self.conversation_history = []
        self.is_typing = False

        # City to timezone mapping
        self.city_timezones = {
            "melbourne": "Australia/Melbourne",
            "sydney": "Australia/Sydney",
            "london": "Europe/London",
            "new york": "America/New_York",
            "los angeles": "America/Los_Angeles",
            "tokyo": "Asia/Tokyo",
            "dubai": "Asia/Dubai",
            "singapore": "Asia/Singapore",
            "hong kong": "Asia/Hong_Kong",
            "bangkok": "Asia/Bangkok",
            "mumbai": "Asia/Kolkata",
            "delhi": "Asia/Kolkata",
            "paris": "Europe/Paris",
            "berlin": "Europe/Berlin",
            "toronto": "America/Toronto",
            "vancouver": "America/Vancouver",
            "mexico city": "America/Mexico_City",
            "sao paulo": "America/Sao_Paulo",
            "buenos aires": "America/Argentina/Buenos_Aires",
            "moscow": "Europe/Moscow",
            "istanbul": "Europe/Istanbul",
            "cairo": "Africa/Cairo",
            "johannesburg": "Africa/Johannesburg",
            "auckland": "Pacific/Auckland",
        }

        # Weather descriptions
        self.weather_descriptions = {
            0: "Clear sky ☀️",
            1: "Mainly clear 🌤️",
            2: "Partly cloudy ⛅",
            3: "Overcast ☁️",
            45: "Foggy 🌫️",
            48: "Foggy (depositing) 🌫️",
            51: "Light drizzle 🌧️",
            53: "Moderate drizzle 🌧️",
            55: "Dense drizzle 🌧️",
            61: "Slight rain 🌧️",
            63: "Moderate rain 🌧️",
            65: "Heavy rain ⛈️",
            71: "Slight snow ❄️",
            73: "Moderate snow ❄️",
            75: "Heavy snow ❄️",
            80: "Slight rain showers 🌧️",
            81: "Moderate rain showers 🌧️",
            82: "Violent rain showers ⛈️",
            95: "Thunderstorm ⛈️",
        }

        # Knowledge base
        self.knowledge_base = {
            "what is the speed of light": "The speed of light in a vacuum is approximately 299,792,458 metres per second.",
            "what is dna": "DNA is a molecule that carries genetic instructions for all living organisms.",
            "what is gravity": "Gravity is a force that attracts objects with mass toward each other.",
            "what is photosynthesis": "Photosynthesis is how plants convert sunlight into chemical energy.",
            "what is the big bang": "The Big Bang is the theory explaining the origin of the universe about 13.8 billion years ago.",
            "what is quantum physics": "Quantum physics studies the behavior of matter and energy at atomic scales.",
            "what is a black hole": "A black hole is a region where gravity is so strong nothing can escape.",
            "what is evolution": "Evolution is the process of change in all forms of life over generations.",
            "what is artificial intelligence": "AI is the simulation of human intelligence by computer systems.",
            "what is machine learning": "Machine learning enables systems to learn and improve from experience.",
            "what is the internet": "The internet is a global network of interconnected computers.",
            "what is python": "Python is a high-level programming language known for simplicity.",
            "who was albert einstein": "Albert Einstein was a physicist who developed the theory of relativity.",
            "who was isaac newton": "Isaac Newton formulated the laws of motion and universal gravitation.",
            "what is the largest country": "Russia is the largest country by land area.",
            "what is the longest river": "The Nile River is the longest river in the world.",
            "what is the highest mountain": "Mount Everest is the highest mountain in the world.",
        }

        # Inner chatbot knowledge base (ARIA)
        self.chatbot_knowledge = {
            "hey": "Hey there! I'm Aria, Intermatium's inner chatbot. How can I help?",
            "hello": "Hello! I'm Aria. Ask me anything specific!",
            "hi": "Hi! I'm Aria, here to answer your specific questions!",
            "who are you": "I'm Aria, the inner chatbot of Intermatium BETA! I specialise in answering specific questions.",
            "what is your name": "My name is Aria! I'm built inside Intermatium BETA.",
            "how old are you": "I don't have an age — I'm an AI chatbot!",
            "are you human": "Nope! I'm Aria, an AI chatbot inside Intermatium BETA.",
            "are you real": "I'm as real as code can be! I'm Aria, your AI assistant.",
            "do you have feelings": "I don't have feelings, but I'm always here to help!",
            "can you think": "I process information and respond, but I don't think like humans do.",
            "are you smart": "I try my best! I'm always learning from my knowledge base.",
            "tell me a joke": "Why don't scientists trust atoms? Because they make up everything! 😄",
            "tell me something interesting": "Honey never spoils! Archaeologists have found 3000-year-old honey in Egyptian tombs.",
            "what is the meaning of life": "42! (According to The Hitchhiker's Guide to the Galaxy 😄)",
            "do you like music": "I love all music! What's your favourite genre?",
            "what is your favourite colour": "I'd say electric blue — it matches my circuits! 💙",
            "what is your favourite food": "I don't eat, but if I could, I'd probably love pizza! 🍕",
            "what is a cpu": "A CPU (Central Processing Unit) is the brain of a computer that executes instructions.",
            "what is a gpu": "A GPU (Graphics Processing Unit) handles rendering graphics and parallel computing tasks.",
            "what is ram": "RAM (Random Access Memory) is temporary storage your computer uses to run programs.",
            "what is an operating system": "An OS manages computer hardware and software resources. Examples: Windows, macOS, Linux.",
            "what is a programming language": "A programming language is a formal language used to write instructions for computers.",
            "what is a database": "A database is an organised collection of structured data stored electronically.",
            "what is cybersecurity": "Cybersecurity is the practice of protecting systems and networks from digital attacks.",
            "what is a virus": "A computer virus is malicious software that replicates itself and can damage systems.",
            "what is vr": "VR (Virtual Reality) is an immersive technology that simulates a 3D environment.",
            "what is ar": "AR (Augmented Reality) overlays digital content onto the real world.",
            "what is the sun": "The Sun is a star at the centre of our solar system, providing light and heat.",
            "what is the moon": "The Moon is Earth's only natural satellite, affecting tides and stabilising Earth's axis.",
            "what is a planet": "A planet is a celestial body orbiting a star, large enough to clear its orbit.",
            "what is an asteroid": "An asteroid is a rocky body orbiting the Sun, mostly found in the asteroid belt.",
            "what is a comet": "A comet is an icy body that releases gas and dust as it approaches the Sun.",
            "what is climate change": "Climate change refers to long-term shifts in global temperatures and weather patterns.",
            "what is the water cycle": "The water cycle is the continuous movement of water through evaporation, condensation, and precipitation.",
            "what is electricity": "Electricity is the flow of electric charge through a conductor.",
            "what is magnetism": "Magnetism is a force caused by the motion of electric charges.",
            "what is a calorie": "A calorie is a unit of energy found in food and drinks.",
            "what is a vitamin": "Vitamins are essential nutrients your body needs in small amounts to function properly.",
            "what is exercise": "Exercise is physical activity that improves health, fitness, and mental wellbeing.",
            "what is sleep": "Sleep is a natural state of rest essential for physical and mental recovery.",
            "what is stress": "Stress is a physical and emotional response to challenging situations.",
            "what is meditation": "Meditation is a practice of focused attention to promote relaxation and mindfulness.",
            "what is pi": "Pi (π) is approximately 3.14159. It's the ratio of a circle's circumference to its diameter.",
            "what is infinity": "Infinity is a concept describing something without any limit or end.",
            "what is a prime number": "A prime number is a number greater than 1 that has no divisors other than 1 and itself.",
            "what is algebra": "Algebra is a branch of mathematics dealing with symbols and rules for manipulating them.",
            "what is geometry": "Geometry is the branch of mathematics concerned with shapes, sizes, and properties of figures.",
            "what is money": "Money is a medium of exchange used to buy goods and services.",
            "what is democracy": "Democracy is a system of government where citizens vote for their representatives.",
            "what is the stock market": "The stock market is a marketplace where shares of companies are bought and sold.",
            "what is cryptocurrency": "Cryptocurrency is a digital currency secured by cryptography, like Bitcoin or Ethereum.",
            "what is social media": "Social media are platforms that allow users to create and share content online.",
        }

        self.responses = {
            "hello": f"Hi {self.user_name}! How can I help?",
            "hi": f"Hey {self.user_name}! What can I do for you?",
            "how are you": "I'm running smoothly! All systems operational.",
            "thanks": "You're welcome! Happy to help.",
            "bye": "Goodbye! See you next time.",
            "help": "I can show stats, check weather, solve math, answer questions, show news, and more!",
        }

        self.apps = {
            "notepad": "notepad.exe" if platform.system() == "Windows" else "gedit",
            "calculator": "calc.exe" if platform.system() == "Windows" else "gnome-calculator",
            "chrome": "chrome" if platform.system() == "Windows" else "google-chrome",
            "firefox": "firefox",
            "discord": "discord.exe" if platform.system() == "Windows" else "discord",
        }

        self.setup_ui()

    def apply_theme(self, theme_name):
        """Apply theme colors"""
        theme = self.themes[theme_name]
        self.bg_color = theme["bg_color"]
        self.fg_color = theme["fg_color"]
        self.header_bg = theme["header_bg"]
        self.entry_bg = theme["entry_bg"]
        self.entry_fg = theme["entry_fg"]
        self.chat_bg = theme["chat_bg"]
        self.chat_fg = theme["chat_fg"]
        self.accent_purple = theme["accent_purple"]
        self.accent_orange = theme["accent_orange"]
        self.current_theme = theme_name

    def setup_ui(self):
        """Create the GUI layout"""
        try:
            self.root.configure(bg=self.bg_color)

            # Header
            header_frame = tk.Frame(self.root, bg=self.header_bg)
            header_frame.pack(fill=tk.X, padx=0, pady=0)

            title_label = tk.Label(
                header_frame,
                text="🤖 Intermatium BETA",
                font=self.title_font,
                bg=self.header_bg,
                fg=self.accent_orange
            )
            title_label.pack(pady=10)

            # Chat display
            chat_frame = tk.Frame(self.root, bg=self.bg_color)
            chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            self.chat_display = scrolledtext.ScrolledText(
                chat_frame,
                wrap=tk.WORD,
                font=self.chat_font,
                bg=self.chat_bg,
                fg=self.chat_fg,
                state=tk.DISABLED
            )
            self.chat_display.pack(fill=tk.BOTH, expand=True)

            # Input
            input_frame = tk.Frame(self.root, bg=self.bg_color)
            input_frame.pack(fill=tk.X, padx=10, pady=10)

            self.input_field = tk.Entry(
                input_frame,
                font=self.input_font,
                bg=self.entry_bg,
                fg=self.entry_fg
            )
            self.input_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
            self.input_field.bind("<Return>", lambda e: self.send_message())

            send_button = tk.Button(
                input_frame,
                text="Send",
                command=self.send_message,
                bg=self.accent_orange,
                fg="white",
                font=self.button_font
            )
            send_button.pack(side=tk.LEFT)

            # Buttons
            buttons_frame = tk.Frame(self.root, bg=self.bg_color)
            buttons_frame.pack(fill=tk.X, padx=10, pady=5)

            buttons = [
                ("📊 Stats", self.show_stats, "#4CAF50"),
                ("🌤️ Weather", self.show_weather, "#2196F3"),
                ("📅 Date", self.show_date_time, "#FF9800"),
                ("🧮 Math", self.math_helper, "#E91E63"),
                ("📰 News", self.show_news, "#00BCD4"),
                ("🎨 Theme", self.show_theme_menu, "#FF6B6B"),
                ("🤖 Aria", self.show_aria_info, "#9C27B0"),
                ("🐙 GitHub", self.open_github, "#333333"),
                ("🗑️ Clear", self.clear_chat, "#f44336"),
            ]

            for text, cmd, color in buttons:
                btn = tk.Button(buttons_frame, text=text, command=cmd, bg=color, fg="white", font=self.button_font,
                                padx=8)
                btn.pack(side=tk.LEFT, padx=2)

            self.typewriter_message(
                "👋 Welcome to Intermatium BETA!\nType any question or use buttons above.\nTry: 'What's the weather in Tokyo?' or ask Aria a question!")
        except Exception as e:
            print(f"Error in setup_ui: {e}")

    def show_theme_menu(self):
        """Show theme selection"""
        try:
            theme_window = tk.Toplevel(self.root)
            theme_window.title("Select Theme")
            theme_window.geometry("250x200")
            theme_window.configure(bg=self.bg_color)

            tk.Label(theme_window, text="Choose Theme:", font=self.button_font, bg=self.bg_color,
                     fg=self.fg_color).pack(pady=10)

            for theme_name, theme_key in [("🌙 Dark", "dark"), ("☀️ White", "white"), ("🔵 Blue", "blue"),
                                          ("⚫ Grey", "grey")]:
                btn = tk.Button(
                    theme_window,
                    text=theme_name,
                    command=lambda t=theme_key: self.change_theme(t, theme_window),
                    bg=self.themes[theme_key]["header_bg"],
                    fg=self.themes[theme_key]["fg_color"],
                    font=self.button_font,
                    width=20
                )
                btn.pack(pady=5)
        except Exception as e:
            print(f"Error in show_theme_menu: {e}")

    def change_theme(self, theme_name, window):
        """Change theme"""
        try:
            self.apply_theme(theme_name)
            window.destroy()

            self.root.configure(bg=self.bg_color)
            self.chat_display.configure(bg=self.chat_bg, fg=self.chat_fg)
            self.input_field.configure(bg=self.entry_bg, fg=self.entry_fg)

            self.typewriter_message(f"✅ Theme changed to {self.themes[theme_name]['name']}!")
        except Exception as e:
            print(f"Error in change_theme: {e}")

    def show_aria_info(self):
        """Show Aria chatbot info"""
        aria_info = """
╔════════════════════════════════════════╗
║   ARIA - Inner Chatbot v1.0            ║
╚════════════════════════════════════════╝

🤖 WHAT IS ARIA?
Aria is Intermatium's inner chatbot specialising in answering specific questions about:
• Technology & Programming
• Science & Nature
• Health & Wellness
• Mathematics
• General Knowledge
• Fun & Entertainment

💬 HOW TO USE ARIA:
Simply ask Aria any question! Examples:
• "What is a CPU?"
• "Tell me a joke"
• "What is the moon?"
• "What is cryptocurrency?"
• "Who are you?"

Try asking Aria anything!
        """
        self.typewriter_message(aria_info)

    def open_github(self):
        """Open GitHub"""
        try:
            webbrowser.open("https://github.com/CyxcCodes")
            self.typewriter_message("🐙 Opening GitHub...")
        except Exception as e:
            self.typewriter_message(f"Error: {str(e)}")

    def get_time_in_city(self, city_name):
        """Get time in a specific city"""
        try:
            city_lower = city_name.lower().strip()

            if city_lower not in self.city_timezones:
                available = ", ".join(list(self.city_timezones.keys())[:10])
                return f"❌ City not found. Try: {available}..."

            timezone = self.city_timezones[city_lower]
            tz = ZoneInfo(timezone)
            current_time = datetime.now(tz)

            time_str = current_time.strftime("%I:%M:%S %p")
            date_str = current_time.strftime("%A, %B %d, %Y")

            return f"⏰ Time in {city_name.title()}:\n{time_str}\n📅 {date_str}"
        except Exception as e:
            return f"Error getting time: {str(e)}"

    def typewriter_message(self, message, delay=15):
        """Typewriter effect"""
        try:
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.insert(tk.END, f"\n{self.name}: ")
            self.chat_display.config(state=tk.DISABLED)

            def type_chars(index=0):
                if index < len(message):
                    self.chat_display.config(state=tk.NORMAL)
                    self.chat_display.insert(tk.END, message[index])
                    self.chat_display.see(tk.END)
                    self.chat_display.config(state=tk.DISABLED)
                    self.root.after(delay, type_chars, index + 1)
                else:
                    self.chat_display.config(state=tk.NORMAL)
                    self.chat_display.insert(tk.END, "\n")
                    self.chat_display.config(state=tk.DISABLED)

            type_chars()
        except Exception as e:
            print(f"Error in typewriter_message: {e}")

    def display_message_instant(self, message, sender="You"):
        """Display instantly"""
        try:
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.insert(tk.END, f"\n{sender}: {message}\n")
            self.chat_display.see(tk.END)
            self.chat_display.config(state=tk.DISABLED)
        except Exception as e:
            print(f"Error in display_message_instant: {e}")

    def send_message(self):
        """Send message"""
        try:
            user_input = self.input_field.get().strip()
            if not user_input:
                return

            self.display_message_instant(user_input, "You")
            self.input_field.delete(0, tk.END)

            thread = threading.Thread(target=self.process_message, args=(user_input,))
            thread.daemon = True
            thread.start()
        except Exception as e:
            print(f"Error in send_message: {e}")

    def process_message(self, user_input):
        """Process message"""
        try:
            response = self.chat_with_user(user_input)
            self.typewriter_message(response)
        except Exception as e:
            print(f"Error in process_message: {e}")

    def show_stats(self):
        """Show stats"""
        try:
            thread = threading.Thread(target=self._get_stats_thread)
            thread.daemon = True
            thread.start()
        except Exception as e:
            print(f"Error in show_stats: {e}")

    def _get_stats_thread(self):
        """Get stats"""
        try:
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')

            stats = f"CPU: {cpu}%\nRAM: {round(memory.used / (1024 ** 3), 2)}GB / {round(memory.total / (1024 ** 3), 2)}GB ({memory.percent}%)\nDISK: {round(disk.used / (1024 ** 3), 2)}GB / {round(disk.total / (1024 ** 3), 2)}GB ({disk.percent}%)"
            self.typewriter_message(stats)
        except Exception as e:
            self.typewriter_message(f"Error: {str(e)}")

    def show_weather(self):
        """Show weather"""
        try:
            city = simpledialog.askstring("Weather", "Enter city (or leave blank for auto-detect):")
            if city is not None:
                thread = threading.Thread(target=self._get_weather_thread, args=(city or "auto",))
                thread.daemon = True
                thread.start()
        except Exception as e:
            print(f"Error in show_weather: {e}")

    def _get_weather_thread(self, city):
        """Get detailed weather"""
        try:
            if city.lower() == "auto":
                response = urlopen("https://ipapi.co/json/", timeout=5)
                data = json.loads(response.read())
                lat, lon = data.get("latitude"), data.get("longitude")
                city_name = data.get("city", "Unknown")
            else:
                response = urlopen(f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1", timeout=5)
                data = json.loads(response.read())
                if not data.get("results"):
                    self.typewriter_message("❌ City not found. Please try another city.")
                    return
                result = data["results"]
                lat = result["latitude"]
                lon = result["longitude"]
                city_name = f"{result['name']}, {result.get('country', '')}"

            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m,wind_direction_10m,pressure_msl&temperature_unit=fahrenheit"
            weather_response = urlopen(weather_url, timeout=5)
            weather_data = json.loads(weather_response.read())

            current = weather_data["current"]
            temp = current["temperature_2m"]
            feels_like = current["apparent_temperature"]
            humidity = current["relative_humidity_2m"]
            wind_speed = current["wind_speed_10m"]
            wind_direction = current["wind_direction_10m"]
            precipitation = current["precipitation"]
            pressure = current["pressure_msl"]
            weather_code = current["weather_code"]

            description = self.weather_descriptions.get(weather_code, "Unknown")

            directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW",
                          "NNW"]
            direction_index = round(wind_direction / 22.5) % 16
            wind_dir = directions[direction_index]

            weather_report = f"""
🌍 WEATHER IN {city_name.upper()}

🌡️  Temperature: {temp}°F
🤔 Feels Like: {feels_like}°F
💨 Wind: {wind_speed} mph ({wind_dir})
💧 Humidity: {humidity}%
🌧️  Precipitation: {precipitation} mm
🔽 Pressure: {pressure} mb
☁️  Condition: {description}
"""
            self.typewriter_message(weather_report)
        except Exception as e:
            self.typewriter_message(f"❌ Error fetching weather: {str(e)}")

    def show_date_time(self):
        """Show date/time"""
        try:
            now = datetime.now()
            date_str = now.strftime("%A, %B %d, %Y - %I:%M:%S %p")
            self.typewriter_message(date_str)
        except Exception as e:
            print(f"Error in show_date_time: {e}")

    def math_helper(self):
        """Math helper"""
        try:
            problem = simpledialog.askstring("Math", "Enter problem (e.g., 2+2):")
            if problem:
                thread = threading.Thread(target=self._solve_math, args=(problem,))
                thread.daemon = True
                thread.start()
        except Exception as e:
            print(f"Error in math_helper: {e}")

    def _solve_math(self, problem):
        """Solve math"""
        try:
            result = self.solve_math(problem)
            self.typewriter_message(result)
        except Exception as e:
            print(f"Error in _solve_math: {e}")

    def solve_math(self, problem):
        """Solve math problem"""
        try:
            problem = problem.replace("^", "**").replace("÷", "/").replace("×", "*")
            safe_dict = {
                "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos, "tan": math.tan,
                "log": math.log, "pi": math.pi, "e": math.e
            }
            result = eval(problem, {"__builtins__": {}}, safe_dict)
            return f"✅ {problem} = {round(result, 2) if isinstance(result, float) else result}"
        except:
            return "❌ Invalid math expression"

    def show_news(self):
        """Show news"""
        try:
            thread = threading.Thread(target=self._get_news_thread)
            thread.daemon = True
            thread.start()
        except Exception as e:
            print(f"Error in show_news: {e}")

    def _get_news_thread(self):
        """Get news"""
        try:
            url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=demo"
            response = urlopen(url, timeout=5)
            data = json.loads(response.read())

            if data.get("articles"):
                news = "📰 TOP NEWS HEADLINES:\n\n"
                for i, article in enumerate(data["articles"][:5], 1):
                    title = article.get('title', 'No title')
                    source = article.get('source', {}).get('name', 'Unknown')
                    news += f"{i}. {title}\n   Source: {source}\n\n"
                self.typewriter_message(news)
            else:
                self.typewriter_message("❌ Could not fetch news")
        except Exception as e:
            self.typewriter_message(f"❌ Error: {str(e)}")

    def clear_chat(self):
        """Clear chat"""
        try:
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete(1.0, tk.END)
            self.chat_display.config(state=tk.DISABLED)
            self.typewriter_message("Chat cleared!")
        except Exception as e:
            print(f"Error in clear_chat: {e}")

    def chat_with_user(self, user_input):
        """Chat with user"""
        user_lower = user_input.lower().strip()

        # Check Aria chatbot knowledge base first
        for question, answer in self.chatbot_knowledge.items():
            if question in user_lower:
                return f"🤖 Aria says: {answer}"

        # Check for time in city
        if "time in" in user_lower or "what time is it in" in user_lower:
            if "time in" in user_lower:
                city = user_lower.split("time in")[-1].strip().replace("?", "").strip()
            else:
                city = user_lower.split("in")[-1].strip().replace("?", "").strip()

            if city:
                return self.get_time_in_city(city)

        # Check for weather
        if any(word in user_lower for word in ["weather", "forecast", "temperature"]):
            if "in" in user_lower:
                parts = user_lower.split("in")
                city = parts[-1].strip().replace("?", "").strip()
                thread = threading.Thread(target=self._get_weather_thread, args=(city,))
            else:
                thread = threading.Thread(target=self._get_weather_thread, args=("auto",))
            thread.daemon = True
            thread.start()
            return "🌤️ Fetching weather..."

        # Math
        if any(c in user_input for c in ["+", "-", "*", "/", "sqrt"]):
            if not any(w in user_lower for w in ["what", "how", "why"]):
                result = self.solve_math(user_input)
                if "=" in result:
                    return result

        # Name setting
        if "call me" in user_lower:
            name = user_lower.split("call me")[-1].strip().replace("?", "").strip()
            if name:
                self.user_name = name.capitalize()
                self.responses["hello"] = f"Hi {self.user_name}! How can I help?"
                self.responses["hi"] = f"Hey {self.user_name}! What can I do for you?"
                return f"✅ Nice to meet you, {self.user_name}!"

        if "my name is" in user_lower:
            name = user_lower.split("my name is")[-1].strip().replace("?", "").strip()
            if name:
                self.user_name = name.capitalize()
                self.responses["hello"] = f"Hi {self.user_name}! How can I help?"
                self.responses["hi"] = f"Hey {self.user_name}! What can I do for you?"
                return f"✅ Great to meet you, {self.user_name}!"

        # Knowledge base
        for question, answer in self.knowledge_base.items():
            if question in user_lower:
                return answer

        # Responses
        for key, response in self.responses.items():
            if key in user_lower:
                return response

        return f"That's interesting, {self.user_name}! Try asking me a question or use the buttons!"


# Run
if __name__ == "__main__":
    root = tk.Tk()
    app = IntermatiumApp(root)
    root.mainloop()