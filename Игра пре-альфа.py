import pygame
import json
import sys
from openai import OpenAI


client = OpenAI(
    api_key="sk-79GgdKZzhyOK8rvnpciFogWX3yA61T5W",
    base_url="https://api.proxyapi.ru/openai/v1",
)
messages = []

class Board:
    # создание поля
    def __init__(self, width, height):
        self.a = 5
        self.b = 6
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.board[self.a][self.b] = 1
        self.board[4][5] = 2
        self.board[4][6] = 3
        self.board[2][7] = 4
        for i in self.board:
            print(i)
        self.zerodirection = set()
        self.visited = set()
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.red = []

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def move(self, x, y):
        if y >= 0 and x >= 0 and y < self.height and x < self.width and self.board[x][y] == 0:
            self.board[self.a][self.b] = 0
            return True


    def prompt(self):
        promt = 'Игровое поле задано матрицей ' + str(self.board) + ', где 0 - пустая клетка, 1 - красная фишка, 2 - непроходимые стены, 3 - жёлтые фишки и 4 - синие фишки. Передвинь все жёлтые фишки на 1 доступную(пустую) ячейку так, чтобы они приблизились к красной. Затем передвинь все синие фишки на 1 доступную(пустую) ячейку так, чтобы они отдалились от красной. В ответе запиши новую матрицу игрового поля. Ответ должен содержать только JSON, без комментариев и дополнительной информации. Пример формата: [[0, 1, 0, 2], [0, 0, 3, 2], [0, 4, 3, 4], [2, 0, 3, 4]]'
        messages.append({"role": "user", "content": promt})
        chat_completion = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            max_tokens=1000
        )
        response_text = chat_completion.choices[0].message.content
        modified_text = response_text.replace('```', '').replace('json', '')
        result = json.loads(modified_text)
        self.board = result
        for i in result:
            print(i)

    def render(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, (255,255,255),
                                 (self.left + j * self.cell_size, self.top + i * self.cell_size,
                                  self.cell_size, self.cell_size), 1)
                if self.board[i][j] == 2:
                    pygame.draw.rect(screen, 'green', (self.left + j * self.cell_size, self.top + i * self.cell_size,
                                  self.cell_size, self.cell_size))
                if self.board[i][j] == 1:
                    pygame.draw.circle(screen, 'red', (self.left + j * self.cell_size + 0.5 * self.cell_size, self.top + i * self.cell_size + self.cell_size // 2), self.cell_size // 2 - 2)
                if self.board[i][j] == 3:
                    pygame.draw.circle(screen, 'yellow', (self.left + j * self.cell_size + 0.5 * self.cell_size, self.top + i * self.cell_size + self.cell_size // 2), self.cell_size // 2 - 2)
                if self.board[i][j] == 4:
                    pygame.draw.circle(screen, 'blue', (self.left + j * self.cell_size + 0.5 * self.cell_size, self.top + i * self.cell_size + self.cell_size // 2), self.cell_size // 2 - 2)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Поле')
    size = width, height = 600, 600
    screen = pygame.display.set_mode(size)
    board = Board(10, 10)
    board.set_view(50, 50, 40)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.cell_define(event.pos)
            elif event.type == pygame.KEYDOWN:
                board.prompt()
                if event.key == pygame.K_LEFT:
                    if board.move(board.a, board.b - 1):
                        board.b -= 1
                        board.board[board.a][board.b] = 1
                    board.render(screen)
                elif event.key == pygame.K_RIGHT:
                    if board.move(board.a, board.b + 1):
                        board.b += 1
                        board.board[board.a][board.b] = 1
                    board.render(screen)
                elif event.key == pygame.K_UP:
                    if board.move(board.a - 1, board.b):
                        board.a -= 1
                        board.board[board.a][board.b] = 1
                    board.render(screen)
                elif event.key == pygame.K_DOWN:
                    if board.move(board.a + 1, board.b):
                        board.a += 1
                        board.board[board.a][board.b] = 1
                    board.render(screen)
        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()