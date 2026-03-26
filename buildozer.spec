[app]

# Información básica de la app
title = GymTracker
package.name = gymtracker
package.domain = com.personal

# Archivo principal
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

# Versión
version = 1.0.0

# Dependencias Python
requirements = python3,kivy==2.3.0,plyer,android

# Orientación
orientation = portrait

# Permisos Android necesarios
android.permissions = INTERNET,RECEIVE_BOOT_COMPLETED,VIBRATE,POST_NOTIFICATIONS,WAKE_LOCK

# SDK Android
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33

# Arquitecturas
android.archs = arm64-v8a, armeabi-v7a

# Servicios Android para notificaciones en background
# android.services = notification:utils/notification_service.py

# Gradle
android.gradle_dependencies = 'androidx.core:core:1.10.0'

# Opciones de compilación
android.allow_backup = True
android.logcat_filters = *:S python:D

# Icono y splash (opcional - reemplazar con archivos propios)
# icon.filename = %(source.dir)s/assets/icon.png
# presplash.filename = %(source.dir)s/assets/splash.png

# Colores de splash
android.presplash_color = #0D0D0D

[buildozer]
log_level = 2
warn_on_root = 1

# Directorio de build
# build_dir = ./.buildozer
# bin_dir = ./bin
