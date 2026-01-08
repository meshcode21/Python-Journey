
# Function to display pixel positions (x,y) of the image
def showPos(img):
    if not img:
        return
     
    for y in range(len(img)):
        for x in range(len(img[y])):
            print(f"({x},{y})",end="\t")
        print()
    print()
    
# Image processing functions for grayscale images represented as 2D lists
def showPixels(img=[]):
    if not img:
        return
    
    for row in img:
        for col in row:
            print(col, end="\t")
        print()
    print()

# Function to brighten an image by a given value
def bright_image(img,value):
    if not img:
        return None
    if value < 0:
        return None

    return [[min(255,pixel+value) for pixel in row] for row in img]

# Function to flip an image horizontally
def horizontalFlip(image):
    if not image:
        return None
    return [row[::-1] for row in image]

# Function to flip an image vertically
def verticalFlip(image):
    if not image:
        return None
    return image[::-1]

# Function to darken an image by a given value
def dark_image(img, value):
    if not img:
        return None
    if value < 0:
        return None
    return [[max(0,pixel-value) for pixel in row] for row in img]

# Function to apply a threshold to an image
def threshold_image(img, th):
    if not img:
        return None
    if th < 0 or th > 255:
        return None
    return [[255 if pixel > th else 0 for pixel in row] for row in img]

# Function to invert the colors of an image
def invert_image(img):
    if not img:
        return None
    return [[255 - pixel for pixel in row] for row in img]

# Function to draw a cross on the image
def draw_cross(image):
    if not image:
        return None
    height = len(image)
    width = len(image[0])
    for i in range(min(height, width)):
        image[i][i] = 255
        image[i][width - 1 - i] = 255
    return image

# Function to crop the center of the image to a given size
def crop_center(img, size):
    if not img:
        return None
    height = len(img)
    width = len(img[0])
    crop_height, crop_width = size
    start_y = (height - crop_height) // 2
    start_x = (width - crop_width) // 2
    end_y = start_y + crop_height
    end_x = start_x + crop_width
    return [row[start_x:end_x] for row in img[start_y:end_y]]

# Main function to demonstrate image processing
def main():
    image = [
    [  0,  5, 10, 15, 20, 25, 30, 35, 40, 45],
    [  5, 10, 15, 20, 25, 30, 35, 40, 45, 50],
    [ 10, 15, 20, 25, 30, 35, 40, 45, 50, 55],
    [ 15, 20, 25, 30, 35, 40, 45, 50, 55, 60],
    [ 20, 25, 30, 35, 40, 45, 50, 55, 60, 65],
    [ 25, 30, 35, 40, 45, 50, 55, 60, 65, 70],
    [ 30, 35, 40, 45, 50, 55, 60, 65, 70, 75],
    [ 35, 40, 45, 50, 55, 60, 65, 70, 75, 80],
    [ 40, 45, 50, 55, 60, 65, 70, 75, 80, 85],
    [ 45, 50, 55, 60, 65, 70, 75, 80, 85, 90],
    [ 50, 55, 60, 65, 70, 75, 80, 85, 90, 95],
    [ 55, 60, 65, 70, 75, 80, 85, 90, 95,100],
    [ 60, 65, 70, 75, 80, 85, 90, 95,100,105],
    [ 65, 70, 75, 80, 85, 90, 95,100,105,110],
    [ 70, 75, 80, 85, 90, 95,100,105,110,115],
]
    print("\nOrigina Image matrix\n")
    showPixels(image)

    # brighting and rotate 90deg
    print("\nAfter image processing\n")
    showPixels(invert_image(crop_center(image, (10, 5))))

main()