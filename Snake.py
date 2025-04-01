import asyncio
from tkinter import *
from tkinter import colorchooser
from random import randint

GAME_WIDTH_MIN = 400
GAME_HEIGHT_MIN = 400
GAME_WIDTH_MAX = 1800
GAME_HEIGHT_MAX = 1100
GAME_WIDTH = 990
GAME_HEIGHT = 690
SPEED = 4
SPACE_SIZE = 30
BODY_PARTS = 7
SNAKE_COLOR = "#88FF88"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"


class Snake:
    def __init__(self, app):
        self.body_size = app.body_parts
        self.coordinates = []
        self.squares = []

        for i in range(0, app.body_parts):
            self.coordinates.append((-i, -i))
            square = app.canvas.create_rectangle(0, 0, app.space_size, app.space_size, fill=app.snake_color,
                                                 tag="snake")
            self.squares.append(square)


class Food:
    def __init__(self, app, coords):

        wrong_coordinates = True

        while wrong_coordinates:
            wrong_coordinates = False

            x = randint(0, int(app.game_width / app.space_size) - 1) * app.space_size
            y = randint(0, int(app.game_height / app.space_size) - 1) * app.space_size

            for snake_x, snake_y in coords:
                if snake_x == x and snake_y == y:
                    wrong_coordinates = True

        self.coordinates = [x, y]

        app.canvas.create_oval(x, y, x + app.space_size, y + app.space_size, fill=app.food_color, tag="food")


class CustomControl:

    def __init__(self, params):
        self.parent = params['parent']
        self.label_text = params['label']
        self.row = params['row']
        self.command = params['command']
        self.default_text = params['default_text']
        self.default_fg = params['default_fg'] if 'default_fg' in params else "#000000"

        # Label before control
        label = Label(self.parent, text=self.label_text, height=2)
        label.grid(row=self.row, column=0)
        # Control
        # Label after control
        label_min_max = Label(self.parent, text=self.default_text, height=2, fg=self.default_fg)
        label_min_max.grid(row=self.row, column=2)


class CustomColorButton(CustomControl):

    def __init__(self, params):
        super().__init__(params)
        self.bg = params['bg']

        # Control
        self.button = Button(self.parent, relief="sunken", borderwidth=2, bg=self.bg, width=14, command=self.command)
        self.button.grid(row=self.row, column=1)


class CustomComboBox(CustomControl):

    def __init__(self, params):
        super().__init__(params)
        self.var_value = params['var_value']
        self.value_from = params['from']
        self.value_to = params['to']
        self.increment = params['increment'] if 'increment' in params else 1

        # Control
        self.string_var = StringVar(value=self.var_value)
        self.spinbox = Spinbox(self.parent, from_=self.value_from, to=self.value_to, increment=self.increment,
                               textvariable=self.string_var, width=14, command=self.command)
        self.spinbox.grid(row=self.row, column=1)
        self.spinbox.bind("<FocusOut>", self.command)


