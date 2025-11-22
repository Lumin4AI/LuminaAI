# PRIVATE.AI - OpenRouter Edition (v3.1.2-STABLE)

A lightweight, aesthetically pleasing terminal-based AI client designed for the "Unix Porn" enthusiast. This tool interfaces with OpenRouter to provide streaming chat capabilities with context memory, wrapped in a beautiful `rich` TUI.

## 🖥️ Preview

> **Theme:** Cyan & Magenta (Cyberpunk/Unix)  
> **Default Model:** Grok 4.1 (Free Tier via OpenRouter)

## ✨ Features

* **Rich TUI:** Utilizes the `rich` library for beautiful panels, tables, and formatted text.
* **Real-time Streaming:** Features a transient spinner for connection handling and smooth, typewriter-style text streaming for responses.
* **Session Memory:** Maintains conversation context throughout the session.
* **Auto-Auth:** Automatically looks for environment variables but falls back to a secure password prompt if the key is missing.
* **Slash Commands:** Built-in shortcuts for clearing screens, resetting memory, or exiting.

## 🛠️ Prerequisites

* Python 3.8+
* An [OpenRouter](https://openrouter.ai/) API Key.

## 📦 Installation

1.  **Clone or Save the script:**
    Save the python file as `private_ai.py`.

2.  **Install Dependencies:**
    This project relies on `openai` for API communication and `rich` for the interface.
    ```bash
    pip install openai rich
    ```

3.  **Set up API Key (Optional but Recommended):**
    You can set your API key as an environment variable to skip the manual entry at startup.
    
    *Linux/macOS:*
    ```bash
    export OPENROUTER_API_KEY="sk-or-v1-..."
    ```
    
    *Windows (PowerShell):*
    ```powershell
    $env:OPENROUTER_API_KEY="sk-or-v1-..."
    ```

## 🚀 Usage

Run the script directly from your terminal:

```bash
python3 private_ai.py
