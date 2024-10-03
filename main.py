import re
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def extract_workshop_id(url):
    # Regular expression pattern to capture the ID from Steam Workshop URL
    pattern = r"steamcommunity\.com/sharedfiles/filedetails/\?id=(\d+)"
    match = re.search(pattern, url)
    
    if match:
        return match.group(1)  # The ID is the first capture group
    else:
        return None

def extract_ids_from_file(file_path, output_file):
    try:
        with open(file_path, 'r') as file:
            urls = file.readlines()
            
        # Remove any extra whitespace or newlines from each URL
        urls = [url.strip() for url in urls]
        
        extracted_ids = []
        for url in urls:
            workshop_id = extract_workshop_id(url)
            if workshop_id:
                extracted_ids.append(workshop_id)
            else:
                print(f"No valid ID found for URL '{url}'")
        
        # Write extracted IDs to the output file
        with open(output_file, 'w') as output:
            for workshop_id in extracted_ids:
                output.write(workshop_id + '\n')
        
        messagebox.showinfo("Success", f"All extracted IDs have been saved to '{output_file}'.")

    except FileNotFoundError:
        messagebox.showerror("Error", f"File '{file_path}' not found.")

def select_input_file():
    file_path = filedialog.askopenfilename(title="Select the Steam URLs file",
                                           filetypes=[("Text Files", "*.txt")])
    input_file_entry.delete(0, tk.END)
    input_file_entry.insert(0, file_path)

def select_output_file():
    file_path = filedialog.asksaveasfilename(title="Select where to save the IDs",
                                             defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt")])
    output_file_entry.delete(0, tk.END)
    output_file_entry.insert(0, file_path)

def process_files():
    input_file = input_file_entry.get()
    output_file = output_file_entry.get()
    
    if input_file and output_file:
        extract_ids_from_file(input_file, output_file)
    else:
        messagebox.showerror("Error", "Please select both input and output files.")

# Create the main window
root = tk.Tk()
root.title("Steam Workshop ID Extractor")

# Create and place the input file widgets
tk.Label(root, text="Select Steam URLs File:").grid(row=0, column=0, padx=10, pady=10)
input_file_entry = tk.Entry(root, width=50)
input_file_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_input_file).grid(row=0, column=2, padx=10, pady=10)

# Create and place the output file widgets
tk.Label(root, text="Select Output File for IDs:").grid(row=1, column=0, padx=10, pady=10)
output_file_entry = tk.Entry(root, width=50)
output_file_entry.grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_output_file).grid(row=1, column=2, padx=10, pady=10)

# Create and place the process button
tk.Button(root, text="Extract IDs", command=process_files, width=20).grid(row=2, column=1, padx=10, pady=20)

# Start the GUI event loop
root.mainloop()
