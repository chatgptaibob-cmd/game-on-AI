# Game On AI

An AI-powered game controller that uses Groq API to process natural language commands and automate tasks in games like Roblox (Blox Fruits).

## Features
- **Natural Language Processing**: Uses Groq (Llama 3) to understand complex commands.
- **Game Automation**: Simulates keyboard and mouse inputs.
- **Roblox Integration**: Specifically tailored for Blox Fruits actions.

## Setup
1. **Groq API Key**: You will be prompted for your Groq API key on the first run. It will be saved in `config.json`.
2. **EXE File**: Run `dist/Game On AI.exe`.
3. **Batch Wrapper**: Alternatively, run `run_game_on_ai.bat`.

## Command Examples
- "open roblox, enter blox fruits"
- "summon besto freindo"
- "accept the highest quest you can"
- "go to the next island if I am high enough level"

## Advanced Usage (Image Recognition)
To make the AI find specific buttons (like the Quest NPC or Quest Select), you can add images to the project folder and use the `find_and_click` function in the source code.

## Disclaimer
Automating games may violate their Terms of Service. Use this tool responsibly.
