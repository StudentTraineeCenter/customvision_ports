from PIL import ImageDraw, Image


def draw_boxes(image_data, predictions):

    if len(predictions) <= 1: #if there are not enough ports
        return None

    image = Image.open(image_data)
    img_width, img_height = image.size
    img = ImageDraw.Draw(image)
    
    for obj in predictions:
        x0 = obj['boundingBox']['left'] * img_width  #upper left corner
        y0 = obj['boundingBox']['top'] * img_height
        x1 = x0 + (obj['boundingBox']['width'] * img_width) #down right corner
        y1 = y0 + (obj['boundingBox']['height'] * img_height)
        shape = [(x0, y0), (x1, y1)]
        img.rectangle(shape, outline ="red")
        img.text((x0 + 10, y0 + 10), obj['tagName'], fill="red")

    return image