import flet as ft
import time
import random

SNAKE_BODY_SIZE = 3
SCORE = 0
DEFAULT_PIXEL = 40


class WhiteSquare(ft.Container):
    def __init__(self, left_padding, color):
        super().__init__()
        self.width = DEFAULT_PIXEL
        self.height = DEFAULT_PIXEL
        self.bgcolor = color
        self.left = left_padding
        self.top = DEFAULT_PIXEL * 4


class ScoreBoard(ft.Text):
    def __init__(self, player_score, left_padding):
        super().__init__()
        self.value = player_score
        self.size = DEFAULT_PIXEL * 2
        self.left = left_padding
        self.opacity = 0.5
        # self.top = top_padding
        # self.font =


snake_movement_state = [True, False, False, False]  # Go Right, Go left, Go Down, Go Up

colors = ['white', 'green', 'blue', 'yellow', 'black']


def main(page: ft.Page):
    global SCORE

    def page_resize(e):
        print("New page size:", page.window_width, page.window_height)

    page.on_resize = page_resize
    page.padding = 0
    snake_body = []
    left_padding = DEFAULT_PIXEL * 6

    food = WhiteSquare(DEFAULT_PIXEL * 15, "red")
    page.add(food)

    for x in range(SNAKE_BODY_SIZE):
        snake_body.append(WhiteSquare(left_padding=left_padding, color="white"))
        left_padding -= DEFAULT_PIXEL

    def on_keyboard(e: ft.KeyboardEvent):
        # print(f"Key: {e.key}, Shift: {e.shift}, Control: {e.ctrl}, Alt: {e.alt}, Meta: {e.meta}")
        if e.key == "Arrow Right":
            for x in range(len(snake_movement_state)):
                snake_movement_state[x] = False
            snake_movement_state[0] = True
        elif e.key == "Arrow Left":
            for x in range(len(snake_movement_state)):
                snake_movement_state[x] = False
            snake_movement_state[1] = True
        elif e.key == "Arrow Down":
            for x in range(len(snake_movement_state)):
                snake_movement_state[x] = False
            snake_movement_state[2] = True
        elif e.key == "Arrow Up":
            for x in range(len(snake_movement_state)):
                snake_movement_state[x] = False
            snake_movement_state[3] = True

    page.on_keyboard_event = on_keyboard

    score_board = ScoreBoard(f"Your Score: {SCORE}", (int(page.width) / 3))

    mother_container = ft.Container(
        ft.Stack(
            controls=[
                score_board,
                ft.Container(
                    ft.Stack(
                        controls=[food]
                    )
                ),
                ft.Container(
                    ft.Stack(
                        controls=snake_body
                    )
                ),
            ]
        ),
        expand=True,
        bgcolor=ft.colors.CYAN_900,
    )

    page.overlay.append(mother_container)

    while True:

        # print(f"Snake's head top - food's top: {int(snake_body[0].top) - int(food.top)}")
        # print(f"Snake's head left - food's left: {int(snake_body[0].left) - int(food.left)}")

        # print("food: ", food.top, food.left)
        # print("snake: ", snake_body[0].top, snake_body[0].left)

        if snake_body[0].top == food.top and snake_body[0].left == food.left:
            # print("Snake just ate the food")
            # print(f"page width {page.width}, height {page.height}")
            # print(f"page width {int(page.width / DEFAULT_PIXEL) - 1}, height {int(page.height / DEFAULT_PIXEL) - 1}")

            food.top = random.randint(2, int(page.height / DEFAULT_PIXEL) - int(DEFAULT_PIXEL / 8)) * DEFAULT_PIXEL
            # print(f"food top new position: {food.top}")
            food.left = random.randint(2, int(page.width / DEFAULT_PIXEL) - int(DEFAULT_PIXEL / 8)) * DEFAULT_PIXEL
            # print(f"food left new position: {food.left}")

            snake_body.append(WhiteSquare(left_padding=left_padding, color="white"))

            SCORE += 1
            score_board.value = f"Your Score: {SCORE}"
            # food.visible = False

        for x in range(len(snake_body) - 1, 0, -1):
            snake_body[x].left = snake_body[x - 1].left
            snake_body[x].top = snake_body[x - 1].top

        for x in range(len(snake_movement_state)):
            if x == 0 and snake_movement_state[x] is True:
                snake_body[0].left += DEFAULT_PIXEL
            elif x == 1 and snake_movement_state[x] is True:
                snake_body[0].left -= DEFAULT_PIXEL
            elif x == 2 and snake_movement_state[x] is True:
                snake_body[0].top += DEFAULT_PIXEL
            elif x == 3 and snake_movement_state[x] is True:
                snake_body[0].top -= DEFAULT_PIXEL

        page.update()
        time.sleep(0.25)


ft.app(target=main, port=8080, host="0.0.0.0")
