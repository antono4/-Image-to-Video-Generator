"""Video generation logic using OpenCV."""

import os
import tempfile
import numpy as np
from PIL import Image
import cv2
from typing import Optional, Callable

from .effects import (
    EffectType, 
    get_effect_function, 
    get_fade_opacity,
    generate_ken_burns_zoom_in,
    generate_ken_burns_zoom_out,
    generate_pan_left,
    generate_pan_right,
    generate_pan_up,
    generate_pan_down,
    generate_zoom_rotate,
    generate_fade_through
)


def generate_video(
    image_path: str,
    output_path: str,
    effect_type: EffectType,
    duration: float = 3.0,
    zoom_level: float = 1.2,
    fps: int = 30,
    progress_callback: Optional[Callable[[float], None]] = None
) -> bool:
    """
    Generate an animated video from a static image.
    
    Args:
        image_path: Path to the input image
        output_path: Path for the output video
        effect_type: Type of animation effect
        duration: Video duration in seconds
        zoom_level: Maximum zoom level for the effect
        fps: Frames per second
        progress_callback: Optional callback for progress updates (0.0 to 1.0)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Load image
        img = Image.open(image_path)
        img_array = np.array(img)
        
        # Convert to RGB if necessary
        if len(img_array.shape) == 2:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2RGB)
        elif img_array.shape[2] == 4:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)
        else:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
        
        img_height, img_width = img_array.shape[:2]
        
        # Calculate output dimensions (match canvas to image with max 1920 width)
        max_width = 1920
        if img_width > max_width:
            scale = max_width / img_width
            canvas_width = max_width
            canvas_height = int(img_height * scale)
        else:
            canvas_width = img_width
            canvas_height = img_height
        
        # Ensure dimensions are even
        canvas_width = canvas_width - (canvas_width % 2)
        canvas_height = canvas_height - (canvas_height % 2)
        
        total_frames = int(duration * fps)
        
        # Setup video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (canvas_width, canvas_height))
        
        # Get effect function
        effect_func = get_effect_function(effect_type)[1]
        
        # Determine start and end zoom based on effect
        if effect_type == EffectType.KEN_BURNS_ZOOM_IN:
            start_zoom = 1.0
            end_zoom = zoom_level
        elif effect_type == EffectType.KEN_BURNS_ZOOM_OUT:
            start_zoom = zoom_level
            end_zoom = 1.0
        elif effect_type == EffectType.ZOOM_ROTATE:
            start_zoom = 1.0
            end_zoom = zoom_level
        else:
            start_zoom = zoom_level
            end_zoom = zoom_level
        
        # Generate frames
        for frame_num in range(total_frames):
            frame = generate_frame(
                img_array,
                frame_num,
                total_frames,
                effect_type,
                effect_func,
                start_zoom,
                end_zoom,
                img_width,
                img_height,
                canvas_width,
                canvas_height
            )
            
            out.write(frame)
            
            if progress_callback:
                progress_callback((frame_num + 1) / total_frames)
        
        out.release()
        return True
        
    except Exception as e:
        print(f"Error generating video: {e}")
        return False


def generate_frame(
    img_array: np.ndarray,
    frame_num: int,
    total_frames: int,
    effect_type: EffectType,
    effect_func: Callable,
    start_zoom: float,
    end_zoom: float,
    img_width: int,
    img_height: int,
    canvas_width: int,
    canvas_height: int
) -> np.ndarray:
    """Generate a single frame with the applied effect."""
    
    # Get effect parameters
    zoom, pan_x, pan_y = effect_func(
        frame_num,
        total_frames,
        start_zoom,
        end_zoom,
        img_width,
        img_height,
        canvas_width,
        canvas_height
    )
    
    # Apply transformations
    if effect_type == EffectType.FADE_THROUGH:
        frame = apply_fade_effect(
            img_array, frame_num, total_frames, zoom,
            img_width, img_height, canvas_width, canvas_height
        )
    else:
        frame = apply_transform(
            img_array, zoom, pan_x, pan_y,
            img_width, img_height, canvas_width, canvas_height
        )
    
    return frame


def apply_transform(
    img_array: np.ndarray,
    zoom: float,
    pan_x: float,
    pan_y: float,
    img_width: int,
    img_height: int,
    canvas_width: int,
    canvas_height: int
) -> np.ndarray:
    """Apply zoom and pan transformation to create a frame."""
    
    # Calculate new dimensions
    new_width = int(img_width * zoom)
    new_height = int(img_height * zoom)
    
    # Resize image
    resized = cv2.resize(img_array, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)
    
    # Calculate crop position based on pan
    center_x = new_width // 2
    center_y = new_height // 2
    
    offset_x = int(center_x * pan_x)
    offset_y = int(center_y * pan_y)
    
    # Calculate crop bounds
    left = max(0, min(center_x + offset_x - canvas_width // 2, new_width - canvas_width))
    top = max(0, min(center_y + offset_y - canvas_height // 2, new_height - canvas_height))
    
    # Ensure we don't go out of bounds
    left = min(left, max(0, new_width - canvas_width))
    top = min(top, max(0, new_height - canvas_height))
    
    # Crop to canvas size
    cropped = resized[top:top + canvas_height, left:left + canvas_width]
    
    # If crop is smaller than canvas (edge case), pad with black
    if cropped.shape[0] < canvas_height or cropped.shape[1] < canvas_width:
        result = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)
        y_offset = (canvas_height - cropped.shape[0]) // 2
        x_offset = (canvas_width - cropped.shape[1]) // 2
        result[y_offset:y_offset + cropped.shape[0], x_offset:x_offset + cropped.shape[1]] = cropped
        return result
    
    return cropped


def apply_fade_effect(
    img_array: np.ndarray,
    frame_num: int,
    total_frames: int,
    zoom: float,
    img_width: int,
    img_height: int,
    canvas_width: int,
    canvas_height: int
) -> np.ndarray:
    """Apply fade through black effect."""
    
    opacity = get_fade_opacity(frame_num, total_frames)
    
    if opacity > 0:
        # Get transformed frame
        frame = apply_transform(
            img_array, zoom, 0, 0,
            img_width, img_height, canvas_width, canvas_height
        )
        # Blend with black
        frame = (frame * opacity).astype(np.uint8)
    else:
        # Black frame
        frame = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)
    
    return frame


def get_video_info(video_path: str) -> dict:
    """Get information about a video file."""
    cap = cv2.VideoCapture(video_path)
    
    info = {
        'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        'fps': cap.get(cv2.CAP_PROP_FPS),
        'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
        'duration': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) / cap.get(cv2.CAP_PROP_FPS)
    }
    
    cap.release()
    return info