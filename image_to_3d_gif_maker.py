# File name: image_to_3d_gif_maker.py
# Description: generates gif of 3d object rotating in space given an image as input
# Author Name: Alvin Matthew
# Date Created: Tuesday, April 7, 2022
# Last Modified: Wednesday, April 8, 2022
# Instructor Name: Mr Tauro

import pygame
import numpy as np
import os
from PIL import Image
from tqdm import tqdm

os.environ["SDL_VIDEODRIVER"] = "dummy" # hides pygame window

pygame.init()
clock = pygame.time.Clock()
WIDTH = HEIGHT = 500 # keep width and height the same
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NFT Generator")

# Constant declarations
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

SCALE_FACTOR = 2 # distance between points
SCALE_FACTOR_CHANGE = 1
original_scale_factor = SCALE_FACTOR
ANGLE_CHANGE = 10*(np.pi/180)
NODE_SIZE = 1

# interpolation function
def convert_ranges(value, value_min, value_max, new_min, new_max):
    return (((value - value_min) * (new_max - new_min)) / (value_max - value_min)) + new_min


# convert 3 values (r, g, b) to one height value
def rgb_to_height(r, g, b):
    return convert_ranges(65536 * r + 256 * g + b, b, 65536 * 255 + 256 * 255 + 255, 0, 1)


def hsv_to_rgb(h, s, v):
    if s == 0.0: v*=255; return (v, v, v)
    i = int(h*6.)
    f = (h*6.)-i; p,q,t = int(255*(v*(1.-s))), int(255*(v*(1.-s*f))), int(255*(v*(1.-s*(1.-f)))); v*=255; i%=6
    if i == 0: return (v, t, p)
    if i == 1: return (q, v, p)
    if i == 2: return (p, v, t)
    if i == 3: return (p, q, v)
    if i == 4: return (t, p, v)
    if i == 5: return (v, p, q)

# collection of functions that rotate a shape by a given angle
#________________________________________________________________
def rotate_x_axis(matrix, theta):
    rotation_matrix = np.array([[1, 0, 0],
                                [0, np.cos(theta), -np.sin(theta)],
                                [0, np.sin(theta), np.cos(theta)]])
    return np.dot(matrix, rotation_matrix)


def rotate_y_axis(matrix, theta):
    rotation_matrix = np.array([[np.cos(theta), 0, np.sin(theta)],
                                [0, 1, 0],
                                [-np.sin(theta), 0, np.cos(theta)]])
    return np.dot(matrix, rotation_matrix)


def rotate_z_axis(matrix, theta):
    rotation_matrix = np.array([[np.cos(theta), -np.sin(theta), 0],
                                [np.sin(theta), np.cos(theta), 0],
                                [0, 0, 1]])
    return np.dot(matrix, rotation_matrix)
#________________________________________________________________


def scale_array(x):
 return x*SCALE_FACTOR + WIDTH//2


def make_gif(flat_image_file_name, flat_image_folder, gif_name, gif_folder):


    # image must have the same width and height
    img_size = 70, 70
    img_path = os.path.join(os.getcwd(), flat_image_folder, flat_image_file_name)
    img = Image.open(img_path)
    img = img.resize((100, 100), Image.ANTIALIAS)
    img_array = np.array(img)

    global BOUND
    BOUND = len(img_array)//2 # integer distance from origin

    # checks if the array index is at the edges of the array to avoid making long triangles
    def in_bound(x):
        for i in range(2*BOUND, (2*BOUND+1)**2+1, 2*BOUND+1):
            if i == x:
                return True
        return False

    # create array to hold all coordinates
    original_points_list = [[x, y, rgb_to_height(img_array[x][y][0], img_array[x][y][1], img_array[x][y][2])*100] for x in range(-BOUND, BOUND+1) for y in range(-BOUND, BOUND+1)]
    original_points_list = np.array(original_points_list)

    projection_matrix = np.array([[1, 0, 0],
                                [0, 1, 0],
                                [0, 0, 0]])


    # draws the net that connects all points
    def draw_coordinate_fill_shape(color_1, color_2, matrix, elem):
        pygame.draw.polygon(WIN, color_1, ((matrix[elem][0], matrix[elem][1]), (matrix[elem+BOUND*2+1][0], matrix[elem+BOUND*2+1][1]), (matrix[elem+BOUND*2+2][0], matrix[elem+BOUND*2+2][1])))
        pygame.draw.polygon(WIN, color_2, ((matrix[elem][0], matrix[elem][1]), (matrix[elem+1][0], matrix[elem+1][1]), (matrix[elem + BOUND*2+2][0], matrix[elem+BOUND*2+2][1])))



    def draw_matrix(matrix, node_size=NODE_SIZE, line_width=1):
        matrix = scale_array(matrix)

        for elem in range(len(matrix)):

            if elem < len(matrix) - BOUND*2-2 and not in_bound(elem):

                color_1 = list(img_array[elem//(BOUND*2+1)][elem//(BOUND*2+1)])
                color_2 = list(img_array[elem//(BOUND*2+2)][elem//(BOUND*2+2)])

                draw_coordinate_fill_shape(color_1, color_2, matrix, elem)



    two_dim_projection = original_points_list
    three_dim_points_copy = original_points_list

    gif_array = [] # stores all rotation instances of array

    for angle in tqdm(np.arange(0, 2*np.pi, ANGLE_CHANGE)):
        WIN.fill(WHITE)

        three_dim_points_copy = rotate_y_axis(three_dim_points_copy, ANGLE_CHANGE)
        three_dim_points_copy = rotate_x_axis(three_dim_points_copy, ANGLE_CHANGE)
        two_dim_projection = np.dot(three_dim_points_copy, projection_matrix)

        draw_matrix(two_dim_projection)

        imgdata = pygame.surfarray.array3d(WIN)
        imgdata = imgdata.swapaxes(0,1)
        gif_array.append(imgdata)

    gif_array = np.array(gif_array, dtype=np.uint8)

    imgs = [Image.fromarray(img) for img in gif_array]
    imgs[0].save(os.path.join(gif_folder, gif_name), save_all=True, append_images=imgs[1:], duration=100, loop=0)


if __name__ == "__main__":
    make_gif('image_0.png', '2d_images', 'test.gif', 'gif_images')
