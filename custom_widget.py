from tkinter import *

class CustomWidget:
    def __init__(self, params):
        self.parent = params['parent']
        self.label_text = params['label']
        self.row = params['row']
        self.command = params['command'] if 'command' in params else ""
        self.default_text = params['default_text']
        self.default_fg = params['default_fg'] if 'default_fg' in params else "#000000"

        # Label before widget
        label = Label(self.parent, text=self.label_text, height=2)
        label.grid(row=self.row, column=0)
        # Widget
        # Label after widget
        label_min_max = Label(self.parent, text=self.default_text, height=2, fg=self.default_fg)
        label_min_max.grid(row=self.row, column=2)


class CustomColorButton(CustomWidget):

    def __init__(self, params):
        super().__init__(params)
        self.bg = params['bg']

        # Widget
        self.button = Button(self.parent, relief="sunken", borderwidth=2, bg=self.bg, width=14, command=self.command)
        self.button.grid(row=self.row, column=1)


class CustomSpinbox(CustomWidget):

    def __init__(self, params):
        super().__init__(params)
        self.var_value = params['var_value']
        self.value_from = params['from']
        self.value_to = params['to']
        self.increment = params['increment'] if 'increment' in params else 1

        # Widget
        self.text_var = StringVar(value=self.var_value)
        self.spinbox = Spinbox(self.parent, from_=self.value_from, to=self.value_to, increment=self.increment,
                               textvariable=self.text_var, width=14, command=self.command, state="readonly")
        self.spinbox.grid(row=self.row, column=1)
