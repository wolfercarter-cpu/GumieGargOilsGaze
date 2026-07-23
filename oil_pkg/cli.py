import sys
import json
from typing import Optional
from rich import print
from rich.panel import Panel
from rich.table import Table
from oil_pkg.core import (
    oil_soak, oil_spill, oil_rag, get_piped_data, 
    oil_pump, oil_skim, oil_tune, oil_spill_table
)
from oil_pkg.editor import launch_editor
from oil_pkg import garg
from oil_pkg.tests import stress_test, test_garg

def show_help():
    title = "[bold magenta]Oil State Engine[/] [dim]v0.1.0[/]"
    description = "A slick terminal utility for state management and script workflows."
    
    table = Table(show_header=True, header_style="bold cyan", box=None, padding=(0, 2))
    table.add_column("Command", style="bold green")
    table.add_column("Arguments", style="yellow")
    table.add_column("Description", style="white")

    table.add_row("soak", "<file> [data]", "Soak up data (or stdin pipe) and save it to persistent storage.")
    table.add_row("spill", "<file>", "Spill (read) data out from persistent storage.")
    table.add_row("rag", "<file>", "Wipe clean / clear persistent state for the given file.")
    table.add_row("pump", "<file> <json>", "Pump a new record into a JSON array file.")
    table.add_row("skim", "<file> <key> <val>", "Skim/remove records matching key=value from array.")
    table.add_row("tune", "<file> <m_key> <m_val> <u_key> <u_val>", "Tune/update a field on matching records.")
    table.add_row("write", "[output_file]", "Launch the interactive Textual long-form text editor UI.")
    table.add_row("table", "<file>", "Spill and render any JSON state file as a clean text table.")
    table.add_row("test", "", "Launch an interactive menu to run system tests.")

    print(Panel.fit(table, title=title, subtitle=description, border_style="magenta"))
    print("\n[dim]Usage:[/] [bold]oil <command> [arguments][/]\n")



def handle_test_command():
    """Interactive menu for the 'oil test' command."""
    options = [
        "stress_test.py (Interactive Visual Demo)",
        "test_garg.py (Silent Unit Tests)",
        "Cancel"
    ]
    
    selected = garg.choose(options=options)
    
    if not selected:
        sys.exit(0)
        
    # Route based on the user's enter press
    if "stress_test.py" in selected[0]:
        print("Launching stress test...")
        stress_test.run_stress_test() 
        
    elif "test_garg.py" in selected[0]:
        print("Launching unit tests...")
        test_garg.run_test() 
        
    else:
        print("Test menu cancelled.")
        sys.exit(0)

def main():
    if len(sys.argv) < 2:
        show_help()
        sys.exit(0)

    command = sys.argv[1].lower()
    args = sys.argv[2:]

    if command in ("--help", "-h", "help"):
        show_help()
        sys.exit(0)

    if command == "soak":
        if not args:
            print("[bold red]Error:[/] 'soak' requires a file path.")
            sys.exit(1)
        file_path = args[0]
        data = args[1] if len(args) > 1 else None
        if data is None:
            piped_lines = get_piped_data()
            data = "\n".join(piped_lines) if piped_lines else ""
        oil_soak(file_path, {"cli_input": data})
        print(f"[green]Successfully soaked data into[/] [cyan]{file_path}[/]")

    elif command == "spill":
        if not args:
            print("[bold red]Error:[/] 'spill' requires a file path.")
            sys.exit(1)
        result = oil_spill(args[0])
        print(result)

    elif command == "table":
        if not args:
            print("[bold red]Error:[/] 'table' requires a file path.")
            sys.exit(1)
        file_path = args[0]
        output = oil_spill_table(file_path)
        print(output)

    elif command == "rag":
        if not args:
            print("[bold red]Error:[/] 'rag' requires a file path.")
            sys.exit(1)
        file_path = args[0]
        success = oil_rag(file_path)
        if success:
            print(f"[yellow]Wiped clean:[/] [cyan]{file_path}[/]")
        else:
            print(f"[dim]Nothing to wipe:[/] [cyan]{file_path}[/] does not exist.")

    elif command == "write":
        output_file = args[0] if args else "untitled.py"
        launch_editor(output_file)
        print(f"[green]Finished writing to[/] [cyan]{output_file}[/]")

    elif command == "pump":
        if len(args) < 2:
            print("[bold red]Error:[/] 'pump' requires a file path and a JSON dictionary string.")
            sys.exit(1)
        file_path = args[0]
        try:
            new_item = json.loads(args[1])
        except json.JSONDecodeError:
            print("[bold red]Error:[/] The item to pump must be valid JSON (e.g., '{\"alias\": \"P920\"}')")
            sys.exit(1)
        
        oil_pump(file_path, new_item)
        print(f"[green]Successfully pumped record into[/] [cyan]{file_path}[/]")

    elif command == "skim":
        if len(args) < 3:
            print("[bold red]Error:[/] 'skim' requires a file path, key, and value.")
            sys.exit(1)
        file_path, key, value = args[0], args[1], args[2]
        oil_skim(file_path, key, value)
        print(f"[yellow]Skimmed records matching {key}={value} from[/] [cyan]{file_path}[/]")

    elif command == "tune":
        if len(args) < 5:
            print("[bold red]Error:[/] 'tune' requires: <file> <match_key> <match_val> <update_key> <update_val>")
            sys.exit(1)
        file_path, m_key, m_val, u_key, u_val = args[0], args[1], args[2], args[3], args[4]
        oil_tune(file_path, m_key, m_val, u_key, u_val)
        print(f"[magenta]Tuned records in[/] [cyan]{file_path}[/] where {m_key}={m_val} -> set {u_key}={u_val}")

    elif command == "test":
        handle_test_command()

    else:
        show_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
