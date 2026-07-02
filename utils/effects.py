"""Animation effect definitions and configurations."""

from enum import Enum
from typing import Tuple, Callable
import math


class EffectType(Enum):
    """Available animation effect types."""
    KEN_BURNS_ZOOM_IN = "ken_burns_zoom_in"
    KEN_BURNS_ZOOM_OUT = "ken_burns_zoom_out"
    PAN_LEFT = "pan_left"
    PAN_RIGHT = "pan_right"
    PAN_UP = "pan_up"
    PAN_DOWN = "pan_down"
    ZOOM_ROTATE = "zoom_rotate"
    FADE_THROUGH = "fade_through"


EFFECT_OPTIONS = [
    "Ken Burns Zoom In",
    "Ken Burns Zoom Out",
    "Pan Left",
    "Pan Right",
    "Pan Up",
    "Pan Down",
    "Zoom & Rotate",
    "Fade Through",
]

EFFECT_MAP = {
    "Ken Burns Zoom In": EffectType.KEN_BURNS_ZOOM_IN,
    "Ken Burns Zoom Out": EffectType.KEN_BURNS_ZOOM_OUT,
    "Pan Left": EffectType.PAN_LEFT,
    "Pan Right": EffectType.PAN_RIGHT,
    "Pan Up": EffectType.PAN_UP,
    "Pan Down": EffectType.PAN_DOWN,
    "Zoom & Rotate": EffectType.ZOOM_ROTATE,
    "Fade Through": EffectType.FADE_THROUGH,
}


def get_effect_function(effect_type: EffectType) -> Tuple[str, Callable]:
    """Get the effect name and generator function."""
    effects = {
        EffectType.KEN_BURNS_ZOOM_IN: ("zoom_in", generate_ken_burns_zoom_in),
        EffectType.KEN_BURNS_ZOOM_OUT: ("zoom_out", generate_ken_burns_zoom_out),
        EffectType.PAN_LEFT: ("pan_left", generate_pan_left),
        EffectType.PAN_RIGHT: ("pan_right", generate_pan_right),
        EffectType.PAN_UP: ("pan_up", generate_pan_up),
        EffectType.PAN_DOWN: ("pan_down", generate_pan_down),
        EffectType.ZOOM_ROTATE: ("zoom_rotate", generate_zoom_rotate),
        EffectType.FADE_THROUGH: ("fade", generate_fade_through),
    }
    return effects.get(effect_type, ("none", lambda *args: None))


def generate_ken_burns_zoom_in(frame: int, total_frames: int, 
                                start_zoom: float, end_zoom: float,
                                img_width: int, img_height: int,
                                canvas_width: int, canvas_height: int) -> Tuple[float, float, float]:
    """Generate Ken Burns zoom in effect parameters."""
    progress = frame / total_frames
    
    # Smooth easing
    eased = ease_in_out_cubic(progress)
    
    zoom = start_zoom + (end_zoom - start_zoom) * eased
    
    # Subtle pan during zoom
    pan_x = 0.02 * math.sin(progress * math.pi * 0.5)
    pan_y = 0.02 * math.cos(progress * math.pi * 0.5)
    
    return zoom, pan_x, pan_y


def generate_ken_burns_zoom_out(frame: int, total_frames: int,
                                 start_zoom: float, end_zoom: float,
                                 img_width: int, img_height: int,
                                 canvas_width: int, canvas_height: int) -> Tuple[float, float, float]:
    """Generate Ken Burns zoom out effect parameters."""
    progress = frame / total_frames
    eased = ease_in_out_cubic(progress)
    
    zoom = start_zoom - (start_zoom - end_zoom) * eased
    
    # Subtle pan
    pan_x = -0.02 * math.sin(progress * math.pi * 0.5)
    pan_y = 0.02 * math.sin(progress * math.pi)
    
    return zoom, pan_x, pan_y


