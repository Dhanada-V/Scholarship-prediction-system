import pytesseract
from pytesseract import Output

def extract_boxes(image):
    data = pytesseract.image_to_data(image, output_type=Output.DICT)

    boxes = []

    for i in range(len(data["text"])):
        if int(data["conf"][i]) > 60 and data["text"][i].strip():
            boxes.append({
                "text": data["text"][i],
                "conf": int(data["conf"][i]),
                "x": data["left"][i],
                "y": data["top"][i],
                "w": data["width"][i],
                "h": data["height"][i]
            })

    return boxes
