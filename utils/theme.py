"""
Tema visual y widgets reutilizables para GymTracker
Paleta oscura con acentos de color
"""

from kivy.utils import get_color_from_hex

# ── Paleta de colores ─────────────────────────────────────────────────────────

COLORS = {
    # Fondos
    'bg_dark':       '#0D0D0D',
    'bg_card':       '#1A1A1A',
    'bg_card_hover': '#242424',
    'bg_surface':    '#141414',

    # Acentos
    'accent_blue':   '#2979FF',
    'accent_teal':   '#00BFA5',
    'accent_orange': '#FF6D00',
    'accent_purple': '#7C4DFF',
    'accent_green':  '#00C853',

    # Texto
    'text_primary':   '#F5F5F5',
    'text_secondary': '#9E9E9E',
    'text_disabled':  '#424242',

    # Estados
    'success':  '#00C853',
    'warning':  '#FFD600',
    'error':    '#FF1744',

    # Días especiales
    'rest':        '#2C2C2C',
    'strength':    '#1A3A5C',
    'hypertrophy': '#1A1A4A',
    'light':       '#1A3A2A',
    'walk':        '#2A3A1A',
}

# Colores RGBA para Kivy (0-1 range)
def color(hex_str, alpha=1.0):
    """Convertir hex a RGBA para Kivy"""
    c = get_color_from_hex(hex_str)
    return (c[0], c[1], c[2], alpha)


# ── Cadena KV base con estilos ────────────────────────────────────────────────

KV_THEME = """
#:import get_color_from_hex kivy.utils.get_color_from_hex

<GymLabel@Label>:
    color: get_color_from_hex('#F5F5F5')
    font_size: '16sp'

<GymTitle@Label>:
    color: get_color_from_hex('#F5F5F5')
    font_size: '24sp'
    bold: True

<GymSubtitle@Label>:
    color: get_color_from_hex('#9E9E9E')
    font_size: '14sp'

<GymButton@Button>:
    background_color: get_color_from_hex('#2979FF')
    background_normal: ''
    color: get_color_from_hex('#FFFFFF')
    font_size: '16sp'
    bold: True
    size_hint_y: None
    height: '52dp'

<GymCard@BoxLayout>:
    canvas.before:
        Color:
            rgba: get_color_from_hex('#1A1A1A')
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [12, 12, 12, 12]
    padding: '16dp'
    spacing: '8dp'
"""