def generate_pan_left(frame: int, total_frames: int,
                      start_zoom: float, end_zoom: float,
                      img_width: int, img_height: int,
                      canvas_width: int, canvas_height: int) -> Tuple[float, float, float]:
    """Generate pan left effect parameters."""
    progress = frame / total_frames
    eased = ease_in_out_cubic(progress)
    
    # Calculate max pan distance
    max_pan_x = max(0, (img_width * start_zoom - canvas_width) / (2 * img_width * start_zoom))
    
    pan_x = -max_pan_x * eased
    pan_y = 0
    
    return start_zoom, pan_x, pan_y


def generate_pan_right(frame: int, total_frames: int,
                        start_zoom: float, end_zoom: float,
                        img_width: int, img_height: int,
                        canvas_width: int, canvas_height: int) -> Tuple[float, float, float]:
    """Generate pan right effect parameters."""
    progress = frame / total_frames
    eased = ease_in_out_cubic(progress)
    
    max_pan_x = max(0, (img_width * start_zoom - canvas_width) / (2 * img_width * start_zoom))
    
    pan_x = max_pan_x * eased
    pan_y = 0
    
    return start_zoom, pan_x, pan_y


def generate_pan_up(frame: int, total_frames: int,
                     start_zoom: float, end_zoom: float,
                     img_width: int, img_height: int,
                     canvas_width: int, canvas_height: int) -> Tuple[float, float, float]:
    """Generate pan up effect parameters."""
    progress = frame / total_frames
    eased = ease_in_out_cubic(progress)
    
    max_pan_y = max(0, (img_height * start_zoom - canvas_height) / (2 * img_height * start_zoom))
    
    pan_x = 0
    pan_y = -max_pan_y * eased
    
    return start_zoom, pan_x, pan_y


def generate_pan_down(frame: int, total_frames: int,
                       start_zoom: float, end_zoom: float,
                       img_width: int, img_height: int,
                       canvas_width: int, canvas_height: int) -> Tuple[float, float, float]:
    """Generate pan down effect parameters."""
    progress = frame / total_frames
    eased = ease_in_out_cubic(progress)
    
    max_pan_y = max(0, (img_height * start_zoom - canvas_height) / (2 * img_height * start_zoom))
    
    pan_x = 0
    pan_y = max_pan_y * eased
    
    return start_zoom, pan_x, pan_y


def generate_zoom_rotate(frame: int, total_frames: int,
                          start_zoom: float, end_zoom: float,
                          img_width: int, img_height: int,
                          canvas_width: int, canvas_height: int) -> Tuple[float, float, float]:
    """Generate zoom and rotate effect parameters."""
    progress = frame / total_frames
    eased = ease_in_out_cubic(progress)
    
    zoom = start_zoom + (end_zoom - start_zoom) * eased
    
    # Circular pan path
    radius = 0.05
    pan_x = radius * math.sin(progress * math.pi * 2)
    pan_y = radius * math.cos(progress * math.pi * 2) - radius
    
    return zoom, pan_x, pan_y


def generate_fade_through(frame: int, total_frames: int,
                           start_zoom: float, end_zoom: float,
                           img_width: int, img_height: int,
                           canvas_width: int, canvas_height: int) -> Tuple[float, float, float]:
    """Generate fade through effect parameters."""
    progress = frame / total_frames
    
    # Use zoom for opacity simulation
    zoom = start_zoom + (end_zoom - start_zoom) * progress
    
    return zoom, 0, 0


def get_fade_opacity(frame: int, total_frames: int) -> float:
    """Get opacity for fade through effect (0-1)."""
    progress = frame / total_frames
    
    if progress < 0.4:
        # Fade out
        return 1.0 - (progress / 0.4)
    elif progress > 0.6:
        # Fade in
        return (progress - 0.6) / 0.4
    else:
        # Black frame in middle
        return 0.0


def ease_in_out_cubic(t: float) -> float:
    """Cubic easing function for smooth animation."""
    if t < 0.5:
        return 4 * t * t * t
    else:
        return 1 - pow(-2 * t + 2, 3) / 2