"""
Pantalla principal (Dashboard) - GymTracker
Muestra el entrenamiento del día, racha y acceso rápido a la rutina
"""

import random
from datetime import date

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
from kivy.clock import Clock

from data.workouts import WORKOUTS, MOTIVATIONAL_MESSAGES, DAY_NAMES_ES
from utils.notifications import send_test_notification


def hex_color(h, a=1.0):
    c = get_color_from_hex(h)
    return (c[0], c[1], c[2], a)


class ColoredBox(BoxLayout):
    """BoxLayout con fondo de color redondeado"""

    def __init__(self, bg_color='#1A1A1A', radius=12, **kwargs):
        super().__init__(**kwargs)
        self.bg_color = bg_color
        self.radius = radius
        self.bind(pos=self._draw, size=self._draw)

    def _draw(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*hex_color(self.bg_color))
            RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[self.radius] * 4
            )


class DayIndicator(ColoredBox):
    """Indicador circular/badge para un día de la semana"""

    def __init__(self, day_letter, is_active=False, is_done=False, **kwargs):
        bg = '#2979FF' if is_active else ('#00C853' if is_done else '#242424')
        super().__init__(
            bg_color=bg,
            radius=25,
            orientation='vertical',
            size_hint=(None, None),
            size=(dp(40), dp(40)),
            **kwargs
        )
        lbl = Label(
            text=day_letter,
            font_size='13sp',
            color=hex_color('#FFFFFF') if (is_active or is_done) else hex_color('#616161'),
            bold=is_active,
        )
        self.add_widget(lbl)


class ExercisePreviewItem(ColoredBox):
    """Ítem de vista previa de ejercicio en dashboard"""

    def __init__(self, exercise, **kwargs):
        super().__init__(
            bg_color='#1E1E1E',
            radius=8,
            orientation='horizontal',
            size_hint_y=None,
            height=dp(44),
            padding=[dp(12), dp(4)],
            **kwargs
        )
        dot = Label(
            text='●',
            font_size='8sp',
            color=hex_color('#2979FF'),
            size_hint_x=None,
            width=dp(20),
        )
        name = Label(
            text=exercise['name'],
            font_size='14sp',
            color=hex_color('#E0E0E0'),
            halign='left',
            valign='middle',
        )
        name.bind(size=name.setter('text_size'))

        sets_reps = Label(
            text=f"{exercise['sets']}×{exercise['reps']}",
            font_size='13sp',
            color=hex_color('#757575'),
            size_hint_x=None,
            width=dp(60),
            halign='right',
        )
        sets_reps.bind(size=sets_reps.setter('text_size'))

        self.add_widget(dot)
        self.add_widget(name)
        self.add_widget(sets_reps)


