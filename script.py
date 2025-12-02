from skimage import io
from skimage.measure import shannon_entropy

photo_jpg = io.imread("f_image.jpg")
entropy_jpg = shannon_entropy(photo_jpg)
print("К-ть інформації про фото типу jpg: " + str(entropy_jpg))


photo_bmp = io.imread("f_image.bmp")
entropy_bmp = shannon_entropy(photo_bmp)
print("К-ть інформації про фото типу bmp: " + str(entropy_bmp))


photo_png = io.imread("f_image.png")
entropy_png = shannon_entropy(photo_png)
print("К-ть інформації про фото типу png: " + str(entropy_png))

