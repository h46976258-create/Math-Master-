import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
import os
import uuid

class MathGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Master")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        
        # Game variables
        self.current_level = 1
        self.score = 0
        self.combo = 0
        self.correct_answer = 0
        self.max_level = 1100
        
        # Statistics
        self.total_questions = 0
        self.correct_answers = 0
        self.max_combo = 0
        
        # Player tracking
        self.player_id = self.get_player_id()
        self.total_players = self.get_total_players()
        
        # Create UI
        self.setup_ui()
        
        # Start game
        self.load_game()
        self.generate_question()
    
    def get_player_id(self):
        """Get or create unique player ID"""
        try:
            if os.path.exists("player_id.json"):
                with open("player_id.json", "r") as f:
                    data = json.load(f)
                    return data.get('player_id', str(uuid.uuid4()))
            else:
                new_id = str(uuid.uuid4())
                with open("player_id.json", "w") as f:
                    json.dump({'player_id': new_id}, f)
                return new_id
        except:
            return str(uuid.uuid4())
    
    def get_total_players(self):
        """Get total number of unique players"""
        try:
            if os.path.exists("players_count.json"):
                with open("players_count.json", "r") as f:
                    data = json.load(f)
                    players = data.get('players', [])
                    
                    # Check if current player is new
                    if self.player_id not in players:
                        players.append(self.player_id)
                        with open("players_count.json", "w") as f:
                            json.dump({'players': players, 'total_players': len(players)}, f)
                    
                    return len(players)
            else:
                # First player
                with open("players_count.json", "w") as f:
                    json.dump({'players': [self.player_id], 'total_players': 1}, f)
                return 1
        except:
            return 1
    
    def setup_ui(self):
        # Main frame
        self.main_frame = tk.Frame(self.root, padx=15, pady=15)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header frame for player count
        header_frame = tk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=5)
        
        # Game title
        title_label = tk.Label(
            header_frame,
            text="Math Master", 
            font=("Arial", 16, "bold"),
            fg="#2c3e50"
        )
        title_label.pack(side=tk.LEFT)
        
        # Player count label (top right)
        self.players_label = tk.Label(
            header_frame,
            text=f" players: {self.total_players}",
            font=("Arial", 9),
            fg="#7f8c8d"
        )
        self.players_label.pack(side=tk.RIGHT)
        
        # Game info display
        info_frame = tk.Frame(self.main_frame)
        info_frame.pack(fill=tk.X, pady=8)
        
        # Current level
        self.level_label = tk.Label(
            info_frame,
            text=f"Level: {self.current_level}/1100",
            font=("Arial", 12),
            fg="#3498db"
        )
        self.level_label.pack()
        
        # Level range
        self.level_range_label = tk.Label(
            info_frame,
            text="",
            font=("Arial", 10),
            fg="#7f8c8d"
        )
        self.level_range_label.pack()
        
        # Score
        self.score_label = tk.Label(
            info_frame,
            text=f"Score: {self.score}",
            font=("Arial", 10),
            fg="#2c3e50"
        )
        self.score_label.pack(pady=8)
        
        # Current Combo
        self.combo_label = tk.Label(
            info_frame,
            text="",
            font=("Arial", 10),
            fg="#27ae60"
        )
        self.combo_label.pack()
        
        # Max Combo Record
        self.max_combo_label = tk.Label(
            info_frame,
            text=f"Record Combo: {self.max_combo}",
            font=("Arial", 9),
            fg="#e74c3c"
        )
        self.max_combo_label.pack()
        
        # Stats label
        self.stats_label = tk.Label(
            info_frame,
            text="Accuracy: 0%",
            font=("Arial", 9),
            fg="#7f8c8d"
        )
        self.stats_label.pack()
        
        # Question
        question_frame = tk.Frame(self.main_frame, pady=15)
        question_frame.pack(fill=tk.X)
        
        self.question_label = tk.Label(
            question_frame,
            text="",
            font=("Arial", 16, "bold"),
            fg="#2c3e50",
            wraplength=350
        )
        self.question_label.pack()
        
        # Answer input
        answer_frame = tk.Frame(self.main_frame, pady=10)
        answer_frame.pack(fill=tk.X)
        
        tk.Label(
            answer_frame,
            text="Your Answer:",
            font=("Arial", 10)
        ).pack()
        
        self.answer_entry = tk.Entry(
            answer_frame,
            font=("Arial", 14),
            justify='center',
            width=15
        )
        self.answer_entry.pack(pady=8)
        self.answer_entry.bind('<Return>', lambda e: self.check_answer())
        
        # Digital Keyboard
        self.create_digital_keyboard()
        
        # Progress bar
        progress_frame = tk.Frame(self.main_frame, pady=15)
        progress_frame.pack(fill=tk.X)
        
        tk.Label(
            progress_frame,
            text="Game Progress:",
            font=("Arial", 9),
            fg="#7f8c8d"
        ).pack()
        
        self.progress = ttk.Progressbar(
            progress_frame,
            orient=tk.HORIZONTAL,
            length=300,
            mode='determinate',
            maximum=1100
        )
        self.progress.pack(pady=5)
        self.progress['value'] = self.current_level
        
        # Buttons frame
        button_frame = tk.Frame(self.main_frame, pady=10)
        button_frame.pack()
        
        self.reset_btn = tk.Button(
            button_frame,
            text="Reset Game",
            font=("Arial", 9),
            command=self.reset_game,
            bg="#f39c12",
            fg="white",
            padx=8,
            pady=5
        )
        self.reset_btn.pack(side=tk.LEFT, padx=3)
        
        self.exit_btn = tk.Button(
            button_frame,
            text="Exit",
            font=("Arial", 9),
            command=self.exit_game,
            bg="#e74c3c",
            fg="white",
            padx=8,
            pady=5
        )
        self.exit_btn.pack(side=tk.LEFT, padx=3)
    
    def create_digital_keyboard(self):
        """Create a digital keyboard for mobile input"""
        keyboard_frame = tk.Frame(self.main_frame, pady=10)
        keyboard_frame.pack()
        
        # Number buttons layout
        buttons = [
            ['7', '8', '9', '⌫'],
            ['4', '5', '6', 'C'],
            ['1', '2', '3', 'Enter'],
            ['0', '.', '-', '']
        ]
        
        for row in buttons:
            btn_row = tk.Frame(keyboard_frame)
            btn_row.pack()
            for button in row:
                if button == 'Enter':
                    btn = tk.Button(
                        btn_row,
                        text=button,
                        font=("Arial", 10, "bold"),
                        width=6,
                        height=2,
                        command=self.check_answer,
                        bg="#2ecc71",
                        fg="white"
                    )
                elif button == '⌫':
                    btn = tk.Button(
                        btn_row,
                        text=button,
                        font=("Arial", 10),
                        width=6,
                        height=2,
                        command=self.backspace,
                        bg="#f39c12",
                        fg="white"
                    )
                elif button == 'C':
                    btn = tk.Button(
                        btn_row,
                        text=button,
                        font=("Arial", 10),
                        width=6,
                        height=2,
                        command=self.clear_input,
                        bg="#e74c3c",
                        fg="white"
                    )
                elif button:
                    btn = tk.Button(
                        btn_row,
                        text=button,
                        font=("Arial", 10),
                        width=6,
                        height=2,
                        command=lambda b=button: self.add_to_input(b)
                    )
                else:
                    btn = tk.Label(btn_row, width=6, height=2)
                
                btn.pack(side=tk.LEFT, padx=2, pady=2)
    
    def add_to_input(self, character):
        """Add character to input field"""
        current = self.answer_entry.get()
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.insert(0, current + character)
    
    def backspace(self):
        """Remove last character from input field"""
        current = self.answer_entry.get()
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.insert(0, current[:-1])
    
    def clear_input(self):
        """Clear input field"""
        self.answer_entry.delete(0, tk.END)
    
    def generate_question(self):
        """Generate a math question based on current level"""
        # Update level info
        self.level_label.config(text=f"Level: {self.current_level}/1100")
        self.progress['value'] = self.current_level
        
        # Determine level range
        level_range = ""
        if self.current_level <= 100:
            level_range = "1-100 (Basic Operations)"
        elif self.current_level <= 200:
            level_range = "101-200 (No numbers below 10)"
        elif self.current_level <= 500:
            level_range = "201-500 (Larger numbers)"
        elif self.current_level <= 900:
            level_range = "501-900 (Decimal numbers)"
        elif self.current_level <= 1000:
            level_range = "901-1000 (Only exponents)"
        else:
            level_range = "1001-1100 (Multiplication 100-999)"
        
        self.level_range_label.config(text=level_range)
        
        # Generate question based on level
        if self.current_level <= 100:
            op = random.choice(['+', '-', '*', '/'])
            if op == '+':
                a = random.randint(1, 100)
                b = random.randint(1, 100)
                self.correct_answer = a + b
                question = f"{a} + {b} = ?"
            elif op == '-':
                a = random.randint(1, 100)
                b = random.randint(a, 100)
                self.correct_answer = b - a
                question = f"{b} - {a} = ?"
            elif op == '*':
                a = random.randint(1, 12)
                b = random.randint(1, 10)
                self.correct_answer = a * b
                question = f"{a} × {b} = ?"
            else:
                b = random.randint(1, 10)
                a = b * random.randint(1, 10)
                self.correct_answer = a // b
                question = f"{a} ÷ {b} = ?"
                
        elif self.current_level <= 200:
            op = random.choice(['+', '-', '*', '/'])
            a = random.randint(10, 100)
            b = random.randint(10, 100)
            if op == '+':
                self.correct_answer = a + b
                question = f"{a} + {b} = ?"
            elif op == '-':
                a, b = max(a, b), min(a, b)
                self.correct_answer = a - b
                question = f"{a} - {b} = ?"
            elif op == '*':
                self.correct_answer = a * b
                question = f"{a} × {b} = ?"
            else:
                b = random.randint(10, 20)
                a = b * random.randint(5, 10)
                self.correct_answer = a // b
                question = f"{a} ÷ {b} = ?"
                    
        elif self.current_level <= 500:
            op = random.choice(['+', '-', '*', '/'])
            a = random.randint(20, 100)
            b = random.randint(20, 100)
            if op == '+':
                self.correct_answer = a + b
                question = f"{a} + {b} = ?"
            elif op == '-':
                a, b = max(a, b), min(a, b)
                self.correct_answer = a - b
                question = f"{a} - {b} = ?"
            elif op == '*':
                self.correct_answer = a * b
                question = f"{a} × {b} = ?"
            else:
                b = random.randint(10, 25)
                a = b * random.randint(5, 10)
                self.correct_answer = a // b
                question = f"{a} ÷ {b} = ?"
                    
        elif self.current_level <= 900:
            op = random.choice(['+', '-', '*', '/'])
            a = round(random.uniform(1, 100), 1)
            b = round(random.uniform(1, 100), 1)
            
            if op == '+':
                self.correct_answer = round(a + b, 1)
                question = f"{a} + {b} = ?"
            elif op == '-':
                a, b = max(a, b), min(a, b)
                self.correct_answer = round(a - b, 1)
                question = f"{a} - {b} = ?"
            elif op == '*':
                self.correct_answer = round(a * b, 1)
                question = f"{a} × {b} = ?"
            else:
                b = round(random.uniform(1, 10), 1)
                a = round(b * random.randint(5, 20), 1)
                self.correct_answer = round(a / b, 1)
                question = f"{a} ÷ {b} = ?"
                
        elif self.current_level <= 1000:
            # Only exponents from 900 to 1000
            base = random.randint(2, 5)
            exponent = random.randint(2, 4)
            self.correct_answer = base ** exponent
            question = f"{base}^{exponent} = ?"
        
        else:  # 1001-1100: Only multiplication from 100 to 999
            a = random.randint(100, 999)
            b = random.randint(100, 999)
            self.correct_answer = a * b
            question = f"{a} × {b} = ?"
        
        self.question_label.config(text=question)
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.focus()
    
    def check_answer(self):
        """Check user's answer"""
        try:
            user_answer = float(self.answer_entry.get())
            correct_answer = float(self.correct_answer)
            
            self.total_questions += 1
            
            # Check answer with small tolerance for floating point numbers
            if abs(user_answer - correct_answer) < 0.0001:
                self.correct_answers += 1
                self.combo += 1
                self.score += 10 * self.combo
                
                # Update max combo record
                if self.combo > self.max_combo:
                    self.max_combo = self.combo
                    self.max_combo_label.config(text=f"Record Combo: {self.max_combo}", fg="#e74c3c")
                
                # Show combo message با رنگ سبز
                if self.combo >= 2:
                    self.combo_label.config(text=f"Combo {self.combo}", fg="#27ae60")
                else:
                    self.combo_label.config(text="Correct!", fg="#27ae60")
                
                self.current_level += 1
                
                # Check if game completed
                if self.current_level > self.max_level:
                    self.show_completion_message()
                else:
                    self.generate_question()
            else:
                # اینجا کامبوی فعلی صفر میشه اما رکورد کامبو دست نخورده باقی میمونه
                self.combo = 0
                self.combo_label.config(text="Wrong! Try again.", fg="#e74c3c")
                self.generate_question()
            
            # Update UI
            self.score_label.config(text=f"Score: {self.score}")
            self.update_stats()
            self.save_game()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")
    
    def update_stats(self):
        """Update statistics display"""
        accuracy = (self.correct_answers / self.total_questions * 100) if self.total_questions > 0 else 0
        self.stats_label.config(text=f"Accuracy: {accuracy:.1f}%")
    
    def show_completion_message(self):
        """Show game completion message"""
        accuracy = (self.correct_answers / self.total_questions * 100) if self.total_questions > 0 else 0
        messagebox.showinfo(
            "Congratulations!",
            f"You completed all 1100 levels!\n\n"
            f"Final Score: {self.score}\n"
            f"Accuracy: {accuracy:.1f}%\n"
            f"Max Combo Record: {self.max_combo}\n\n"
            f"You are a true Math Master!"
        )
    
    def save_game(self):
        """Save game progress"""
        data = {
            'current_level': self.current_level,
            'score': self.score,
            'combo': self.combo,
            'max_combo': self.max_combo,
            'total_questions': self.total_questions,
            'correct_answers': self.correct_answers
        }
        
        try:
            with open("math_game_save.json", "w") as f:
                json.dump(data, f)
        except:
            pass
    
    def load_game(self):
        """Load game progress"""
        try:
            if os.path.exists("math_game_save.json"):
                with open("math_game_save.json", "r") as f:
                    data = json.load(f)
                    self.current_level = data.get('current_level', 1)
                    self.score = data.get('score', 0)
                    self.combo = data.get('combo', 0)
                    self.max_combo = data.get('max_combo', 0)
                    self.total_questions = data.get('total_questions', 0)
                    self.correct_answers = data.get('correct_answers', 0)
                    
                    # آپدیت نمایش رکورد کامبو
                    self.max_combo_label.config(text=f"Record Combo: {self.max_combo}")
        except:
            pass
    
    def reset_game(self):
        """Reset game progress"""
        if messagebox.askyesno("Reset Game", "Are you sure you want to reset all progress?"):
            self.current_level = 1
            self.score = 0
            self.combo = 0
            self.max_combo = 0
            self.total_questions = 0
            self.correct_answers = 0
            
            # آپدیت نمایش
            self.max_combo_label.config(text=f"Record Combo: {self.max_combo}")
            self.combo_label.config(text="")
            
            self.generate_question()
            self.save_game()
    
    def exit_game(self):
        """Exit the game"""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.save_game()
            self.root.quit()

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = MathGame(root)
    root.mainloop()