class Popup:
    def __init__(self, parent):
        self.parent = parent
        self.popup = Toplevel(parent.win)
        self.popup.title("Options")
        self.popup.resizable(False, False)

        self.old_game_width = self.parent.game_width
        self.old_game_height = self.parent.game_height
        self.old_game_speed = self.parent.game_speed
        self.old_space_size = self.parent.space_size
        self.old_body_parts = self.parent.body_parts
        self.old_snake_color = self.parent.snake_color
        self.old_food_color = self.parent.food_color
        self.old_background_color = self.parent.background_color

        frame = Frame(self.popup)
        frame.grid()

        self.game_width = CustomComboBox({
            'parent': frame,
            'label': "Game width:",
            'row': 0,
            'var_value': self.parent.game_width,
            'from': GAME_WIDTH_MIN,
            'to': GAME_WIDTH_MAX,
            'increment': self.parent.space_size,
            'command': self.change_game_width,
            'default_text': f"(min: {GAME_WIDTH_MIN}, max: {GAME_WIDTH_MAX}, step:*)"
        })

        self.game_height = CustomComboBox({
            'parent': frame,
            'label': "Game height:",
            'row': 1,
            'var_value': self.parent.game_height,
            'from': GAME_HEIGHT_MIN,
            'to': GAME_HEIGHT_MAX,
            'increment': self.parent.space_size,
            'command': self.change_game_height,
            'default_text': f"(min: {GAME_HEIGHT_MIN}, max: {GAME_HEIGHT_MAX}, step:*)"
        })

        self.game_speed = CustomComboBox({
            'parent': frame,
            'label': "Game speed:",
            'row': 2,
            'var_value': self.parent.game_speed,
            'from': 1,
            'to': 10,
            'command': self.change_game_speed,
            'default_text': "(min: 1, max: 10)"
        })

        self.space_size = CustomComboBox({
            'parent': frame,
            'label': "Space size:",
            'row': 3,
            'var_value': self.parent.space_size,
            'from': 10,
            'to': 100,
            'increment': 10,
            'command': self.change_space_size,
            'default_text': "(min: 10, max: 100, step: 10)"
        })

        self.body_parts = CustomComboBox({
            'parent': frame,
            'label': "Body parts:",
            'row': 4,
            'var_value': self.parent.body_parts,
            'from': 1,
            'to': 100,
            'command': self.change_body_parts,
            'default_text': "(min: 1, max: 100)"
        })

        self.snake_color = CustomColorButton({
            'parent': frame,
            'label': "Snake color:",
            'row': 5,
            'bg': self.parent.snake_color,
            'command': self.change_snake_color,
            'default_text': f"(default: {self.parent.snake_color})",
            'default_fg': SNAKE_COLOR
        })

        self.food_color = CustomColorButton({
            'parent': frame,
            'label': "Food color:",
            'row': 6,
            'bg': self.parent.food_color,
            'command': self.change_food_color,
            'default_text': f"(default: {self.parent.food_color})",
            'default_fg': FOOD_COLOR
        })

        self.background_color = CustomColorButton({
            'parent': frame,
            'label': "Background:",
            'row': 7,
            'bg': self.parent.background_color,
            'command': self.change_background_color,
            'default_text': f"(default: {self.parent.background_color})",
            'default_fg': BACKGROUND_COLOR
        })

        label_frame = Frame(self.popup)
        label_frame.grid()
        label = Label(label_frame, text="*step dependent from Space size", justify="left")
        label.grid(row=0, column=0)

        button_frame = Frame(self.popup)
        button_frame.grid()

        close_button = Button(button_frame, text="OK", width=10, command=self.ok_button)
        close_button.grid(row=0, column=0, padx=10, pady=10)

        cancel_button = Button(button_frame, text="Cancel", width=10, command=self.cancel_button)
        cancel_button.grid(row=0, column=1)

        default_button = Button(button_frame, text="Default", width=10, command=self.default_button)
        default_button.grid(row=0, column=2, padx=10)

        self.popup.update()

        popup_width = self.popup.winfo_width()
        popup_height = self.popup.winfo_height()
        popup_x = parent.x + int((parent.window_width - popup_width) / 2)
        popup_y = parent.y + int((parent.window_height - popup_height) / 2)

        self.popup.geometry(f"{popup_width}x{popup_height}+{popup_x}+{popup_y}")

        self.popup.transient(parent.win)
        self.popup.grab_set()
        self.popup.focus_set()
        self.popup.wait_window()

    def ok_button(self):

        if self.parent.game_width != int(self.game_width.spinbox.get()):
            self.change_game_width()
        if self.parent.game_height != int(self.game_height.spinbox.get()):
            self.change_game_height()
        if (self.parent.old_game_speed != int(self.game_speed.spinbox.get()) or
                self.parent.game_speed != int(self.game_speed.spinbox.get())):
            self.change_game_speed()
        if self.parent.space_size != int(self.space_size.spinbox.get()):
            self.change_space_size()
        if self.parent.body_parts != int(self.body_parts.spinbox.get()):
            self.change_body_parts()

        self.popup.destroy()

        if self.parent.game_width != self.old_game_width or self.parent.game_height != self.old_game_height:
            self.parent.resize()

        self.parent.canvas.delete(ALL)
        self.parent.canvas.config(bg=self.parent.background_color)
        self.parent.before_new_game()

    def cancel_button(self):
        self.parent.game_width = self.old_game_width
        self.parent.game_height = self.old_game_height
        self.parent.game_speed = self.old_game_speed
        self.parent.space_size = self.old_space_size
        self.parent.body_parts = self.old_body_parts
        self.parent.snake_color = self.old_snake_color
        self.parent.food_color = self.old_food_color
        self.parent.background_color = self.old_background_color
        self.popup.destroy()

    def default_button(self):
        self.parent.game_width = GAME_WIDTH
        self.parent.game_height = GAME_HEIGHT
        self.parent.game_speed = SPEED
        self.parent.space_size = SPACE_SIZE
        self.parent.body_parts = BODY_PARTS
        self.parent.snake_color = SNAKE_COLOR
        self.parent.food_color = FOOD_COLOR
        self.parent.background_color = BACKGROUND_COLOR

        self.game_width.string_var.set(str(GAME_WIDTH))
        self.game_height.string_var.set(str(GAME_HEIGHT))
        self.game_speed.string_var.set(str(SPEED))
        self.space_size.string_var.set(str(SPACE_SIZE))
        self.body_parts.string_var.set(str(BODY_PARTS))
        self.snake_color.button.config(bg=SNAKE_COLOR)
        self.food_color.button.config(bg=FOOD_COLOR)
        self.background_color.button.config(bg=BACKGROUND_COLOR)

    def change_game_width(self, Event=None):
        width = int(self.game_width.spinbox.get())

        division_width = width / self.parent.space_size
        integer_division_width = width // self.parent.space_size

        if width == GAME_WIDTH_MIN and integer_division_width != division_width:

            self.parent.game_width = integer_division_width * self.parent.space_size + self.parent.space_size
            self.game_width.string_var.set(str(self.parent.game_width))

        elif integer_division_width != division_width:
            self.parent.game_width = integer_division_width * self.parent.space_size
            self.game_width.string_var.set(str(self.parent.game_width))

        else:
            self.parent.game_width = width

    def change_game_height(self, Event=None):
        height = int(self.game_height.spinbox.get())

        division_height = height / self.parent.space_size
        integer_division_height = height // self.parent.space_size

        if height == GAME_HEIGHT_MIN and integer_division_height != division_height:

            self.parent.game_height = integer_division_height * self.parent.space_size + self.parent.space_size
            self.game_height.string_var.set(str(self.parent.game_height))

        elif integer_division_height != division_height:

            self.parent.game_height = integer_division_height * self.parent.space_size
            self.game_height.string_var.set(str(self.parent.game_height))

        else:
            self.parent.game_height = height

    def change_game_speed(self, Event=None):
        self.parent.game_speed = int(self.game_speed.spinbox.get())
        self.parent.old_game_speed = self.parent.game_speed

    def change_space_size(self, Event=None):
        self.parent.space_size = int(self.space_size.spinbox.get())

        width = int(self.game_width.spinbox.get())

        division_width = width / self.parent.space_size
        integer_division_width = width // self.parent.space_size

        if width <= GAME_WIDTH_MIN or width >= GAME_WIDTH_MAX or integer_division_width != division_width:

            width = integer_division_width * self.parent.space_size

            if width > GAME_WIDTH_MAX:
                width = integer_division_width * self.parent.space_size - self.parent.space_size
            elif width < GAME_WIDTH_MIN:
                width = integer_division_width * self.parent.space_size + self.parent.space_size

        height = int(self.game_height.spinbox.get())

        division_height = height / self.parent.space_size
        integer_division_height = height // self.parent.space_size

        if height <= GAME_HEIGHT_MIN or height >= GAME_HEIGHT_MAX or integer_division_height != division_height:

            height = integer_division_height * self.parent.space_size

            if height > GAME_HEIGHT_MAX:
                height = integer_division_height * self.parent.space_size - self.parent.space_size
            elif height < GAME_HEIGHT_MIN:
                height = integer_division_height * self.parent.space_size + self.parent.space_size

        self.parent.game_height = height
        self.parent.game_width = width

        self.game_width.string_var.set(str(self.parent.game_width))
        self.game_height.string_var.set(str(self.parent.game_height))

        self.game_width.spinbox.config(increment=self.parent.space_size)
        self.game_height.spinbox.config(increment=self.parent.space_size)

    def change_body_parts(self, Event=None):
        self.parent.body_parts = int(self.body_parts.spinbox.get())

    def change_snake_color(self):
        if color := colorchooser.askcolor(title="Pick a color of shake")[1]:
            self.parent.snake_color = color
            self.snake_color.button.config(bg=color)

    def change_food_color(self):
        if color := colorchooser.askcolor(title="Pick a color of food")[1]:
            self.parent.food_color = color
            self.food_color.button.config(bg=color)

    def change_background_color(self):
        if color := colorchooser.askcolor(title="Pick a background color")[1]:
            self.parent.background_color = color
            self.background_color.button.config(bg=color)


