import pgzrun
import random
import time
from pgzero.builtins import *
import speech_recognition as sr
r = sr.Recognizer()
import threading
import queue

command_queue = queue.Queue()
command_list = []

voice_commands = {
    "вверх": "move_up",
    "вниз": "move_down",
    "влево": "move_left",
    "вправо": "move_right",
    "up": "move_up",
    "down": "move_down",
    "left": "move_left",
    "right": "move_right"
}



# Размеры игрового окна
WIDTH = 320
HEIGHT = 411
TITLE = "Игровой котик"
FPS = 60

# Класс для игры
class Game:
    def __init__(self):
        # URL для отправки запросов
        self.ui = Actor("ui", center=(WIDTH / 2 + 20, HEIGHT /2 - 158))
        self.bg = Actor("background", center=(WIDTH / 2, HEIGHT / 2 + 48))
        self.cat = Cat()
        self.coin = Coin()
        self.cells = [Cell(i * 32, j * 32 + 93) for i in range(10) for j in range(10)]
        music.play("music")
        music.set_volume(0.01) 

    # Метод для отрисовки игры
    def draw(self):
        screen.draw.filled_rect(Rect(0, 0, 320, 92), (255, 255, 255))
        self.ui.draw()
        self.bg.draw()
        for cell in self.cells:
            cell.draw()
        self.update()
        self.coin.draw()
        self.cat.draw()
        screen.draw.text("Игровой котик", center=(self.ui.x, self.ui.y), color=(0,0,0), fontname=("font"))
    
    # Метод для обработки запросов от API
        
    # Метод для обновления игры
    def update(self):
        self.cat.update()

# Класс для кота
class Cat:
    def __init__(self):
        self.actor = Actor("cat_sit_down", center=(random.randint(0, 9) * 32 + 16, random.randint(0, 9) * 32 + 106))
        # Изображения для анимации кота
        self.images_left = [
            "cat_walk_left_1",
            "cat_walk_left_2",
            "cat_walk_left_3",
            "cat_sit_left"
            ]
        self.images_right = [
            "cat_walk_right_1",
            "cat_walk_right_2",
            "cat_walk_right_3",
            "cat_sit_right"
            ]
        self.images_up = [
            "cat_walk_up_1",
            "cat_walk_up_2",
            "cat_walk_up_3",
            "cat_sit_up"
            ]
        self.images_down = [
            "cat_walk_down_1",
            "cat_walk_down_2",
            "cat_walk_down_3",
            "cat_sit_down"
            ]
        self.frame = 0
        self.direction = None
        self.animation_playing = False
        self.animation_frame = 0

    # Метод для отрисовки кота
    def draw(self):
        self.actor.draw()
        
    # Метод для обработки нажатия клавиши
    def on_key_down(self, button_label):
        # Проверка анимации
        if self.animation_playing:
            return
        # Обработка перемещения кота
        if button_label == "move_left" and self.actor.x > 16:
            self.animation_playing = True
            self.animation_frame = 0
            self.direction = "left"
            animate(self.actor, tween='linear', duration=2, x=self.actor.x - 32, on_finished=self.on_animation_finished)
            self.animate_move()
        elif button_label == "move_right" and self.actor.x < 304:
            self.animation_playing = True
            self.animation_frame = 0
            self.direction = "right"
            animate(self.actor, tween='linear', duration=2, x=self.actor.x + 32, on_finished=self.on_animation_finished)
            self.animate_move()
        elif button_label == "move_up" and self.actor.y > 112:
            self.animation_playing = True
            self.animation_frame = 0
            self.direction = "up"
            animate(self.actor, tween='linear', duration=2, y=self.actor.y - 32 , on_finished=self.on_animation_finished)
            self.animate_move()
        elif button_label == "move_down" and self.actor.y < 400:
            self.animation_playing = True
            self.animation_frame = 0
            self.direction = "down"
            animate(self.actor, tween='linear', duration=2, y=self.actor.y + 32, on_finished=self.on_animation_finished)
            self.animate_move()

    # Метод для анимации перемещения кота
    def animate_move(self):
        # Запланирование обновления анимации
        clock.schedule_interval(self.update, 0.1)

    # Метод для обработки окончания анимации
    def on_animation_finished(self):
        # Проверка столкновения с монетой
        collision_check_result = self.actor.colliderect(game.coin.actor)
        if collision_check_result:
            # Воспроизведение звука сбора монеты
            sounds.coin_collect.play()
            # Обновление монеты
            game.coin.update()
        # Сброс флага анимации
        self.animation_playing = False
        # Установка изображения кота в зависимости от направления движения
        if self.direction == "left":
            self.actor.image = "cat_sit_left"
        elif self.direction == "right":
            self.actor.image = "cat_sit_right"
        elif self.direction == "up":
            self.actor.image = "cat_sit_up"
        elif self.direction == "down":
            self.actor.image = "cat_sit_down"

    # Метод для обновления кота
    def update(self):
        # Проверка анимации
        if self.animation_playing:
            # Обновление текущего кадра анимации
            self.animation_frame = (self.animation_frame + 1) % 3
            # Пауза между кадрами анимации
            time.sleep(0.1)
            # Установка изображения кота в зависимости от направления движения
            if self.direction == "left":
                self.actor.image = self.images_left[self.animation_frame]
            elif self.direction == "right":
                self.actor.image = self.images_right[self.animation_frame]
            elif self.direction == "up":
                self.actor.image = self.images_up[self.animation_frame]
            elif self.direction == "down":
                self.actor.image = self.images_down[self.animation_frame]
            

