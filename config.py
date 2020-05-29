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
    font_color=COLOR_BLACK,
    background_color=COLOR_CYAN,
    position={
        # Top lef corner
        'x': 5,  # %
        'y': 10,  # %
    }
)

time = dict(
    pomodoro={
        'm': 25},
    short_break={
        'm': 5},
    long_break={
        'm': 10}
)

keys = dict(
    time_pomodoro='p',
    time_short_break='s',
    time_long_break='l',
    reset_timer='r',
    show_hide_instructions='h',
    start_stop_timer=32             # space key code
)

instructions = dict(
    show_at_start=True,
    text='Keyboard Shortcuts             \n' 
         'SPACE Start or Stop the timer  \n' +
         keys['time_pomodoro'].capitalize()          + '  Pomodoro                    \n'+
         keys['time_short_break'].capitalize()       + '  Short Break                 \n'+
         keys['time_long_break'].capitalize()        + '  Long Break                  \n'+
         keys['reset_timer'].capitalize()            + '  Reset Timer                 \n'+
         keys['show_hide_instructions'].capitalize() + '  Show/Hide Instructions      ',
    position={
        # Top left corner
        'x': 5,  # %
        'y': 50,  # %
    },
)

alarm_sound_file = 'analog-alarm-clock.wav'

