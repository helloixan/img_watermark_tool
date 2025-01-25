from PIL import Image

WTM_PADDING = 1/30

def add_wtm(wtm: Image.Image, img:Image.Image, wtm_options: dict) :
    # Resize watermark so it can fit and smaller than the image
    new_wtm_width = int(wtm_options['resize_factor'] * img.width)
    coef = new_wtm_width / wtm.width
    new_wtm_height = int(wtm.height * coef)
    new_wtm = wtm.resize((new_wtm_width, new_wtm_height))

    # Set the position
    wtm_position = set_coor_wtm(new_wtm, img, wtm_options)
    
    # Set the Opacity
    set_opacity_wtm(new_wtm, wtm_options)

    new_img = img.copy()
    new_img.paste(new_wtm, wtm_position, new_wtm)
    return new_img

def set_coor_wtm(resized_wtm: Image.Image, img: Image.Image, wtm_options: dict) :
    postition = wtm_options['position']
    padding = int(img.width // (1 / WTM_PADDING))

    if postition == 'top left' :
        x = padding
        y = padding
    elif postition == 'center' :
        x = int(img.width / 2 - resized_wtm.width / 2)
        y = int(img.height / 2 - resized_wtm.height / 2)
    elif postition == "top right" :
        x = int(img.width - padding - resized_wtm.width)
        y = padding
    elif postition == 'bottom right':
        x = int(img.width - padding - resized_wtm.width)
        y = int(img.height - padding - resized_wtm.height)
    else :
        x = padding
        y = int(img.height - padding - resized_wtm.height)

    return x, y

def set_opacity_wtm(new_wtm: Image.Image, wtm_options: dict) :
    opacity_level = int(wtm_options['opacity'] * 255)

    alpha = new_wtm.getchannel('A')
    new_alpha = alpha.point(lambda i: opacity_level if i > 0 else 0)

    new_wtm.putalpha(new_alpha)