time = dict(  # Time in minutes
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

key_code = dict(
    space=32,
    p=112,
    s=115,
    l=108,
    r=114
)

action_key_code = dict(
    start=32,  # space key
    stop=32,  # space key
    reset_timer=ord('r'),
    pomodoro_time=ord('p'),
    short_break=ord('s'),
    long_break=ord('l'),
)
