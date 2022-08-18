--------------- Facial Search in Database of Images -----------------

1. What does this program do?

   This is a python program, which performs the “facial search” on a database of images.
   Initially, we will populate the database with face images along with their metadata. Then we will give unknown face image to the program
   and program will have to match that unknown face in its database of images and have to return top-k matches of images.
   We have used FastAPI framework and PostgreSQL in making of this application. We have used Uvicorn for invoking application which will done by
   sending an HTTP post request to the API’s endpoint.

2. A description of how this program works (i.e. its logic)

   This program is made using Python as a programming language, FASTAPI framework and PostgreSQL as database engine. We have implemented four fuctions in this program, namely
   search_face: This function is used to do facial search on given database of images and return top-k matches of images.
   add_face: This fuction is used to add a face image into database along with its metadata.
   add_faces_in_bulk: This function is used to add face images in bulk to the database along with the metadata.
   get_face_info: This fuction is used for retrieving the details of a face record from Database.

   Testing of this program is done using the pytest on Labeled Faces in the Wild (LFW) face dataset.
   For testing following functions are implemented:
   test_search_faces: Input parameters are k, strictness and image file.
   test_add_face: Have to upload face image file using FASTAPI swagger UI on "http://127.0.0.1:8000/docs#/default/add_face".
   test_add_faces_in_bulk: Have to upload zip file of images using FASTAPI swagger UI on "http://127.0.0.1:8000/docs#/default/add_faces_in_bulk_add_faces_in_bulk__post".
   test_get_face_info: Input parameter is a face image id and outputs Metadata corresponding to that id.

3. How to compile and run this program

   To run the main.py file: uvicorn main:app --reload
   To run the test_main.py file: coverage run -m pytest test_main.py
   After running the program from terminal, open 'http://127.0.0.1:8000/docs#/' in browser. It will open FastAPI swagger UI for uploading files and providing parameters.
