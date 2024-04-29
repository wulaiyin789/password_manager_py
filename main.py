import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from database import delete_password, insert_password, retrieve_password, update_password
from encryption_master_password import decrypt_master_password, encrypt_master_password, generate_salt

class PasswordManagerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Password Manager")

        # Create a frame to center the master password input
        center_frame = ttk.Frame(master)
        center_frame.pack(expand=True)

        self.label_password = ttk.Label(center_frame, text="Enter Master Password:", font=("Arial", 14))
        self.label_password.pack(pady=10)

        self.entry_password = ttk.Entry(center_frame, show="*", font=("Arial", 12), width=20)
        self.entry_password.pack()

        self.button_submit_password = ttk.Button(center_frame, text="Submit", command=self.submit_password, style="Blue.TButton")
        self.button_submit_password.pack(pady=10)

    def submit_password(self):
        # Encrypt the master password (for demonstration purposes)
        master_password = "your_master_password"
        salt = generate_salt()

        encrypted_password, iv = encrypt_master_password(master_password, salt)

        # Decrypt and verify the master password
        decrypted_password = decrypt_master_password(encrypted_password, iv, master_password, salt)
        if decrypted_password == master_password:
            print("Master password decrypted successfully!")
            self.show_email_input()
        else:
            print("Invalid master password!")

    def show_email_input(self):
        # Clear the center frame and create a new frame for email input
        for widget in self.master.winfo_children():
            widget.destroy()

        email_frame = ttk.Frame(self.master)
        email_frame.pack(expand=True)

        self.label_email = ttk.Label(email_frame, text="Enter Email:", font=("Arial", 14))
        self.label_email.pack(pady=10)

        self.entry_email = ttk.Entry(email_frame, font=("Arial", 12), width=20)
        self.entry_email.pack()

        self.button_submit_email = ttk.Button(email_frame, text="Retrieve Password", command=self.retrieve_password, style="Blue.TButton")
        self.button_submit_email.pack(pady=10)
        
        # Button to create password
        self.button_create_password = ttk.Button(email_frame, text="Create Password", command=self.show_create_password_frame, style="Green.TButton")
        self.button_create_password.pack(pady=5)

        # Button to update password
        self.button_update_password = ttk.Button(email_frame, text="Update Password", command=self.show_update_password_frame, style="Green.TButton")
        self.button_update_password.pack(pady=5)

        # Button to delete password
        self.button_delete_password = ttk.Button(email_frame, text="Delete Password", command=self.show_delete_password_frame, style="Red.TButton")
        self.button_delete_password.pack(pady=5)
        
    def show_create_password_frame(self):
        # Clear the center frame and create a new frame for updating password
        for widget in self.master.winfo_children():
            widget.destroy()

        create_frame = ttk.Frame(self.master)
        create_frame.pack(expand=True)

        self.label_create_email = ttk.Label(create_frame, text="Enter Email:", font=("Arial", 14))
        self.label_create_email.pack(pady=10)

        self.entry_create_email = ttk.Entry(create_frame, font=("Arial", 12), width=20)
        self.entry_create_email.pack()

        self.label_new_password = ttk.Label(create_frame, text="Enter New Password:", font=("Arial", 14))
        self.label_new_password.pack(pady=10)

        self.entry_new_password = ttk.Entry(create_frame, font=("Arial", 12), width=20, show="*")
        self.entry_new_password.pack()

        self.button_submit_create = ttk.Button(create_frame, text="Create", command=self.create_password_action, style="Green.TButton")
        self.button_submit_create.pack(pady=10)
        
        self.create_back_button()
        
    def show_update_password_frame(self):
        # Clear the center frame and create a new frame for updating password
        for widget in self.master.winfo_children():
            widget.destroy()

        update_frame = ttk.Frame(self.master)
        update_frame.pack(expand=True)

        self.label_update_email = ttk.Label(update_frame, text="Enter Email:", font=("Arial", 14))
        self.label_update_email.pack(pady=10)

        self.entry_update_email = ttk.Entry(update_frame, font=("Arial", 12), width=20)
        self.entry_update_email.pack()

        self.label_new_password = ttk.Label(update_frame, text="Enter New Password:", font=("Arial", 14))
        self.label_new_password.pack(pady=10)

        self.entry_new_password = ttk.Entry(update_frame, font=("Arial", 12), width=20, show="*")
        self.entry_new_password.pack()

        self.button_submit_update = ttk.Button(update_frame, text="Update", command=self.update_password_action, style="Green.TButton")
        self.button_submit_update.pack(pady=10)
        
        self.create_back_button()
        
    def show_delete_password_frame(self):
        # Clear the center frame and create a new frame for deleting password
        for widget in self.master.winfo_children():
            widget.destroy()

        delete_frame = ttk.Frame(self.master)
        delete_frame.pack(expand=True)

        self.label_delete_email = ttk.Label(delete_frame, text="Enter Email to Delete:", font=("Arial", 14))
        self.label_delete_email.pack(pady=10)

        self.entry_delete_email = ttk.Entry(delete_frame, font=("Arial", 12), width=20)
        self.entry_delete_email.pack()

        self.button_submit_delete = ttk.Button(delete_frame, text="Delete", command=self.delete_password_action, style="Red.TButton")
        self.button_submit_delete.pack(pady=10)
        
        self.create_back_button()
        
    def create_back_button(self):
        back_button = ttk.Button(self.master, text="<", command=self.show_email_input)
        back_button.place(x=10, y=10)  # Adjust the position as needed


    def retrieve_password(self):
        email = self.entry_email.get()
        password = retrieve_password(self.entry_email.get())
        
        messagebox.showinfo("Password", f"Password for {email}: {password}")
        
    def create_password_action(self):
        email = self.entry_create_email.get()
        new_password = self.entry_new_password.get()
        # Call the create_password function with email and new_password
        insert_password(email, new_password)  # Assuming 'site' is the email itself
        messagebox.showinfo("Success", "Password created successfully!")
        self.show_email_input()  # Go back to the email retrieval page after updating

    def update_password_action(self):
        email = self.entry_update_email.get()
        new_password = self.entry_new_password.get()
        # Call the update_password function with email and new_password
        update_password(email, new_password)  # Assuming 'site' is the email itself
        messagebox.showinfo("Success", "Password updated successfully!")
        self.show_email_input()  # Go back to the email retrieval page after updating
        
    def delete_password_action(self):
        email = self.entry_delete_email.get()
        # Call the update_password function with email and new_password
        delete_password(email)  # Assuming 'site' is the email itself
        messagebox.showinfo("Success", "Password deleted successfully!")
        self.show_email_input()  # Go back to the email retrieval page after updating

# Create the main window
root = tk.Tk()

# Set window size and position
window_width = 400
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Create custom style for buttons
style = ttk.Style()
style.configure("Yellow.TButton", background="#524512", font=("Arial", 12))
style.configure("Blue.TButton", background="#007bff", font=("Arial", 12))
style.configure("Green.TButton", background="#28a745", font=("Arial", 12))
style.configure("Red.TButton", background="#dc3545", font=("Arial", 12))

# Create an instance of the PasswordManagerApp class
app = PasswordManagerApp(root)

# Run the application
root.mainloop()