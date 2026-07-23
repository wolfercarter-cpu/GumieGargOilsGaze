# Oil State Engine 🛢️

> A sleek terminal utility and developer toolkit for frictionless state management, JSON array manipulation, and gorgeous Charmbracelet/Rich TUI workflows.

---

## 🛠️ The Architecture

The **Oil State Engine** is broken down into modular components designed to make CLI scripting and local state persistence effortless:

* **`core.py`** — The raw state engine handling file persistence, reading, and powerful JSON array mutators (the ultimate `jq` killers).
* **`garg.py`** — A Python wrapper around **Charmbracelet's `gum`**, bringing interactive menus, prompts, and formatted tables to your scripts.
* **`editor.py`** — Powers a Textual-based long-form text editor UI for rich interactive sessions.
* **`cli.py`** — The central Rich-powered command hub linking everything together into a global terminal utility.

---

## 🛢️ Core Engine Verbs (`core.py`)

### 1. Basic State Management
* **`oil_soak(file, data)`**: Dumps variables or data safely into a persistent JSON state file (supports direct data or stdin piping).
* **`oil_spill(file)`**: Reads and returns data out from persistent storage.
* **`oil_spill_table(file)`**: Spills and formats any JSON state file into a gorgeous terminal text table.
* **`oil_rag(file)`**: Completely wipes clean and deletes the state file out of existence when done.

### 2. The Array Mutators (The `jq` Killers)
Instead of writing complex, messy `jq` command pipelines, handle JSON arrays cleanly in Python:
* **`oil_pump(file, record)`**: Appends a brand new record dictionary into a JSON array file.
  * *Equivalent to:* `jq '. += [{"new":"item"}]' state.json > tmp && mv tmp state.json`
* **`oil_skim(file, key, val)`**: Deletes a specific, unwanted record matching `key=value` from your array.
* **`oil_tune(file, match_key, match_val, update_key, update_val)`**: Updates a specific field inside a matching record (e.g., flipping status flags).

---

## 🎨 The Visual CLI Toolkit (`garg.py`)

* **`garg.get_input()`**: Securely asks the user for strings or hidden passwords.
* **`garg.choose()`**: Gives the user a quick, interactive selection list.
* **`garg.table()`**: Instantly turns data sets or CSV files into interactive table views.
* **`garg.log()`**: Prints out clean, timestamped status updates.

---

## 🚀 Global CLI Commands

Once installed, use the global `oil` utility directly in your terminal:

| Command | Arguments | Description |
| :--- | :--- | :--- |
| **`soak`** | `<file>` | Soak up data (or stdin pipe) and save it to persistent storage. |
| **`spill`** | `<file>` | Spill (read) raw data out from persistent storage. |
| **`table`** | `<file>` | Render any JSON state file as a clean, padded text table. |
| **`rag`** | `<file>` | Wipe clean / clear persistent state for the given file. |
| **`pump`** | `<file>` `<json>` | Pump a new record into a JSON array file. |
| **`skim`** | `<file>` `<key>` `<val>` | Skim/remove records matching `key=value` from array. |
| **`tune`** | `<file>` `<m_key>` `<m_val>` `<u_key>` `<u_val>` | Tune/update a field on matching records. |
| **`write`** | — | Launch the interactive Textual long-form text editor UI. |
| **`test`** | — | Launch an interactive menu to run system tests. |

---

## 📦 Quick Start & Testing

Test out the engine directly in your workspace:

```bash
# Add a record to a JSON state file
oil pump watchlist.json '{"ticker": "AAPL", "status": "active"}'

# View it as a formatted table
oil table watchlist.json

# Clean up state when finished
oil rag watchlist.json

