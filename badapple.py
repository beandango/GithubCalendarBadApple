import cv2
import numpy as np
from PIL import Image, ImageDraw
import imageio

# Load the video
cap = cv2.VideoCapture('badapple.mp4')

# GitHub activity graph color palette in dark mode (from lightest to darkest)
palette = [(57, 211, 83), (38, 166, 65), (0, 109, 50), (14, 68, 41), (22, 27, 34)]

# Cell size (including spacing)
cell_size = 10
spacing = 2.5

# Canvas size
canvas_size = ((53 + 1) * cell_size, (7 + 1) * cell_size)

frame_count = 0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret:
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Downscale the frame to match the size of the GitHub activity graph
        small = cv2.resize(gray, (53, 7), interpolation=cv2.INTER_AREA)
        
        # Map the grayscale levels to the GitHub color palette
        bins = np.linspace(0, 256, len(palette) * 2)
        bins = np.concatenate(([0], bins[len(palette):], [256]))
        indices = np.digitize(small, bins=bins) - 1
        colored = np.array(palette)[indices]

        # Create a new image with the GitHub dark mode background color
        img = Image.new('RGB', canvas_size, color=(13, 17, 23))
        draw = ImageDraw.Draw(img)

        # Draw the cells
        for i in range(53):
            for j in range(7):
                top_left = (i * cell_size + spacing, j * cell_size + spacing)
                bottom_right = ((i + 1) * cell_size - spacing, (j + 1) * cell_size - spacing)
                color = tuple(colored[j, i])
                draw.rectangle([top_left, bottom_right], fill=color)
        
        # Save the image
        img.save(f'frames/frame_{frame_count}.png')
        
        frame_count += 1
    else:
        break

cap.release()

# Define the images
images = [f'frames/frame_{i}.png' for i in range(frame_count)]

# Convert images to video
video = imageio.mimsave('bad_apple_output.mp4', [imageio.imread(file) for file in images], fps=30)



