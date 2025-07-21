import tkinter as tk
import csv

# Sample data
positions = {
    "School Leader": ["Alice", "Bob", "Charlie"],
    "Assistant Leader": ["David", "Eva"],
    "Sports Captain": ["Faisal", "Grace", "Hannah"]
}

votes = []

class VotingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("School Parliament Voting")
        self.position_names = list(positions.keys())
        self.index = 0
        self.build_ui()

    def build_ui(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=50)

        self.label = tk.Label(self.frame, text="", font=("Arial", 18))
        self.label.pack(pady=10)

        self.buttons = []
        self.display_position()

    def display_position(self):
        if self.index >= len(self.position_names):
            self.show_thank_you()
            self.save_votes()
            return

        for btn in self.buttons:
            btn.destroy()
        self.buttons.clear()

        pos = self.position_names[self.index]
        self.label.config(text=f"Vote for: {pos}")

        for i, candidate in enumerate(positions[pos]):
            btn = tk.Button(self.frame, text=f"{i+1}. {candidate}", width=30,
                            command=lambda c=candidate: self.record_vote(pos, c))
            btn.pack(pady=5)
            self.buttons.append(btn)

    def record_vote(self, position, candidate):
        votes.append({"Position": position, "Candidate": candidate})
        self.index += 1
        self.display_position()

    def show_thank_you(self):
        self.label.config(text="Thank you for voting!")
        for btn in self.buttons:
            btn.destroy()

    def save_votes(self):
        with open("votes.csv", "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["Position", "Candidate"])
            for vote in votes:
                writer.writerow(vote)

root = tk.Tk()
app = VotingApp(root)
root.mainloop()