# Класс для монеты
class Coin:
    def __init__(self):
        self.actor = Actor("coin", center=(random.randint(0, 9) * 32 + 16, random.randint(0, 9) * 32 + 112))

    # Метод для отрисовки монеты
    def draw(self):
        self.actor.draw()
        
    # Метод для обновления монеты
    def update(self):
        # Установка случайных координат монеты
        self.actor.x = random.randint(0, 9) * 32 + 16
        self.actor.y = random.randint(0, 9) * 32 + 112


# Класс для ячеек
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Метод для отрисовки ячейки
    def draw(self):
        screen.draw.line((self.x, self.y), (self.x + 32, self.y), (0, 0, 0))
        screen.draw.line((self.x + 32, self.y), (self.x + 32, self.y + 32), (0, 0, 0))
        screen.draw.line((self.x + 32, self.y + 32), (self.x, self.y + 32), (0, 0, 0))
        screen.draw.line((self.x, self.y + 32), (self.x, self.y), (0, 0, 0))


# Создание игры
game = Game()

# Функция для отрисовки игры
def draw():
    game.draw()

# Функция для обработки нажатия клавиши
def on_key_down():
    game.cat.on_key_down()
    
# Функция для отправки запроса на сбор монеты
def get_api_data(button_label):
    game.cat.on_key_down(button_label)
    

# Функция для запуска игры
def start():
    # record()
    pgzrun.go()
    
def record():
    recognizer = sr.Recognizer()
    while True:
        with sr.Microphone(device_index=2) as source:
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio, language="ru-RU")
                handle_voice_command(text)
                print(text)
            except sr.UnknownValueError:
                print("Ошибка распознавания голосовой команды")

def handle_voice_command(text):
    commands = text.split()
    for command in commands:
        if command in voice_commands:
            action = voice_commands[command]
            command_list.append(action)
            print("Добавлена команда:", action)
        else:
            print("Неизвестная голосовая команда")
            
def execute_commands():
    if not game.cat.animation_playing and command_list:
        action = command_list.pop(0)
        if action == "move_up":
            game.cat.on_key_down("move_up")
        elif action == "move_down":
            game.cat.on_key_down("move_down")
        elif action == "move_left":
            game.cat.on_key_down("move_left")
        elif action == "move_right":
            game.cat.on_key_down("move_right")
    clock.schedule_unique(execute_commands, 0.1)

def start():
    threading.Thread(target=record).start()
    clock.schedule_unique(execute_commands, 0.5)
    pgzrun.go()
    
# Запуск игры
start()