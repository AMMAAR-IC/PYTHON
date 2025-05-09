import argparse
import json
import os
import sys
import textwrap
import time
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, font
from typing import Dict, List, Optional, Tuple, Union
import random
import webbrowser
from datetime import datetime

# Try to import optional dependencies with fallbacks
try:
    from googlesearch import search

    HAS_GOOGLE_SEARCH = True
except ImportError:
    HAS_GOOGLE_SEARCH = False
    print("Warning: googlesearch-python module not installed. Google search functionality will be limited.")
    print("Install with: pip install googlesearch-python")


    # Simple fallback implementation
    def search(query, stop=10, pause=2):
        print(f"[Simulation] Searching Google for: {query}")
        yield f"https://www.example.com/search?q={query.replace(' ', '+')}"

try:
    import language_tool_python

    HAS_LANGUAGE_TOOL = True
except ImportError:
    HAS_LANGUAGE_TOOL = False
    print("Warning: language_tool_python not installed. Grammar correction will be disabled.")
    print("Install with: pip install language-tool-python")

try:
    import wikipedia

    HAS_WIKIPEDIA = True
except ImportError:
    HAS_WIKIPEDIA = False
    print("Warning: wikipedia module not installed. Wikipedia functionality will be limited.")
    print("Install with: pip install wikipedia")

try:
    from PIL import Image, ImageTk

    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("Warning: PIL module not installed. Some GUI features will be limited.")
    print("Install with: pip install pillow")

# Configuration and settings
CONFIG_FILE = os.path.expanduser("~/.search_assistant_config.json")
DEFAULT_CONFIG = {
    "search_engines": ["google", "wikipedia"],
    "results_count": 3,
    "history_file": os.path.expanduser("~/.search_assistant_history.json"),
    "max_history": 50,
    "wrap_width": 80,
    "auto_correct": True,
    "search_delay": 2.0,
    "theme": "dark",  # 'light' or 'dark'
    "font_size": 10,
    "window_width": 1000,
    "window_height": 700
}

# Color schemes
THEMES = {
    "light": {
        "bg": "#f5f5f5",
        "fg": "#333333",
        "accent": "#3498db",
        "accent_dark": "#2980b9",
        "highlight": "#e1f0fa",
        "sidebar": "#e0e0e0",
        "card_bg": "#ffffff",
        "card_border": "#dddddd",
        "success": "#2ecc71",
        "warning": "#f39c12",
        "error": "#e74c3c",
        "button": "#3498db",
        "button_text": "#ffffff",
        "input_bg": "#ffffff",
        "input_border": "#cccccc"
    },
    "dark": {
        "bg": "#1e1e2e",
        "fg": "#cdd6f4",
        "accent": "#89b4fa",
        "accent_dark": "#74c7ec",
        "highlight": "#313244",
        "sidebar": "#181825",
        "card_bg": "#313244",
        "card_border": "#45475a",
        "success": "#a6e3a1",
        "warning": "#f9e2af",
        "error": "#f38ba8",
        "button": "#89b4fa",
        "button_text": "#1e1e2e",
        "input_bg": "#313244",
        "input_border": "#45475a"
    }
}


def load_config() -> Dict:
    """Load or create configuration file"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            print("Error reading config file. Using defaults.")
    save_config(DEFAULT_CONFIG)
    return DEFAULT_CONFIG


def save_config(config: Dict) -> None:
    """Save configuration to file"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
    except IOError as e:
        print(f"Error saving config: {e}")


class GrammarCorrector:
    """Handles text grammar correction"""

    def __init__(self):
        self.tool = language_tool_python.LanguageTool('en-US') if HAS_LANGUAGE_TOOL else None

    def correct_grammar(self, text: str) -> Tuple[str, List[Dict]]:
        """Correct grammar and return corrected text and corrections made"""
        if not self.tool:
            return text, []
        try:
            matches = self.tool.check(text)
            corrected = language_tool_python.utils.correct(text, matches)
            corrections = [{"original": match.context, "message": match.message, "replacements": match.replacements[:3]}
                           for match in matches]
            return corrected, corrections
        except Exception as e:
            print(f"Grammar correction error: {e}")
            return text, []


