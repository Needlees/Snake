import pytest

from src.snake import App


@pytest.fixture(scope="class")
def app():
    app = App(debug=True)
    yield app
    app.close()


@pytest.fixture(scope="class")
def game():
    app = App(debug=True)
    app.new_game()
    yield app.game
    app.close()


@pytest.fixture(scope="class")
def popup():
    app = App(debug=True)
    app.win.after(100, lambda: app.win.destroy())
    app.options()
    yield app.popup



class TestPopup:
    def test_popup(self, popup):
        assert popup.snake_color == popup.parent.snake_color

class TestApp:
    def test_score_label(self, app):
        score_text = app.label_score.cget("text")
        assert score_text == "Score: 0"

    def test_random_position(self, app):
        coords = app.random_position()
        assert coords
        assert isinstance(coords, tuple)

    def test_draw_snake_part(self, app):
        snake_part = app.draw_snake_part(*app.random_position())
        assert isinstance(snake_part, int)
        app.canvas.delete(snake_part)

    def test_draw_food(self, app):
        food = app.draw_food(*app.random_position())
        assert isinstance(food, int)
        app.canvas.delete(food)

    def test_erase_snake_tail(self, app):
        cnt = len(app.canvas.find_all())

        tail = app.draw_snake_part(*app.random_position())
        assert len(app.canvas.find_all()) == cnt + 1

        app.erase_snake_tail(tail)
        assert len(app.canvas.find_all()) == cnt

    def test_erase_food(self, app):
        cnt = len(app.canvas.find_withtag("food"))

        app.draw_food(*app.random_position())
        assert len(app.canvas.find_withtag("food")) == cnt + 1

        app.erase_food()
        assert len(app.canvas.find_withtag("food")) == cnt

    def test_redraw_score(self, app):
        def get_score():
            score_text = app.label_score.cget("text")
            return int(score_text.split()[-1])

        assert get_score() == 0
        app.game.score = 25
        app.redraw_score()
        assert get_score() == 25
        app.game.score = 0

    def test_init_new_game(self, app):
        app.init_new_game()
        assert len(app.canvas.find_withtag("gameover")) == 1
        assert app.menu_bar.entrycget(1, "state") == 'normal'
        assert app.menu_bar.entrycget(2, "state") == 'normal'
        assert app.win.bind() == ()

    def test_new_game(self, app):
        app.new_game()
        assert len(app.canvas.find_withtag("gameover")) == 0
        assert app.menu_bar.entrycget(1, "state") == 'disabled'
        assert app.menu_bar.entrycget(2, "state") == 'disabled'
        assert app.win.bind() != ()
        app.init_new_game()

    def test_win_resize(self, app):
        app.game_width = 500
        app.game_height = 500
        app.win_resize()
        assert int(app.canvas["width"]) == 500
        assert int(app.canvas["height"]) == 500


class TestGame:
    def test_food(self, game):
        game.reset()
        coords = game.food.coordinates
        assert coords
        game.food.respawn()
        coords = game.food.coordinates
        assert coords

    def test_snake(self, game):
        game.reset()
        coords = game.snake.coordinates
        assert coords
        squares = game.snake.squares
        assert squares
        assert game.app.body_parts == len(coords)
        assert game.app.body_parts == len(squares)

    def test_reset(self, game):
        game.score = 10
        game.direction = 'up'
        del game.food
        del game.snake
        game.reset()
        assert game.score == 0
        assert game.direction == 'down'
        assert game.food
        assert game.snake

    @pytest.mark.parametrize(
        "snake_coords, food_coords, direction, res",
        [
            ([(100, 100)], (100, 110), "down", False),
            ([(100, 100)], (100, 110), "up", True),
            ([(100, 100)], (90, 100), "left", False),
            ([(100, 100)], (90, 100), "right", True),
            ([(0, 0)], (90, 100), "left", True),
        ]
    )
    def test_next_turn(self, snake_coords, food_coords, direction, res, game):
        game.food.coordinates = food_coords
        game.snake.coordinates = snake_coords
        game.app.space_size = 10

        game.direction = direction
        game.next_turn()
        assert (game.food.coordinates == food_coords) == res
        game.reset()

    @pytest.mark.parametrize(
        "direction, new_direction, res",
        [
            ('up', 'down', False),
            ('left', 'right', False),
            ('left', 'up', True),
            ('down', 'right', True),
        ]
    )
    def test_change_direction(self, direction, new_direction, res, game):
        game.direction = direction
        game.change_direction(new_direction)
        assert (game.direction == new_direction) == res

    @pytest.mark.parametrize(
        "coords, res",
        [
            ([(-1, -1)], True),
            ([(100, 100), (110, 100)], False)
        ]
    )
    def test_check_collisions(self, coords, res, game):
        assert game.check_collisions(coords) == res

    def test_speed_up(self, game):
        game_speed = game.game_speed
        game.speed_up()
        assert game.game_speed > game_speed
        game.game_speed = game_speed

    def test_game_over(self, game):
        game.game_over()
