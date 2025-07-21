import tkinter as tk
import csv

# Candidate Data
positions = [
    {"title": "School Leader", "candidates": ["Alice", "Bob", "Charlie"]},
    {"title": "Assistant Leader", "candidates": ["David", "Eva"]},
    {"title": "Sports Captain", "candidates": ["Faisal", "Grace", "Hannah"]}
]

class VotingApp:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-fullscreen', True)  # Fullscreen mode
        self.root.protocol("WM_DELETE_WINDOW", self.disable_event)  # Disable close
        self.root.bind("<Alt-F4>", self.disable_event)  # Try to block ALT+F4
        self.root.bind("<Escape>", self.disable_event)

        self.index = 0
        self.votes = []
        self.label_title = tk.Label(root, text="", font=("Arial", 36), pady=20)
        self.label_title.pack()

        self.label_instructions = tk.Label(root, text="", font=("Arial", 28))
        self.label_instructions.pack()

        self.show_position()
        root.bind("<Key>", self.key_pressed)

    def show_position(self):
        if self.index >= len(positions):
            self.label_title.config(text="Thank you for voting!")
            self.label_instructions.config(text="You may now leave the booth.")
            return

        pos = positions[self.index]
        self.label_title.config(text=f"Vote for {pos['title']}")
        options = [f"{i+1}. {name}" for i, name in enumerate(pos['candidates'])]
        self.label_instructions.config(text="\n".join(options) + "\n\nPress 1, 2, 3... to vote.")

    def key_pressed(self, event):
        if self.index >= len(positions):
            return  # Voting over

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
            pass  # Ignore invalid keys

    def save_vote(self, position, candidate):
        with open("votes.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([position, candidate])

    def disable_event(self, event=None):
        return "break"  # Prevent window closing or escape

root = tk.Tk()
app = VotingApp(root)
root.mainloop()