class SearchAssistant:
    """Main search assistant class"""

    def __init__(self, config: Dict = None):
        self.config = config or load_config()
        self.grammar = GrammarCorrector()
        self.history = self._load_history()

    def _load_history(self) -> List[Dict]:
        """Load search history"""
        history_file = self.config.get("history_file")
        if history_file and os.path.exists(history_file):
            try:
                with open(history_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def _save_history(self) -> None:
        """Save search history"""
        history_file = self.config.get("history_file")
        if not history_file:
            return
        max_history = self.config.get("max_history", 50)
        if len(self.history) > max_history:
            self.history = self.history[-max_history:]
        try:
            with open(history_file, 'w') as f:
                json.dump(self.history, f, indent=2)
        except IOError as e:
            print(f"Error saving history: {e}")

    def add_question_mark_if_needed(self, text: str) -> str:
        """Add question mark if text appears to be a question"""
        question_starters = {"who", "what", "where", "when", "why", "how", "is", "are", "was", "were", "do", "does",
                             "did", "can", "could", "would", "should", "will", "shall", "have", "has", "had", "may",
                             "might", "must"}
        words = text.lower().split()
        is_likely_question = (words and words[0] in question_starters) or (
                    len(words) > 1 and words[0] in {"can", "could", "would", "will"} and words[1] in {"you", "i", "we",
                                                                                                      "they"})
        return text + "?" if is_likely_question and not text.endswith("?") else text

    def fetch_google_results(self, query: str, limit: int = 3) -> List[Dict]:
        """Fetch Google search results"""
        results = []
        if not HAS_GOOGLE_SEARCH:
            results.append({"error": "Google search module not installed", "source": "Google"})
            return results

        try:
            for i, result in enumerate(search(query, stop=limit, pause=self.config.get("search_delay", 2))):
                if i >= limit:
                    break
                results.append({"url": result, "source": "Google"})
        except Exception as e:
            results.append({"error": f"Error fetching Google results: {e}", "source": "Google"})
        return results

    def fetch_wikipedia_results(self, query: str, sentences: int = 5) -> Dict:
        """Fetch Wikipedia results"""
        if not HAS_WIKIPEDIA:
            return {"error": "Wikipedia module not installed", "source": "Wikipedia"}
        result = {"source": "Wikipedia", "query": query}
        try:
            summary = wikipedia.summary(query, sentences=sentences)
            page = wikipedia.page(query)
            result.update({"title": page.title, "summary": summary, "url": page.url,
                           "categories": page.categories[:5] if hasattr(page, 'categories') else []})
        except wikipedia.exceptions.DisambiguationError as e:
            result.update({"disambiguation": True, "options": e.options[:7],
                           "message": f"Multiple Wikipedia pages match '{query}'"})
        except wikipedia.exceptions.PageError:
            search_results = wikipedia.search(query, results=3)
            result.update({"search_results": search_results,
                           "message": f"No exact Wikipedia match for '{query}', but found related pages"} if search_results else {
                "message": f"No Wikipedia information found for '{query}'"})
        except Exception as e:
            result.update({"error": f"Wikipedia error: {e}"})
        return result

    def process_query(self, text: str) -> Dict:
        """Process a query and return search results"""
        start_time = time.time()
        corrected_text, corrections = self.grammar.correct_grammar(text) if self.config.get("auto_correct", True) else (
        text, [])
        final_text = self.add_question_mark_if_needed(corrected_text)
        results = {"original_query": text, "processed_query": final_text, "was_corrected": text != corrected_text,
                   "corrections": corrections, "timestamp": time.time(), "search_results": {}}
        engines = self.config.get("search_engines", ["google", "wikipedia"])
        result_count = self.config.get("results_count", 3)

        if "google" in engines:
            results["search_results"]["google"] = self.fetch_google_results(final_text, result_count)
        if "wikipedia" in engines:
            results["search_results"]["wikipedia"] = self.fetch_wikipedia_results(final_text)

        results["execution_time"] = time.time() - start_time
        self.history.append({"query": final_text, "timestamp": results["timestamp"]})
        self._save_history()
        return results


class HyperlinkManager:
    """Manages hyperlinks in Text widgets"""

    def __init__(self, text):
        self.text = text
        self.text.tag_config("hyperlink", foreground="blue", underline=1)
        self.text.tag_bind("hyperlink", "<Enter>", self._enter)
        self.text.tag_bind("hyperlink", "<Leave>", self._leave)
        self.text.tag_bind("hyperlink", "<Button-1>", self._click)
        self.reset()

    def reset(self):
        self.links = {}

    def add(self, action):
        tag = f"hyperlink-{len(self.links)}"
        self.links[tag] = action
        return "hyperlink", tag

    def _enter(self, event):
        self.text.config(cursor="hand2")

    def _leave(self, event):
        self.text.config(cursor="")

    def _click(self, event):
        for tag in self.text.tag_names(tk.CURRENT):
            if tag[:9] == "hyperlink-":
                self.links[tag]()
                return


class SearchAssistantGUI:
    """GUI for the Search Assistant"""

    def __init__(self, root):
        self.root = root
        self.config = load_config()
        self.assistant = SearchAssistant(self.config)
        self.theme = self.config.get("theme", "dark")
        self.colors = THEMES[self.theme]

        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface"""
        self.root.title("Search Assistant")
        self.root.geometry(f"{self.config.get('window_width', 1000)}x{self.config.get('window_height', 700)}")
        self.root.minsize(800, 600)

        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use clam theme as base

        # Configure colors based on theme
        self.root.configure(bg=self.colors["bg"])
        self.style.configure("TFrame", background=self.colors["bg"])
        self.style.configure("TLabel", background=self.colors["bg"], foreground=self.colors["fg"])
        self.style.configure("TButton",
                             background=self.colors["button"],
                             foreground=self.colors["button_text"],
                             borderwidth=0,
                             focusthickness=0,
                             font=('Helvetica', 10, 'bold'))
        self.style.map("TButton",
                       background=[('active', self.colors["accent_dark"])],
                       foreground=[('active', self.colors["button_text"])])

        # Create custom font
        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font.configure(family="Helvetica", size=self.config.get("font_size", 10))
        self.text_font = font.Font(family="Helvetica", size=self.config.get("font_size", 10))
        self.heading_font = font.Font(family="Helvetica", size=self.config.get("font_size", 10) + 4, weight="bold")

        # Main layout - split into sidebar and content
        self.main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_paned.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        # Sidebar frame
        self.sidebar_frame = ttk.Frame(self.main_paned, style="Sidebar.TFrame")
        self.sidebar_frame.configure(width=200)
        self.style.configure("Sidebar.TFrame", background=self.colors["sidebar"])

        # Content frame
        self.content_frame = ttk.Frame(self.main_paned)

        self.main_paned.add(self.sidebar_frame, weight=1)
        self.main_paned.add(self.content_frame, weight=4)

        # Set up sidebar
        self.setup_sidebar()

        # Set up content area
        self.setup_content()

    def setup_sidebar(self):
        """Set up the sidebar with history and settings"""
        # Logo/Title
        title_frame = ttk.Frame(self.sidebar_frame, style="Sidebar.TFrame")
        title_frame.pack(fill=tk.X, padx=10, pady=(20, 10))

        title_label = ttk.Label(title_frame, text="Search Assistant",
                                font=('Helvetica', 14, 'bold'),
                                foreground=self.colors["accent"],
                                background=self.colors["sidebar"])
        title_label.pack(side=tk.LEFT, padx=5)

        # Divider
        divider = ttk.Separator(self.sidebar_frame, orient=tk.HORIZONTAL)
        divider.pack(fill=tk.X, padx=10, pady=5)

        # History section
        history_label = ttk.Label(self.sidebar_frame, text="Recent Searches",
                                  font=('Helvetica', 11, 'bold'),
                                  foreground=self.colors["fg"],
                                  background=self.colors["sidebar"])
        history_label.pack(anchor=tk.W, padx=15, pady=(10, 5))

        # History list
        self.history_frame = ttk.Frame(self.sidebar_frame, style="Sidebar.TFrame")
        self.history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.update_history_list()

        # Settings section at bottom
        settings_frame = ttk.Frame(self.sidebar_frame, style="Sidebar.TFrame")
        settings_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=10)

        # Theme toggle
        theme_frame = ttk.Frame(settings_frame, style="Sidebar.TFrame")
        theme_frame.pack(fill=tk.X, pady=5)

        theme_label = ttk.Label(theme_frame, text="Theme:",
                                background=self.colors["sidebar"],
                                foreground=self.colors["fg"])
        theme_label.pack(side=tk.LEFT, padx=5)

        self.theme_var = tk.StringVar(value=self.theme)
        theme_menu = ttk.OptionMenu(theme_frame, self.theme_var, self.theme, "light", "dark",
                                    command=self.change_theme)
        theme_menu.pack(side=tk.RIGHT, padx=5)

        # Settings button
        settings_button = ttk.Button(settings_frame, text="Settings",
                                     command=self.open_settings)
        settings_button.pack(fill=tk.X, pady=5)

    def update_history_list(self):
        """Update the history list in the sidebar"""
        # Clear existing history items
        for widget in self.history_frame.winfo_children():
            widget.destroy()

        # Create scrollable canvas for history items
        canvas = tk.Canvas(self.history_frame, bg=self.colors["sidebar"],
                           highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.history_frame, orient="vertical",
                                  command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style="Sidebar.TFrame")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Add history items
        if not self.assistant.history:
            no_history_label = ttk.Label(scrollable_frame, text="No search history",
                                         foreground=self.colors["fg"],
                                         background=self.colors["sidebar"])
            no_history_label.pack(pady=10, padx=5, anchor=tk.W)
        else:
            # Display most recent searches first
            for item in reversed(self.assistant.history[-10:]):
                query = item["query"]
                timestamp = datetime.fromtimestamp(item["timestamp"]).strftime("%H:%M:%S")

                history_item = ttk.Frame(scrollable_frame, style="Sidebar.TFrame")
                history_item.pack(fill=tk.X, pady=2, padx=2)

                # Make the entire frame clickable
                history_item.bind("<Button-1>", lambda e, q=query: self.load_history_query(q))

                query_label = ttk.Label(history_item, text=query if len(query) < 25 else query[:22] + "...",
                                        foreground=self.colors["fg"],
                                        background=self.colors["sidebar"],
                                        cursor="hand2")
                query_label.pack(anchor=tk.W, padx=5, pady=2)
                query_label.bind("<Button-1>", lambda e, q=query: self.load_history_query(q))

                time_label = ttk.Label(history_item, text=timestamp,
                                       foreground=self.colors["fg"],
                                       background=self.colors["sidebar"],
                                       font=('Helvetica', 8))
                time_label.pack(anchor=tk.W, padx=5, pady=(0, 2))

    def load_history_query(self, query):
        """Load a query from history into the search box and execute it"""
        self.query_var.set(query)
        self.execute_search()

    def setup_content(self):
        """Set up the main content area"""
        # Search bar at top
        search_frame = ttk.Frame(self.content_frame)
        search_frame.pack(fill=tk.X, padx=20, pady=20)

        self.query_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.query_var,
                                 font=('Helvetica', 12))
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        search_entry.bind("<Return>", lambda e: self.execute_search())

        # Style the entry widget
        search_entry.configure(style="Search.TEntry")
        self.style.configure("Search.TEntry",
                             fieldbackground=self.colors["input_bg"],
                             foreground=self.colors["fg"],
                             bordercolor=self.colors["input_border"],
                             lightcolor=self.colors["input_border"],
                             darkcolor=self.colors["input_border"])

        search_button = ttk.Button(search_frame, text="Search",
                                   command=self.execute_search)
        search_button.pack(side=tk.RIGHT)

        # Results area
        self.results_frame = ttk.Frame(self.content_frame)
        self.results_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # Initial message
        self.initial_message_frame = ttk.Frame(self.results_frame)
        self.initial_message_frame.pack(fill=tk.BOTH, expand=True)

        welcome_message = """
        Welcome to Search Assistant!

        Type your query in the search box above and press Enter or click Search.

        Features:
        • Search Google and Wikipedia
        • Grammar correction
        • Search history
        • Dark/Light theme

        Try asking a question like "What is quantum computing?" or "Who wrote Hamlet?"
        """

        welcome_label = ttk.Label(self.initial_message_frame,
                                  text=welcome_message,
                                  justify=tk.CENTER,
                                  foreground=self.colors["fg"],
                                  background=self.colors["bg"],
                                  font=('Helvetica', 12))
        welcome_label.pack(expand=True)

        # Status bar
        self.status_frame = ttk.Frame(self.root)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(self.status_frame, textvariable=self.status_var,
                                 anchor=tk.W, padding=(10, 2))
        status_label.pack(side=tk.LEFT)

        # Progress indicator (hidden initially)
        self.progress = ttk.Progressbar(self.status_frame, mode="indeterminate", length=100)

    def execute_search(self):
        """Execute the search query"""
        query = self.query_var.get().strip()
        if not query:
            return

        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        # Show progress
        self.status_var.set("Searching...")
        self.progress.pack(side=tk.RIGHT, padx=10, pady=2)
        self.progress.start(10)
        self.root.update_idletasks()

        # Run search in a separate thread to keep UI responsive
        threading.Thread(target=self._search_thread, args=(query,), daemon=True).start()

    def _search_thread(self, query):
        """Run search in a separate thread"""
        try:
            results = self.assistant.process_query(query)
            # Schedule UI update on the main thread
            self.root.after(0, lambda: self.display_results(results))
        except Exception as e:
            self.root.after(0, lambda: self.show_error(str(e)))

    def show_error(self, error_message):
        """Display an error message"""
        self.progress.stop()
        self.progress.pack_forget()
        self.status_var.set("Error occurred")

        for widget in self.results_frame.winfo_children():
            widget.destroy()

        error_frame = ttk.Frame(self.results_frame)
        error_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        error_label = ttk.Label(error_frame,
                                text=f"An error occurred:\n{error_message}",
                                foreground=self.colors["error"],
                                background=self.colors["bg"],
                                justify=tk.CENTER,
                                font=('Helvetica', 12))
        error_label.pack(expand=True)

    def display_results(self, results):
        """Display search results in the UI"""
        self.progress.stop()
        self.progress.pack_forget()
        self.status_var.set(f"Search completed in {results['execution_time']:.2f} seconds")

        # Update history list
        self.update_history_list()

        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        # Create scrollable results area
        canvas = tk.Canvas(self.results_frame, bg=self.colors["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.results_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.configure(style="TFrame")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mousewheel for scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Query section
        query_frame = ttk.Frame(scrollable_frame)
        query_frame.pack(fill=tk.X, padx=10, pady=10)

        query_label = ttk.Label(query_frame,
                                text=f"Query: {results['original_query']}",
                                font=self.heading_font,
                                foreground=self.colors["fg"],
                                background=self.colors["bg"])
        query_label.pack(anchor=tk.W)

        if results["was_corrected"]:
            corrected_label = ttk.Label(query_frame,
                                        text=f"Corrected to: {results['processed_query']}",
                                        font=self.text_font,
                                        foreground=self.colors["success"],
                                        background=self.colors["bg"])
            corrected_label.pack(anchor=tk.W, pady=(5, 0))

            if results["corrections"]:
                corrections_frame = ttk.Frame(query_frame)
                corrections_frame.pack(fill=tk.X, pady=10)

                corrections_label = ttk.Label(corrections_frame,
                                              text="Grammar Corrections:",
                                              font=('Helvetica', 10, 'bold'),
                                              foreground=self.colors["fg"],
                                              background=self.colors["bg"])
                corrections_label.pack(anchor=tk.W)

                for c in results["corrections"]:
                    correction_label = ttk.Label(corrections_frame,
                                                 text=f"• {c['message']}",
                                                 foreground=self.colors["fg"],
                                                 background=self.colors["bg"],
                                                 wraplength=600)
                    correction_label.pack(anchor=tk.W, padx=10, pady=2)

        # Display Wikipedia results
        if "wikipedia" in results["search_results"]:
            self.display_wikipedia_results(scrollable_frame, results["search_results"]["wikipedia"])

        # Display Google results
        if "google" in results["search_results"]:
            self.display_google_results(scrollable_frame, results["search_results"]["google"])

    def display_wikipedia_results(self, parent, wiki_results):
        """Display Wikipedia results"""
        wiki_frame = ttk.Frame(parent)
        wiki_frame.pack(fill=tk.X, padx=10, pady=10)

        # Create card-like appearance
        wiki_card = ttk.Frame(wiki_frame)
        wiki_card.pack(fill=tk.X, pady=5)
        wiki_card.configure(style="Card.TFrame")
        self.style.configure("Card.TFrame",
                             background=self.colors["card_bg"],
                             borderwidth=1,
                             relief="solid")

        # Card header
        header_frame = ttk.Frame(wiki_card)
        header_frame.pack(fill=tk.X, padx=15, pady=10)
        header_frame.configure(style="CardHeader.TFrame")
        self.style.configure("CardHeader.TFrame", background=self.colors["card_bg"])

        wiki_title = ttk.Label(header_frame,
                               text="Wikipedia Results",
                               font=('Helvetica', 14, 'bold'),
                               foreground=self.colors["accent"],
                               background=self.colors["card_bg"])
        wiki_title.pack(anchor=tk.W)

        # Card content
        content_frame = ttk.Frame(wiki_card)
        content_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        content_frame.configure(style="CardContent.TFrame")
        self.style.configure("CardContent.TFrame", background=self.colors["card_bg"])

        if "error" in wiki_results:
            error_label = ttk.Label(content_frame,
                                    text=f"Error: {wiki_results['error']}",
                                    foreground=self.colors["error"],
                                    background=self.colors["card_bg"],
                                    wraplength=600)
            error_label.pack(anchor=tk.W)
        elif "disambiguation" in wiki_results and wiki_results["disambiguation"]:
            message_label = ttk.Label(content_frame,
                                      text=wiki_results["message"],
                                      foreground=self.colors["fg"],
                                      background=self.colors["card_bg"],
                                      wraplength=600)
            message_label.pack(anchor=tk.W, pady=(0, 10))

            options_frame = ttk.Frame(content_frame)
            options_frame.pack(fill=tk.X)
            options_frame.configure(style="CardContent.TFrame")

            for opt in wiki_results["options"]:
                option_button = ttk.Button(options_frame,
                                           text=opt,
                                           command=lambda q=opt: self.load_history_query(q))
                option_button.pack(anchor=tk.W, pady=2)
        elif "search_results" in wiki_results:
            message_label = ttk.Label(content_frame,
                                      text=wiki_results["message"],
                                      foreground=self.colors["fg"],
                                      background=self.colors["card_bg"],
                                      wraplength=600)
            message_label.pack(anchor=tk.W, pady=(0, 10))

            options_frame = ttk.Frame(content_frame)
            options_frame.pack(fill=tk.X)
            options_frame.configure(style="CardContent.TFrame")

            for opt in wiki_results["search_results"]:
                option_button = ttk.Button(options_frame,
                                           text=opt,
                                           command=lambda q=opt: self.load_history_query(q))
                option_button.pack(anchor=tk.W, pady=2)
        elif "summary" in wiki_results:
            title_label = ttk.Label(content_frame,
                                    text=f"Title: {wiki_results['title']}",
                                    font=('Helvetica', 12, 'bold'),
                                    foreground=self.colors["fg"],
                                    background=self.colors["card_bg"])
            title_label.pack(anchor=tk.W, pady=(0, 10))

            # Create text widget for summary with hyperlink support
            summary_text = scrolledtext.ScrolledText(content_frame,
                                                     wrap=tk.WORD,
                                                     width=70,
                                                     height=10,
                                                     font=self.text_font,
                                                     bg=self.colors["card_bg"],
                                                     fg=self.colors["fg"])
            summary_text.pack(fill=tk.X, pady=5)
            summary_text.insert(tk.END, wiki_results["summary"])
            summary_text.config(state=tk.DISABLED)  # Make read-only

            # URL and categories
            url_frame = ttk.Frame(content_frame)
            url_frame.pack(fill=tk.X, pady=5)
            url_frame.configure(style="CardContent.TFrame")

            url_label = ttk.Label(url_frame,
                                  text="URL: ",
                                  foreground=self.colors["fg"],
                                  background=self.colors["card_bg"])
            url_label.pack(side=tk.LEFT)

            hyperlink = ttk.Label(url_frame,
                                  text=wiki_results["url"],
                                  foreground=self.colors["accent"],
                                  background=self.colors["card_bg"],
                                  cursor="hand2")
            hyperlink.pack(side=tk.LEFT)
            hyperlink.bind("<Button-1>", lambda e, url=wiki_results["url"]: webbrowser.open_new(url))

            if "categories" in wiki_results and wiki_results["categories"]:
                categories = ", ".join(wiki_results["categories"])
                categories_label = ttk.Label(content_frame,
                                             text=f"Categories: {categories}",
                                             foreground=self.colors["fg"],
                                             background=self.colors["card_bg"],
                                             wraplength=600)
                categories_label.pack(anchor=tk.W, pady=5)

    def display_google_results(self, parent, google_results):
        """Display Google search results"""
        if not google_results:
            return

        google_frame = ttk.Frame(parent)
        google_frame.pack(fill=tk.X, padx=10, pady=10)

        # Create card-like appearance
        google_card = ttk.Frame(google_frame)
        google_card.pack(fill=tk.X, pady=5)
        google_card.configure(style="Card.TFrame")

        # Card header
        header_frame = ttk.Frame(google_card)
        header_frame.pack(fill=tk.X, padx=15, pady=10)
        header_frame.configure(style="CardHeader.TFrame")

        google_title = ttk.Label(header_frame,
                                 text="Google Search Results",
                                 font=('Helvetica', 14, 'bold'),
                                 foreground=self.colors["accent"],
                                 background=self.colors["card_bg"])
        google_title.pack(anchor=tk.W)

        # Card content
        content_frame = ttk.Frame(google_card)
        content_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        content_frame.configure(style="CardContent.TFrame")

        for i, result in enumerate(google_results):
            result_frame = ttk.Frame(content_frame)
            result_frame.pack(fill=tk.X, pady=5)
            result_frame.configure(style="CardContent.TFrame")

            if "error" in result:
                error_label = ttk.Label(result_frame,
                                        text=f"Error: {result['error']}",
                                        foreground=self.colors["error"],
                                        background=self.colors["card_bg"],
                                        wraplength=600)
                error_label.pack(anchor=tk.W)
            elif "url" in result:
                url_label = ttk.Label(result_frame,
                                      text=f"{i + 1}. ",
                                      foreground=self.colors["fg"],
                                      background=self.colors["card_bg"])
                url_label.pack(side=tk.LEFT)

                hyperlink = ttk.Label(result_frame,
                                      text=result["url"],
                                      foreground=self.colors["accent"],
                                      background=self.colors["card_bg"],
                                      cursor="hand2")
                hyperlink.pack(side=tk.LEFT)
                hyperlink.bind("<Button-1>", lambda e, url=result["url"]: webbrowser.open_new(url))

    def change_theme(self, *args):
        """Change the application theme"""
        self.theme = self.theme_var.get()
        self.colors = THEMES[self.theme]
        self.config["theme"] = self.theme
        save_config(self.config)

        # Restart application to apply theme
        messagebox.showinfo("Theme Changed", "The theme will be applied after restarting the application.")

    def open_settings(self):
        """Open settings dialog"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("500x400")
        settings_window.configure(bg=self.colors["bg"])
        settings_window.transient(self.root)
        settings_window.grab_set()

        # Make window modal
        settings_window.focus_set()

        # Settings content
        settings_frame = ttk.Frame(settings_window)
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        title_label = ttk.Label(settings_frame, text="Settings",
                                font=('Helvetica', 16, 'bold'),
                                foreground=self.colors["fg"],
                                background=self.colors["bg"])
        title_label.pack(anchor=tk.W, pady=(0, 20))

        # Search engines
        engines_frame = ttk.Frame(settings_frame)
        engines_frame.pack(fill=tk.X, pady=10)

        engines_label = ttk.Label(engines_frame, text="Search Engines:",
                                  font=('Helvetica', 12, 'bold'),
                                  foreground=self.colors["fg"],
                                  background=self.colors["bg"])
        engines_label.pack(anchor=tk.W)

        # Google checkbox
        self.google_var = tk.BooleanVar(value="google" in self.config["search_engines"])
        google_check = ttk.Checkbutton(engines_frame, text="Google",
                                       variable=self.google_var)
        google_check.pack(anchor=tk.W, padx=20, pady=5)

        # Wikipedia checkbox
        self.wiki_var = tk.BooleanVar(value="wikipedia" in self.config["search_engines"])
        wiki_check = ttk.Checkbutton(engines_frame, text="Wikipedia",
                                     variable=self.wiki_var)
        wiki_check.pack(anchor=tk.W, padx=20, pady=5)

        # Results count
        count_frame = ttk.Frame(settings_frame)
        count_frame.pack(fill=tk.X, pady=10)

        count_label = ttk.Label(count_frame, text="Number of Results:",
                                font=('Helvetica', 12, 'bold'),
                                foreground=self.colors["fg"],
                                background=self.colors["bg"])
        count_label.pack(anchor=tk.W)

        self.count_var = tk.IntVar(value=self.config["results_count"])
        count_spinbox = ttk.Spinbox(count_frame, from_=1, to=10,
                                    textvariable=self.count_var, width=5)
        count_spinbox.pack(anchor=tk.W, padx=20, pady=5)

        # Auto-correct
        correct_frame = ttk.Frame(settings_frame)
        correct_frame.pack(fill=tk.X, pady=10)

        self.correct_var = tk.BooleanVar(value=self.config["auto_correct"])
        correct_check = ttk.Checkbutton(correct_frame,
                                        text="Enable Grammar Correction",
                                        variable=self.correct_var)
        correct_check.pack(anchor=tk.W)

        # Font size
        font_frame = ttk.Frame(settings_frame)
        font_frame.pack(fill=tk.X, pady=10)

        font_label = ttk.Label(font_frame, text="Font Size:",
                               font=('Helvetica', 12, 'bold'),
                               foreground=self.colors["fg"],
                               background=self.colors["bg"])
        font_label.pack(anchor=tk.W)

        self.font_var = tk.IntVar(value=self.config["font_size"])
        font_spinbox = ttk.Spinbox(font_frame, from_=8, to=16,
                                   textvariable=self.font_var, width=5)
        font_spinbox.pack(anchor=tk.W, padx=20, pady=5)

        # Buttons
        button_frame = ttk.Frame(settings_frame)
        button_frame.pack(fill=tk.X, pady=20)

        save_button = ttk.Button(button_frame, text="Save",
                                 command=lambda: self.save_settings(settings_window))
        save_button.pack(side=tk.RIGHT, padx=5)

        cancel_button = ttk.Button(button_frame, text="Cancel",
                                   command=settings_window.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=5)

    def save_settings(self, window):
        """Save settings and close dialog"""
        # Update search engines
        engines = []
        if self.google_var.get():
            engines.append("google")
        if self.wiki_var.get():
            engines.append("wikipedia")

        if not engines:
            messagebox.showerror("Error", "You must select at least one search engine.")
            return

        self.config["search_engines"] = engines
        self.config["results_count"] = self.count_var.get()
        self.config["auto_correct"] = self.correct_var.get()
        self.config["font_size"] = self.font_var.get()

        save_config(self.config)
        self.assistant.config = self.config

        messagebox.showinfo("Settings Saved",
                            "Settings have been saved. Some changes may require restarting the application.")
        window.destroy()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = SearchAssistantGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
