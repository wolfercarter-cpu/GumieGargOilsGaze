# stress test
from oil_pkg import garg
import os

def run_stress_test():
    print("=== GARGOIL STRESS TEST ===\n")

    # 1. Test Confirm
    ready = garg.confirm("Ready to test the remaining commands?")
    if not ready:
        print("Test aborted. Maybe later!")
        return

    # 2. Test Filter
    print("\n--- Testing Filter ---")
    options = ["Neovim", "Ghostty", "Zellij", "Docker", "Textual", "Gum", "Python"]
    tech = garg.filter_options(options, prompt="Search> ")
    print(f"You filtered down to: {tech}")

    # 3. Test Write (Multiline input)
    print("\n--- Testing Write ---")
    notes = garg.write(placeholder="Write a quick sentence...", header="Multiline Input Test", height=6)
    print(f"You wrote:\n{notes}")

    # 4. Test Join
    print("\n--- Testing Join ---")
    box1 = garg.style(" Left Box ", border="rounded", foreground="212", padding="1 2")
    box2 = garg.style(" Right Box ", border="thick", foreground="082", padding="1 2")
    joined = garg.join(box1, box2, horizontal=True, align="center")
    print(joined)

    # 5. Test Format (Markdown rendering)
    print("\n--- Testing Format (Markdown) ---")
    md_text = "# Markdown Test\nThis text is **bold**, this is *italic*, and this is `code`."
    formatted = garg.format_text(md_text, fmt_type="markdown")
    print(formatted)

    # 6. Test File Picker
    print("\n--- Testing File Picker ---")
    picked_file = garg.file_picker(path=".")
    print(f"You selected: {picked_file}")

    # 7. Setup Dummy Files for Table and Pager
    csv_path = "dummy_test.csv"
    with open(csv_path, "w") as f:
        f.write("Name,Tool,Role\nOil,Python,Backend\nGum,Go,Frontend\nZellij,Rust,Multiplexer")
    
    pager_path = "dummy_pager.txt"
    with open(pager_path, "w") as f:
        f.write("GARGOIL PAGER TEST\n\n" + ("Keep scrolling down...\n" * 40) + "You made it to the bottom!")

    # 8. Test Table
    print("\n--- Testing Table ---")
    input("Press Enter to open the Table view (press 'q' or 'ESC' to exit table)...")
    garg.table(csv_path)

    # 9. Test Pager
    print("\n--- Testing Pager ---")
    input("\nPress Enter to open the Pager view (press 'q' to exit pager)...")
    garg.pager(file_path=pager_path)

    # Cleanup temporary files
    os.remove(csv_path)
    os.remove(pager_path)
    print("\n=== ALL TESTS COMPLETE ===")

if __name__ == "__main__":
    run_stress_test()
