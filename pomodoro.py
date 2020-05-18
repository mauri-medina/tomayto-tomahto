from asciimatics.screen import Screen
from asciimatics.effects import Effect
from asciimatics.renderers import FigletText
from asciimatics.scene import Scene
from asciimatics.exceptions import ResizeScreenError
from asciimatics.event import KeyboardEvent

import sys

from datetime import datetime, timedelta

import config


class Timer:
    """
    Timer that store information for remaining time
    """

    def __init__(self, seconds: int, timer_finish_callback):
        self._initial_total_time = seconds
        self._time_delta = timedelta(seconds=seconds)

        self._finish_callback = timer_finish_callback

        self._last_tick_time = None
        self._is_running = False
        self._is_finished = False

    def start(self) -> None:
        self._is_running = True

    def stop(self) -> None:
        self._is_running = False

    def reset(self) -> None:
        self._time_delta = timedelta(seconds=self._initial_total_time)
        self._last_tick_time = None
        self._is_running = False
        self._is_finished = False

    def is_running(self) -> bool:
        return self._is_running

    def set_total_seconds(self, seconds: int):
        self._initial_total_time = seconds

    def tick(self) -> str:
        if self._is_finished:
            return

        now = datetime.now()

        # is the first tick of the timer?
        if self._last_tick_time is None:
            self._last_tick_time = now

        if self._is_running:
            delta_time = now - self._last_tick_time
            self._time_delta -= timedelta(microseconds=delta_time.microseconds)

            if self._time_delta.seconds <= 0.0 and self.is_running():
                self._end_timer()

        self._last_tick_time = now
        return self.get_time_str()

    def get_time_str(self) -> str:
        hour, minute, seconds = str(self._time_delta).split(':')
        return ':'.join([minute, seconds.split('.')[0]])

    def _end_timer(self):
        self._is_finished = True
        self._timer_finish_callback()


class TimerEffect(Effect):
    """
    Renders a timer time in the screen.
    """

    def __init__(self, screen: Screen,
                 x: int, y: int,
                 font='standard', width=200,
                 font_color=Screen.COLOUR_GREEN, background_color=Screen.COLOUR_BLACK, **kwargs):
        """
        :param timer: Timer object
        :param screen: The Screen being used for the Scene.
        :param x: X coordinate for the top left corner of the timer.
        :param y: Y coordinate for the top left corner of the timer.
        :param width: Width of the timer.
        :param height: Width of the timer.
        :param background_color: Background colour for the timer.

        Also see the common keyword arguments in :py:obj:`.Effect`.
        """
        super(TimerEffect, self).__init__(screen, **kwargs)

        self._screen = screen
        self._x = x
        self._y = y
        self._font = font
        self._width = width
        self._font_color = font_color
        self._bg_color = background_color
        self._old_text = ''

    def reset(self):
        pass

    def _update(self, frame_no):
        # We can't save timer as a variable because
        # effects are created every time the screen is resized
        new_text = timer.tick()

        # only draw when text is changed to avoid flickering(updates to fast)
        if new_text != self._old_text:
            self._old_text = new_text

            renderer = FigletText(new_text)
            image, colours = renderer.rendered_text

            # If screen is not cleared old numbers may still be visible after update
            self._screen.clear()

            for (i, line) in enumerate(image):
                self._screen.paint(
                    line, self._x, self._y + i,
                    colour=self._font_color, bg=self._bg_color)

    @property
    def stop_frame(self):
        pass


class PomodoroController(Scene):
    """
    Scene to control the pomodoro application
    This class handles the user input, updating required Effects as needed
    """

    def __init__(self, screen: Screen):
        self._screen = screen

        effects = [TimerEffect(screen, 50, self._screen.height // 2)]

        super(PomodoroController, self).__init__(effects, -1)

    def process_event(self, event):
        # Allow standard event processing first
        if super(PomodoroController, self).process_event(event) is None:
            return

        # check for my key handlers
        if isinstance(event, KeyboardEvent):
            key = event.key_code
            if key == 32:  # Space bar key
                if timer.is_running():
                    timer.stop()
                else:
                    timer.start()
            elif key == ord('r'):
                timer.reset()
            elif key == ord('p'):
                timer.set_total_seconds(config.time['pomodoro']['s'])
                timer.reset()
                timer.start()
            elif key == ord('s'):
                timer.set_total_seconds(config.time['short_break']['s'])
                timer.reset()
                timer.start()
            elif key == ord('l'):
                timer.set_total_seconds(config.time['long_break']['s'])
                timer.reset()
                timer.start()
        else:
            return event


def pomodoro(screen: Screen) -> None:
    screen.play([PomodoroController(screen)], stop_on_resize=True)


# TODO remove this, is only used for debug
import winsound

if __name__ == "__main__":
    timer = Timer(config.time['pomodoro']['s'], None)

    # This is the start of the Screen
    # Is called every time the screen is resized, so from here on everything must be stateless
    while True:
        winsound.Beep(440, 500)
        try:
            Screen.wrapper(pomodoro)
            sys.exit(0)
        except ResizeScreenError:
            pass