class DashboardScreen(Screen):
    """Pantalla principal del dashboard"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self):
        """Construir la interfaz del dashboard"""
        # Fondo principal
        with self.canvas.before:
            Color(*hex_color('#0D0D0D'))
            self._bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=lambda *a: setattr(self._bg_rect, 'pos', self.pos))
        self.bind(size=lambda *a: setattr(self._bg_rect, 'size', self.size))

        # Layout raíz con scroll
        scroll = ScrollView(do_scroll_x=False)
        root = BoxLayout(
            orientation='vertical',
            spacing=dp(16),
            padding=[dp(20), dp(40), dp(20), dp(20)],
            size_hint_y=None,
        )
        root.bind(minimum_height=root.setter('height'))

        today = date.today()
        weekday = today.weekday()
        workout = WORKOUTS[weekday]

        # ── Header ──────────────────────────────────────────────────────
        header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
        )
        app_title = Label(
            text='💪 GymTracker',
            font_size='22sp',
            bold=True,
            color=hex_color('#F5F5F5'),
            halign='left',
        )
        app_title.bind(size=app_title.setter('text_size'))

        date_lbl = Label(
            text=today.strftime('%d/%m/%Y'),
            font_size='14sp',
            color=hex_color('#757575'),
            halign='right',
            size_hint_x=None,
            width=dp(100),
        )
        date_lbl.bind(size=date_lbl.setter('text_size'))

        header.add_widget(app_title)
        header.add_widget(date_lbl)
        root.add_widget(header)

        # ── Card del día actual ─────────────────────────────────────────
        day_card = ColoredBox(
            bg_color=workout['color'],
            radius=16,
            orientation='vertical',
            size_hint_y=None,
            height=dp(140),
            padding=[dp(20), dp(16)],
            spacing=dp(8),
        )

        day_name_lbl = Label(
            text=f"{workout['emoji']}  {DAY_NAMES_ES[weekday]}",
            font_size='14sp',
            color=hex_color('#9E9E9E'),
            halign='left',
            size_hint_y=None,
            height=dp(22),
        )
        day_name_lbl.bind(size=day_name_lbl.setter('text_size'))

        workout_title = Label(
            text=workout['name'],
            font_size='26sp',
            bold=True,
            color=hex_color('#FFFFFF'),
            halign='left',
            size_hint_y=None,
            height=dp(38),
        )
        workout_title.bind(size=workout_title.setter('text_size'))

        workout_desc = Label(
            text=workout['description'],
            font_size='13sp',
            color=hex_color('#BDBDBD'),
            halign='left',
            valign='top',
        )
        workout_desc.bind(size=workout_desc.setter('text_size'))

        day_card.add_widget(day_name_lbl)
        day_card.add_widget(workout_title)
        day_card.add_widget(workout_desc)
        root.add_widget(day_card)

        # ── Indicadores de la semana ────────────────────────────────────
        week_box = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(80),
            spacing=dp(6),
        )
        week_title = Label(
            text='Esta semana',
            font_size='13sp',
            color=hex_color('#757575'),
            halign='left',
            size_hint_y=None,
            height=dp(20),
        )
        week_title.bind(size=week_title.setter('text_size'))

        days_row = BoxLayout(
            orientation='horizontal',
            spacing=dp(8),
            size_hint_y=None,
            height=dp(44),
        )

        day_letters = ['L', 'M', 'X', 'J', 'V', 'S', 'D']
        storage = App.get_running_app().storage if App.get_running_app() else None

        weekly = storage.get_weekly_progress() if storage else {}
        completed_days = list(weekly.values()) if weekly else []

        for i, letter in enumerate(day_letters):
            is_active = (i == weekday)
            is_done = completed_days[i] if i < len(completed_days) else False
            indicator = DayIndicator(
                day_letter=letter,
                is_active=is_active,
                is_done=is_done,
            )
            days_row.add_widget(indicator)

        week_box.add_widget(week_title)
        week_box.add_widget(days_row)
        root.add_widget(week_box)

        # ── Estadísticas (racha + sesiones) ────────────────────────────
        stats_row = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(90),
            spacing=dp(12),
        )

        streak = storage.get_streak() if storage else 0
        total = storage.get_total_sessions() if storage else 0

        for value, label_text, emoji, accent in [
            (f"{streak}", "días de racha", "🔥", '#FF6D00'),
            (f"{total}", "sesiones totales", "🏆", '#FFD600'),
        ]:
            stat_card = ColoredBox(
                bg_color='#1A1A1A',
                radius=12,
                orientation='vertical',
                padding=[dp(12), dp(8)],
                spacing=dp(4),
            )
            val_lbl = Label(
                text=f"{emoji} {value}",
                font_size='22sp',
                bold=True,
                color=hex_color(accent),
                halign='center',
                size_hint_y=None,
                height=dp(38),
            )
            val_lbl.bind(size=val_lbl.setter('text_size'))

            desc_lbl = Label(
                text=label_text,
                font_size='12sp',
                color=hex_color('#757575'),
                halign='center',
                size_hint_y=None,
                height=dp(20),
            )
            desc_lbl.bind(size=desc_lbl.setter('text_size'))

            stat_card.add_widget(val_lbl)
            stat_card.add_widget(desc_lbl)
            stats_row.add_widget(stat_card)

        root.add_widget(stats_row)

        # ── Mensaje motivacional ────────────────────────────────────────
        wtype = workout.get('type', 'rest')
        messages = MOTIVATIONAL_MESSAGES.get(wtype, MOTIVATIONAL_MESSAGES['rest'])
        motivation = random.choice(messages)

        motiv_card = ColoredBox(
            bg_color='#141414',
            radius=12,
            orientation='vertical',
            size_hint_y=None,
            height=dp(60),
            padding=[dp(16), dp(8)],
        )
        motiv_lbl = Label(
            text=motivation,
            font_size='15sp',
            color=hex_color('#B0BEC5'),
            halign='center',
            valign='middle',
            italic=True,
        )
        motiv_lbl.bind(size=motiv_lbl.setter('text_size'))
        motiv_card.add_widget(motiv_lbl)
        root.add_widget(motiv_card)

        # ── Vista previa de ejercicios ──────────────────────────────────
        exercises = workout.get('exercises', [])
        if exercises:
            preview_title = Label(
                text='Ejercicios de hoy',
                font_size='16sp',
                bold=True,
                color=hex_color('#E0E0E0'),
                halign='left',
                size_hint_y=None,
                height=dp(28),
            )
            preview_title.bind(size=preview_title.setter('text_size'))
            root.add_widget(preview_title)

            preview_box = BoxLayout(
                orientation='vertical',
                spacing=dp(6),
                size_hint_y=None,
            )
            # Mostrar máximo 4 ejercicios en preview
            for ex in exercises[:4]:
                item = ExercisePreviewItem(ex)
                preview_box.add_widget(item)
            preview_box.bind(minimum_height=preview_box.setter('height'))

            if len(exercises) > 4:
                more_lbl = Label(
                    text=f'+{len(exercises) - 4} ejercicios más...',
                    font_size='13sp',
                    color=hex_color('#2979FF'),
                    halign='left',
                    size_hint_y=None,
                    height=dp(24),
                )
                more_lbl.bind(size=more_lbl.setter('text_size'))
                preview_box.add_widget(more_lbl)

            root.add_widget(preview_box)

        # ── Botones de acción ────────────────────────────────────────────
        root.add_widget(Widget(size_hint_y=None, height=dp(8)))

        # Botón principal: ver rutina
        btn_routine = self._make_button(
            text='Ver Rutina Completa  →',
            bg_color='#2979FF',
            callback=self._go_to_routine,
        )
        root.add_widget(btn_routine)

        # Botón progreso
        btn_progress = self._make_button(
            text='📊  Mi Progreso',
            bg_color='#1E1E1E',
            text_color='#B0BEC5',
            callback=self._go_to_progress,
        )
        root.add_widget(btn_progress)

        # Botón test notificación
        btn_notif = self._make_button(
            text='🔔  Probar Notificación',
            bg_color='#141414',
            text_color='#616161',
            callback=self._test_notification,
        )
        root.add_widget(btn_notif)

        root.add_widget(Widget(size_hint_y=None, height=dp(20)))

        scroll.add_widget(root)
        self.add_widget(scroll)

    def _make_button(self, text, bg_color='#2979FF', text_color='#FFFFFF', callback=None):
        """Crear botón estilizado"""
        btn = Button(
            text=text,
            font_size='16sp',
            bold=True,
            background_normal='',
            background_color=hex_color(bg_color),
            color=hex_color(text_color),
            size_hint_y=None,
            height=dp(54),
        )
        # Bordes redondeados vía canvas
        with btn.canvas.before:
            Color(*hex_color(bg_color))
            btn._bg = RoundedRectangle(pos=btn.pos, size=btn.size, radius=[10] * 4)
        btn.bind(pos=lambda *a: setattr(btn._bg, 'pos', btn.pos))
        btn.bind(size=lambda *a: setattr(btn._bg, 'size', btn.size))
        btn.background_color = (0, 0, 0, 0)

        if callback:
            btn.bind(on_release=lambda x: callback())
        return btn

    def _go_to_routine(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'routine'

    def _go_to_progress(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'progress'

    def _test_notification(self):
        send_test_notification()

    def on_enter(self):
        """Refrescar UI al entrar a la pantalla"""
        self.clear_widgets()
        self._build_ui()
