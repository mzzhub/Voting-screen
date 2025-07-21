import tkinter as tk
import csv

positions = [
    {"title": "School Leader", "candidates": ["Alice", "Bob", "Charlie"]},
    {"title": "Assistant Leader", "candidates": ["David", "Eva"]},
    {"title": "Sports Captain", "candidates": ["Faisal", "Grace", "Hannah"]}
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
        self.staff_window.geometry("800x600+0+0")  # Screen 1
        self.staff_window.attributes('-topmost', True)

        title = tk.Label(self.staff_window, text="Staff Control Panel", font=("Arial", 24))
        title.pack(pady=30)

        self.status_label = tk.Label(self.staff_window, text="Waiting to start...", font=("Arial", 20), fg="gray")
        self.status_label.pack(pady=20)

        start_btn = tk.Button(self.staff_window, text="Start Voting", font=("Arial", 20), command=self.start_voting)
        start_btn.pack(pady=40)

    def create_student_window(self):
        self.student_window = tk.Toplevel(self.root)
        self.student_window.title("Student Voting")
        self.student_window.geometry("800x600+1000+0")  # Adjust this for screen 2 position
        self.student_window.attributes('-fullscreen', True)

        self.student_title = tk.Label(self.student_window, text="Please wait for staff to begin voting...",
                                      font=("Arial", 30), wraplength=1000)
        self.student_title.pack(pady=100)

        self.student_instructions = tk.Label(self.student_window, text="", font=("Arial", 24))
        self.student_instructions.pack()

        self.student_window.bind("<Key>", self.key_pressed)

    def start_voting(self):
        self.voting_active = True
        self.index = 0
        self.votes.clear()
        self.status_label.config(text="Voting in progress...", fg="green")
        self.show_position()

    def show_position(self):
        if not self.voting_active:
            return

        if self.index >= len(positions):
            self.student_title.config(text="Thank you for voting!")
            self.student_instructions.config(text="Please leave the booth.")
            self.status_label.config(text="Waiting to start...", fg="gray")
            self.voting_active = False
            self.root.after(5000, self.reset_student_screen)
            return

        pos = positions[self.index]
        self.student_title.config(text=f"Vote for {pos['title']}")
        options = [f"{i+1}. {name}" for i, name in enumerate(pos['candidates'])]
        self.student_instructions.config(text="\n".join(options) + "\n\nPress 1, 2, 3... to vote.")

    def key_pressed(self, event):
        if not self.voting_active or self.index >= len(positions):
            return

        key = event.char
        pos = positions[self.index]
        try:
            choice = int(key) - 1
            if 0 <= choice < len(pos['candidates']):
                selected = pos['candidates'][choice]
                self.save_vote(pos['title'], selected)
                self.index += 1
                self.show_position()
        except:
            pass

    def save_vote(self, position, candidate):
        with open("votes.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([position, candidate])

    def reset_student_screen(self):
        self.student_title.config(text="Please wait for staff to begin voting...")
        self.student_instructions.config(text="")
        self.voting_active = False

root = tk.Tk()
root.withdraw()  # Hide the root window
app = VotingSystem(root)
root.mainloop()
