import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import csv
import os

positions = [
    {
        "title": "School Leader",
        "candidates": [
            {"name": "Alice", "photo": "images/alice.jpg", "symbol": "images/alice_symbol.jpg"},
            {"name": "Bob", "photo": "images/bob.jpg", "symbol": "images/bob_symbol.jpg"},
            {"name": "Charlie", "photo": "images/charlie.jpg", "symbol": "images/charlie_symbol.jpg"}
        ]
    },
    {
        "title": "Assistant Leader",
        "candidates": [
            {"name": "David", "photo": "images/david.jpg", "symbol": "images/david_symbol.png"},
            {"name": "Eva", "photo": "images/eva.jpg", "symbol": "images/eva_symbol.png"}
        ]
    }
]

class VotingSystem:
    def __init__(self, root):
        self.root = root
        self.voting_active = False
        self.index = 0
        self.votes = []

        self.create_staff_window()
        self.create_student_window()

    def create_staff_window(self):
        self.staff_window = tk.Toplevel(self.root)
        self.staff_window.title("Staff Control")
        self.staff_window.geometry("800x600+0+0")
        self.staff_window.attributes('-topmost', True)

        title = tk.Label(self.staff_window, text="Staff Control Panel", font=("Arial", 32, "bold"))
        title.pack(pady=30)

        self.status_label = tk.Label(self.staff_window, text="Waiting to start...", font=("Arial", 24), fg="gray")
        self.status_label.pack(pady=20)

        start_btn = tk.Button(self.staff_window, text="Start Voting", font=("Arial", 24), command=self.start_voting)
        start_btn.pack(pady=40)

    def create_student_window(self):
        self.student_window = tk.Toplevel(self.root)
        self.student_window.title("Student Voting")
        self.student_window.geometry("1920x1080+1000+0")  # Change as needed
        self.student_window.attributes('-fullscreen', True)

        self.student_title = tk.Label(self.student_window, text="Please wait for staff to begin voting...",
                                      font=("Arial", 36, "bold"), justify="center")
        self.student_title.pack(pady=50)

        self.options_frame = tk.Frame(self.student_window)
        self.options_frame.pack()

    def start_voting(self):
        self.voting_active = True
        self.index = 0
        self.votes.clear()
        self.status_label.config(text="Voting in progress...", fg="green")
        self.show_position()

    def show_position(self):
        for widget in self.options_frame.winfo_children():
            widget.destroy()

        if not self.voting_active:
            return

        if self.index >= len(positions):
            self.student_title.config(text="Thank you for voting!\nPlease leave the booth.")
            self.status_label.config(text="Waiting to start...", fg="gray")
            self.voting_active = False
            self.root.after(5000, self.reset_student_screen)
            return

        pos = positions[self.index]
        self.student_title.config(text=f"Vote for {pos['title']}")
        self.candidate_buttons = []

        for candidate in pos["candidates"]:
            btn_frame = tk.Frame(self.options_frame, pady=10)
            btn_frame.pack(anchor="center")

            # Load candidate and symbol images
            photo_img = self.load_image(candidate["photo"], (120, 120))
            symbol_img = self.load_image(candidate["symbol"], (80, 80))

            photo_label = tk.Label(btn_frame, image=photo_img)
            photo_label.image = photo_img
            photo_label.pack(side="left", padx=20)

            symbol_label = tk.Label(btn_frame, image=symbol_img)
            symbol_label.image = symbol_img
            symbol_label.pack(side="left", padx=10)

            name_button = tk.Button(btn_frame, text=candidate["name"], font=("Arial", 28, "bold"),
                                    command=lambda c=candidate: self.cast_vote(c["name"]))
            name_button.pack(side="left", padx=40, ipadx=30, ipady=10)

    def load_image(self, path, size):
        if not os.path.exists(path):
            return None
        image = Image.open(path)
        image = image.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)

    def cast_vote(self, candidate_name):
        if not self.voting_active:
            return
        pos_title = positions[self.index]["title"]
        self.save_vote(pos_title, candidate_name)
        self.index += 1
        self.show_position()

    def save_vote(self, position, candidate):
        with open("votes.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([position, candidate])

    def reset_student_screen(self):
        self.student_title.config(text="Please wait for staff to begin voting...")
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        self.voting_active = False

root = tk.Tk()
root.withdraw()
app = VotingSystem(root)
root.mainloop()
