import qrcode
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import subprocess

def get_desktop_path():
    """Returns the correct Desktop path for the current user."""
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    
    # Check if the Desktop exists, else use Documents
    if not os.path.exists(desktop):
        desktop = os.path.join(os.path.expanduser("~"), "Documents")  # Fallback
    
    return desktop

def generate_qr():
    data = entry.get()
    if not data:
        messagebox.showerror("Error", "Please enter some text or URL")
        return

    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill="black", back_color="white")

    # Get the correct Desktop path
    desktop_path = get_desktop_path()
    qr_path = os.path.join(desktop_path, "My_QR_Code.png")  # Save as 'My_QR_Code.png'

    try:
        img.save(qr_path)
        print(f"QR Code saved at: {qr_path}")  # Print the path in VS Code terminal
        messagebox.showinfo("Success", f"QR Code saved on Desktop as 'My_QR_Code.png'")

        # Open the saved QR Code image
        os.startfile(qr_path)  

        # Open File Explorer and highlight the saved file
        subprocess.Popen(f'explorer /select,"{qr_path}"')

    except Exception as e:
        messagebox.showerror("Error", f"Could not save QR code: {e}")
        return

    # Display the QR code in GUI
    img = Image.open(qr_path)
    img = img.resize((200, 200), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)
    
    qr_label.config(image=img)
    qr_label.image = img  # Keep reference

# Create GUI window
root = tk.Tk()
root.title("QR Code Generator")
root.geometry("400x500")

# Input field
tk.Label(root, text="Enter text or URL:", font=("Arial", 12)).pack(pady=10)
entry = tk.Entry(root, font=("Arial", 12), width=30)
entry.pack(pady=5)

# Generate button
tk.Button(root, text="Generate QR Code", font=("Arial", 12), command=generate_qr).pack(pady=10)

# QR Code display
qr_label = tk.Label(root)
qr_label.pack(pady=10)

# Run the GUI
root.mainloop()
