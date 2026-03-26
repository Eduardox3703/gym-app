"""
Pantalla de progreso - GymTracker
Muestra racha, historial semanal y estadísticas generales
"""

from datetime import date, timedelta

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Rectangle, Ellipse
from kivy.utils import get_color_from_hex
from kivy.metrics import dp

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


class StatCard(ColoredBox):
    """Tarjeta de estadística individual"""

    def __init__(self, value, label, emoji, accent_color, **kwargs):
        super().__init__(
            bg_color='#1A1A1A',
            radius=14,
            orientation='vertical',
            padding=[dp(12), dp(14)],
            spacing=dp(4),
            **kwargs,
        )
        emoji_lbl = Label(
            text=emoji,
            font_size='28sp',
            halign='center',
            size_hint_y=None,
            height=dp(40),
        )
        val_lbl = Label(
            text=str(value),
            font_size='28sp',
            bold=True,
            color=hex_color(accent_color),
            halign='center',
            size_hint_y=None,
            height=dp(36),
        )
        val_lbl.bind(size=val_lbl.setter('text_size'))
        desc_lbl = Label(
            text=label,
            font_size='12sp',
            color=hex_color('#616161'),
            halign='center',
            size_hint_y=None,
            height=dp(20),
        )
        desc_lbl.bind(size=desc_lbl.setter('text_size'))
        self.add_widget(emoji_lbl)
        self.add_widget(val_lbl)
        self.add_widget(desc_lbl)


class WeekCalendar(ColoredBox):
    """Calendario semanal mostrando dias completados"""

    def __init__(self, storage, **kwargs):
        super().__init__(
            bg_color='#141414',
            radius=14,
            orientation='vertical',
            padding=[dp(16), dp(14)],
            spacing=dp(10),
            size_hint_y=None,
            height=dp(130),
            **kwargs,
        )
        title = Label(
            text='Esta semana',
            font_size='14sp',
            bold=True,
            color=hex_color('#9E9E9E'),
            halign='left',
            size_hint_y=None,
            height=dp(22),
        )
        title.bind(size=title.setter('text_size'))
        self.add_widget(title)

        days_grid = GridLayout(
            cols=7,
            spacing=dp(4),
            size_hint_y=None,
            height=dp(76),
        )

        today = date.today()
        monday = today - timedelta(days=today.weekday())
        day_letters = ['L', 'M', 'X', 'J', 'V', 'S', 'D']
        weekly = storage.get_weekly_progress() if storage else {}
        completed_list = list(weekly.values()) if weekly else [False] * 7
        workout_days = {1, 2, 3, 4, 6}  # dias con entrenamiento

        for i in range(7):
            is_today = (i == today.weekday())
            is_done = completed_list[i] if i < len(completed_list) else False
            is_workout = i in workout_days

            cell = BoxLayout(
                orientation='vertical',
                spacing=dp(2),
                size_hint_y=None,
                height=dp(72),
            )

            # Circulo de estado
            circle_widget = Widget(size_hint_y=None, height=dp(40))
            self._draw_circle(circle_widget, is_today, is_done, is_workout)

            letter_lbl = Label(
                text=day_letters[i],
                font_size='11sp',
                color=hex_color('#2979FF') if is_today else (
                    hex_color('#FFFFFF') if is_done else hex_color('#424242')
                ),
                halign='center',
                size_hint_y=None,
                height=dp(18),
                bold=is_today,
            )

            cell.add_widget(circle_widget)
            cell.add_widget(letter_lbl)
            days_grid.add_widget(cell)

        self.add_widget(days_grid)

    def _draw_circle(self, widget, is_today, is_done, is_workout):
        def draw(*args):
            widget.canvas.clear()
            cx = widget.x + widget.width / 2
            cy = widget.y + widget.height / 2
            r = dp(16)
            with widget.canvas:
                if is_today:
                    Color(*hex_color('#2979FF'))
                elif is_done:
                    Color(*hex_color('#00C853'))
                elif is_workout:
                    Color(*hex_color('#252525'))
                else:
                    Color(*hex_color('#171717'))
                Ellipse(pos=(cx - r, cy - r), size=(r * 2, r * 2))

                # Icono dentro del circulo
                if is_done:
                    Color(*hex_color('#FFFFFF'))
                elif is_today:
                    Color(*hex_color('#FFFFFF'))
                else:
                    Color(0, 0, 0, 0)

        draw()
        widget.bind(pos=draw, size=draw)


