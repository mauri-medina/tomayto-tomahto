# Text colors for use when printing to the Screen.
COLOR_BLACK = 0
COLOR_RED = 1
COLOR_GREEN = 2
COLOR_YELLOW = 3
COLOR_BLUE = 4
COLOR_MAGENTA = 5
COLOR_CYAN = 6
COLOR_WHITE = 7

timer = dict(
    font='larry3d',
    font_color=COLOR_BLUE,
    background_color=COLOR_GREEN,
    position={
        # Top lef corner
        'x': 5,  # %
        'y': 10,  # %
    }
)

time = dict(
    pomodoro={
        'm': 25,
        's': 5},
    short_break={
        'm': 5,
        's': 5 * 60},
    long_break={
        'm': 10,
        's': 10 * 60}
)

instructions = dict(
    text='Keyboard Shortcuts             \n' 
         'SPACE Start or Stop the timer  \n' 
         'P  Pomodoro                    \n' 
         'S  Short Break                 \n'
         'L  Long Break                  \n'
         'R  Reset Timer                 \n'
         'H  Show/Hide Instructions      ',
    position={
        # Top left corner
        'x': 5,  # %
        'y': 50,  # %
    },
)

alarm_sound_file = 'analog-alarm-clock.wav'
