import keyboard
import platform

# Beep function for different OS
def beep():
    if platform.system() == 'Windows':
        import winsound
        winsound.Beep(1000, 100)  # frequency (Hz), duration (ms)
    else:
        import os
        os.system('printf "\a"')  # ANSI beep (may not work on all terminals)

print("Start typing... (Press ESC to exit)")

while True:
    event = keyboard.read_event()
    if event.event_type == keyboard.KEY_DOWN:
        print(f'You pressed: {event.name}')
        beep()
        if event.name == 'esc':
            break
