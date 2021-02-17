import console_engine as a
from clear_cache import clear as clear_cache
from threading import Thread as thread
from os import system as cmd_run
from os import access as file_exists
from os import F_OK as file_exists_param
from random import randint as rand


if not __name__ == '__main__':
    exit()
a.title('Pixelsuft Console Snake')
cmd_run('color 0a')


default_fps = 60
default_speed = 2
max_speed = 40
fps = default_fps
vector = 'right'
temp_vector = 'right'
score = 0


play_eat_sound = file_exists('music\\eat.wav', file_exists_param)
at = input('Enter default speed (2): ')
if at:
    try:
        default_speed = int(at)
    except ValueError:
        pass
at = input('Enter max speed (40): ')
if at:
    try:
        max_speed = int(at)
    except ValueError:
        pass
at = input('Enter default fps (60): ')
if at:
    try:
        default_fps = int(at)
    except ValueError:
        pass
a.text(
    'Resize window and press any key to continue...',
    (0, 0),
    start=a.fore.GREEN,
    end=a.style.RESET_ALL
)
a.convert()
a.up_screen()
a.display()
a.wait_for_key()
a.reload_screen_size()
a.reload_size()
a.reload_geometry()
a.reload_mouse_pos()
a.clear()
a.up_screen()
a.title(f'Pixelsuft Console Snake [{a.width}x{a.height}]')
menu_running = False
game_running = True
snd_main_class = a.wav_mixer()
if a.width < 25 or a.height < 10:
    a.print_center('This window is veery small')
    a.convert()
    a.up_screen()
    a.display()
    exit()


def game_over():
    global fps
    global game_running
    game_running = False
    t_f_p_s = fps
    fps = default_fps
    snd_main_class.stop()
    a.clear()
    n = int(a.width / 2 - 13 / 2)
    a.text('Game Over :(', (n, 0), start=a.fore.GREEN, end=a.style.RESET_ALL)
    a.text(
        f'Score : {score}', (n, 1), start=a.fore.GREEN, end=a.style.RESET_ALL
    )
    a.text(
        f'Speed : {t_f_p_s}', (n, 2), start=a.fore.GREEN, end=a.style.RESET_ALL
    )
    a.text('Escape - Exit', (n, 3), start=a.fore.GREEN, end=a.style.RESET_ALL)
    a.text('R - Restart', (n, 4), start=a.fore.GREEN, end=a.style.RESET_ALL)
    a.text('M - Menu', (n, 5), start=a.fore.GREEN, end=a.style.RESET_ALL)
    a.convert()
    a.up_screen()
    a.display()
    to = 'exit'
    if file_exists('music\\fail1.wav', file_exists_param):
        snd_main_class.load('music\\fail' + str(rand(1, 3)) + '.wav')
        snd_main_class.async_play()
    while True:
        key_r = a.wait_for_key()
        if key_r == b'\x1b':
            to = 'exit'
            break
        elif key_r == b'r':
            to = 'restart'
            break
        elif key_r == b'm':
            to = 'menu'
            break
    a.clear()
    if to == 'exit':
        exit()
    elif to == 'menu':
        menu()
    elif to == 'restart':
        game_loop()


def waitkey_space():
    global menu_running
    while menu_running:
        if a.get_async_key_state(a.VK_SPACE):
            menu_running = False


def vec_right():
    global temp_vector
    while game_running:
        if a.get_async_key_state(a.VK_RIGHT):
            if not vector == 'left' and not vector == 'right':
                temp_vector = 'right'


def vec_left():
    global temp_vector
    while game_running:
        if a.get_async_key_state(a.VK_LEFT):
            if not vector == 'left' and not vector == 'right':
                temp_vector = 'left'


def vec_up():
    global temp_vector
    while game_running:
        if a.get_async_key_state(a.VK_UP):
            if not vector == 'down' and not vector == 'up':
                temp_vector = 'up'


def vec_down():
    global temp_vector
    while game_running:
        if a.get_async_key_state(a.VK_DOWN):
            if not vector == 'down' and not vector == 'up':
                temp_vector = 'down'


