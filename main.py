import os
import json
import time
import sys
import webbrowser
import pyautogui
import pydirectinput
import cv2
import numpy as np
from groq import Groq
import keyboard
import subprocess

# Optional voice support
try:
    import speech_recognition as sr
    VOICE_SUPPORT = True
except ImportError:
    VOICE_SUPPORT = False

# Configuration
CONFIG_FILE = "config.json"
SUPPORTED_MODEL = "openai/gpt-oss-20b"

# Screen size for scaling coordinates
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

def get_coords(x_percent, y_percent):
    return int(SCREEN_WIDTH * x_percent / 100), int(SCREEN_HEIGHT * y_percent / 100)

def load_config():
    if not os.path.exists(CONFIG_FILE):
        api_key = input("Enter your Groq API Key: ")
        config = {"groq_api_key": api_key}
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f)
        return config
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

config = load_config()
client = Groq(api_key=config["groq_api_key"])

# Action Mappings
def find_and_click(image_path, confidence=0.8):
    try:
        location = pyautogui.locateOnScreen(image_path, confidence=confidence)
        if location:
            center = pyautogui.center(location)
            pyautogui.click(center)
            return True
    except Exception as e:
        print(f"Error finding {image_path}: {e}")
    return False

def open_roblox():
    print("Opening Roblox...")
    webbrowser.open("https://www.roblox.com/home")
    time.sleep(5)

def open_application(app_name):
    print(f"Opening application: {app_name}...")
    try:
        # Try to open via start command
        subprocess.run(f"start {app_name}", shell=True, check=True)
    except Exception as e:
        # Fallback to searching in common paths or using shell execute
        print(f"Failed to open {app_name} directly. Trying shell execute...")
        try:
            os.startfile(app_name)
        except:
            print(f"Could not open {app_name}. Please ensure it is installed and in your PATH.")

def enter_game(game_name):
    print(f"Searching for {game_name}...")
    # Scaling: Search bar is roughly at 40% width, 10% height
    search_x, search_y = get_coords(40, 10)
    pyautogui.click(search_x, search_y)
    time.sleep(1)
    pyautogui.write(game_name)
    pyautogui.press("enter")
    time.sleep(3)
    # First result roughly at 40% width, 30% height
    res_x, res_y = get_coords(40, 30)
    pyautogui.click(res_x, res_y)
    time.sleep(2)
    # Play button roughly at 80% width, 50% height
    play_x, play_y = get_coords(80, 50)
    pyautogui.click(play_x, play_y)

def summon_besto_freindo():
    print("Summoning Besto Freindo...")
    pydirectinput.press('v') 
    time.sleep(1)

def accept_highest_quest():
    print("Accepting highest quest...")
    pydirectinput.press('e')
    time.sleep(1)
    # Quest select roughly middle-bottom
    q_x, q_y = get_coords(50, 60)
    pyautogui.click(q_x, q_y)
    time.sleep(0.5)
    # Confirm roughly middle-lower-bottom
    c_x, c_y = get_coords(50, 70)
    pyautogui.click(c_x, c_y)

def check_level_and_move():
    print("Checking level and island requirements...")
    # Placeholder for OCR logic
    pass

def listen_for_voice():
    if not VOICE_SUPPORT:
        print("Voice support is not available (pyaudio missing).")
        return None
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        audio = r.listen(source, timeout=5)
    try:
        command = r.recognize_google(audio)
        print(f"You said: {command}")
        return command
    except Exception as e:
        print(f"Could not recognize voice: {e}")
        return None

def process_command(user_input):
    prompt = f"""
    You are an AI computer and game controller. 
    Convert the following user command into a list of executable actions.
    User command: "{user_input}"
    
    Available actions:
    - open_roblox()
    - open_application(app_name)
    - enter_game(name)
    - summon_besto_freindo()
    - accept_highest_quest()
    - check_level_and_move()
    
    Return a JSON object with a key "actions" containing a list of objects with "action" and "params".
    Example: {{"actions": [{{"action": "open_application", "params": {{"app_name": "brave"}}}}]}}
    """
    
    try:
        completion = client.chat.completions.create(
            model=SUPPORTED_MODEL,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        response = json.loads(completion.choices[0].message.content)
        return response.get("actions", [])
    except Exception as e:
        print(f"Error processing command with AI: {e}")
        return []

def execute_actions(actions):
    for action_data in actions:
        action = action_data.get("action")
        params = action_data.get("params", {})
        
        if action == "open_roblox":
            open_roblox()
        elif action == "open_application":
            open_application(params.get("app_name"))
        elif action == "enter_game":
            enter_game(params.get("name", "Blox Fruits"))
        elif action == "summon_besto_freindo":
            summon_besto_freindo()
        elif action == "accept_highest_quest":
            accept_highest_quest()
        elif action == "check_level_and_move":
            check_level_and_move()
        
        time.sleep(1)

def main():
    print("=== Game On AI ===")
    print(f"Screen Resolution: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
    print(f"Voice Support: {'Enabled' if VOICE_SUPPORT else 'Disabled (pyaudio missing)'}")
    print("Press 'q' to quit, 'v' for voice command, or type your command.")
    
    while True:
        if keyboard.is_pressed('q'):
            print("Quitting...")
            break
            
        if VOICE_SUPPORT and keyboard.is_pressed('v'):
            user_input = listen_for_voice()
        else:
            # Check if user wants to type
            user_input = input("Command (type or press 'v' for voice): ")
        
        if not user_input:
            time.sleep(0.1)
            continue
            
        actions = process_command(user_input)
        if actions:
            print(f"Executing {len(actions)} actions...")
            execute_actions(actions)
        else:
            print("No valid actions found for that command.")

if __name__ == "__main__":
    main()
