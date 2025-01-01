import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk

items = [
    ["Blush $24", "Concealer $22", "Eye Liner $11"],
    ["Bronzer $25", "Powder $35", "Lip Liner $8"],
    ["Mascara $13", "Eye Shadow $24", "Lip Oil $12"]
]

items_cost = [
    [24, 22, 11],
    [25, 35, 8],
    [13, 24, 12]
]

def calculate_total():
    total = 0
    try:
        for i in range(3):
            for j in range(3):
                quantity_str = entries[i][j].get()
                quantity = int(quantity_str) if quantity_str else 0
                if quantity < 0:
                    raise ValueError("Quantity cannot be negative.")
                total += items_cost[i][j] * quantity
        total_label_var.set(f"Total: ${total}")
    except ValueError as ve:
        messagebox.showerror("Invalid Input", f"Please enter valid quantities.\n{ve}")

def resize_image(path, max_width, max_height):
    try:
        img = Image.open(path)
        img.thumbnail((max_width, max_height), Image.ANTIALIAS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        messagebox.showerror("Image Error", f"Failed to load image.\n{e}")
        return None

# Initialize the main window
root = tk.Tk()
root.title("Zoot's Cosmetics")
root.configure(bg="#7EE0FE")
root.geometry("600x600")
root.resizable(False, False)

# Load the logo image
try:
    logo_image = PhotoImage(file="zootslogos.png")
except tk.TclError:
    messagebox.showerror("Error", "Could not load logo image. Ensure 'zootslogos.png' is in the same directory.")
    logo_image = None

# Create the main frame
main_frame = tk.Frame(root, bg="#7EE0FE")
main_frame.pack(pady=10, padx=10, fill="both", expand=True)

# Load and resize the logo image
logo_path = "zootslogos.png"  # Ensure this path is correct
max_logo_width = 300  # Adjust as needed
max_logo_height = 100  # Adjust as needed
logo_image = resize_image(logo_path, max_logo_width, max_logo_height)

# Display the logo at the top center
if logo_image:
    logo_label = tk.Label(main_frame, image=logo_image, bg="#7EE0FE")
    logo_label.grid(row=0, column=0, columnspan=3, pady=(10, 20))
else:
    # If the logo fails to load, display a placeholder text
    logo_label = tk.Label(main_frame, text="Zoot's Cosmetics", bg="#7EE0FE", font=("Cooper Black", 16))
    logo_label.grid(row=0, column=0, columnspan=3, pady=(10, 20))

# Create a frame for the grid of items
grid_frame = tk.Frame(main_frame, bg="#7EE0FE")
grid_frame.grid(row=1, column=0, padx=20, pady=10)

# Create the 3x3 grid of labels and entries
entries = []  # To store references to Entry widgets
for i in range(3):
    row_entries = []
    for j in range(3):
        # Item Label
        item_label = tk.Label(
            grid_frame,
            text=items[i][j],
            bg="#7EE0FE",
            fg="white",
            font=("Cooper Black", 12),
            padx=10,
            pady=5
        )
        item_label.grid(row=i*2, column=j, padx=10, pady=5, sticky="w")

        # Quantity Entry
        entry = tk.Entry(grid_frame, width=10, justify='center')
        entry.grid(row=i*2+1, column=j, padx=10, pady=5)
        row_entries.append(entry)
    entries.append(row_entries)

bottom_frame = tk.Frame(main_frame, bg="#7EE0FE")
bottom_frame.grid(row=2, column=0, pady=20)

# Calculate Total Button
calculate_button = tk.Button(
    bottom_frame,
    text="Calculate Total",
    command=calculate_total,
    bg="#4CAF50",
    fg="white",
    font=("Cooper Black", 12),
    padx=10,
    pady=5
)
calculate_button.pack(side="left", padx=10)

# Total Label
total_label_var = tk.StringVar()
total_label_var.set("Total: $0")
total_label = tk.Label(
    bottom_frame,
    textvariable=total_label_var,
    bg="#7EE0FE",
    fg="white",
    font=("Cooper Black", 14)
)
total_label.pack(side="left", padx=10)

# Run the application
root.mainloop()