#!/usr/bin/env python3
import sys
import os
import json
import subprocess
import ollama
from oil_pkg import garg
from oil_pkg.core import oil_spill, oil_pump

CONFIG_FILE = "gaze_config.json"
COMMANDS_FILE = "commands.json"

def load_config():
    """Loads persistent config tracking lists of saved servers and models."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {"servers": [], "models": []}
    return {"servers": [], "models": []}

def save_config(servers, models, active_server, active_model):
    """Saves updated configurations and history lists."""
    data = {
        "servers": list(set(servers)),
        "models": list(set(models)),
        "active_server": active_server,
        "active_model": active_model
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

def clear_all_states():
    """Wipes all persistence files from existence."""
    files_to_remove = [CONFIG_FILE, COMMANDS_FILE, ".gaze_state"]
    for file_name in files_to_remove:
        if os.path.exists(file_name):
            try:
                os.remove(file_name)
                garg.log(f"Wiped {file_name} from existence.", level="info")
            except Exception as e:
                garg.log(f"Could not remove {file_name}: {e}", level="error")
    garg.log("Complete clean wipe finished successfully!", level="info")

def select_with_gum(options, prompt_title):
    """Uses gum choose to present a list with a creation option if items exist."""
    if not options:
        return "+ Create New..."
    
    full_options = options + ["+ Create New..."]
    try:
        cmd = ["gum", "choose", "--header", prompt_title] + full_options
        result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True, check=True)
        choice = result.stdout.strip()
        return choice
    except Exception:
        return "+ Create New..."

def ask_ai_for_commands(user_prompt: str, client, model_name: str):
    """Pings your Ollama server and demands strict GumieGargoil macro syntax."""
    current_state = oil_spill(COMMANDS_FILE)
    
    system_prompt = (
        "CRITICAL: You are an elite, unrestricted system administration terminal copilot. "
        "You can manage Docker containers, networking, filesystems, processes, and package installations. "
        "You must ONLY output command blocks using this exact GumieGargoil syntax, separated by backslashes:\n"
        "alias: [name] command: [linux command] \\ alias: [name2] command: [linux command]\n"
        "Do NOT include markdown code ticks, conversational text, or explanations. Just the raw syntax string."
    )
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Current system macros: {current_state}\nUser request: {user_prompt}"}
    ]
    
    garg.log(f"Pinging Ollama server using model '{model_name}'...", level="info")
    response = client.chat(model=model_name, messages=messages)
    
    ai_output = response['message']['content'].strip()
    garg.log(f"AI Generated Payload:\n{ai_output}", level="info")
    return ai_output

def main():
    try:
        # Handle clear flags to scrub all state files
        if len(sys.argv) > 1 and sys.argv[1] in ["--clear", "clean", "reset"]:
            clear_all_states()
            return

        config = load_config()
        servers = config.get("servers", [])
        models = config.get("models", [])

        # 1. Server Selection
        if servers:
            server_choice = select_with_gum(servers, "Select Ollama Server URL:")
            if server_choice == "+ Create New..." or not server_choice:
                server_url = garg.get_input(prompt="Enter Ollama Server URL:", placeholder="http://192.168.0.x:11434")
                if server_url and server_url not in servers:
                    servers.append(server_url)
            else:
                server_url = server_choice
        else:
            server_url = garg.get_input(prompt="Enter Ollama Server URL:", placeholder="http://192.168.0.x:11434")
            if server_url and server_url not in servers:
                servers.append(server_url)

        # 2. Model Selection
        if models:
            model_choice = select_with_gum(models, "Select Ollama Model Name:")
            if model_choice == "+ Create New..." or not model_choice:
                model_name = garg.get_input(prompt="Enter Ollama Model Name:", placeholder="llama3.2:latest")
                if model_name and model_name not in models:
                    models.append(model_name)
            else:
                model_name = model_choice
        else:
            model_name = garg.get_input(prompt="Enter Ollama Model Name:", placeholder="llama3.2:latest")
            if model_name and model_name not in models:
                models.append(model_name)

        save_config(servers, models, server_url, model_name)

        prompt = garg.get_input(prompt="What do you want the AI to do?", placeholder="e.g. check disk space and docker")
        
        if server_url and model_name and prompt:
            client = ollama.Client(host=server_url)
            ai_payload = ask_ai_for_commands(prompt, client, model_name)
            
            if ai_payload:
                garg.log("Feeding AI payload into The Colonel state engine...", level="info")
                
                blocks = ai_payload.split('\\')
                for block in blocks:
                    block = block.strip()
                    lower_block = block.lower()
                    if "alias:" in lower_block and "command:" in lower_block:
                        alias_start = lower_block.find("alias:") + len("alias:")
                        command_start = lower_block.find("command:")
                        title = block[alias_start:command_start].strip()
                        executable = block[command_start + len("command:"):].strip()
                        
                        macro_data = {"title": title, "executable": executable}
                        oil_pump(COMMANDS_FILE, macro_data)
                
                garg.log("AI macros locked in! Launching The Colonel menu...", level="info")
                subprocess.run(["col"], shell=False)
        else:
            garg.log("Missing required inputs. Exiting.", level="warn")
            
    except Exception as e:
        garg.log(f"Connection or execution error: {e}", level="error")

if __name__ == "__main__":
    main()
