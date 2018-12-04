import os
import boto3
import easygui
import json
import cv2 as cv

s3 = boto3.resource('s3')
client = boto3.client('rekognition', 'ap-northeast-1')

# Upload file to S3
file = easygui.fileopenbox(msg=None, title="Pick an image", filetypes=["*.jpg", "*.png"],
                           multiple=False)
fileName = os.path.basename(file)
filePath = os.path.abspath(file)
# s3.meta.client.upload_file(filePath, 'source-vantuan5644', fileName, ExtraArgs=None, Callback=None, Config=None)

functionSelect = easygui.choicebox(msg="Select an option\nWord-by-word searching or line searching?",
                                   title="Choose searching method",
                                   choices=("Word-by-word", "Line"))
with open(fileName, 'rb') as image:
    results = client.detect_text(Image={'Bytes': image.read()})

    # Response syntax
    # print(json.dumps(results['TextDetections'], indent=4, sort_keys=True))

    # Use OpenCV to display bounding box
    imgCV = cv.imread(fileName)
    imgHeight, imgWidth = imgCV.shape[:2]
    if functionSelect == "Word-by-word":
        for id in range(0, len(results['TextDetections'])):
            diary = results['TextDetections'][id]
            if diary['Type'] == 'WORD':
                print("Detected Text: ", diary['DetectedText'], "\n")
                width = round((diary['Geometry']['BoundingBox']['Width']) * imgWidth)
                height = round((diary['Geometry']['BoundingBox']['Height']) * imgHeight)
                left = round((diary['Geometry']['BoundingBox']['Left']) * imgWidth)
                top = round((diary['Geometry']['BoundingBox']['Top']) * imgHeight)
                right = left + width
                bottom = top + height
                cv.rectangle(imgCV, (left, top), (right, bottom), (255, 0, 0), 1)
        cv.namedWindow('Processed Image',cv.WINDOW_FREERATIO)
        cv.imshow('Processed Image', imgCV)

        cv.imwrite("result_"+fileName, imgCV)
        cv.waitKey(0)

    if functionSelect == "Line":
        for id in range(0, len(results['TextDetections'])):
            diary = results['TextDetections'][id]
            if diary['Type'] == 'LINE':
                print("Detected Text: ", diary['DetectedText'], "\n")
                width = round((diary['Geometry']['BoundingBox']['Width']) * imgWidth)
                height = round((diary['Geometry']['BoundingBox']['Height']) * imgHeight)
                left = round((diary['Geometry']['BoundingBox']['Left']) * imgWidth)
                top = round((diary['Geometry']['BoundingBox']['Top']) * imgHeight)
                right = left + width
                bottom = top + height
                cv.rectangle(imgCV, (left, top), (right, bottom), (0, 0, 255), 1)
        cv.namedWindow('Processed Image',cv.WINDOW_FREERATIO)

        cv.imshow('Processed Image', imgCV)
        cv.waitKey(0)
        cv.imwrite('result.jpg')

