import cv2

try:
    image = cv2.imread('dip/image.png', cv2.IMREAD_GRAYSCALE)
    # Display the image
    cv2.imshow("My Image", image)

    # Wait until any key is pressed
    cv2.waitKey(0)

    # Close the window
    cv2.destroyAllWindows()
    
except Exception as e:
    print("\n\nError loading image:", e)