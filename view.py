import tkinter as tk
from model import Model


class View(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.geometry("400x600")
        self.model = Model()

        self.display_var = tk.StringVar()
        self.history_var = tk.StringVar(value="")

        self.create_widgets()

    def create_widgets(self):
        display = tk.Entry(self, textvariable=self.display_var, font=('Arial', 20), bd=10, insertwidth=4, width=20,
                           justify='right')
        display.grid(row=0, column=0, columnspan=4)

        buttons = [
            ('CLR', 1, 0), ('DEL', 1, 1), ('^', 1, 2), ('/', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('*', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
            ('0', 5, 0), ('.', 5, 1), ('mod', 5, 2), ('=', 5, 3)
        ]

        for (text, row, column) in buttons:
            button = tk.Button(self, text=text, font=('Arial', 12), padx=20, pady=20,
                               command=lambda t=text: self.on_button_click(t))
            button.grid(row=row, column=column)

        history_label = tk.Label(self, text="History", font=('Arial', 12), pady=20)
        history_label.grid(row=6, column=0, columnspan=4)

        # clear_history_button = tk.Button(self, text="Clear History", font=('Arial', 12), padx=10,
        #                                  command=self.model.clear_history)
        # clear_history_button.grid(row=7, column=0, columnspan=4)

        self.history_display = tk.Listbox(self, font=('Arial', 12), height=5)
        self.history_display.grid(row=8, column=0, columnspan=4, padx=10, pady=10)

    def update_display(self):
        self.display_var.set(self.model.expression)

    def update_history(self):
        self.history_display.delete(0, tk.END)
        for exp, result in self.model.history:
            self.history_display.insert(tk.END, f"{exp} = {result}")

    def on_button_click(self, char):
        if char == '=':
            result = self.model.evaluate_expression()
            self.update_display()
            self.update_history()
        elif char == 'CLR':
            self.model.clear_expression()
            self.update_display()
        elif char == 'DEL':
            self.model.delete_last()
            self.update_display()
        # elif char == 'Clear History':
        #     self.model.clear_history()
        #     self.update_history()
        else:
            self.model.add_to_expression(char)
            self.update_display()