class App:
    def __init__(self):
        self.win = Tk()
        self.win.title("Snake game")
        self.win.resizable(False, False)

        self.game_width = GAME_WIDTH
        self.game_height = GAME_HEIGHT
        self.game_speed = SPEED
        self.space_size = SPACE_SIZE
        self.body_parts = BODY_PARTS
        self.snake_color = SNAKE_COLOR
        self.food_color = FOOD_COLOR
        self.background_color = BACKGROUND_COLOR

        self.score = 0
        self.direction = 'down'
        self.old_game_speed = self.game_speed
        self.stop_task = True

        self.label = Label(self.win, text="Score: {}".format(self.score), font=('consolas', 40))
        self.label.pack()

        self.canvas = Canvas(self.win, bg=self.background_color, height=self.game_height, width=self.game_width)
        self.canvas.pack()

        self.menu_bar = Menu(self.win)
        self.win.config(menu=self.menu_bar)
        self.menu_bar.add_command(label="New Game", command=self.new_game)
        self.menu_bar.add_command(label="Options", command=self.options)
        self.menu_bar.add_command(label="Exit", command=self.close)

        self.win_init()

        self.win.protocol("WM_DELETE_WINDOW", self.close)

        self.before_new_game()

    def bind_keys(self):
        self.win.bind('<Left>', lambda event: self.change_direction('left'))
        self.win.bind('<Right>', lambda event: self.change_direction('right'))
        self.win.bind('<Up>', lambda event: self.change_direction('up'))
        self.win.bind('<Down>', lambda event: self.change_direction('down'))
        self.win.bind('<space>', self.speed_up)

    def unbind_keys(self):
        self.win.unbind('<Left>')
        self.win.unbind('<Right>')
        self.win.unbind('<Up>')
        self.win.unbind('<Down>')
        self.win.unbind('<space>')

    def speed_up(self, event):
        self.game_speed = 10

    def win_init(self):
        self.win.update()

        self.window_width = self.canvas.winfo_width()
        self.window_height = self.canvas.winfo_height() + self.label.winfo_height() + self.menu_bar.winfo_height()

        self.x = int(self.win.winfo_screenwidth() / 2 - self.window_width / 2)
        self.y = int(self.win.winfo_screenheight() / 2 - self.window_height / 2)

        self.win.geometry(f"{self.window_width}x{self.window_height}+{self.x}+{self.y}")

    def resize(self):
        # self.win.geometry(f"{GAME_WIDTH_MAX + 200}x{GAME_HEIGHT_MAX + 100}")
        self.win.geometry("1900x1400")
        self.canvas.config(height=self.game_height, width=self.game_width)
        self.win_init()

    def before_new_game(self):
        self.new_game_text = self.canvas.create_text(
            self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2,
            font=('consolas', 25),
            text="Press any key to\nstart a new game...", fill="#FFFFFF",
            tag="newgame"
        )

        self.game_speed = self.old_game_speed
        self.unbind_keys()

        self.menu_bar.entryconfig(1, state="normal")
        self.menu_bar.entryconfig(2, state="normal")

        if self.stop_task:
            asyncio.run(self.wait_keypress())

    async def blink_text(self):
        colors = ["#FFFFFF", "#FF0000", "#00FF00", "#0000FF"]

        while True:
            current_color = self.canvas.itemconfigure("newgame")["fill"][4]
            next_color = colors[colors.index(current_color) - 1]
            self.canvas.itemconfigure("newgame", fill=next_color)
            await asyncio.sleep(1)

    async def win_update(self):
        while True:
            self.win.update()
            await asyncio.sleep(0.01)

    async def wait_keypress(self):
        self.stop_task = False
        self.win.bind("<KeyPress>", self.new_game)

        blink_text_task = asyncio.create_task(self.blink_text())
        win_update_task = asyncio.create_task(self.win_update())

        while not self.stop_task:
            await asyncio.sleep(0.1)

        blink_text_task.cancel()

        try:
            await blink_text_task
            await win_update_task
        except asyncio.CancelledError:
            print("\nАсинхронная задача остановлена!")

    def close(self):
        self.stop_task = True
        self.win.destroy()

    def run(self):
        self.win.mainloop()

    def next_turn(self, snake, food):
        x, y = snake.coordinates[0]

        if self.direction == "up":
            y -= self.space_size
        elif self.direction == "down":
            y += self.space_size
        elif self.direction == "left":
            x -= self.space_size
        elif self.direction == "right":
            x += self.space_size

        snake.coordinates.insert(0, (x, y))
        square = self.canvas.create_rectangle(x, y, x + self.space_size, y + self.space_size, fill=self.snake_color)
        snake.squares.insert(0, square)

        if x == food.coordinates[0] and y == food.coordinates[1]:
            self.score += 1
            self.label.config(text="Score: {}".format(self.score))
            self.canvas.delete("food")

            self.game_speed = self.old_game_speed
            food = Food(self, snake.coordinates)
        else:
            del snake.coordinates[-1]
            self.canvas.delete(snake.squares[-1])
            del snake.squares[-1]

        if self.check_collisions(snake.coordinates):
            self.game_over()
        else:
            self.win.after(int(300 / self.game_speed), self.next_turn, snake, food)

    def change_direction(self, new_direction):
        if ((new_direction == 'left' and self.direction != 'right')
                or (new_direction == 'right' and self.direction != 'left')
                or (new_direction == 'up' and self.direction != 'down')
                or (new_direction == 'down' and self.direction != 'up')):
            self.direction = new_direction

    def check_collisions(self, coords):

        x, y = coords[0]
        if (x < 0 or x >= self.game_width) or (y < 0 or y >= self.game_height):
            return True

        if len(coords) != len(set(coords)):
            return True

        return False

    def game_over(self):
        self.canvas.delete(ALL)
        self.canvas.create_text(
            self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2 - 120,
            font=('consolas', 60),
            text="GAME OVER",
            fill="red",
            tag="gameover"
        )

        self.before_new_game()

    def new_game(self, event=None):
        self.stop_task = True
        self.menu_bar.entryconfig(1, state="disabled")
        self.menu_bar.entryconfig(2, state="disabled")

        self.canvas.delete(ALL)

        self.score = 0
        self.direction = 'down'
        self.label.config(text="Score: 0")
        self.bind_keys()

        self.snake = Snake(self)
        self.food = Food(self, self.snake.coordinates)

        self.next_turn(self.snake, self.food)

    def options(self):
        popup = Popup(self)


if __name__ == '__main__':
    app = App()
    app.run()
