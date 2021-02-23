import os

import cv2

WEATHER_INTENTS = [
    {
        'name': 'cloud',
        'tokens': ('foggy', 'cloudy', 'overcast'),
        'image': 'files/cloud.png',
        'gradient': (59, 59, 59)
    },
    {
        'name': 'rain',
        'tokens': ('rain', 'drizzle'),
        'image': 'files/rain.png',
        'gradient': (255, 0, 26)
    },
    {
        'name': 'snow',
        'tokens': ('snow',),
        'image': 'files/snow.png',
        'gradient': (255, 205, 26)
    },
    {
        'name': 'sun',
        'tokens': ('clear', 'sun',),
        'image': 'files/sun.png',
        'gradient': (26, 228, 255)
    }
]


def make_gradient(image, color):
    for y in range(image.shape[0]):
        b, g, r = color
        cv2.line(image, (0, y), (image.shape[1], y), color=color)
        if b < 255:
            b += 1
        if g < 255:
            g += 1
        if r < 255:
            r += 1
        color = (b, g, r)


def view_image(image, name_of_window):
    cv2.namedWindow(name_of_window, cv2.WINDOW_NORMAL)
    cv2.imshow(name_of_window, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def save_image(image, path, image_name):
    if os.path.exists(path):
        file_name = path + image_name
        cv2.imwrite(file_name, image)
        print(f'Saved at {file_name}')
    else:
        os.makedirs(path)
        file_name = path + image_name
        cv2.imwrite(file_name, image)
        print(f'Saved at {file_name}')
