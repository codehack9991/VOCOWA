from operator import add
from numpy import subtract
from PIL import Image, ImageMath


def merge(name_img1, name_img2, position_wrt_img1=(0, 0)):
    """
    Merges two images. Currently, works for -ve position too

    :param name_img1: Image 1
    :param name_img2: Image 2
    :param position_wrt_img1: Merging w.r.t. top left corner of image 1
    :return:
    """
    if position_wrt_img1 > (0, 0):
        img1 = Image.open(name_img1)
        img2 = Image.open(name_img2)
    else:
        position_wrt_img1 = tuple(subtract((0, 0), position_wrt_img1))
        img2 = Image.open(name_img1)
        img1 = Image.open(name_img2)

    w, h = map(max, map(add, img2.size, position_wrt_img1), img1.size)

    # pasting img1 on img2
    _img1 = Image.new('RGB', size=(w, h), color=0)
    _img1.paste(img1, (0, 0))

    # pasting opposite way
    _img2 = Image.new('RGB', size=(w, h), color=0)
    _img2.paste(img2, position_wrt_img1)

    return Image.blend(_img1, _img2, alpha=0.5)


def merge_BW(name_img1, name_img2, PWSB):
    """
    Merges two BW images
    Calculates Top Left Corner of img2 in expected (resultant) image
    
    :param name_img1: Image 1
    :param name_img2: Image 2
    :param PWSB : Point Where Scan Began in img1
    
    :return : Updated PWSB ,in resultant map
    """

    img1 = Image.open(name_img1)
    img2 = Image.open(name_img2)

    # TODO Negative Corner Issue
    # PWSB will be positive. Corner May not be
    corner = tuple(subtract(PWSB, (img2.size[0]/2, img2.size[1]/2)))

    w = max(img2.size[0] + corner[0], img1.size[0]) - min(0, corner[0])
    h = max(img2.size[1] + corner[1], img1.size[1]) - min(0, corner[1])

    # Create 2 canvas
    _img1 = Image.new('L', size=(w, h), color=0)
    _img2 = Image.new('L', size=(w, h), color=0)

    if corner[0] >= 0 and corner[1] >= 0:
        _img1.paste(img1, (0, 0))
        _img2.paste(img2, corner)
    elif corner[0] <= 0 and corner[1] <= 0:
        _img1.paste(img1, tuple(subtract((0, 0), corner)))
        _img2.paste(img2, (0, 0))
    elif corner[0] <= 0 and corner[1] >= 0:
        _img1.paste(img1, (w - img1.size[0], 0))
        _img2.paste(img2, (0, h - img2.size[1]))
    else:
        _img1.paste(img1, (0, h - img1.size[1]))
        _img2.paste(img2, (w - img2.size[0], 0))

    i = ImageMath.eval("a|b", a=_img1, b=_img2)
    i.convert('L').save('result.jpg')

    for i in range(2):
        if img2.size[i] / 2 > PWSB[i]:  # PWSB will be positive
            PWSB[i] = img2.size[i] / 2

    return PWSB
