import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.utils import platform, get_color_from_hex
from kivy.clock import Clock

from screens.dashboard import DashboardScreen
from screens.routine import RoutineScreen
from screens.progress import ProgressScreen
from utils.notifications import schedule_daily_notification
from utils.storage import Storage


class GymTrackerApp(App):
    title = "GymTracker 💪"

    def build(self):
        try:
            from kivy.core.window import Window
            Window.clearcolor = get_color_from_hex('#0D0D0D')
        except Exception:
            pass

        self.storage = Storage()
        sm = ScreenManager(transition=SlideTransition())
        sm.add_widget(DashboardScreen(name='dashboard'))
        sm.add_widget(RoutineScreen(name='routine'))
        sm.add_widget(ProgressScreen(name='progress'))
        Clock.schedule_once(self._setup_notifications, 2)
        return sm

    def _setup_notifications(self, dt):
        schedule_daily_notification()

    def on_pause(self):
        return True

    def on_resume(self):
        pass


if __name__ == '__main__':
    GymTrackerApp().run()
