
from PIL import Image
from collections import Counter
import numpy as np


def resize_image(img, max_dimension=600):

    width, height = img.size

    if width > max_dimension or height > max_dimension:

        if width > height:
            new_width = max_dimension
            new_height = int((max_dimension / width) * height)
        else:
            new_height = max_dimension
            new_width = int((max_dimension / height) * width)

        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        print(f"Image resized with size {img.size}")
        return img

    else:

        return img







def display_color(color):
    # Convert np.uint8 tuple to standard integer tuple
    color_int = tuple(map(int, color))
    return color_int
def rgb_distance(c1, c2):
    return np.linalg.norm(np.array(c1) - np.array(c2))

def group_similar_colors(pixels, threshold=15):

    def rgb_distance(c1, c2):
        return np.linalg.norm(np.array(c1) - np.array(c2))

    grouped_colors = []
    seen_colors = set()

    for color in pixels:
        if color not in seen_colors:
            # Group similar colors
            group = [color]
            for other_color in pixels:
                if other_color not in seen_colors and rgb_distance(color, other_color) < threshold:
                    group.append(other_color)
                    seen_colors.add(other_color)
            # Compute average color for the group
            avg_color = np.mean(group, axis=0).astype(int)
            grouped_colors.append(tuple(avg_color))

    return grouped_colors

def rgb_to_hex(rgb):

    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])
def get_most_popular_colors(image_path, num_colors=6000, threshold=15):
    # Load the image
    img = Image.open(image_path)
    img = resize_image(img)
    img = img.convert('RGB')  # Ensure image is in RGB mode

    img_np = np.array(img)

    # Reshape the image to be a list of pixels
    pixels = img_np.reshape(-1, 3)

    # Convert pixels to a list of tuples
    pixels = [tuple(pixel) for pixel in pixels]

    # Count the frequency of each color
    color_counts = Counter(pixels)

    # Find the most common colors
    most_common_colors = color_counts.most_common(num_colors)

    # Extract the colors
    top_colors = [display_color(color) for color, count in most_common_colors]

    top_colors_similar = [display_color(color) for color in group_similar_colors(top_colors, threshold=threshold)[:30]]

    top_colors_similar_hex = [rgb_to_hex(color) for color in top_colors_similar]


    return  top_colors_similar_hex,  top_colors_similar




