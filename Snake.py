from tkinter import *
from tkinter import colorchooser
import random
import threading
import time

GAME_WIDTH_MIN = 400
GAME_HEIGHT_MIN = 400
GAME_WIDTH_MAX = 1800
GAME_HEIGHT_MAX = 1200
GAME_WIDTH = 1000
GAME_HEIGHT = 700
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
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = app.canvas.create_rectangle(x, y, x + app.space_size, y + app.space_size, fill=app.snake_color, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self, app, coords):

        wrong_coordinates = True

        while wrong_coordinates:
            wrong_coordinates = False

            x = random.randint(0, int(app.game_width / app.space_size) - 1) * app.space_size
            y = random.randint(0, int(app.game_height / app.space_size) - 1) * app.space_size

            for snake_x, snake_y in coords:
                if snake_x == x and snake_y == y:
                    wrong_coordinates = True

        self.coordinates = [x, y]

        app.canvas.create_oval(x, y, x + app.space_size, y + app.space_size, fill=app.food_color, tag="food")

class Popup:
    def __init__(self, parent):
        self.parent = parent
        self.popup = Toplevel(parent.win)
        self.popup.title("Options")
        self.popup.resizable(False, False)

        frame = Frame(self.popup)
        frame.grid()

        game_width_label = Label(frame, text="Game width:", width=16, height=2)
        game_width_label.grid(row=0, column=0)
        self.game_width_var = StringVar(value=self.parent.game_width)
        self.game_width = Spinbox(frame, from_=GAME_WIDTH_MIN, to=GAME_WIDTH_MAX, increment=self.parent.space_size,
                                  textvariable=self.game_width_var, width=16,
                                  command=self.change_game_width)
        self.game_width.grid(row=0, column=1)

        game_height_label = Label(frame, text="Game height:", width=16, height=2)
        game_height_label.grid(row=1, column=0)
        self.game_height_var = StringVar(value=self.parent.game_height)
        self.game_height = Spinbox(frame, from_=GAME_HEIGHT_MIN, to=GAME_HEIGHT_MAX, increment=self.parent.space_size,
                                   textvariable=self.game_height_var, width=16, command=self.change_game_height)
        self.game_height.grid(row=1, column=1)

        game_speed_label = Label(frame, text="Game speed:", width=16, height=2)
        game_speed_label.grid(row=2, column=0)
        self.game_speed_var = StringVar(value=self.parent.game_speed)
        self.game_speed = Spinbox(frame, from_=1, to=10, textvariable=self.game_speed_var,
                                  width=16, command=self.change_game_speed)
        self.game_speed.grid(row=2, column=1)

        space_size_label = Label(frame, text="Space size:", width=16, height=2)
        space_size_label.grid(row=3, column=0)
        self.space_size_var = StringVar(value=self.parent.space_size)
        self.space_size = Spinbox(frame, from_=10, to=100, increment=10, textvariable=self.space_size_var,
                                  width=16, command=self.change_space_size)
        self.space_size.grid(row=3, column=1)

        body_parts_label = Label(frame, text="Body parts:", width=16, height=2)
        body_parts_label.grid(row=4, column=0)
        self.body_parts_var = StringVar(value=self.parent.body_parts)
        self.body_parts = Spinbox(frame, from_=1, to=100, textvariable=self.body_parts_var,
                                  width=16, command=self.change_body_parts)
        self.body_parts.grid(row=4, column=1)

        snake_color_label = Label(frame, text="Snake color:", width=16, height=2)
        snake_color_label.grid(row=5, column=0)
        self.snake_color = Button(frame, relief="sunken", borderwidth=2, bg=self.parent.snake_color,
                                  width=14, command=self.change_snake_color)
        self.snake_color.grid(row=5, column=1)

        food_color_label = Label(frame, text="Food color:", width=16, height=2)
        food_color_label.grid(row=6, column=0)
        self.food_color = Button(frame, relief="sunken", borderwidth=2, bg=self.parent.food_color,
                                 width=14, command=self.change_food_color)
        self.food_color.grid(row=6, column=1)

        background_color_label = Label(frame, text="Background color:", width=16, height=2)
        background_color_label.grid(row=7, column=0)
        self.background_color = Button(frame, relief="sunken", borderwidth=2, bg=self.parent.background_color,
                                       width=14, command=self.change_background_color)
        self.background_color.grid(row=7, column=1)

        close_button = Button(frame, text="OK", width=10, command=self.ok_button)
        close_button.grid(row=10, column=0)

        default_button = Button(frame, text="Default", width=10, command=self.default_button)
        default_button.grid(row=10, column=1)

        popup_width = 250
        popup_height = 320
        popup_x = parent.x + int((parent.window_width - popup_width) / 2)
        popup_y = parent.y + int((parent.window_height - popup_height) / 2)

        self.popup.geometry(f"{popup_width}x{popup_height}+{popup_x}+{popup_y}")

        self.popup.transient(parent.win)
        self.popup.grab_set()
        self.popup.focus_set()
        self.popup.wait_window()

    def ok_button(self):
        self.popup.destroy()
        self.parent.resize()
        self.parent.new_game()

    def default_button(self):
        self.parent.game_width = GAME_WIDTH
        self.parent.game_height = GAME_HEIGHT
        self.parent.game_speed = SPEED
        self.parent.space_size = SPACE_SIZE
        self.parent.body_parts = BODY_PARTS
        self.parent.snake_color = SNAKE_COLOR
        self.parent.food_color = FOOD_COLOR
        self.parent.background_color = BACKGROUND_COLOR

        self.game_width_var.set(str(GAME_WIDTH))
        self.game_height_var.set(str(GAME_HEIGHT))
        self.game_speed_var.set(str(SPEED))
        self.space_size_var.set(str(SPACE_SIZE))
        self.body_parts_var.set(str(BODY_PARTS))
        self.snake_color.config(bg=SNAKE_COLOR)
        self.food_color.config(bg=FOOD_COLOR)
        self.background_color.config(bg=BACKGROUND_COLOR)

    def change_game_width(self):
        self.parent.game_width = int(self.game_width.get())

    def change_game_height(self):
        self.parent.game_height = int(self.game_height.get())

    def change_game_speed(self):
        self.parent.game_speed = int(self.game_speed.get())

    def change_space_size(self):
        self.parent.space_size = int(self.space_size.get())

    def change_body_parts(self):
        self.parent.body_parts = int(self.body_parts.get())

    def change_snake_color(self):
        if color := colorchooser.askcolor(title="Pick a color of shake")[1]:
            self.parent.snake_color = color
            self.snake_color.config(bg=color)

    def change_food_color(self):
        if color := colorchooser.askcolor(title="Pick a color of food")[1]:
            self.parent.food_color = color
            self.food_color.config(bg=color)

    def change_background_color(self):
        if color := colorchooser.askcolor(title="Pick a background color")[1]:
            self.parent.background_color = color
            self.background_color.config(bg=color)

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
        self.thread_is_alive = False
        self.old_game_speed = self.game_speed


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

        self.win.bind('<Left>', lambda event: self.change_direction('left'))
        self.win.bind('<Right>', lambda event: self.change_direction('right'))
        self.win.bind('<Up>', lambda event: self.change_direction('up'))
        self.win.bind('<Down>', lambda event: self.change_direction('down'))
        self.before_new_game()

    def speed_up(self, event):
        if self.old_game_speed == self.game_speed:
            self.old_game_speed = self.game_speed
        self.game_speed = 10

    def win_init(self):
        self.win.update()

        self.window_width = self.canvas.winfo_width()
        self.window_height = self.canvas.winfo_height() + self.label.winfo_height() + self.menu_bar.winfo_height()

        self.x = int(self.win.winfo_screenwidth()/2 - self.window_width/2)
        self.y = int(self.win.winfo_screenheight()/2 - self.window_height/2)

        self.win.geometry(f"{self.window_width}x{self.window_height}+{self.x}+{self.y}")

    def resize(self):
        self.win.geometry("1900x1200")
        self.canvas.config(bg=self.background_color, height=self.game_height, width=self.game_width)
        self.win_init()

    def before_new_game(self):
        self.new_game_text = self.canvas.create_text(self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2,
                                font=('consolas', 25), text="Press any button to\nstart a new game...", fill="white", tag="newgame")

        self.game_speed = self.old_game_speed

        self.win.unbind('<space>')
        self.win.bind('<KeyPress>', self.new_game)

        self.menu_bar.entryconfig(1, state="normal")
        self.menu_bar.entryconfig(2, state="normal")

        self.thread = threading.Thread(target=self.blink_text)
        self.thread.start()

    def blink_text(self):
        colors = ["#FF0000", "#00FF00", "#0000FF"]
        self.thread_is_alive = True

        while self.thread_is_alive:
            try:
                self.current_color = self.canvas.itemconfigure("newgame")["fill"][4]

                if self.current_color == colors[0]:
                    self.canvas.itemconfigure("newgame", fill=colors[1])
                elif self.current_color == colors[1]:
                    self.canvas.itemconfigure("newgame", fill=colors[2])
                elif self.current_color == colors[2]:
                    self.canvas.itemconfigure("newgame", fill=colors[0])
                else:
                    self.canvas.itemconfigure("newgame", fill=colors[1])
                time.sleep(1)
            except:
                self.thread_is_alive = False

    def close(self):
        self.thread_is_alive = False
        if self.thread.is_alive():
            del self.thread
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

        if self.check_collisions(snake):
            self.game_over()
        else:
            self.win.after(int(300/self.game_speed), self.next_turn, snake, food)

    def change_direction(self,new_direction):
        if ((new_direction == 'left' and self.direction != 'right')
                or (new_direction == 'right' and self.direction != 'left')
                or (new_direction == 'up' and self.direction != 'down')
                or (new_direction == 'down' and self.direction != 'up')):
            self.direction = new_direction

    def check_collisions(self, snake):
        x, y = snake.coordinates[0]

        if (x < 0 or x >= self.game_width) or (y < 0 or y >= self.game_height):
            return True

        for body_part in snake.coordinates[1:]:
            if x == body_part[0] and y == body_part[1]:
                return True

        return False

    def game_over(self):
        self.canvas.delete(ALL)
        self.canvas.create_text(self.canvas.winfo_width()/2, self.canvas.winfo_height()/2 - 120,
                           font=('consolas', 60), text="GAME OVER", fill="red", tag="gameover")

        self.before_new_game()

    def new_game(self, event=None):

        self.menu_bar.entryconfig(1, state="disabled")
        self.menu_bar.entryconfig(2, state="disabled")

        self.thread_is_alive = False

        self.win.bind('<space>', self.speed_up)
        self.win.unbind('<KeyPress>')
        self.canvas.delete(ALL)

        self.score = 0
        self.direction = 'down'
        self.label.config(text="Score: 0")

        self.snake = Snake(self)
        self.food = Food(self, self.snake.coordinates)

        self.next_turn(self.snake, self.food)

    def options(self):
        popup = Popup(self)

if __name__ == '__main__':
    app = App()
    app.run()