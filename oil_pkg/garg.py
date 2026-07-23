"""
garg.py - The Python wrapper for Gum, designed for the Oil ecosystem.
Provides a set of utilities for building command-line interfaces.
"""

import subprocess
import sys

# ==========================================
# Original Prompt & Selection Commands
# ==========================================

def choose(prompt: str = None, options: list = None, limit: int = 1) -> list:
    """Choose an option from a list of choices.

    Args:
        prompt (str): The question to ask the user (optional). Defaults to None.
        options (list): A list of choices to present to the user. Defaults to None.
        limit (int, optional): How many choices can be selected. Defaults to 1.

    Returns:
        list: A list of the user's choices.
    """
    command = ["gum", "choose"]
    if prompt:
        print(prompt)
    if limit > 1:
        command.append(f"--limit={limit}")
    if options:
        command += options
    
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True, check=False)
    if result.returncode != 0:
        return []
    # Strip whitespace and split by newline in case of multiple selections
    return [choice for choice in result.stdout.strip().split("\n") if choice]


def confirm(prompt: str = None) -> bool:
    """Confirm a user's choice.

    Args:
        prompt (str, optional): Prompt you would like to display to user. 

    Returns:
        bool: True if user confirms, False otherwise.
    """
    command = ["gum", "confirm"]
    if prompt:
        command.append(prompt)
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True, check=False)
    return result.returncode == 0


def get_input(prompt: str = None, placeholder: str = None) -> str:
    """Prompt the user for input.

    Args:
        prompt (str, optional): Prompt you would like to display to user. 
        placeholder (str, optional): Placeholder text for the input. 

    Returns:
        str: User's input.
    """
    command = ["gum", "input"]
    if prompt:
        command.append(f"--prompt={prompt}")
    if placeholder:
        command.append(f"--placeholder={placeholder}")

    result = subprocess.run(command, stdout=subprocess.PIPE, text=True, check=False)
    return result.stdout.strip()


def spin(command: list, show_output: bool = False, spinner: str = None, text: str = None) -> None:
    """Display a spinner while running a script/command.

    Args:
        command (list): Command to execute while spinning (e.g., ["sleep", "5"]).
        show_output (bool, optional): Show or pipe output of command. Defaults to False.
        spinner (str, optional): Style of the spinner (line, dot, minidot, etc.).
        text (str, optional): Text to display while spinning.
    """
    cmd = ["gum", "spin"]
    if text:
        cmd.append(f"--title={text}")
    if spinner:
        cmd.append(f"--spinner={spinner}")
    if show_output:
        cmd.append("--show-output")
        
    cmd.append("--")
    cmd.extend(command)
    
    result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True, check=False)
    if show_output and result.stdout:
        print(result.stdout)


def log(text: str, level: str = "info", time_format: str = None) -> None:
    """Log a message.

    Args:
        text (str): Text to log.
        level (str, optional): Log level (none, debug, info, warn, error, fatal).
        time_format (str, optional): Time format to use.
    """
    command = ["gum", "log"]
    if level:
        command.append(f"--level={level}")
    if time_format:
        command.append(f"--time={time_format}")
    command.append(text)
    
    subprocess.run(command, stdout=subprocess.PIPE, text=True, check=False)


# ==========================================
# New Commands Added for garg.py
# ==========================================

def filter_options(options: list, placeholder: str = "Filter...", prompt: str = "> ") -> str:
    """Filter through a list of items dynamically.

    Args:
        options (list): A list of items to filter through.
        placeholder (str, optional): Text displayed when no input is entered.
        prompt (str, optional): The prompt indicator.

    Returns:
        str: The selected item from the filter.
    """
    command = ["gum", "filter", f"--placeholder={placeholder}", f"--prompt={prompt}"]
    # Passing options via standard input handles huge lists better than command line arguments
    result = subprocess.run(command, input="\n".join(options), stdout=subprocess.PIPE, text=True, check=False)
    return result.stdout.strip()


