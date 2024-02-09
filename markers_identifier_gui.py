import tkinter as tk
from tkinter import filedialog

def switch_index(filename, output_file, sampling_rate, feedback_text):
    switch_found = False
    switch_index = None
    markers = {}

    with open(filename, 'r') as file, open(output_file, 'w') as output:
        for idx, line in enumerate(file, start=1):
            columns = line.strip().split()
            if len(columns) >= 11:
                value_in_third_column = float(columns[2])

                # Modify the condition to identify the switch
                if not switch_found and value_in_third_column > 4 and idx > 1:
                    switch_found = True
                    switch_index = idx

                binary_digits = columns[3:11]
                binary_string = ''.join(['1' if digit == '5' else '0' for digit in binary_digits])
                decimal_number = int(binary_string[::-1], 2)

                # Calculate the relative distance from the switch in milliseconds
                if 1 <= decimal_number <= 10 and decimal_number not in markers:
                    time_from_switch = round((idx - switch_index) / sampling_rate * 1000) if switch_found else 0
                    # Write the output to the file as a rounded integer
                    print(f"{decimal_number}\t{time_from_switch}", file=output)
                    markers[decimal_number] = time_from_switch

    if switch_found:
        feedback_text.set(f"LED on found at line {switch_index}, corresponding to {switch_index/sampling_rate*1000:.2f} ms after the onset of the BIOPAC recordings")
    else:
        feedback_text.set("No LED trigger found")

    # Print marker summary
    if markers:
        feedback_text.set(feedback_text.get() + "\nIdentified markers:")
        for marker, time in markers.items():
            feedback_text.set(feedback_text.get() + f"\nMarker {marker}: {time} ms after the LED turned on")

# GUI creation function
def create_gui():
    gui = tk.Tk()
    gui.title("Marker Identification GUI")

    # Function to handle file browsing
    def browse_file():
        filename = filedialog.askopenfilename()
        file_entry.delete(0, tk.END)
        file_entry.insert(0, filename)

    # Function to run the script
    def run_script():
        filename = file_entry.get()
        output_file = output_entry.get()
        sampling_rate = int(sampling_entry.get())
        feedback_text.set("")  # Clear previous feedback
        switch_index(filename, output_file, sampling_rate, feedback_text)
        feedback_text.set(feedback_text.get() + f"\nScript executed. Output file: {output_file}")

    # GUI components
    file_label = tk.Label(gui, text="Input File:")
    file_entry = tk.Entry(gui, width=50)
    browse_button = tk.Button(gui, text="Browse", command=browse_file)

    sampling_label = tk.Label(gui, text="Sampling Frequency (Hz):")
    sampling_entry = tk.Entry(gui)

    output_label = tk.Label(gui, text="Output File:")
    output_entry = tk.Entry(gui, width=50)

    run_button = tk.Button(gui, text="Run Script", command=run_script)

    feedback_text = tk.StringVar()
    feedback_label = tk.Label(gui, textvariable=feedback_text)

    # Arrange components in the grid
    file_label.grid(row=0, column=0, sticky="e", padx=10, pady=10)
    file_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=10)
    browse_button.grid(row=0, column=3, padx=10, pady=10)

    sampling_label.grid(row=1, column=0, sticky="e", padx=10, pady=10)
    sampling_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=10)

    output_label.grid(row=2, column=0, sticky="e", padx=10, pady=10)
    output_entry.grid(row=2, column=1, columnspan=2, padx=10, pady=10)

    run_button.grid(row=3, column=0, columnspan=4, pady=20)

    feedback_label.grid(row=4, column=0, columnspan=4, pady=10)

    # Start the GUI event loop
    gui.mainloop()

# Run the GUI
create_gui()
