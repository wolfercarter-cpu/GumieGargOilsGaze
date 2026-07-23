# test_garg
from oil_pkg import garg
import time

def run_test():
    # 1. Test Styling & Logging
    garg.log("Starting Gargoil test sequence...", level="info")
    title = garg.style(" GARGOIL TEST SUITE ", foreground="212", border="thick", bold=True)
    print(f"\n{title}\n")

    # 2. Test Input
    name = garg.get_input(prompt="What is your name? ", placeholder="Enter name here...")
    
    # 3. Test Choose
    print("\nWhich feature are you most excited about?")
    options = ["Modularity", "Speed", "No Bash Boilerplate", "Looks Cool"]
    choice = garg.choose(options=options)
    
    # 4. Test Spinner (Simulating some backend work)
    print("\nProcessing your answers...")
    # We pass a simple sleep command to the spinner
    garg.spin(["sleep", "3"], spinner="minidot", text="Initializing core engine...")

    # 5. Output Results
    print(f"\nAwesome to meet you, {name}!")
    if choice:
        print(f"I agree, '{choice[0]}' is definitely the best part.")
    else:
        print("You didn't pick anything!")

if __name__ == "__main__":
    run_test()