def write(placeholder: str = "Write something...", header: str = "", width: int = 0, height: int = 0) -> str:
    """Open a multi-line text editor.

    Args:
        placeholder (str, optional): Placeholder text.
        header (str, optional): Header text above the text box.
        width (int, optional): Width of the text box.
        height (int, optional): Height of the text box.

    Returns:
        str: The multi-line text entered by the user.
    """
    command = ["gum", "write", f"--placeholder={placeholder}"]
    if header:
        command.append(f"--header={header}")
    if width:
        command.append(f"--width={width}")
    if height:
        command.append(f"--height={height}")

    result = subprocess.run(command, stdout=subprocess.PIPE, text=True, check=False)
    return result.stdout.strip()


def file_picker(path: str = ".", directory: bool = False, show_hidden: bool = False) -> str:
    """Interactively pick a file or folder from the directory tree.

    Args:
        path (str, optional): Starting path. Defaults to current directory (".").
        directory (bool, optional): If True, allows selecting directories instead of files.
        show_hidden (bool, optional): If True, shows hidden files/folders.

    Returns:
        str: The path to the selected file or directory.
    """
    command = ["gum", "file", path]
    if directory:
        command.append("--directory")
    if show_hidden:
        command.append("--all")

    result = subprocess.run(command, stdout=subprocess.PIPE, text=True, check=False)
    return result.stdout.strip()


def style(text: str, foreground: str = None, background: str = None, border: str = None, bold: bool = False, padding: str = None, margin: str = None) -> str:
    """Apply styling, coloring, and borders to a block of text.

    Args:
        text (str): The text to style.
        foreground (str, optional): Foreground color (hex code or 0-255).
        background (str, optional): Background color (hex code or 0-255).
        border (str, optional): Border style (normal, rounded, thick, double).
        bold (bool, optional): Make text bold.
        padding (str, optional): Padding inside the border (e.g., "1 2").
        margin (str, optional): Margin outside the border (e.g., "1 2").

    Returns:
        str: The stylized string (contains ANSI escape codes).
    """
    command = ["gum", "style"]
    if foreground:
        command.append(f"--foreground={foreground}")
    if background:
        command.append(f"--background={background}")
    if border:
        command.append(f"--border={border}")
    if padding:
        command.append(f"--padding={padding}")
    if margin:
        command.append(f"--margin={margin}")
    if bold:
        command.append("--bold")
        
    command.append(text)
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True, check=False)
    return result.stdout


def join(*texts: str, horizontal: bool = False, align: str = "left") -> str:
    """Join multiple text blocks vertically or horizontally.

    Args:
        texts (str): Multiple string arguments to join together.
        horizontal (bool, optional): Join blocks side-by-side if True. Defaults to vertical.
        align (str, optional): Alignment (left, center, right, bottom, middle, top).

    Returns:
        str: The combined block of text.
    """
    command = ["gum", "join", f"--align={align}"]
    if horizontal:
        command.append("--horizontal")
    else:
        command.append("--vertical")
        
    command.extend(texts)
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True, check=False)
    return result.stdout


def format_text(text: str, fmt_type: str = "markdown") -> str:
    """Format text (useful for rendering Markdown code blocks or emojis in terminal).

    Args:
        text (str): The text/markdown to format.
        fmt_type (str, optional): Type of formatting (markdown, template, code, emoji).

    Returns:
        str: Formatted terminal text.
    """
    command = ["gum", "format", f"--type={fmt_type}"]
    # Using stdin so massive strings (like entire markdown files) don't break arg length limits
    result = subprocess.run(command, input=text, stdout=subprocess.PIPE, text=True, check=False)
    return result.stdout


def pager(text: str = None, file_path: str = None) -> None:
    """Scroll through long text or a file using a pager (like 'less').

    Args:
        text (str, optional): The string text to paginate.
        file_path (str, optional): A file path to read and paginate instead.
    """
    command = ["gum", "pager"]
    
    if file_path:
        with open(file_path, 'r') as f:
            text = f.read()

    subprocess.run(command, input=text, stdout=sys.stdout, text=True, check=False)


def table(csv_file: str) -> None:
    """Render a CSV file as an interactive table.

    Args:
        csv_file (str): The path to the CSV file to display.
    """
    command = ["gum", "table", f"--file={csv_file}"]
    subprocess.run(command, stdout=sys.stdout, text=True, check=False)
