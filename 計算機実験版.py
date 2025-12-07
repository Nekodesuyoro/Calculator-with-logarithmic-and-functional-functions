import tkinter as tk
import math
import re

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("電卓改改")
        self.root.geometry("500x600")

        
        self.entry = tk.Entry(root, width=30, font=("Arial", 20), justify="right")
        self.entry.pack(pady=20)

        
        button_frame = tk.Frame(root)
        button_frame.pack()

        
        buttons = [
            ["7","8","9","/"],
            ["4","5","6","*"],
            ["1","2","3","-"],
            ["0","C","=","+"],
            ["sin","cos","tan","√"],
            ["log","(",")","."],
            ["π","Exit"]
        ]

        for row_index, row in enumerate(buttons):
            for col_index, text in enumerate(row):
                button = tk.Button(button_frame, text=text, width=5, height=2, font=("Arial",18),
                                   command=lambda t=text: self.on_button_click(t))
                button.grid(row=row_index, column=col_index, padx=5, pady=5)

    def on_button_click(self, char):
        if char == "C":
            self.entry.delete(0, tk.END)

        elif char == "=":
            try:
                expression = self.entry.get()

                
                expression = re.sub(r'sin\(([^)]+)\)', r'math.sin(math.radians(\1))', expression)
                expression = re.sub(r'cos\(([^)]+)\)', r'math.cos(math.radians(\1))', expression)
                expression = re.sub(r'tan\(([^)]+)\)', r'math.tan(math.radians(\1))', expression)

            
                def replace_log(match):
                    content = match.group(1)
                    if ',' in content:
                        parts = content.split(',', 1)
                        base = parts[0].strip()
                        num = parts[1].strip()
                        return f'math.log({num},{base})'
                    else:
                    
                        return f'math.log({content})'
                
                expression = re.sub(r'log\(([^)]+)\)', replace_log, expression)

                
                expression = expression.replace('π', str(math.pi))

                
                result = eval(expression, {"__builtins__": None, "math": math})
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, str(result))
            except Exception as e:
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, f"Error: {type(e).__name__}")

        elif char in ["sin","cos","tan"]:
            current_pos = self.entry.index(tk.INSERT)
            self.entry.insert(current_pos, f"{char}()")
            self.entry.icursor(current_pos + len(char) + 1)  

        elif char == "√":
            current_pos = self.entry.index(tk.INSERT)
            self.entry.insert(current_pos, "math.sqrt(")

        elif char == "log":
            current_pos = self.entry.index(tk.INSERT)
            self.entry.insert(current_pos, "log(,)")
            self.entry.icursor(current_pos + 4)  

        elif char == "π":
            current_pos = self.entry.index(tk.INSERT)
            self.entry.insert(current_pos, "π")

        elif char == "Exit":
            self.root.destroy()

        else:
            current_pos = self.entry.index(tk.INSERT)
            self.entry.insert(current_pos, char)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()