import tkinter as tk
from tkinter import messagebox, PhotoImage
from PIL import Image, ImageTk
import sqlite3
from datetime import datetime

# Initialize SQLite database
db_conn = sqlite3.connect("zoots_cosmetics.db")
cursor = db_conn.cursor()

# Create the orders table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        items TEXT,
        total INTEGER,
        timestamp TEXT
    )
""")
db_conn.commit()

# Items and their corresponding costs
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

def resize_image(path, max_width, max_height):
    """
    Resizes an image to fit within the specified width and height while maintaining aspect ratio.
    """
    try:
        img = Image.open(path)
        img.thumbnail((max_width, max_height), Image.ANTIALIAS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        messagebox.showerror("Image Error", f"Failed to load image.\n{e}")
        return None

def submit_order():
    """
    Calculates the total cost of the order, validates inputs, and submits the order to the database.
    """
    total = 0
    order_details = []
    try:
        for i in range(3):
            for j in range(3):
                quantity_str = entries[i][j].get()
                quantity = int(quantity_str) if quantity_str else 0
                if quantity < 0:
                    raise ValueError("Quantity cannot be negative.")
                if quantity > 0:
                    # Extract the item name without the price
                    item_name = items[i][j].split(' $')[0]
                    order_details.append(f"{item_name} x{quantity}")
                total += items_cost[i][j] * quantity

        if not order_details:
            messagebox.showinfo("Empty Order", "No items were ordered.")
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO orders (items, total, timestamp) VALUES (?, ?, ?)",
            (", ".join(order_details), total, timestamp)
        )
        db_conn.commit()
        total_label_var.set(f"Total: ${total}")
        messagebox.showinfo("Order Submitted", f"Order submitted successfully!\nTotal: ${total}")

        # Clear the entries after submission
        for row in entries:
            for entry in row:
                entry.delete(0, tk.END)

    except ValueError as ve:
        messagebox.showerror("Invalid Input", f"Please enter valid quantities.\n{ve}")

def show_most_expensive_order():
    """
    Fetches and displays the most expensive order from the database.
    """
    cursor.execute("SELECT * FROM orders ORDER BY total DESC LIMIT 1")
    result = cursor.fetchone()
    if result:
        messagebox.showinfo(
            "Most Expensive Order",
            f"Order ID: {result[0]}\nItems: {result[1]}\nTotal: ${result[2]}\nTime: {result[3]}"
        )
    else:
        messagebox.showinfo("No Orders", "No orders have been placed yet.")

def show_most_recent_order():
    """
    Fetches and displays the most recent order from the database.
    """
    cursor.execute("SELECT * FROM orders ORDER BY timestamp DESC LIMIT 1")
    result = cursor.fetchone()
    if result:
        messagebox.showinfo(
            "Most Recent Order",
            f"Order ID: {result[0]}\nItems: {result[1]}\nTotal: ${result[2]}\nTime: {result[3]}"
        )
    else:
        messagebox.showinfo("No Orders", "No orders have been placed yet.")

# Initialize the main window
root = tk.Tk()
root.title("Zoot's Cosmetics")
root.configure(bg="#7EE0FE")
root.geometry("800x700")  # Increased size for better layout
root.resizable(False, False)

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
    logo_label = tk.Label(
        main_frame,
        text="Zoot's Cosmetics",
        bg="#7EE0FE",
        fg="white",
        font=("Cooper Black", 24)
    )
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

# Create a frame for the buttons and total label
bottom_frame = tk.Frame(main_frame, bg="#7EE0FE")
bottom_frame.grid(row=2, column=0, pady=20)

# Submit Order Button
submit_button = tk.Button(
    bottom_frame,
    text="Submit Order",
    command=submit_order,
    bg="#4CAF50",
    fg="white",
    font=("Cooper Black", 12),
    padx=10,
    pady=5
)
submit_button.pack(side="left", padx=10)

# Most Expensive Order Button
expensive_button = tk.Button(
    bottom_frame,
    text="Most Expensive Order",
    command=show_most_expensive_order,
    bg="#FF5722",
    fg="white",
    font=("Cooper Black", 12),
    padx=10,
    pady=5
)
expensive_button.pack(side="left", padx=10)

# Most Recent Order Button
recent_button = tk.Button(
    bottom_frame,
    text="Most Recent Order",
    command=show_most_recent_order,
    bg="#2196F3",
    fg="white",
    font=("Cooper Black", 12),
    padx=10,
    pady=5
)
recent_button.pack(side="left", padx=10)

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


root.mainloop()

def on_closing():
    """
    Handles cleanup when the window is closed.
    """
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        db_conn.close()
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
