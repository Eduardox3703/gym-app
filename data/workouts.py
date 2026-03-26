"""
Definición de rutinas de entrenamiento por día de la semana
"""

WORKOUTS = {
    0: {  # Lunes
        "name": "Descanso",
        "type": "rest",
        "emoji": "😴",
        "color": "#2C2C2C",
        "exercises": [],
        "description": "Día de recuperación. Descansa, estira y prepárate para mañana.",
    },
    1: {  # Martes
        "name": "Torso – Fuerza",
        "type": "strength",
        "emoji": "🏋️",
        "color": "#1A3A5C",
        "exercises": [
            {"name": "Press de banca", "sets": 4, "reps": "6–8", "id": "tue_01"},
            {"name": "Remo con barra", "sets": 4, "reps": "6–8", "id": "tue_02"},
            {"name": "Press militar", "sets": 3, "reps": "6–8", "id": "tue_03"},
            {"name": "Jalón al pecho", "sets": 3, "reps": "8", "id": "tue_04"},
            {"name": "Curl de bíceps", "sets": 3, "reps": "10", "id": "tue_05"},
            {"name": "Tríceps en polea", "sets": 3, "reps": "10", "id": "tue_06"},
        ],
        "description": "Sesión de fuerza en torso. Pesos altos, pocas repeticiones.",
    },
    2: {  # Miércoles
        "name": "Pierna – Fuerza",
        "type": "strength",
        "emoji": "🦵",
        "color": "#1A3A5C",
        "exercises": [
            {"name": "Sentadilla", "sets": 4, "reps": "6–8", "id": "wed_01"},
            {"name": "Peso muerto rumano", "sets": 3, "reps": "6–8", "id": "wed_02"},
            {"name": "Prensa", "sets": 3, "reps": "8", "id": "wed_03"},
            {"name": "Curl femoral", "sets": 3, "reps": "10", "id": "wed_04"},
            {"name": "Pantorrilla", "sets": 4, "reps": "12–15", "id": "wed_05"},
        ],
        "description": "Sesión de fuerza en piernas. Enfócate en la técnica.",
    },
    3: {  # Jueves
        "name": "Torso – Hipertrofia",
        "type": "hypertrophy",
        "emoji": "💪",
        "color": "#1A1A4A",
        "exercises": [
            {"name": "Press inclinado mancuernas", "sets": 4, "reps": "8–12", "id": "thu_01"},
            {"name": "Remo en máquina", "sets": 4, "reps": "8–12", "id": "thu_02"},
            {"name": "Elevaciones laterales", "sets": 4, "reps": "12–15", "id": "thu_03"},
            {"name": "Face pull", "sets": 3, "reps": "12–15", "id": "thu_04"},
            {"name": "Curl de bíceps", "sets": 3, "reps": "12", "id": "thu_05"},
            {"name": "Tríceps overhead", "sets": 3, "reps": "12", "id": "thu_06"},
        ],
        "description": "Sesión de hipertrofia en torso. Volumen y conexión mente-músculo.",
    },
    4: {  # Viernes
        "name": "Pierna – Hipertrofia",
        "type": "hypertrophy",
        "emoji": "🔥",
        "color": "#1A1A4A",
        "exercises": [
            {"name": "Prensa", "sets": 4, "reps": "10–12", "id": "fri_01"},
            {"name": "Extensión de cuadríceps", "sets": 3, "reps": "12–15", "id": "fri_02"},
            {"name": "Curl femoral", "sets": 3, "reps": "12–15", "id": "fri_03"},
            {"name": "Peso muerto ligero", "sets": 3, "reps": "10", "id": "fri_04"},
            {"name": "Pantorrilla", "sets": 4, "reps": "15", "id": "fri_05"},
        ],
        "description": "Sesión de hipertrofia en piernas. Siente el ardor.",
    },
    5: {  # Sábado
        "name": "Actividad ligera",
        "type": "light",
        "emoji": "🧘",
        "color": "#1A3A2A",
        "exercises": [],
        "description": "Movilidad, yoga, natación o cualquier actividad de baja intensidad. Tu cuerpo lo agradecerá.",
    },
    6: {  # Domingo
        "name": "Caminata larga",
        "type": "walk",
        "emoji": "🚶",
        "color": "#2A3A1A",
        "exercises": [
            {"name": "Caminata 12–18 km", "sets": 1, "reps": "objetivo", "id": "sun_01"},
        ],
        "description": "Caminata larga a ritmo moderado. Objetivo: 12–18 km.\nIdeal en naturaleza o parque.",
    },
}

MOTIVATIONAL_MESSAGES = {
    "rest": [
        "El descanso es parte del entrenamiento 💤",
        "Recupera, recarga y vuelve más fuerte 🔋",
        "Hoy descansas. Mañana conquistas 🌅",
    ],
    "strength": [
        "La fuerza no se regala, se gana 💪",
        "Cada rep te acerca a tu mejor versión ⚡",
        "Pesos altos, mente fuerte 🔥",
    ],
    "hypertrophy": [
        "El músculo crece en el esfuerzo sostenido 📈",
        "Volumen, consistencia, resultados 💎",
        "Hoy construyes el cuerpo de mañana 🏗️",
    ],
    "light": [
        "El movimiento ligero acelera la recuperación 🌊",
        "Activo pero descansado. El equilibrio perfecto ⚖️",
        "Muévete con intención hoy 🧘",
    ],
    "walk": [
        "Cada kilómetro cuenta. Sal a conquistarlos 🗺️",
        "La caminata larga limpia la mente y fortalece el cuerpo 🌿",
        "12–18 km entre tú y tu objetivo 👟",
    ],
}

DAY_NAMES_ES = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
