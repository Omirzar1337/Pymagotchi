import time
import random
import tkinter as tk
from tkinter import messagebox

class Tamagotchi:
    def __init__(self, name):
        self.name = name
        self.hunger = 50
        self.happiness = 50
        self.health = 100
        self.is_alive = True
        self.mood = "Neutral"

    def update_mood(self):
        if self.health <= 30:
            self.mood = "Sick"
        elif self.hunger <= 20:
            self.mood = "Hungry"
        elif self.happiness >= 80:
            self.mood = "Happy"
        else:
            self.mood = "Neutral"

    def update(self):
        self.hunger = max(0, self.hunger - random.randint(1, 3))
        self.happiness = max(0, self.happiness - random.randint(1, 2))
        if self.hunger <= 20 or self.happiness <= 20:
            self.health = max(0, self.health - random.randint(1, 5))
        if self.health <= 0:
            self.is_alive = False
        self.update_mood()

    def feed(self):
        self.hunger = min(100, self.hunger + 20)
        self.happiness = min(100, self.happiness + 10)
        messagebox.showinfo("Feed", f"You fed {self.name}. They look happier!")

    def play(self):
        self.happiness = min(100, self.happiness + 20)
        self.hunger = max(0, self.hunger - 10)
        messagebox.showinfo("Play", f"You played with {self.name}. They had fun!")

class RoundedButton(tk.Canvas):
    def __init__(self, master=None, text="", radius=25, bg="#00CED1", fg="white", font=("Arial", 12), command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(bg=master["bg"], highlightthickness=0)
        self.radius = radius
        self.bg = bg
        self.fg = fg
        self.font = font
        self.command = command
        self.text = text  # Store the button text as an instance variable

        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_hover)
        self.bind("<Leave>", self._on_leave)

        self.draw_button(self.text)

    def draw_button(self, text):
        self.delete("all")
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()

        # Draw rounded rectangle
        self.create_rounded_rectangle(0, 0, width, height, radius=self.radius, fill=self.bg, outline=self.bg)

        # Add text
        self.create_text(width // 2, height // 2, text=text, fill=self.fg, font=self.font)

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1,
        ]
        return self.create_polygon(points, **kwargs, smooth=True)

    def _on_click(self, event):
        if self.command:
            self.command()

    def _on_hover(self, event):
        self.config(cursor="hand2")
        self.draw_button(self.text)  # Use the stored text

    def _on_leave(self, event):
        self.config(cursor="")
        self.draw_button(self.text)  # Use the stored text

class TamagotchiApp:
    def __init__(self, root):
        self.root = root
        self.pet = None

        # Turquoise color palette
        self.bg_color = "#E0F7FA"  # Light turquoise background
        self.button_color = "#00CED1"  # Turquoise buttons
        self.button_hover_color = "#008B8B"  # Darker turquoise for hover
        self.text_color = "#00695C"  # Dark teal text
        self.status_bg = "#FFFFFF"  # White status background
        self.status_fg = "#00695C"  # Dark teal status text

        # Configure root window
        root.title("Tamagotchi Game")
        root.attributes('-topmost', True)  # Keep the window always on top
        root.resizable(False, False)  # Disable window resizing
        root.configure(bg=self.bg_color)

        # Name entry
        self.name_label = tk.Label(root, text="Enter your pet's name:", bg=self.bg_color, fg=self.text_color, font=("Arial", 14))
        self.name_label.pack(pady=5)

        self.name_entry = tk.Entry(root, font=("Arial", 12), bd=2, relief="flat", bg="white")
        self.name_entry.pack(pady=5)

        # Start button
        self.start_button = RoundedButton(root, text="Start", radius=20, bg=self.button_color, fg="white", font=("Arial", 12), command=self.start_game, width=100, height=40)
        self.start_button.pack(pady=10)

        # Status label
        self.status_label = tk.Label(root, text="", font=("Arial", 14), bg=self.status_bg, fg=self.status_fg, padx=10, pady=10, bd=0, relief="flat")
        self.status_label.pack(pady=10)

        # Buttons (initially hidden)
        self.feed_button = RoundedButton(root, text="Feed", radius=20, bg=self.button_color, fg="white", font=("Arial", 12), command=self.feed_pet, width=100, height=40)
        self.play_button = RoundedButton(root, text="Play", radius=20, bg=self.button_color, fg="white", font=("Arial", 12), command=self.play_with_pet, width=100, height=40)
        self.quit_button = RoundedButton(root, text="Quit", radius=20, bg="#FF4500", fg="white", font=("Arial", 12), command=root.quit, width=100, height=40)

    def start_game(self):
        pet_name = self.name_entry.get().strip()
        if not pet_name:
            messagebox.showwarning("Name Required", "Please enter a name for your pet.")
            return

        self.pet = Tamagotchi(pet_name)
        self.name_label.pack_forget()
        self.name_entry.pack_forget()
        self.start_button.pack_forget()

        # Show the buttons after starting the game
        self.feed_button.pack(side=tk.LEFT, padx=10)
        self.play_button.pack(side=tk.LEFT, padx=10)
        self.quit_button.pack(side=tk.LEFT, padx=10)

        self.update_pet_status()

    def update_pet_status(self):
        if self.pet:
            self.pet.update()
            status_text = (
                f"{self.pet.name}'s Status:\n"
                f"Hunger: {self.pet.hunger}/100\n"
                f"Happiness: {self.pet.happiness}/100\n"
                f"Health: {self.pet.health}/100\n"
                f"Mood: {self.pet.mood}"
            )
            if not self.pet.is_alive:
                status_text += "\nOh no! Your pet has passed away..."
                self.disable_buttons()
            self.status_label.config(text=status_text)

            if self.pet.is_alive:
                self.root.after(2000, self.update_pet_status)

    def disable_buttons(self):
        self.feed_button.config(state=tk.DISABLED)
        self.play_button.config(state=tk.DISABLED)

    def feed_pet(self):
        if self.pet and self.pet.is_alive:
            self.pet.feed()

    def play_with_pet(self):
        if self.pet and self.pet.is_alive:
            self.pet.play()

if __name__ == "__main__":
    root = tk.Tk()
    app = TamagotchiApp(root)
    root.mainloop()