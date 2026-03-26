"""
Pantalla de rutina del día con checklist de ejercicios
"""

from datetime import date

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Rectangle, Line
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from kivy.animation import Animation

from data.workouts import WORKOUTS, DAY_NAMES_ES


def hex_color(h, a=1.0):
    c = get_color_from_hex(h)
    return (c[0], c[1], c[2], a)


class ColoredBox(BoxLayout):
    def __init__(self, bg_color='#1A1A1A', radius=12, **kwargs):
        super().__init__(**kwargs)
        self.bg_color = bg_color
        self.radius = radius
        self.bind(pos=self._draw, size=self._draw)

    def _draw(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*hex_color(self.bg_color))
            RoundedRectangle(pos=self.pos, size=self.size, radius=[self.radius] * 4)


class ExerciseCheckItem(ColoredBox):
    """
    Ítem de ejercicio con checkbox táctil.
    Se marca/desmarca al tocar.
    """

    def __init__(self, exercise, storage, day_str, on_toggle_callback=None, **kwargs):
        self.exercise = exercise
        self.storage = storage
        self.day_str = day_str
        self.on_toggle_callback = on_toggle_callback
        self._is_done = storage.is_exercise_completed(exercise['id'], day_str)

        bg = '#1E2E1E' if self._is_done else '#1A1A1A'
        super().__init__(
            bg_color=bg,
            radius=10,
            orientation='horizontal',
            size_hint_y=None,
            height=dp(62),
            padding=[dp(14), dp(8)],
            spacing=dp(12),
            **kwargs,
        )
        self._build()

    def _build(self):
        self.clear_widgets()

        # Checkbox visual
        check_box = Widget(size_hint=(None, None), size=(dp(28), dp(28)))
        self._draw_checkbox(check_box)
        self.add_widget(check_box)
        self._check_widget = check_box

        # Texto del ejercicio
        text_col = BoxLayout(orientation='vertical', spacing=dp(2))

        name_lbl = Label(
            text=self.exercise['name'],
            font_size='15sp',
            bold=True,
            color=hex_color('#9E9E9E') if self._is_done else hex_color('#F0F0F0'),
            halign='left',
            valign='middle',
        )
        name_lbl.bind(size=name_lbl.setter('text_size'))

        sets_lbl = Label(
            text=f"{self.exercise['sets']} series  ×  {self.exercise['reps']} reps",
            font_size='13sp',
            color=hex_color('#616161') if self._is_done else hex_color('#757575'),
            halign='left',
            valign='middle',
        )
        sets_lbl.bind(size=sets_lbl.setter('text_size'))

        text_col.add_widget(name_lbl)
        text_col.add_widget(sets_lbl)
        self.add_widget(text_col)

        # Marca de completado
        if self._is_done:
            done_lbl = Label(
                text='✓',
                font_size='20sp',
                bold=True,
                color=hex_color('#00C853'),
                size_hint_x=None,
                width=dp(30),
                halign='right',
            )
            self.add_widget(done_lbl)

        # Hacer el ítem táctil
        self.bind(on_touch_down=self._on_tap)

    def _draw_checkbox(self, widget):
        widget.canvas.clear()
        with widget.canvas:
            if self._is_done:
                Color(*hex_color('#00C853'))
                RoundedRectangle(pos=widget.pos, size=widget.size, radius=[6] * 4)
                Color(*hex_color('#FFFFFF'))
                # Dibujar checkmark como líneas
            else:
                Color(*hex_color('#333333'))
                RoundedRectangle(pos=widget.pos, size=widget.size, radius=[6] * 4)
                Color(*hex_color('#555555'))
                Line(
                    rounded_rectangle=(
                        widget.pos[0], widget.pos[1],
                        widget.size[0], widget.size[1],
                        6
                    ),
                    width=1.5
                )

        widget.bind(pos=lambda *a: self._draw_checkbox(widget))
        widget.bind(size=lambda *a: self._draw_checkbox(widget))

    def _on_tap(self, instance, touch):
        if self.collide_point(*touch.pos):
            self._toggle()
            return True
        return False

    def _toggle(self):
        """Alternar estado completado del ejercicio"""
        self._is_done = self.storage.toggle_exercise(self.exercise['id'], self.day_str)

        # Animar y redibujar
        new_bg = '#1E2E1E' if self._is_done else '#1A1A1A'
        self.bg_color = new_bg
        self._draw(self)
        self._build()

        if self.on_toggle_callback:
            self.on_toggle_callback()


