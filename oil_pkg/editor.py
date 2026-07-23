import sys
from pathlib import Path
from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Label, TextArea, Static
from textual.containers import Vertical
from rich.style import Style
from textual.widgets.text_area import TextAreaTheme

my_theme = TextAreaTheme(
    name="my_cool_theme",
    cursor_style=Style(color="purple", bgcolor="green"),
    cursor_line_style=Style(bgcolor="purple"),
    syntax_styles={
        "string": Style(color="purple"),
        "comment": Style(color="green", italic=True),
        "keyword": Style(color="cyan"),    
        "include": Style(color="cyan"),    
        "operator": Style(color="magenta"),    
        "function": Style(color="yellow"),       
        "variable": Style(color="white"),
        "number": Style(color="#FFA500"),        
    }
)

# We removed the emoji from this base string so we can append it dynamically later
base_shortcut_key_text = (
    "[b purple]Ctrl+C[/] [green]Copy[/]   |  "
    "[b purple]Ctrl+V[/] [green]Paste[/]   |  "
    "[b purple]Ctrl+X[/] [green]Cut[/]\n"
    "[b purple]Ctrl+Z[/] [green]Undo[/]   |  "
    "[b purple]Ctrl+Y[/] [green]Redo[/]   |  "
    "[b purple]F7[/] [green]Select All[/]   |  "
    "[b purple]Ctrl+S[/] [green]Save[/]   |  "
    "[b purple]Ctrl+Q[/] [green]Quit[/]"
)

class EditorApp(App):
    CSS_PATH = "ed.tcss"
    BINDINGS = [
        ("ctrl+q", "quit", "Quit"),
        ("ctrl+s", "save", "Save") 
    ]

    def __init__(self, filename: str):
        super().__init__()
        self.filename = filename

    def compose(self) -> ComposeResult:
        yield Label(f"Oil Write - {self.filename}", id="l1")
        with Vertical(id="v1"):
            yield TextArea.code_editor(language="python")
            
        # Append the red X to the end of your keys on startup
        yield Static(base_shortcut_key_text + "   |  [b]Status:[/] ❌", id="s1")

    def on_mount(self) -> None:
        text_area = self.query_one(TextArea)
        text_area.register_theme(my_theme)
        text_area.theme = "my_cool_theme"

        file_path = Path(self.filename)
        if file_path.is_file():
            text_area.text = file_path.read_text()

    def action_save(self) -> None:
        """Called when the user presses Ctrl+S."""
        text_area = self.query_one(TextArea)
        
        with open(self.filename, "w") as file:
            file.write(text_area.text)
            
        # Grab the static widget by its ID and update it to the green check
        status_bar = self.query_one("#s1", Static)
        status_bar.update(base_shortcut_key_text + "   |  [b]Status:[/] ✅")

    @on(TextArea.Changed)
    def mark_unsaved(self) -> None:
        """Called automatically whenever text is modified."""
        # Flips the status back to a red X the moment you type anything new
        status_bar = self.query_one("#s1", Static)
        status_bar.update(base_shortcut_key_text + "   |  [b]Status:[/] ❌")

def launch_editor(filename: str):
    app = EditorApp(filename=filename)
    app.run()

if __name__ == "__main__":
    target_file = sys.argv[1] if len(sys.argv) > 1 else "untitled.py"
    launch_editor(target_file)