class HistoryRow(ColoredBox):
    """Fila de historial de sesion"""

    def __init__(self, day_str, weekday_name, workout_name, **kwargs):
        super().__init__(
            bg_color='#1A1A1A',
            radius=8,
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            padding=[dp(14), dp(8)],
            spacing=dp(12),
            **kwargs,
        )
        dot = Label(
            text='✓',
            font_size='16sp',
            color=hex_color('#00C853'),
            size_hint_x=None,
            width=dp(24),
            bold=True,
        )
        info = BoxLayout(orientation='vertical', spacing=dp(2))

        name_lbl = Label(
            text=workout_name,
            font_size='14sp',
            bold=True,
            color=hex_color('#E0E0E0'),
            halign='left',
        )
        name_lbl.bind(size=name_lbl.setter('text_size'))

        date_lbl = Label(
            text=f"{weekday_name}  {day_str}",
            font_size='12sp',
            color=hex_color('#616161'),
            halign='left',
        )
        date_lbl.bind(size=date_lbl.setter('text_size'))

        info.add_widget(name_lbl)
        info.add_widget(date_lbl)

        self.add_widget(dot)
        self.add_widget(info)


class ProgressScreen(Screen):
    """Pantalla de progreso y estadisticas"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self):
        with self.canvas.before:
            Color(*hex_color('#0D0D0D'))
            self._bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=lambda *a: setattr(self._bg, 'pos', self.pos))
        self.bind(size=lambda *a: setattr(self._bg, 'size', self.size))

        app = App.get_running_app()
        storage = app.storage if app else None

        scroll = ScrollView(do_scroll_x=False)
        root = BoxLayout(
            orientation='vertical',
            spacing=dp(16),
            padding=[dp(20), dp(40), dp(20), dp(24)],
            size_hint_y=None,
        )
        root.bind(minimum_height=root.setter('height'))

        # Header
        header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(48),
            spacing=dp(8),
        )
        back_btn = Button(
            text='<',
            font_size='20sp',
            background_normal='',
            background_color=(0, 0, 0, 0),
            color=hex_color('#F5F5F5'),
            size_hint_x=None,
            width=dp(48),
        )
        with back_btn.canvas.before:
            Color(*hex_color('#1A1A1A'))
            back_btn._bg = RoundedRectangle(pos=back_btn.pos, size=back_btn.size, radius=[10] * 4)
        back_btn.bind(pos=lambda *a: setattr(back_btn._bg, 'pos', back_btn.pos))
        back_btn.bind(size=lambda *a: setattr(back_btn._bg, 'size', back_btn.size))
        back_btn.bind(on_release=lambda x: self._go_back())

        title_lbl = Label(
            text='Mi Progreso',
            font_size='20sp',
            bold=True,
            color=hex_color('#F5F5F5'),
            halign='left',
        )
        title_lbl.bind(size=title_lbl.setter('text_size'))

        header.add_widget(back_btn)
        header.add_widget(title_lbl)
        root.add_widget(header)

        # Tarjetas de estadisticas
        streak = storage.get_streak() if storage else 0
        total = storage.get_total_sessions() if storage else 0
        completed_days = storage.get_completed_days() if storage else []
        weeks_active = max(1, len(set(
            date.fromisoformat(d).isocalendar()[1] for d in completed_days
        ))) if completed_days else 0

        stats_grid = GridLayout(
            cols=2,
            spacing=dp(12),
            size_hint_y=None,
            height=dp(150),
        )

        stats_grid.add_widget(StatCard(
            value=streak,
            label="Dias de racha",
            emoji="🔥",
            accent_color='#FF6D00',
        ))
        stats_grid.add_widget(StatCard(
            value=total,
            label="Sesiones totales",
            emoji="🏆",
            accent_color='#FFD600',
        ))
        stats_grid.add_widget(StatCard(
            value=weeks_active,
            label="Semanas activas",
            emoji="📅",
            accent_color='#00BFA5',
        ))

        # Promedio por semana
        avg = round(total / weeks_active, 1) if weeks_active > 0 else 0
        stats_grid.add_widget(StatCard(
            value=avg,
            label="Sesiones/semana",
            emoji="📈",
            accent_color='#7C4DFF',
        ))

        root.add_widget(stats_grid)

        # Calendario semanal
        week_cal = WeekCalendar(storage=storage)
        root.add_widget(week_cal)

        # Racha visual grande
        streak_card = ColoredBox(
            bg_color='#1A1A1A',
            radius=16,
            orientation='horizontal',
            size_hint_y=None,
            height=dp(90),
            padding=[dp(20), dp(16)],
            spacing=dp(16),
        )
        flame_lbl = Label(
            text='🔥',
            font_size='42sp',
            size_hint_x=None,
            width=dp(60),
        )
        streak_info = BoxLayout(orientation='vertical', spacing=dp(4))

        streak_val = Label(
            text=f"{streak} dias consecutivos",
            font_size='20sp',
            bold=True,
            color=hex_color('#FF6D00'),
            halign='left',
        )
        streak_val.bind(size=streak_val.setter('text_size'))

        if streak == 0:
            streak_msg = "Aun no tienes racha. Empieza hoy!"
        elif streak == 1:
            streak_msg = "Primer dia completado. Sigue manana!"
        elif streak < 7:
            streak_msg = f"Vas bien! {7 - streak} dias para 1 semana"
        elif streak < 30:
            streak_msg = f"Increible! {30 - streak} dias para 1 mes"
        else:
            streak_msg = "Leyenda del gimnasio. Sigue asi!"

        streak_sub = Label(
            text=streak_msg,
            font_size='13sp',
            color=hex_color('#757575'),
            halign='left',
        )
        streak_sub.bind(size=streak_sub.setter('text_size'))

        streak_info.add_widget(streak_val)
        streak_info.add_widget(streak_sub)
        streak_card.add_widget(flame_lbl)
        streak_card.add_widget(streak_info)
        root.add_widget(streak_card)

        # Historial reciente
        if completed_days:
            hist_title = Label(
                text='Historial reciente',
                font_size='16sp',
                bold=True,
                color=hex_color('#E0E0E0'),
                halign='left',
                size_hint_y=None,
                height=dp(28),
            )
            hist_title.bind(size=hist_title.setter('text_size'))
            root.add_widget(hist_title)

            # Mostrar ultimos 10 dias completados
            recent = sorted(completed_days, reverse=True)[:10]
            for day_str in recent:
                try:
                    d = date.fromisoformat(day_str)
                    weekday = d.weekday()
                    workout = WORKOUTS.get(weekday, {})
                    workout_name = workout.get('name', 'Entrenamiento')
                    weekday_name = DAY_NAMES_ES[weekday]
                    row = HistoryRow(
                        day_str=day_str,
                        weekday_name=weekday_name,
                        workout_name=workout_name,
                    )
                    root.add_widget(row)
                    root.add_widget(Widget(size_hint_y=None, height=dp(4)))
                except Exception:
                    pass
        else:
            empty = Label(
                text='Aun no hay sesiones registradas.\nCompleta tu primer entrenamiento!',
                font_size='15sp',
                color=hex_color('#424242'),
                halign='center',
                size_hint_y=None,
                height=dp(60),
            )
            empty.bind(size=empty.setter('text_size'))
            root.add_widget(empty)

        root.add_widget(Widget(size_hint_y=None, height=dp(20)))

        scroll.add_widget(root)
        self.add_widget(scroll)

    def _go_back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'dashboard'

    def on_enter(self):
        self.clear_widgets()
        self._build_ui()
