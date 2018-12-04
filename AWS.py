#
# import cv2 as cv
# import os
# import boto3
# import easygui
# import json
# import cv2 as cv
# s3=boto3.resource('s3')
# client=boto3.client('rekognition','ap-northeast-1')
#
#
# # Use a file in local, detect the largest face and show the details
# file=easygui.fileopenbox(msg=None,title="Pick an image",default='*',filetypes = ["*.jpg", "*.png"],multiple=False)
# fileName=os.path.abspath ( file )
# with open(fileName, 'rb') as image:
#     faceResults = client.detect_faces(Image={'Bytes': image.read()},Attributes=['ALL'])
#     # Using CV to show the img
#     imgCV=cv.imread(fileName)
#     imgHeight,imgWidth=imgCV.shape[:2]
#     width=round((faceResults['FaceDetails'][0]['BoundingBox']['Width'])*imgWidth)
#     height=round((faceResults['FaceDetails'][0]['BoundingBox']['Height'])*imgHeight)
#     left = round((faceResults['FaceDetails'][0]['BoundingBox']['Left'])*imgWidth)
#     top = round((faceResults['FaceDetails'][0]['BoundingBox']['Top'])*imgHeight)
#     for faceDetail in faceResults['FaceDetails']:
# #         print ( 'The detected face is between ' + str ( faceDetail['AgeRange']['Low'] )
# #                 + ' and ' + str ( faceDetail['AgeRange']['High'] ) + ' years old' )
# #        Print out face details
#
#         print ( 'Face detailed attributes:' )
#         print ( json.dumps ( faceDetail , indent=4 , sort_keys=True ) )
#
#     # Draw face bounding box
#     cv.namedWindow ( 'Processed Image' , cv.WINDOW_AUTOSIZE )
#     cv.rectangle(imgCV,(left,top),(left+width,top+height),(0,255,0),3)
#     cv.imshow('Processed Image',imgCV)
#     k = cv.waitKey ( 0 ) & 0xFF
#     if k == 27:
#         cv.destroyAllWindows()
#
# # Upload sources file to the bucket
# sourceFiles=easygui.fileopenbox(msg=None,title="Upload source images",default='*',filetypes = ["*.jpg", "*.png"],multiple=True)
# for file in sourceFiles:
#     fileName=os.path.basename ( file )
#     filePath=os.path.abspath ( file )
#     s3.meta.client.upload_file ( filePath , 'source-vantuan5644' , fileName , ExtraArgs=None , Callback=None , Config=None )
#     client.index_faces (
#         CollectionId='FaceGroup' ,
#         DetectionAttributes=[
#         ] ,
#         ExternalImageId=fileName
#         Image={
#             'S3Object': {
#                 'Bucket': 'source-vantuan5644' ,
#                 'Name': fileName ,
#             } ,
#         } ,
#     )
#
# # Capture your face
# cv.namedWindow ( 'Camera' ,cv.WINDOW_AUTOSIZE)
# cap = cv.VideoCapture ( 0 )
# detected=False
# def on_mouse ( event , x , y , flags , params):
#     global detected
#     if event == cv.EVENT_LBUTTONDBLCLK:
#         detected = True
# # Your image is now 'frame'
# while cap.isOpened ( ):
#     ret , frame = cap.read ( )
#     cv.imshow ( 'Camera' , frame )
#     cv.setMouseCallback ( 'Camera' , on_mouse)
#     print(detected)
#     if detected == True:
#         cap.release()
#         cv.destroyWindow('Camera')
#     k=cv.waitKey(1) & 0xFF
#     if k==27:
#         break
#
# # Init Haar cascade
# face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
# gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
# faces = face_cascade.detectMultiScale(gray,1.3,5)
# print(faces)
#
#
# if any(map(len,faces)):
#     # Compare the frame with faces in face collection
#     cv.imwrite('frame.jpg',frame)
#     s3.meta.client.upload_file ( 'frame.jpg' , 'target-vantuan5644' , 'frame.jpg' , ExtraArgs=None , Callback=None , Config=None )
#     with open('frame.jpg','rb') as image:
#         faceSearching = client.search_faces_by_image(
#             CollectionId='FaceGroup',
#             FaceMatchThreshold=90,
#             Image={'Bytes': image.read() },
#             MaxFaces=1,
#             )
#     # Deternmine face bouding box in the frame
#
#     print(faceSearching)
#     imgHeight,imgWidth=frame.shape[:2]
#     width=round((faceSearching['SearchedFaceBoundingBox']['Width'])*imgWidth)
#     height=round((faceSearching['SearchedFaceBoundingBox']['Height'])*imgHeight)
#     left = round((faceSearching['SearchedFaceBoundingBox']['Left'])*imgWidth)
#     top = round((faceSearching['SearchedFaceBoundingBox']['Top'])*imgHeight)
#     bottom=top+width
#     right=left+width
#
#     if not faceSearching['FaceMatches']:
#         font = cv.FONT_HERSHEY_SIMPLEX
#         cv.putText(frame,"Can't find your face in the library",(100,100), font, 1,(0,0,255),2,cv.LINE_AA)
#         for (x , y , w , h) in faces:
#             cv.rectangle ( frame , (x , y) , (x + w , y + h) , (255 , 0 , 0) , 2 )
#
#     else:
#         imageID=""
#         accuracy=faceSearching['FaceMatches'][0]['Similarity']
#         print(accuracy)
#         cv.rectangle(frame,(left,top),(right,bottom),(255,0,0),3)
#         font = cv.FONT_HERSHEY_SIMPLEX
#         imageID = faceSearching['FaceMatches'][0]['Face']['ExternalImageId']
#         cv.putText(frame,'You are'+ ' ' + imageID[0:len(imageID)-6], (left,top+height), font, 1,(0,255,0),2,cv.LINE_AA)
#         cv.putText(frame,str(accuracy),(left,top), font, 1,(255,255,255),2,cv.LINE_AA)
#     cv.imshow('Capture',frame)
#     cv.waitKey(0)
# else:
#     font = cv.FONT_HERSHEY_SIMPLEX
#     cv.putText ( frame , "Can't find any faces" , (100 , 100) , font , 1 , (0 , 0 , 255) , 2 ,
#                  cv.LINE_AA )
#     cv.imshow('Capture',frame)
#     cv.waitKey(0)
#
#
import easygui
easygui.egdemo()