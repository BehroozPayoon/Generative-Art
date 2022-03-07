import colorsys

from PIL import Image, ImageDraw, ImageChops
import random

target_size = 256
scale_factor = 2
image_size = target_size * scale_factor
image_bg_color = (0, 0, 0)
padding = 16 * scale_factor
points = []


def generate_art(path: str):
    image = Image.new("RGB", (image_size, image_size), image_bg_color)
    generate_points()
    make_points_centered()

    thickness = 0
    start_color = generate_random_color()
    end_color = generate_random_color()
    for i, point in enumerate(points):
        overlay_image = Image.new("RGB", (image_size, image_size), image_bg_color)
        overlay_draw = ImageDraw.Draw(overlay_image)

        start_point = point
        if i == len(points) - 1:
            end_point = points[0]
        else:
            end_point = points[i + 1]
        coordinates = (start_point, end_point)
        thickness += scale_factor
        line_color = interpolate_color(start_color, end_color, i / len(points) - 1)
        overlay_draw.line(coordinates, fill=line_color, width=thickness)
        image = ImageChops.add(image, overlay_image)
    image = image.resize((target_size, target_size), resample=Image.ANTIALIAS)
    image.save(path)


def generate_points():
    del points[:]
    for _ in range(10):
        points.append((random.randint(padding, image_size - padding),
                       random.randint(padding, image_size - padding)))


def make_points_centered():
    min_x = min([p[0] for p in points])
    max_x = max([p[0] for p in points])
    min_y = min([p[1] for p in points])
    max_y = max([p[1] for p in points])

    delta_x = min_x - (image_size - max_x)
    delta_y = min_y - (image_size - max_y)

    for i, point in enumerate(points):
        points[i] = (point[0] - delta_x // 2, point[1] - delta_y // 2)


def generate_random_color():
    h = random.random()
    s = 1
    v = 1

    float_rgb = colorsys.hsv_to_rgb(h, s, v)
    rgb = [int(x * 255) for x in float_rgb]
    return tuple(rgb)


def interpolate_color(start_color, end_color, factor: float):
    recip = 1 - factor
    return (
        int(start_color[0] * recip) + int(end_color[0] * factor),
        int(start_color[1] * recip) + int(end_color[1] * factor),
        int(start_color[2] * recip) + int(end_color[2] * factor),
    )


if __name__ == "__main__":
    for i in range(10):
        generate_art(f"images/test_image_{i}.png")