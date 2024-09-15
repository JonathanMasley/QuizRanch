import kivy
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.properties import NumericProperty
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle


class ResizableLabel(Label):
    font_size_hint = NumericProperty(0.05)  # Proportion of the window height

    def __init__(self, **kwargs):
        super(ResizableLabel, self).__init__(**kwargs)
        Window.bind(on_resize=self.update_font_size)
        self.update_font_size()

    def update_font_size(self, *args):
        self.font_size = Window.height * self.font_size_hint


class ResizableButton(Button):
    font_size_hint = NumericProperty(0.05)  # Proportion of the window height

    def __init__(self, **kwargs):
        super(ResizableButton, self).__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)  # Make the default background transparent
        self.background_normal = ''  # Remove the default background image

        # Set up the rounded rectangle background
        with self.canvas.before:
            Color(0.2, 0.6, 0.8, 1)  # Example color (adjust as needed)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[20])  # Adjust radius for roundness

        # Bind the size and position to update the rounded rectangle when resized
        self.bind(size=self._update_rect, pos=self._update_rect)
        Window.bind(on_resize=self.update_font_size)
        self.update_font_size()

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def update_font_size(self, *args):
        # Dynamically set font size based on window height
        self.font_size = Window.height * self.font_size_hint


class ResizableTextInput(TextInput):
    font_size_hint = NumericProperty(0.05)  # Proportion of the window height

    def __init__(self, **kwargs):
        super(ResizableTextInput, self).__init__(**kwargs)
        Window.bind(on_resize=self.update_font_size)
        self.update_font_size()

    def update_font_size(self, *args):
        self.font_size = Window.height * self.font_size_hint
