import sys
import os
from PIL import Image, ImageFilter, ImageEnhance



current_directory = os.path.abspath(os.path.dirname(__file__))
images_directory = os.path.join(current_directory, "images")

with Image.open(os.path.join(images_directory, "pac-man-ghost-thumbnail.png")) as picture:
    
    black_white = picture.convert("L")
    black_white.save(os.path.join(images_directory, "black_white.png"))

    mirror = picture.transpose(Image.FLIP_LEFT_RIGHT)
    mirror.save(os.path.join(images_directory, "mirror.png"))
    
    # NOTE: Have to convert the Palletted image (i.e., image in P mode)to RGB before applying filters
    if picture.mode == "P":
        picture = picture.convert("RGB")
        
    blur = picture.filter(ImageFilter.BLUR)
    blur.save(os.path.join(images_directory, "blur.png"))


    # Image Enhancements
    contract = ImageEnhance.Contrast(picture)
    contract = contract.enhance(2.0) # 2.0 is the factor by which contrast is increased by 200%
    contract.save(os.path.join(images_directory, "contrast.png"))
    
    # This is the same as the 3 lines just above these lines
    color = ImageEnhance.Color(picture).enhance(2.0)
    color.save(os.path.join(images_directory, "color.png"))
    
    


    # picture = picture.convert("L")
    # picture = picture.convert("RGBA")
    # picture = picture.rotate(90)
    # picture = picture.transpose(Image.FLIP_LEFT_RIGHT)
    # picture = picture.filter(ImageFilter.SHARPEN)
    # enhancer = ImageEnhance.Contrast(picture)
    # picture = enhancer.enhance(2.0)
    # enhancer = ImageEnhance.Color(picture)
    # picture = enhancer.enhance(2.0)
    # enhancer = ImageEnhance.Brightness(picture)
    # picture = enhancer.enhance(2.0)
    # picture.show()