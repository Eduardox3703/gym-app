"""
Utilidad de almacenamiento local usando JSON
Guarda ejercicios completados, historial y rachas
"""

import json
import os
from datetime import date, datetime, timedelta
from kivy.utils import platform


def get_storage_path():
    """Obtener ruta de almacenamiento según la plataforma"""
    if platform == 'android':
        from android.storage import app_storage_path
        return app_storage_path()
    else:
        # En escritorio, usar directorio del script
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(base, 'gymtracker_data')
        os.makedirs(path, exist_ok=True)
        return path


class Storage:
    """Gestor de almacenamiento local"""

    def __init__(self):
        self.storage_dir = get_storage_path()
        self.data_file = os.path.join(self.storage_dir, 'gymdata.json')
        self._data = self._load()

    def _load(self):
        """Cargar datos desde archivo JSON"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return self._default_data()

    def _default_data(self):
        """Estructura de datos por defecto"""
        return {
            "completed_exercises": {},   # {"2024-01-15": ["tue_01", "tue_02"]}
            "completed_days": [],        # ["2024-01-15", "2024-01-16"]
            "streak": 0,
            "last_streak_date": None,
            "total_sessions": 0,
        }

    def save(self):
        """Guardar datos al archivo JSON"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self._data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Error guardando datos: {e}")

    # ── Ejercicios completados ──────────────────────────────────────────

    def get_completed_exercises(self, day_str=None):
        """Obtener ejercicios completados para un día"""
        if day_str is None:
            day_str = date.today().isoformat()
        return self._data["completed_exercises"].get(day_str, [])

    def toggle_exercise(self, exercise_id, day_str=None):
        """Marcar/desmarcar un ejercicio como completado"""
        if day_str is None:
            day_str = date.today().isoformat()

        if day_str not in self._data["completed_exercises"]:
            self._data["completed_exercises"][day_str] = []

        completed = self._data["completed_exercises"][day_str]
        if exercise_id in completed:
            completed.remove(exercise_id)
            is_done = False
        else:
            completed.append(exercise_id)
            is_done = True

        self.save()
        return is_done

    def is_exercise_completed(self, exercise_id, day_str=None):
        """Verificar si un ejercicio está completado"""
        if day_str is None:
            day_str = date.today().isoformat()
        return exercise_id in self.get_completed_exercises(day_str)

    # ── Días completados y racha ────────────────────────────────────────

    def mark_day_complete(self, day_str=None):
        """Marcar un día de entrenamiento como completado"""
        if day_str is None:
            day_str = date.today().isoformat()

        if day_str not in self._data["completed_days"]:
            self._data["completed_days"].append(day_str)
            self._data["total_sessions"] += 1
            self._update_streak(day_str)
            self.save()

    def _update_streak(self, day_str):
        """Actualizar la racha de días consecutivos"""
        today = date.fromisoformat(day_str)
        last_str = self._data.get("last_streak_date")

        if last_str:
            last = date.fromisoformat(last_str)
            diff = (today - last).days
            if diff == 1:
                self._data["streak"] += 1
            elif diff > 1:
                self._data["streak"] = 1
            # diff == 0: mismo día, no cambiar
        else:
            self._data["streak"] = 1

        self._data["last_streak_date"] = day_str

    def get_streak(self):
        """Obtener racha actual de días"""
        return self._data.get("streak", 0)

    def get_total_sessions(self):
        """Obtener total de sesiones completadas"""
        return self._data.get("total_sessions", 0)

    def get_completed_days(self):
        """Obtener lista de días completados"""
        return self._data.get("completed_days", [])

    def is_today_complete(self):
        """Verificar si el día de hoy fue completado"""
        return date.today().isoformat() in self._data.get("completed_days", [])

    # ── Progreso semanal ────────────────────────────────────────────────

    def get_weekly_progress(self):
        """Obtener progreso de la semana actual"""
        today = date.today()
        # Obtener el lunes de esta semana
        monday = today - timedelta(days=today.weekday())
        week_days = [monday + timedelta(days=i) for i in range(7)]

        progress = {}
        for d in week_days:
            d_str = d.isoformat()
            progress[d_str] = d_str in self._data.get("completed_days", [])
        return progress

    def get_completion_percentage(self, day_str=None):
        """Calcular porcentaje de ejercicios completados hoy"""
        if day_str is None:
            day_str = date.today().isoformat()
        completed = self.get_completed_exercises(day_str)
        return len(completed)
