# import cv2
# import numpy as np

# def morphological_gradient(image, kernel_size):
#     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
#     gradient = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel)

#     return gradient

# # Load color image
# input_image = cv2.imread("./img/bond.jpg")

# # Apply morphological gradient with increasing kernel size
# gradient_image = input_image.copy()
# for kernel_size in range(3, 21, 2):
#     gradient_image = morphological_gradient(gradient_image, kernel_size)

# # Display the images
# cv2.imshow("Original Image", input_image)
# cv2.imshow("Morphological Gradient", gradient_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()




import cv2
import numpy as np

# Load color image
img = cv2.imread("./img/bond.jpg")

# Define initial structuring element
kernel_size = 3
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))

# Apply morphological gradient with increasing kernel size
for i in range(10):
    gradient = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)
    kernel_size += 2
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))

    # Display result
    cv2.imshow("Morphological gradient with increasing kernel size", gradient)
    cv2.waitKey(0)



cv2.destroyAllWindows()