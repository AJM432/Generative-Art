#https://www.youtube.com/watch?v=BMq2Jrvp9AA, https://www.blog.pythonlibrary.org/2021/02/23/drawing-shapes-on-images-with-python-and-pillow/, 
#pillow library

from PIL import Image, ImageDraw, ImageChops
import random
import colorsys
import math


target_size_px = 1000
padding_px = 5

#area of triangle of three given points
def area(points:list):
    line_lengths = []

    for i, val in enumerate(points):
        p1 = val
        #the second point is either the next point or the first point
        if i == len(points)-1:
            p2 = points[0]
        else:
            p2 = points[i+1]

        #finding side lengths
        distance = math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
        line_lengths.append(distance)

    #heron's formula
    s = sum(line_lengths)/2
    a,b,c = line_lengths
    area = math.sqrt(s*(s-a)*(s-b)*(s-c))
    
    return area



#makes a random point
def random_point():
    return(random.randint(padding_px, target_size_px - padding_px), random.randint(padding_px, target_size_px - padding_px))

#returns a random colour
def random_color():
    #Hue saturation and value --> defining colours in a way that isn't rgb to generate colours to get the same hue of a colour

    #between 0 and 1
    h = random.random()
    #s and v at 1 make it always bright
    s = 1
    v = 1

    #convert hsv to rgb and to 255 as opposed to 1
    float_rgb = colorsys.hsv_to_rgb(h,s,v)
    rgb  = [int(x*255) for x in float_rgb]

    return tuple(rgb)

#returns the complementary colour to the h value entered
def complementary_color(old_h):
    h = abs(old_h+0.5)

    if h>1:
        h -=1

    s = 1
    v = 1

    #convert hsv to rgb and to 255 as opposed to 1
    float_rgb = colorsys.hsv_to_rgb(h,s,v)
    rgb  = [int(x*255) for x in float_rgb]

    return tuple(rgb)

#gets points for a n-sided polygon that takes up a certain size of the page
def big_polygon_points(num_vertices, decimal_of_page):

    while True:
        #getting variable number of points
        points = tuple([random_point() for i in range(num_vertices)])

        #checking min and max size of points
        min_x = min([i[0] for i in points])
        max_x = max([i[0] for i in points])
        min_y = min([i[1] for i in points])
        max_y = max([i[1] for i in points])

        #if the triangle has a large enough area it will return it, otherwise it goes back to the top of the loop if it's a tiny triangle
        if num_vertices == 3 and area(list(points)) > target_size_px**2 * decimal_of_page**3:
            break
        elif num_vertices == 3:
            continue

        #if polygon is big enough it'll return it, otherwise it goes back up to the top of the loop
        if abs(min_x-max_x) > target_size_px*decimal_of_page and abs(min_x-max_x) > target_size_px*decimal_of_page:
            break
        
    return(list(points))



