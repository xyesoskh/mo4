from moviepy.editor import *
import numpy as np

# Путь к изображению
img_path = "skeleton.png"  # Замени на своё имя файла

# Длительность анимации
duration = 6

# Загружаем изображение
clip = ImageClip(img_path, duration=duration)

# Анимационные эффекты: зубы, улыбка
def animate_frame(get_frame, t):
    frame = get_frame(t).copy()

    # Скрежет зубами (периодические горизонтальные сдвиги нижней части)
    if 1 < t < 3:
        shift = int(2 * np.sin(20 * np.pi * t))
        frame[frame.shape[0]//2:] = np.roll(frame[frame.shape[0]//2:], shift, axis=1)

    # Улыбка — сдвиг нижней части вниз
    if 5 < t < 6:
        shift_down = int(5 * (t - 5))
        frame[frame.shape[0]//2:] = np.roll(frame[frame.shape[0]//2:], shift_down, axis=0)

    # Моргающий глаз (затухание верхней части)
    if int(t * 2) % 4 == 0 and 0.5 < t % 2 < 0.6:
        frame[:frame.shape[0]//4] = (frame[:frame.shape[0]//4] * 0.3).astype(np.uint8)

    return frame

# Применяем эффекты
animated_clip = clip.fl(animate_frame)

# Эффекты движения: приближение + покачивание
final_clip = (
    animated_clip
    .resize(lambda t: 1 + 0.02 * t)  # приближение (заглядывает в экран)
    .set_position(lambda t: ("center", 10 * np.sin(2 * np.pi * t)))  # движение вверх-вниз (лупа)
)

# Сохраняем в файл
final_clip.write_videofile("neon_skeleton_animation.mp4", fps=24)
