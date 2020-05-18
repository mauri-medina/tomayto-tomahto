from asciimatics.screen import Screen
from asciimatics.effects import Effect
from asciimatics.renderers import FigletText
from asciimatics.scene import Scene
from asciimatics.exceptions import ResizeScreenError
from asciimatics.event import KeyboardEvent

import sys

from datetime import datetime, timedelta


class Timer:
    """
    Timer that store information for remaining time
    """

    def __init__(self, seconds: int, timer_finish_callback):

        self._timer_total_time = seconds
        self._time_delta = timedelta(seconds=seconds)

        self._timer_finish_callback = timer_finish_callback

        self._last_tick_time = None
        self._is_running = True
        self._is_finished = False

        self.start()

    def start(self) -> None:
        self._is_running = True

    def pause(self) -> None:
        self._is_running = False

    def resume(self):
        self._is_running = True

    def tick(self) -> None:
        if self._is_finished:
            return

        now = datetime.now()

        # is the first tick of the timer?
        if self._last_tick_time is None:
            self._last_tick_time = now

        if self._is_running:
            delta_time = now - self._last_tick_time
            self._time_delta -= timedelta(microseconds=delta_time.microseconds)

            if self._time_delta.seconds <= 0.0:
                self._end_timer()

        self._last_tick_time = now

    def get_time_str(self) -> str:
        hour, minute, seconds = str(self._time_delta).split(':')
        return ':'.join([minute, seconds.split('.')[0]])

    def _end_timer(self):
        self._is_finished = True
        self._timer_finish_callback()

    # TODO sacar esto de aca
    # def process_event(self, event):
    #     if isinstance(event, KeyboardEvent):
    #         key = event.key_code
    #         if key == Screen.KEY_UP:
    #             self._is_running = not self._is_running


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
        global timer
        timer.tick()
        new_text = timer.get_time_str()

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




def pomodoro(screen: Screen) -> None:

    effects = [TimerEffect(screen, 50, screen.height // 2)]
    screen.play([Scene(effects, -1)], stop_on_resize=True)


timer = Timer(1500, None)

# This is the start of the Screen
# This method is called every time the screen is resized, so from here on everything must be stateless
import winsound

while True:
    winsound.Beep(440, 500)
    try:
        Screen.wrapper(pomodoro)
        sys.exit(0)
    except ResizeScreenError:
        pass
