from asciimatics.screen import Screen
from asciimatics.effects import Effect, Print
from asciimatics.renderers import FigletText, SpeechBubble
from asciimatics.scene import Scene
from asciimatics.exceptions import ResizeScreenError, StopApplication
from asciimatics.event import KeyboardEvent

import sys

from datetime import datetime, timedelta

from playsound import playsound
import threading
import os.path
import config


# Timer must be outside of a scene or effect because those objects reset everytime the screen is resized
class Timer:
    """
    Timer that store information for remaining time
    """

    def __init__(self, minutes: int, timer_finish_callback):
        self._finish_callback = timer_finish_callback

        self.set_total_time(minutes)
        self._setup_timer()

    def _setup_timer(self):
        self.accumulated_microseconds = 0
        self._last_tick_time = None
        self._is_running = False
        self._is_finished = False

    def start(self) -> None:
        self._is_running = True

    def stop(self) -> None:
        self._is_running = False

    def reset(self) -> None:
        self._setup_timer()

    def is_running(self) -> bool:
        return self._is_running

    def set_total_time(self, minutes: int):
        self._total_time_seconds = minutes * 60
        self._total_time_microseconds = self._total_time_seconds * 1000000

    def tick(self) -> None:
        if self._is_finished:
            return

        now = datetime.now()

        # is the first tick of the timer?
        if self._last_tick_time is None:
            self._last_tick_time = now

        if self._is_running:
            delta_time = now - self._last_tick_time

            self.accumulated_microseconds += delta_time.microseconds
            dt = self._total_time_microseconds - self.accumulated_microseconds
            if dt <= 0.0 and self.is_running():
                self._end_timer()

        self._last_tick_time = now

    def get_time_str(self) -> str:
        # we need to take on account that a seconds pass when 1000000 microseconds has passed
        # if we not do this, 0 seconds with 50000 microseconds left it's considered as 0 seconds but its not yet zero
        accumulated_seconds = self.accumulated_microseconds // 1000000
        dt = self._total_time_seconds - accumulated_seconds
        hour, minute, seconds = str(timedelta(seconds=dt)).split(':')
        return ':'.join([minute, seconds.split('.')[0]])

    def _end_timer(self):
        self._is_finished = True
        if self._finish_callback:
            # Use a thread to not hang up the application until the sound finish playing
            th = threading.Thread(target=self._finish_callback)
            th.start()

    def set_on_end_timer_listener(self, listener: any) -> None:
        self._finish_callback = listener


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
        self._renderer = None

    def reset(self):
        pass

    def _update(self, frame_no):
        # We can't save timer as a variable because
        # effects are created every time the screen is resized
        timer.tick()
        new_text = timer.get_time_str()

        if new_text != self._old_text:

            self._old_text = new_text

            old_image = None
            if self._renderer:
                old_image, _ = self._renderer.rendered_text

            self._renderer = FigletText(new_text, font=self._font)
            new_image, colours = self._renderer.rendered_text

            # Draw new image
            new_image_max_line_len = -1
            for (i, line) in enumerate(new_image):
                size = len(line)
                if size > new_image_max_line_len:
                    new_image_max_line_len = size

                self._screen.paint(
                    line, self._x, self._y + i,
                    colour=self._font_color, bg=self._bg_color)

            # If old image is longer than current image we must clear old image left over
            if old_image:
                for (i, line) in enumerate(old_image):
                    old_line_size = len(line)
                    if old_line_size > new_image_max_line_len:
                        filler_size = old_line_size - new_image_max_line_len
                        self._screen.paint(" " * filler_size, self._x + len(new_image[i]), self._y + i)

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

        timer.set_on_end_timer_listener(self.on_timer_finish)

        effects = []

        # Create Instructions effect
        self._instructions = None
        if config.instructions['show_at_start']:
            self._instructions = self._create_instructions_effect()
            effects.append(self._instructions)

        # Create timer effect
        x = int(self._screen.width * (config.timer['position']['x'] / 100))
        y = int(self._screen.height * (config.timer['position']['y'] / 100))

        self._timer_effect = TimerEffect(
            screen, x, y,
            font=config.timer['font'],
            font_color=config.timer['font_color'],
            background_color=config.timer['background_color'])

        effects.append(self._timer_effect)

        super(PomodoroController, self).__init__(effects, -1)

    def on_timer_finish(self):
        path = os.path.join('resources', config.alarm_sound_file)
        playsound(path)

    def process_event(self, event):
        # Allow standard event processing first
        if super(PomodoroController, self).process_event(event) is None:
            return

        # check for my key handlers
        if isinstance(event, KeyboardEvent):
            key = event.key_code
            if key == Screen.ctrl("c"):
                raise StopApplication("User quit")
            elif key == config.keys['start_stop_timer']:
                if timer.is_running():
                    timer.stop()
                else:
                    timer.start()
            elif key == config.keys['reset_timer']:
                timer.reset()
            elif key == config.keys['time_pomodoro']:
                timer.set_total_time(config.time['pomodoro']['m'])
                timer.reset()
                timer.start()
            elif key == config.keys['time_short_break']:
                timer.set_total_time(config.time['short_break']['m'])
                timer.reset()
                timer.start()
            elif key == config.keys['time_long_break']:
                timer.set_total_time(config.time['long_break']['m'])
                timer.reset()
                timer.start()
            elif key == config.keys['show_hide_instructions']:
                self._toggle_instructions_visibility()

        else:
            return event

    def _toggle_instructions_visibility(self):
        if self._instructions and self._instructions in self.effects:
            # remove effect from scene and clear it in the next frame
            self._instructions.delete_count = 1
        else:
            # we have to create a new effect since the last one have been removed by the screen
            self._instructions = self._create_instructions_effect()
            self.add_effect(self._instructions)

    def _create_instructions_effect(self):
        x = int(self._screen.width * (config.instructions['position']['x'] / 100))
        y = int(self._screen.height * (config.instructions['position']['y'] / 100))
        return Print(self._screen, SpeechBubble(config.instructions['text'], uni=True), y, x)


def pomodoro(screen: Screen) -> None:
    screen.play([PomodoroController(screen)], stop_on_resize=True)


if __name__ == "__main__":
    timer = Timer(config.time['pomodoro']['m'], None)

    # This is the start of the Screen
    # Is called every time the screen is resized, so from here on everything must be stateless
    while True:
        try:
            Screen.wrapper(pomodoro, catch_interrupt=True)
            sys.exit(0)
        except ResizeScreenError:
            pass
