"""A simple countdown timer for the command line with optional sound.

Displays the time remaining in minutes and plays a sound when done.
Option to set in-between reminder times to play a secondary sound.

Configuration:
- assign stop_sound and notification_sound
- change play() to use your preferred audio player (currently ffplay)
"""

import time
import os


stop_sound = 'bell.ogg'
notification_sound = 'click.ogg'

UPDATE_INTERVAL = 6   # minimum timer update interval in seconds
clear_console = True  # request to hide the previous output
                      # while displaying remaining time
play_sounds = True    # request to play sounds (requires ffplay)

for file in notification_sound, stop_sound:
    assert ';' not in file and '|' not in file  # safeguard
    

def play(file):
    global play_sounds
    if play_sounds:
        # trigger ffplay via the system console
        print(prompt := f"ffplay -autoexit -nodisp {file}")
        exitcode = os.system(prompt)
        play_sounds = (exitcode == 0)

def update(message, times):
    global clear_console
    if clear_console:
        print(prompt := "cls" if os.name == 'nt' else "clear")
        exitcode = os.system(prompt)
        clear_console = (exitcode == 0)
    print(f'{message} / {times}')


# ========================== PROGRAM START ===========================

def main():
    times_input = input('enter times in min, \n'
                        + 'e.g. 30 40 for a 40 min timer with '
                        + 'an audio reminder at 30 min \n> ')

    times = [float(t) * 60 for t in times_input.split(' ')]
    times_graphic = ' '.join(str(int(t) // 60) + 'm' for t in times)

    start_time = time.time()

    play(notification_sound)
    k = 1  # number of times to repeat sound, +1 for each checkpoint

    while times:
        if (cur_time := time.time() - start_time) < times[0]:
            mins, secs = divmod(int(cur_time), 60)
            update(f'{mins:02d}:{secs:02d}', times_graphic)
            time.sleep(UPDATE_INTERVAL)
        else:
            for i in range(k):
                play(notification_sound)
            times.pop(0)
            times_graphic = ' '.join(str(int(t) // 60) + 'm' for t in times)
            k += 1

    play(stop_sound)

    input(f'timer ended - enter to restart > ')


if __name__ == '__main__':
    while True:
        main()