def game_loop():
    global game_running
    global vector
    global temp_vector
    global score
    global fps
    temp_vector = 'right'
    vector = 'right'
    fps = default_speed
    game_running = True
    thread(target=vec_left).start()
    thread(target=vec_right).start()
    thread(target=vec_up).start()
    thread(target=vec_down).start()
    apple = (rand(0, a.width - 1), rand(0, a.height - 1))
    score = 0
    snake = [(2, 3), (3, 3), (4, 3), (5, 3)]
    if play_eat_sound:
        snd_main_class.load('music\\eat.wav')
    while game_running:
        a.clear()
        a.text(
            'Score: ' + str(score),
            (0, 0),
            start=a.fore.GREEN,
            end=a.style.RESET_ALL
        )
        if temp_vector == 'right':
            snake.append(((snake[-1][0] + 1), (snake[-1][1])))
            vector = 'right'
        elif temp_vector == 'left':
            snake.append(((snake[-1][0] - 1), (snake[-1][1])))
            vector = 'left'
        elif temp_vector == 'up':
            snake.append(((snake[-1][0]), (snake[-1][1]) - 1))
            vector = 'up'
        elif temp_vector == 'down':
            snake.append(((snake[-1][0]), (snake[-1][1]) + 1))
            vector = 'down'
        if snake[-1] == apple:
            score += 1
            if play_eat_sound:
                snd_main_class.async_play()
            if fps < max_speed:
                fps += rand(0, 2)
            apple = (rand(0, a.width - 1), rand(0, a.height - 1))
        else:
            snake.remove(snake[0])
        a.point(a.fore.RED + 'O' + a.style.RESET_ALL, apple)
        if snake[0] in snake[1:]:
            game_over()
        elif snake[-1][0] < 0 or snake[-1][1] < 0:
            game_over()
        elif snake[-1][0] > a.width or snake[-1][1] > a.height:
            game_over()
        for i in range(len(snake)):
            if i == len(snake) - 1:
                try:
                    a.point(a.back.RED + ' ' + a.style.RESET_ALL, (snake[i]))
                except IndexError:
                    pass
            else:
                try:
                    a.point(a.back.GREEN + ' ' + a.style.RESET_ALL, (snake[i]))
                except IndexError:
                    pass
        a.convert()
        a.up_screen()
        a.display()
        a.tick(fps)


def menu():
    music_menu = False
    if file_exists('music\\menu.wav', file_exists_param):
        music_menu = True
        snd_main_class.load('music\\menu.wav')
        snd_main_class.async_play()
    global menu_running
    menu_running = True
    txx_m = (
        '00000 0   0 00000 0   0 00000',
        '0     00  0 0   0 0  0  0    ',
        '00000 0 0 0 00000 000   00000',
        '    0 0  00 0   0 0  0  0    ',
        '00000 0   0 0   0 0   0 00000'
    )
    tmp_r = {'0': str(a.back.GREEN + ' ' + a.style.RESET_ALL)}
    for i in range(len(txx_m)):
        a.text(txx_m[i], (int(a.width / 2 - 29 / 2), i), replacer=tmp_r)
    backward_m = False
    count = 0
    a.text(
        'Press Space To Start...',
        (int(a.width / 2 - 23 / 2), int(a.height / 2) + 4),
        start=a.fore.GREEN,
        end=a.style.RESET_ALL
    )
    to_sleep = int(fps / 10)
    thread(target=waitkey_space).start()
    while menu_running:
        if backward_m:
            if count > to_sleep:
                count = 0
                backward_m = False
            else:
                a.text(
                    'Press Space To Start...',
                    (int(a.width / 2 - 23 / 2), int(a.height / 2) + 4),
                    start=a.back.GREEN + a.fore.BLACK,
                    end=a.style.RESET_ALL
                )
                count += 1
        else:
            if count > to_sleep:
                count = 0
                backward_m = True
            else:
                a.text(
                    'Press Space To Start...',
                    (int(a.width / 2 - 23 / 2), int(a.height / 2) + 4),
                    start=a.fore.GREEN,
                    end=a.style.RESET_ALL
                )
                count += 1
        a.convert()
        a.up_screen()
        a.display()
        a.tick(fps)
    if music_menu:
        snd_main_class.stop()
    game_loop()


menu()
clear_cache()
