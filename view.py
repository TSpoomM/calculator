import math
import tkinter as tk
from tkinter import scrolledtext

from model import Model


class View(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.geometry("450x650")
        self.model = Model()

        self.display_var = tk.StringVar()
        self.history_var = tk.StringVar(value="")

        self.init_components()
        self.bind_keys()

    def init_components(self):
        display_frame = tk.Frame(self)
        display_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        self.make_display()
        keypad = self.make_keypad()
        self.make_history()
        operators = self.make_operator_pad()

        keypad.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        operators.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        self.bind_history()

    def bind_history(self):
        self.history_display.tag_bind("clickable", "<Double-Button-1>", self.on_history_double_click)

    def bind_keys(self):
        for child in self.winfo_children():
            if isinstance(child, tk.Frame):
                for button in child.winfo_children():
                    button.bind('<Button-1>', self.button_pressed)

    def on_history_double_click(self, event):
        if isinstance(event.widget, tk.Button):
            selected_index = self.history_display.curselection()
            if selected_index:
                selected_item = self.history_display.get(selected_index[0])
                self.model.expression = selected_item
                old_function = selected_item.split('=')[0].strip()
                print(f"Old function: {old_function}")

    def button_pressed(self, event):
        if isinstance(event.widget, tk.Button):
            button = event.widget
            value = button['text']
            print(value)

    def make_display(self):
        """ Create Display. """
        display = tk.Entry(self, textvariable=self.display_var, font=('Arial', 20), bd=10, insertwidth=4, width=23,
                           justify='right')
        display.configure(bg='black', fg='yellow')
        display.pack(side='top', fill=tk.BOTH, padx=10, pady=10)

    def make_keypad(self) -> tk.Frame:
        """ Create Keypad. """
        frame = tk.Frame(self)

        # Numeric keys
        buttons = []
        for i in range(1, 10):
            button = tk.Button(frame, text=str(i), command=lambda t=str(i): self.on_button_click(t),
                               width=10, height=3, padx=8, pady=9)
            button.grid(row=(i - 1) // 3 + 1, column=(i - 1) % 3, sticky=tk.NSEW)
            buttons.append(button)

        # Configure buttons
        del_button = tk.Button(frame, text='DEL', command=self.on_del_click,
                               width=10, height=3, padx=8, pady=9)
        clr_button = tk.Button(frame, text='CLR', command=self.on_clr_click,
                               width=10, height=3, padx=8, pady=9)
        clr_history = tk.Button(frame, text='Clear History', command=self.on_clear_history_click,
                                width=10, height=3, padx=8, pady=9)
        equal_button = tk.Button(frame, text='=', command=lambda t='=': self.on_button_click(t),
                                 width=10, height=3, padx=8, pady=9)
        button0 = tk.Button(frame, text='0', command=lambda t='0': self.on_button_click(t),
                            width=10, height=3, padx=8, pady=9)
        dot_button = tk.Button(frame, text='.', command=lambda t='.': self.on_button_click(t),
                               width=10, height=3, padx=8, pady=9)

        # Position
        del_button.grid(row=0, column=1, sticky=tk.NSEW)
        clr_button.grid(row=0, column=0, sticky=tk.NSEW)
        clr_history.grid(row=0, column=2, sticky=tk.NSEW)
        equal_button.grid(row=4, column=2, sticky=tk.NSEW)
        button0.grid(row=4, column=1, sticky=tk.NSEW)
        dot_button.grid(row=4, column=0, sticky=tk.NSEW)

        buttons.append(equal_button)
        buttons.append(button0)
        buttons.append(dot_button)

        return frame

    def make_operator_pad(self) -> tk.Frame:
        """ Create Operator. """
        frame = tk.Frame(self)

        rows = 0
        column = 0

        # Operator keys
        operators = ['(', ')', '+', '-', '*', '/', '^', '%', 'exp', 'ln', 'log', 'sqrt']
        for i, operator in enumerate(operators):
            button = tk.Button(frame, text=operator, command=lambda t=operators[i]: self.on_button_click(t), width=10,
                               height=3, padx=3, pady=3)
            button.grid(row=rows, column=column, sticky=tk.NSEW)
            rows += 1
            if rows > 5:
                column += 1
                rows = 0

        return frame

    def make_history(self):
        """ Create History. """
        self.history_display = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=40, height=10, state=tk.NORMAL)
        self.history_display.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=10, pady=10)

    def update_display(self):
        """ Update Display. """
        self.display_var.set(self.model.expression)

    def update_history(self):
        """ Update History. """
        self.history_display.delete(1.0, tk.END)
        for exp, result in self.model.history:
            self.history_display.insert(tk.END, f"{exp} = {result}\n", "clickable")

    def on_del_click(self):
        self.model.delete_last()
        self.update_display()

    def on_clr_click(self):
        self.model.clear_expression()
        self.update_display()

    def on_clear_history_click(self):
        self.model.clear_history()
        self.update_history()

    def on_button_click(self, char):
        """ Check to Calculate. """
        if char == '=':
            result = self.model.evaluate_expression()
            self.model.expression = result
            self.update_display()
            self.update_history()
        else:
            self.model.add_to_expression(char)
            self.update_display()

    def run(self):
        self.mainloop()
