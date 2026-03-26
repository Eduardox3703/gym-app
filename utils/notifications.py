"""
Utilidad de notificaciones usando plyer
Compatible con Android a través de Buildozer
"""

from datetime import datetime
from kivy.utils import platform


def schedule_daily_notification():
    """
    Programar notificación diaria a las 6:00 PM
    Usa plyer para compatibilidad con Android
    """
    try:
        from plyer import notification
        _send_notification_if_needed(notification)
    except ImportError:
        print("plyer no disponible – notificaciones deshabilitadas en escritorio")
    except Exception as e:
        print(f"Error en notificaciones: {e}")


def _send_notification_if_needed(notification):
    """Enviar notificación según el día y la hora"""
    now = datetime.now()
    weekday = now.weekday()  # 0=Lunes, 6=Domingo

    # Solo enviar si es aproximadamente las 6 PM (18:00)
    # En Android real, se usaría un servicio en segundo plano
    # Aquí verificamos si estamos en el horario correcto
    is_evening = now.hour == 18

    if not is_evening:
        # Para testing, enviar igual en modo debug
        if platform != 'android':
            _send_notification_now(notification, weekday)
        return

    _send_notification_now(notification, weekday)


def _send_notification_now(notification, weekday=None):
    """Enviar la notificación inmediatamente"""
    if weekday is None:
        weekday = datetime.now().weekday()

    if weekday == 6:  # Domingo
        title = "GymTracker 🚶"
        message = "Caminata larga: objetivo 12–18 km 🚶‍♂️ ¡Sal a caminar!"
    elif weekday == 0:  # Lunes
        title = "GymTracker 😴"
        message = "Hoy es día de descanso. Recupera tu energía 💤"
    elif weekday == 5:  # Sábado
        title = "GymTracker 🧘"
        message = "Actividad ligera hoy. Muévete a tu ritmo 🌿"
    else:
        title = "GymTracker 💪"
        message = "¡Hora de entrenar! Tu rutina de hoy te espera 🔥"

    try:
        notification.notify(
            title=title,
            message=message,
            app_name="GymTracker",
            app_icon='',
            timeout=10,
        )
    except Exception as e:
        print(f"No se pudo enviar notificación: {e}")


def send_test_notification():
    """Enviar notificación de prueba"""
    try:
        from plyer import notification
        notification.notify(
            title="GymTracker ✅",
            message="Las notificaciones están funcionando correctamente 🎉",
            app_name="GymTracker",
            timeout=5,
        )
        return True
    except Exception as e:
        print(f"Error en notificación de prueba: {e}")
        return False
