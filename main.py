from polygon_maker import make_picture
from image_to_3d_gif_maker import make_gif
import os
from tqdm import tqdm

# Error checking input
# ______________________________
num_images = int(input("How many images would you like: "))
while True:
    if num_images <= 0:
        print('Number of images must be a positive integer!')
        num_images = int(input("How many images would you like: "))
    else:
        break
# ______________________________


# Create 2d images and put them in 2d images folder
# ______________________________
flat_image_folder_path = os.path.join(os.getcwd(), '2d_images')
gif_image_folder_path = os.path.join(os.getcwd(), 'gif_images')
for x in tqdm(range(num_images)):
    make_picture(os.path.join(flat_image_folder_path, f"image_{x}.png"))
# ______________________________


# Create 3d gif images and put then in 3d images folder
# ______________________________

for img_counter, image_file in enumerate(os.listdir(flat_image_folder_path)):
    if image_file.split('.')[1] == 'png':
        # make_gif(os.path.join(gif_image_folder_path, f"image_{x}.gif"))
        make_gif(image_file, '2d_images',
                 f"image_{img_counter}.gif", 'gif_images')
# ______________________________
