#!/usr/bin/env python3
import sys
import subprocess
from datetime import datetime

# Importing your global GumieGargoil toolkit
from oil_pkg import garg
from oil_pkg.core import oil_pump, oil_spill, oil_skim, oil_rag

STATE_FILE = "commands.json"

def add_batch_macros(batch_string: str):
    """Parses a batch string and pumps multiple separate commands into the state file."""
    blocks = batch_string.split('\\')
    
    added_count = 0
    for block in blocks:
        block = block.strip()
        if not block:
            continue
            
        lower_block = block.lower()
        if "alias:" in lower_block and "command:" in lower_block:
            alias_start = lower_block.find("alias:") + len("alias:")
            command_start = lower_block.find("command:")
            
            title = block[alias_start:command_start].strip()
            executable = block[command_start + len("command:"):].strip()
            
            macro_data = {
                "title": title,
                "executable": executable,
                "added_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            oil_pump(STATE_FILE, macro_data)
            added_count += 1
            garg.log(f"Pumped: '{title}' -> [ {executable} ]", level="info")
        else:
            garg.log(f"Skipped invalid block (missing alias/command): {block}", level="warn")
            
    garg.log(f"Successfully added {added_count} new macros to {STATE_FILE}!", level="info")

def run_menu():
    """Spills the state file, renders the UI, and executes the choice."""
    saved_macros = oil_spill(STATE_FILE)
    
    if not saved_macros or not isinstance(saved_macros, list):
        garg.log("No commands saved yet! Use 'col add ...' to add some.", level="warn")
        sys.exit(0)

    options_map = {
        f"{macro['title']}  —  [ {macro['executable']} ]": macro['executable']
        for macro in saved_macros
    }
    
    display_options = list(options_map.keys())

    selected_choice = garg.choose(
        prompt="Select a macro to execute:", 
        options=display_options
    )

    if selected_choice:
        choice_str = selected_choice[0] if isinstance(selected_choice, list) else selected_choice
        command_to_run = options_map.get(choice_str)
        
        if command_to_run:
            garg.log(f"Executing: {command_to_run}", level="info")
            subprocess.run(command_to_run, shell=True)
        else:
            garg.log("Error finding the command to run.", level="error")
    else:
        garg.log("No macro selected. Exiting.", level="warn")

def remove_macro():
    """Interactively select a macro to delete using oil_skim."""
    saved_macros = oil_spill(STATE_FILE)
    
    if not saved_macros or not isinstance(saved_macros, list):
        garg.log("No commands saved to delete.", level="warn")
        return

    options_map = {
        f"{macro['title']}  —  [ {macro['executable']} ]": macro['title']
        for macro in saved_macros
    }
    
    display_options = list(options_map.keys())
    display_options.append("Cancel")

    selected_choice = garg.choose(
        prompt="Select a macro to DELETE (or Cancel):", 
        options=display_options
    )

    if selected_choice:
        choice_str = selected_choice[0] if isinstance(selected_choice, list) else selected_choice
        
        if choice_str == "Cancel":
            garg.log("Deletion cancelled.", level="info")
            return
            
        title_to_remove = options_map.get(choice_str)
        
        if title_to_remove:
            oil_skim(STATE_FILE, "title", title_to_remove)
            garg.log(f"Successfully skimmed '{title_to_remove}' from {STATE_FILE}!", level="info")

def clear_macros():
    """Wipes the entire commands.json state file using oil_rag."""
    success = oil_rag(STATE_FILE)
    if success:
        garg.log(f"Successfully cleared all macros from {STATE_FILE}!", level="info")
    else:
        garg.log("No commands file found to clear.", level="warn")

def show_help():
    """Prints a clean syntax guide for The Colonel."""
    help_text = """
============================================================
 🎖️  THE COLONEL (col) - Persistent Command Macro Runner 🎖️
============================================================

Usage / Syntax Hints:

1. Run the Interactive Menu
   Command:  col
   Details:  Spills 'commands.json' and opens the Garg UI to execute macros.

2. Add Batch Macros
   Command:  col add "alias: update command: apt update \\ alias: upgrade command: apt upgrade -y"
   Details:  Pumps alias/command pairs separated by a backslash (\\) into your state file.

3. Remove an Individual Macro
   Command:  col rm (or remove, delete)
   Details:  Opens an interactive menu to delete a specific macro.

4. Clear the Entire List
   Command:  col clear (or reset, rag)
   Details:  Wipes the entire commands.json database clean using oil_rag.

5. Show this Help Menu
   Command:  col help (or -h, --help)
============================================================
"""
    print(help_text)

def main():
    args = sys.argv[1:]
    
    if len(args) == 0:
        run_menu()
        return

    command = args[0].lower()

    if command in ["help", "-h", "--help"]:
        show_help()
    elif command == "add":
        batch_string = " ".join(args[1:])
        if batch_string.strip():
            add_batch_macros(batch_string)
        else:
            garg.log("You must provide an alias and command string. See 'col help'.", level="warn")
    elif command in ["remove", "rm", "delete"]:
        remove_macro()
    elif command in ["clear", "reset", "rag"]:
        clear_macros()
    else:
        garg.log(f"Unknown command '{command}'.", level="error")
        show_help()

if __name__ == "__main__":
    main()