def make_picture(output_path):

    #variable for if there is going to be overlay or not
    overlay = False


    #making the black image 
    image_bg_color = (0,0,0)
    image = Image.new("RGB", (target_size_px, target_size_px), image_bg_color)
    draw = ImageDraw.Draw(image)


    polygon_color = random_color() #color of polygon 
    polygon_color_h = colorsys.rgb_to_hsv(polygon_color[0]/255, polygon_color[1]/255, polygon_color[2]/255)[0] #converts (r,g,b) to (h,s,v), and takes the 0th index of the tuple (h)



    #drawing a line
    edge_pts = [(0,0), (0, target_size_px), (target_size_px, 0), (target_size_px, target_size_px)] #possible edge
    pts_for_line = (edge_pts.pop(random.randint(0,3)), edge_pts.pop(random.randint(0,2))) #choosing points for the line
    line_color = complementary_color(polygon_color_h + random.uniform(-0.3, 0.3)) #the line color will be almost complementary

    if not overlay:
        draw.line(pts_for_line, fill = line_color, width = random.randint(int(target_size_px*0.1),int(target_size_px*0.25)))
    else:
        #overlay canvas by making a new canvas FOR THE LINE
        overlay_image = Image.new("RGB", size = (target_size_px, target_size_px), color = image_bg_color)
        overlay_draw = ImageDraw.Draw(overlay_image)
        overlay_draw.line(pts_for_line, fill = random_color(), width = random.randint(20,60)) #drawing the line (onto the overlay image)
        image = ImageChops.add(image, overlay_image) #adding the overlay onto the image, by setting the reference of the image to the image we are saving (to add on colour to make it brighter)



    


    #comes up with the tuple for polygon points
    polygon = big_polygon_points(random.randint(3,5),0.5)
    #polygon = ((200,3), (300,40), (50,100))




    #draw bounding box by getting the minimum and maximum x and y values
    min_x = min([point[0] for point in polygon])
    max_x = max([point[0] for point in polygon])
    min_y = min([point[1] for point in polygon])
    max_y = max([point[1] for point in polygon])
    #draw.rectangle((min_x, min_y, max_x, max_y), outline = (255,0,0))

    #center the image
    delta_x = min_x - (target_size_px - max_x) #difference of distance on left and distance on right
    delta_y = min_y - (target_size_px - max_y)

    #push every point over by half the difference between the two x distances, and the 2 y distances
    for i, point in enumerate(polygon):
        polygon[i] = (point[0] - delta_x//2, point[1] - delta_y//2)

    polygon_tuple = tuple(polygon) #we need a tuple for the polygon function


    
    if not overlay:
        draw.polygon(polygon_tuple, fill = polygon_color, outline = None) #drawing the polygon
    else:
        #overlay canvas by making a new canvas FOR THE POLYGON
        overlay_image = Image.new("RGB", size = (target_size_px, target_size_px), color = image_bg_color)
        overlay_draw = ImageDraw.Draw(overlay_image)
        overlay_draw.polygon(polygon_tuple, fill = polygon_color, outline = None) #drawing the polygon (onto the overlay image)
        image = ImageChops.add(image, overlay_image) #adding the overlay onto the image, by setting the reference of the image to the image we are saving (to add on colour to make it brighter)




    #drawing a circle around one of the points
    circle_pt = polygon[random.randint(0, len(polygon)-1)]#determining the point that gets the circle around it
    circle_radius = random.randint(5, padding_px) #radius for the circle
    circle_bounding_box = ((circle_pt[0]-circle_radius, circle_pt[1]-circle_radius), (circle_pt[0]+circle_radius, circle_pt[1]+circle_radius)) #the two points that bound the box for the circle
    
    if not overlay:
        draw.ellipse(circle_bounding_box, fill = complementary_color(polygon_color_h)) #drawing the ellipse
    else:
        #overlay canvas by making a new canvas FOR THE CIRCLE
        overlay_image = Image.new("RGB", size = (target_size_px, target_size_px), color = image_bg_color)
        overlay_draw = ImageDraw.Draw(overlay_image)
        overlay_draw.ellipse(circle_bounding_box, fill = complementary_color(polygon_color_h)) #drawing the ellipse (onto the overlay image)
        image = ImageChops.add(image, overlay_image) #adding the overlay onto the image, by setting the reference of the image to the image we are saving (to add on colour to make it brighter)


    image.save(output_path)


    

"""
    #overlay canvas by constantly making a new canvas (GENERIC)
    overlay_image = Image.new("RGB", size = (target_size_px, target_size_px), color = image_bg_color)
    overlay_draw = ImageDraw.Draw(overlay_image)
    overlay_draw.line(line_xy, fill = line_color, width = thickness) #drawing the line (onto the overlay image)
    image = ImageChops.add(image, overlay_image) #adding the overlay onto the image, by setting the reference of the image to the image we are saving (to add on colour to make it brighter)
"""


if __name__ == "__main__":
    num_images = 2
    for i in range(num_images):
        make_picture(f"image{i}.jpeg")
