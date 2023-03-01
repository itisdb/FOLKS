import webbrowser
import cv2

# Load the image
from PIL import Image, ImageEnhance

img = cv2.imread('test.jpg')

gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

inverted_gray_image = cv2.bitwise_not(gray_image)

blurred_img = cv2.GaussianBlur(inverted_gray_image, (21, 21), 0)

inverted_blurred_img = cv2.bitwise_not(blurred_img)

pencil_sketch_img = cv2.divide(gray_image,inverted_blurred_img, scale=256.0)

pencil_sketch_img = ImageEnhance.Contrast(Image.fromarray(pencil_sketch_img)).enhance(6)
# pencil_sketch_img = ImageEnhance.Sharpness(pencil_sketch_img).enhance(3)
pencil_sketch_img = pencil_sketch_img.save('pencil_sketch.jpg')

