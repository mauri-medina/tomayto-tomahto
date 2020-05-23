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
    font='standard',
    font_color=COLOR_MAGENTA,
    background_color=COLOR_YELLOW
)

time = dict(
    pomodoro={
        'm': 25,
        's': 25 * 60},
    short_break={
        'm': 5,
        's': 5 * 60},
    long_break={
        'm': 10,
        's': 10 * 60}
)
