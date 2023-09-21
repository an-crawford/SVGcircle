#!/usr/bin/env python
# coding: utf-8

# In[215]:


import math
import svgwrite
from scipy.optimize import fsolve
import numpy as np 

# Create a new SVG drawing
def CircleSVG(image, output, circle_radius, total_images, height = 1000, width = 1000, original_svg_width = 80, original_svg_height = 100): 
    dwg = svgwrite.Drawing(output, profile='tiny', size=(height, width))

    # Load the original SVG image
    original_svg = svgwrite.image.Image(image)
    
    def f(n):
        return (total_images - n-1) - (((n ** 2 + n) /2 )* 8)

    n = np.ceil(fsolve(f, 4))
    num_circles = n+1
    num_circles = int(num_circles)
    n2 = num_circles - 1
    k = (total_images - n2)/((n2**2 +n2)/2)

    # Spacing between circles
    circle_spacing = 4 * circle_radius  
    current_images = 0 
    
    # Create concentric circles with variable images
    for i in range(num_circles):
        radius = circle_radius + i * circle_spacing  # Calculate the radius for each circle

        # Calculate the number of images for the current circle
        if i ==0: 
            num_images = 1
            current_images +=1
        else:
            if current_images + round(i * k + 1) < total_images: 
                num_images = round(i * k + 1)
                current_images += num_images
            else: 
                num_images = total_images - current_images
                current_images += num_images
        #print(num_images)
        # Create duplicates on the current circle
        for j in range(num_images):
            if i == 0: 
                x = (width/2) - (original_svg_width/2)
                y = (height/2) - (original_svg_height/2)
            else:
                angle = (j / num_images) * 2 * math.pi  # Calculate the angle for each image
                x = (width/2) + radius * math.cos(angle) - original_svg_width / 2
                y = (height/2) + radius * math.sin(angle) - original_svg_height / 2

            # Duplicate the original SVG image
            duplicate_svg = svgwrite.image.Image(image)

            # Set the position and size of the duplicated image
            duplicate_svg['x'] = str(x)
            duplicate_svg['y'] = str(y)
            duplicate_svg['width'] = str(original_svg_width)
            duplicate_svg['height'] = str(original_svg_height)

            # Add the duplicated image to the drawing
            dwg.add(duplicate_svg)

    # Save the drawing to an SVG file
    dwg.save()


# In[218]:


CircleSVG(image = 'person.svg', output = 'output_variable_images_per_circle.svg',  circle_radius = 24, total_images= 69)


# In[ ]:




