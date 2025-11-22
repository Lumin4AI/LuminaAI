#!/usr/bin/env python3
"""
PRIVATE.AI - OpenRouter Edition (Fixed Streaming)
Author: PRIVATE.AI Architect
Version: 3.1.2-STABLE
"""

import os
import sys
import time
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.prompt import Prompt
from rich.progress import SpinnerColumn, Progress, TextColumn
from rich import box

# --- Configuration ---
REAL_MODEL_NAME = "x-ai/grok-4.1-fast:free"
DISPLAY_MODEL_NAME = "GROK 4.1"
API_KEY_ENV_VAR = "OPENROUTER_API_KEY"
BASE_URL = "https://openrouter.ai/api/v1"

# --- Unix Porn Theme ---
THEME_COLOR = "cyan"
ACCENT_COLOR = "magenta"
ERROR_COLOR = "red"
SYSTEM_COLOR = "green"

console = Console()

class PrivateAISession:
    def __init__(self):
        self.history = []
        self.api_key = self._get_api_key()
        self._setup_ai()
        
    def _get_api_key(self):
        key = os.getenv(API_KEY_ENV_VAR)
        if not key:
            console.print(Panel("WARNING: OPENROUTER_API_KEY not found.", 
                                title="[bold red]System Alert[/]", border_style="red"))
            key = Prompt.ask(f"[{ACCENT_COLOR}]Enter OpenRouter Key[/]", password=True)
            if not key:
                sys.exit(1)
        return key

    def _setup_ai(self):
        try:
            self.client = OpenAI(base_url=BASE_URL, api_key=self.api_key)
        except Exception as e:
            console.print(f"[{ERROR_COLOR}]Init Error: {e}[/]")
            sys.exit(1)

    def append_user_message(self, message):
        self.history.append({"role": "user", "content": message})

    def append_ai_message(self, message):
        self.history.append({"role": "assistant", "content": message})
        
    def clear_memory(self):
        self.history = []
        console.print(f"[{SYSTEM_COLOR}]>> MEMORY PURGED.[/]")

def print_banner():
    banner_text = """
 /$$                               /$$                          /$$$$$$  /$$$$$$
| $$                              |__/                         /$$__  $$|_  $$_/
| $$       /$$   /$$ /$$$$$$/$$$$  /$$ /$$$$$$$   /$$$$$$     | $$  \ $$  | $$  
| $$      | $$  | $$| $$_  $$_  $$| $$| $$__  $$ |____  $$    | $$$$$$$$  | $$  
| $$      | $$  | $$| $$ \ $$ \ $$| $$| $$  \ $$  /$$$$$$$    | $$__  $$  | $$  
| $$      | $$  | $$| $$ | $$ | $$| $$| $$  | $$ /$$__  $$    | $$  | $$  | $$  
| $$$$$$$$|  $$$$$$/| $$ | $$ | $$| $$| $$  | $$|  $$$$$$$ /$$| $$  | $$ /$$$$$$
|________/ \______/ |__/ |__/ |__/|__/|__/  |__/ \_______/|__/|__/  |__/|______/
                                                                                
                                                                                
                                                                                
    """
    
    info_table = Table(show_header=False, box=box.SIMPLE, border_style=THEME_COLOR)
    info_table.add_column("Key", style=f"bold {THEME_COLOR}")
    info_table.add_column("Value", style="white")
    info_table.add_row("GATEWAY", "OPENROUTER")
    info_table.add_row("STATUS", "CONNECTED")
    
    panel = Panel(
        Text(banner_text, style=f"bold {THEME_COLOR}", justify="center"),
        subtitle=f"[bold {ACCENT_COLOR}]v1.0.0[/]",
        border_style=THEME_COLOR,
    )
    console.print(panel)
    console.print(info_table, justify="center")
    console.print(f"\n[{SYSTEM_COLOR}]>> SYSTEM READY.[/]\n")

def stream_response(session, user_input):
    """Streams response handling cursor carefully."""
    
    stream = None
    
    # Phase 1: Show Spinner ONLY while waiting for connection
    # We use transient=True so it vanishes completely when done
    with Progress(
        SpinnerColumn(spinner_name="dots12", style=ACCENT_COLOR),
        TextColumn("[bold cyan]Routing...[/]"),
        transient=True, 
    ) as progress:
        progress.add_task("connect", total=None)
        try:
            stream = session.client.chat.completions.create(
                model=REAL_MODEL_NAME,
                messages=session.history,
                stream=True,
            )
        except Exception as e:
            console.print(f"\n[{ERROR_COLOR}]>> CONNECTION ERROR: {e}[/]")
            return

    # Phase 2: Spinner is gone. Now we print clean text.
    if stream:
        full_response = ""
        console.print(f"[bold {ACCENT_COLOR}]PRIVATE.AI >[/] ", end="")
        
        try:
            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    # sys.stdout.write allows adding to the same line perfectly
                    sys.stdout.write(content)
                    sys.stdout.flush()
                    full_response += content
            
            session.append_ai_message(full_response)
            sys.stdout.write("\n") # Final newline
            sys.stdout.flush()
            
        except Exception as e:
            console.print(f"\n[{ERROR_COLOR}]>> STREAM INTERRUPTION: {e}[/]")

def main():
    session = PrivateAISession()
    console.clear()
    print_banner()

    while True:
        try:
            user_input = Prompt.ask(f"[bold white]USER[/]")
            
            if user_input.lower() in ['exit', '/q']:
                console.print(f"[{SYSTEM_COLOR}]>> DISCONNECTING.[/]")
                break
            if user_input.lower() in ['clear', '/c']:
                console.clear()
                print_banner()
                continue
            if user_input.lower() in ['reset', '/r']:
                session.clear_memory()
                continue
            if not user_input.strip():
                continue

            session.append_user_message(user_input)
            stream_response(session, user_input)
            console.print(f"[{THEME_COLOR}]{'─' * console.width}[/]")

        except KeyboardInterrupt:
            console.print(f"\n[{SYSTEM_COLOR}]>> SHUTDOWN.[/]")
            break
        except Exception as e:
            console.print(f"[{ERROR_COLOR}]ERROR: {e}[/]")
            break

if __name__ == "__main__":
    main()
