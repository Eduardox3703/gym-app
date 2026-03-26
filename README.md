# GymTracker 💪

Aplicación Android personal para seguimiento de rutina de gimnasio.
Desarrollada con Python + Kivy, compilable con Buildozer.

---

## Estructura del proyecto

```
gym_app/
├── main.py                  # Punto de entrada de la app
├── buildozer.spec           # Configuración de compilación para Android
├── requirements.txt
│
├── data/
│   ├── __init__.py
│   └── workouts.py          # Definición de rutinas por día
│
├── screens/
│   ├── __init__.py
│   ├── dashboard.py         # Pantalla principal
│   ├── routine.py           # Pantalla de ejercicios del día
│   └── progress.py          # Pantalla de progreso y estadísticas
│
└── utils/
    ├── __init__.py
    ├── storage.py           # Persistencia JSON local
    ├── notifications.py     # Notificaciones con plyer
    └── theme.py             # Colores y estilos reutilizables
```

---

## Funcionalidades

### Dashboard
- Muestra el entrenamiento del día según el calendario semanal
- Indicadores de días cumplidos en la semana
- Racha actual y total de sesiones
- Mensaje motivacional aleatorio según el tipo de entrenamiento

### Rutina del día
- Lista completa de ejercicios con series y repeticiones
- Checklist interactivo: toca cada ejercicio para marcarlo
- Barra de progreso visual
- Botón para marcar el día como completado

### Progreso
- Estadísticas: racha, sesiones totales, semanas activas, promedio semanal
- Calendario semanal con días completados destacados
- Historial de las últimas 10 sesiones

### Notificaciones
- Notificación diaria a las 6:00 PM
- Mensaje adaptado al tipo de entrenamiento del día
- Mensaje especial los domingos para la caminata

---

## Calendario de entrenamiento

| Día        | Entrenamiento              |
|------------|---------------------------|
| Lunes      | 😴 Descanso                |
| Martes     | 🏋️ Torso – Fuerza          |
| Miércoles  | 🦵 Pierna – Fuerza         |
| Jueves     | 💪 Torso – Hipertrofia     |
| Viernes    | 🔥 Pierna – Hipertrofia    |
| Sábado     | 🧘 Actividad ligera        |
| Domingo    | 🚶 Caminata larga (12–18km)|

---

## Instalación para desarrollo (escritorio)

```bash
# 1. Instalar dependencias
pip install kivy plyer

# 2. Ejecutar la app
cd gym_app
python main.py
```

---

## Compilar APK con Buildozer

### Requisitos previos
```bash
# En Ubuntu/Debian
sudo apt update
sudo apt install -y python3-pip build-essential git python3 python3-dev
sudo apt install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
sudo apt install -y libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev zlib1g-dev
sudo apt install -y libgstreamer1.0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good
sudo apt install -y build-essential libsqlite3-dev sqlite3 bzip2 libbz2-dev
sudo apt install -y zip unzip openjdk-17-jdk

# Instalar Buildozer
pip install buildozer
```

### Compilar
```bash
cd gym_app

# Primera compilación (descarga Android SDK/NDK, tarda ~20 min)
buildozer android debug

# El APK se genera en: bin/gymtracker-1.0.0-arm64-v8a-debug.apk
```

### Instalar en dispositivo
```bash
# Con el dispositivo conectado por USB (debug habilitado)
buildozer android deploy run

# O copiar el APK manualmente
adb install bin/gymtracker-1.0.0-arm64-v8a-debug.apk
```

### Compilación de release (firmada)
```bash
# Generar keystore (solo primera vez)
keytool -genkey -v -keystore gymtracker.keystore -alias gymtracker -keyalg RSA -keysize 2048 -validity 10000

# En buildozer.spec, agregar:
# android.keystore = gymtracker.keystore
# android.keyalias = gymtracker

buildozer android release
```

---

## Notas sobre notificaciones en Android

Las notificaciones en segundo plano en Android moderno requieren:
1. Permiso `POST_NOTIFICATIONS` (Android 13+) – ya incluido en buildozer.spec
2. Un servicio en background para notificaciones programadas

Para notificaciones exactas a las 6 PM, se recomienda usar `android.alarm` 
o un `Service` de Kivy. La implementación actual envía la notificación
cuando la app está abierta. Para notificaciones sin abrir la app, 
considera integrar `plyer.alarm` o un servicio Android nativo.

---

## Datos almacenados

Los datos se guardan en `gymtracker_data/gymdata.json`:
```json
{
  "completed_exercises": {
    "2024-01-16": ["tue_01", "tue_02", "tue_03"]
  },
  "completed_days": ["2024-01-15", "2024-01-16"],
  "streak": 2,
  "last_streak_date": "2024-01-16",
  "total_sessions": 2
}
```

En Android, los datos se almacenan en el directorio privado de la app
(no requiere permisos de almacenamiento externo).