class RoutineScreen(Screen):
    """Pantalla de rutina del día"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self):
        """Construir la interfaz de la rutina"""
        with self.canvas.before:
            Color(*hex_color('#0D0D0D'))
            self._bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=lambda *a: setattr(self._bg, 'pos', self.pos))
        self.bind(size=lambda *a: setattr(self._bg, 'size', self.size))

        today = date.today()
        self.day_str = today.isoformat()
        self.weekday = today.weekday()
        self.workout = WORKOUTS[self.weekday]

        app = App.get_running_app()
        self.storage = app.storage if app else None

        scroll = ScrollView(do_scroll_x=False)
        self.root_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(12),
            padding=[dp(20), dp(40), dp(20), dp(24)],
            size_hint_y=None,
        )
        self.root_layout.bind(minimum_height=self.root_layout.setter('height'))

        self._populate()

        scroll.add_widget(self.root_layout)
        self.add_widget(scroll)

    def _populate(self):
        rl = self.root_layout
        rl.clear_widgets()

        workout = self.workout
        exercises = workout.get('exercises', [])

        # ── Header con botón volver ──────────────────────────────────
        header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(48),
            spacing=dp(8),
        )

        back_btn = Button(
            text='←',
            font_size='22sp',
            background_normal='',
            background_color=hex_color('#1A1A1A'),
            color=hex_color('#F5F5F5'),
            size_hint_x=None,
            width=dp(48),
        )
        with back_btn.canvas.before:
            Color(*hex_color('#1A1A1A'))
            back_btn._bg = RoundedRectangle(pos=back_btn.pos, size=back_btn.size, radius=[10] * 4)
        back_btn.bind(pos=lambda *a: setattr(back_btn._bg, 'pos', back_btn.pos))
        back_btn.bind(size=lambda *a: setattr(back_btn._bg, 'size', back_btn.size))
        back_btn.background_color = (0, 0, 0, 0)
        back_btn.bind(on_release=lambda x: self._go_back())

        title = Label(
            text=f"{workout['emoji']}  {workout['name']}",
            font_size='19sp',
            bold=True,
            color=hex_color('#F5F5F5'),
            halign='left',
        )
        title.bind(size=title.setter('text_size'))

        header.add_widget(back_btn)
        header.add_widget(title)
        rl.add_widget(header)

        # ── Descripción del día ──────────────────────────────────────
        desc_card = ColoredBox(
            bg_color='#141414',
            radius=10,
            orientation='vertical',
            size_hint_y=None,
            height=dp(52),
            padding=[dp(14), dp(8)],
        )
        desc_lbl = Label(
            text=workout.get('description', ''),
            font_size='13sp',
            color=hex_color('#9E9E9E'),
            halign='left',
            valign='middle',
        )
        desc_lbl.bind(size=desc_lbl.setter('text_size'))
        desc_card.add_widget(desc_lbl)
        rl.add_widget(desc_card)

        # ── Barra de progreso ────────────────────────────────────────
        if exercises:
            completed_count = len(
                self.storage.get_completed_exercises(self.day_str)
            ) if self.storage else 0
            total_ex = len(exercises)

            progress_box = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=dp(52),
                spacing=dp(6),
            )

            prog_header = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(20),
            )
            prog_lbl = Label(
                text='Progreso',
                font_size='13sp',
                color=hex_color('#757575'),
                halign='left',
            )
            prog_lbl.bind(size=prog_lbl.setter('text_size'))

            self.prog_count_lbl = Label(
                text=f"{completed_count}/{total_ex}",
                font_size='13sp',
                bold=True,
                color=hex_color('#00C853'),
                halign='right',
            )
            self.prog_count_lbl.bind(size=self.prog_count_lbl.setter('text_size'))

            prog_header.add_widget(prog_lbl)
            prog_header.add_widget(self.prog_count_lbl)

            # Barra visual
            bar_bg = Widget(size_hint_y=None, height=dp(6))
            self._progress_bar_bg = bar_bg
            self._prog_total = total_ex
            with bar_bg.canvas:
                Color(*hex_color('#2A2A2A'))
                bar_bg._bg_rect = RoundedRectangle(
                    pos=bar_bg.pos, size=bar_bg.size, radius=[3] * 4
                )
                Color(*hex_color('#00C853'))
                w = (completed_count / total_ex) * bar_bg.width if total_ex > 0 else 0
                bar_bg._fill_rect = RoundedRectangle(
                    pos=bar_bg.pos,
                    size=(w, bar_bg.height),
                    radius=[3] * 4
                )

            def update_bar(*args):
                bar_bg._bg_rect.pos = bar_bg.pos
                bar_bg._bg_rect.size = bar_bg.size
                cc = len(self.storage.get_completed_exercises(self.day_str)) if self.storage else 0
                bar_bg._fill_rect.pos = bar_bg.pos
                bar_bg._fill_rect.size = (
                    (cc / self._prog_total) * bar_bg.width if self._prog_total > 0 else 0,
                    bar_bg.height,
                )

            bar_bg.bind(pos=update_bar, size=update_bar)
            self._update_bar = update_bar

            progress_box.add_widget(prog_header)
            progress_box.add_widget(bar_bg)
            rl.add_widget(progress_box)

        # ── Lista de ejercicios ──────────────────────────────────────
        if exercises:
            section_lbl = Label(
                text='Ejercicios',
                font_size='15sp',
                bold=True,
                color=hex_color('#E0E0E0'),
                halign='left',
                size_hint_y=None,
                height=dp(28),
            )
            section_lbl.bind(size=section_lbl.setter('text_size'))
            rl.add_widget(section_lbl)

            for ex in exercises:
                item = ExerciseCheckItem(
                    exercise=ex,
                    storage=self.storage,
                    day_str=self.day_str,
                    on_toggle_callback=self._on_exercise_toggled,
                )
                rl.add_widget(item)
                rl.add_widget(Widget(size_hint_y=None, height=dp(4)))

        else:
            # Día de descanso o actividad ligera
            rest_card = ColoredBox(
                bg_color='#1A1A1A',
                radius=16,
                orientation='vertical',
                size_hint_y=None,
                height=dp(180),
                padding=[dp(20), dp(24)],
                spacing=dp(12),
            )
            emoji_lbl = Label(
                text=workout['emoji'],
                font_size='52sp',
                halign='center',
                size_hint_y=None,
                height=dp(70),
            )
            rest_title = Label(
                text=workout['name'],
                font_size='20sp',
                bold=True,
                color=hex_color('#E0E0E0'),
                halign='center',
                size_hint_y=None,
                height=dp(32),
            )
            rest_desc = Label(
                text=workout.get('description', ''),
                font_size='14sp',
                color=hex_color('#9E9E9E'),
                halign='center',
                valign='top',
            )
            rest_desc.bind(size=rest_desc.setter('text_size'))
            rest_card.add_widget(emoji_lbl)
            rest_card.add_widget(rest_title)
            rest_card.add_widget(rest_desc)
            rl.add_widget(rest_card)

        rl.add_widget(Widget(size_hint_y=None, height=dp(8)))

        # ── Botón "Completar entrenamiento" ──────────────────────────
        if exercises or workout['type'] in ('rest', 'light', 'walk'):
            self._build_complete_button(rl)

        rl.add_widget(Widget(size_hint_y=None, height=dp(20)))

    def _build_complete_button(self, container):
        """Crear o actualizar botón de completar entrenamiento"""
        is_done = self.storage.is_today_complete() if self.storage else False

        if is_done:
            btn = Button(
                text='✅  Entrenamiento completado',
                font_size='16sp',
                background_normal='',
                background_color=(0, 0, 0, 0),
                color=hex_color('#00C853'),
                size_hint_y=None,
                height=dp(56),
            )
            with btn.canvas.before:
                Color(*hex_color('#0D2B1A'))
                btn._bg = RoundedRectangle(pos=btn.pos, size=btn.size, radius=[12] * 4)
            btn.bind(pos=lambda *a: setattr(btn._bg, 'pos', btn.pos))
            btn.bind(size=lambda *a: setattr(btn._bg, 'size', btn.size))
        else:
            btn = Button(
                text='🏁  Marcar día como completado',
                font_size='16sp',
                bold=True,
                background_normal='',
                background_color=(0, 0, 0, 0),
                color=hex_color('#FFFFFF'),
                size_hint_y=None,
                height=dp(56),
            )
            with btn.canvas.before:
                Color(*hex_color('#2979FF'))
                btn._bg = RoundedRectangle(pos=btn.pos, size=btn.size, radius=[12] * 4)
            btn.bind(pos=lambda *a: setattr(btn._bg, 'pos', btn.pos))
            btn.bind(size=lambda *a: setattr(btn._bg, 'size', btn.size))
            btn.bind(on_release=lambda x: self._complete_day())

        container.add_widget(btn)

    def _on_exercise_toggled(self):
        """Callback cuando se marca/desmarca un ejercicio"""
        if hasattr(self, '_update_bar'):
            self._update_bar()
        if hasattr(self, 'prog_count_lbl') and self.storage:
            completed = len(self.storage.get_completed_exercises(self.day_str))
            total = len(self.workout.get('exercises', []))
            self.prog_count_lbl.text = f"{completed}/{total}"

    def _complete_day(self):
        """Marcar el día como completado"""
        if self.storage:
            self.storage.mark_day_complete(self.day_str)
        # Refrescar UI
        self.clear_widgets()
        self._build_ui()

    def _go_back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'dashboard'

    def on_enter(self):
        self.clear_widgets()
        self._build_ui()
