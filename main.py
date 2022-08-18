from fastapi import FastAPI, File, UploadFile, Form
import psycopg2
import sys
import os
from zipfile import ZipFile
from PIL import Image
from PIL.ExifTags import TAGS
from io import BytesIO
import re

app = FastAPI()

@app.post("/search_faces/")
async def search_faces(k : int,strictness: float,file: UploadFile = File(..., description="An image file, possible containing multiple human faces.")):
    try:
        # Establishing connection with database.
        with psycopg2.connect(host = 'localhost',dbname = 'postgres',user = 'postgres',password = 'abhi',port = 5432) as conn:
            # Using curser for running queries.
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM image_data")
                all_images = cur.fetchall()
                d = {} # dictionary for storing matched face image and their id's.
                
                # Using face_recognition for facial search.
                test_image = face_recognition.load_image_file(file.filename)
                test_image_encoding = face_recognition.face_encodings(test_image)
                for i in range(len(all_images)):
                    byte_array = all_images[i][1]
                    fout = open('image.jpg','wb')
                    fout.write(byte_array)
                    known_image = face_recognition.load_image_file("image.jpg")
                    known_image_encoding = face_recognition.face_encodings(known_image)
                    #strictness = 0.6
                    for img in test_image_encoding:
                        face_distance = face_recognition.face_distance(known_image_encoding,img)
                        for j, face_distance in enumerate(face_distance):
                            if(face_distance<=strictness):
                                if all_images[i][0] not in d.keys():
                                    d[all_images[i][0]]=face_distance
                d_sorted = sorted(d.items(), key=lambda x: x[1])
                p = 0
                #print(d)
                ls = []
                while (p < k):
                    p+=1
                    for (img_id, face_distance) in d_sorted:
                        ls.append(img_id)
                conn.commit()
                conn.close()
    except Exception as Error:
        print(Error)
    return ls

@app.post("/add_face/")
async def add_face(file: UploadFile = File(..., description="An image file having a single human face.")):
    try:
        # Establishing connection with database.
        with psycopg2.connect(host = 'localhost',dbname = 'postgres',user = 'postgres',password = 'abhi',port = 5432) as conn:   
            # Opening image file.
            with open(file.filename, "rb") as image:
                # Below, metadata of image is extracting out form image file.
                s = ""
                im = Image.open(file.filename)
                if im._getexif() is not None:
                    for tag, value in im._getexif().items():
                        if tag in TAGS:
                            s = s + str(TAGS[tag]) + ": " + str(value) + " "
                
                # Converting image file into byte array form to store in database efficiently.
                img = image.read()
                binary_img = psycopg2.Binary(img)
                name = (re.sub('\.jpg$|\.jpeg$|\.png$', '', file.filename)).upper()
                metadata = "Name: " + name + "; " + s
                
                # Running queries for creating table and inserting data into database using cursor.
                with conn.cursor() as cur:
                    create_script = '''CREATE TABLE IF NOT EXISTS image_data (img_id SERIAL PRIMARY KEY, byte_array BYTEA, METADATA text NULL)'''
                    cur.execute(create_script)
                    insert_script  = 'INSERT INTO image_data (byte_array,METADATA) VALUES (%s,%s)'
                    cur.execute(insert_script, (binary_img,metadata))
                    conn.commit()
                    conn.close()
    except Exception as Error:
        print(Error)
    return {"file_name":file.filename}


@app.post("/add_faces_in_bulk/")
async def add_faces_in_bulk(file: UploadFile = File(..., description="A ZIP file containing multiple face images.")):
    try:
        # Establishing connection with database
        with psycopg2.connect(host = 'localhost',dbname = 'postgres',user = 'postgres',password = 'abhi',port = 5432) as conn:
            # Using curser for running queries
            with conn.cursor() as cur:
                create_script = '''CREATE TABLE IF NOT EXISTS image_data (img_id SERIAL PRIMARY KEY, byte_array BYTEA, METADATA text NULL)'''
                cur.execute(create_script)
                
                # Reading image files from uploaded .zip file
                file_zip = ZipFile(file.filename)
                file_obj = [file_zip.read(item) for item in file_zip.namelist()]
                file_list = file_zip.namelist()
                
                # Extracting metadata of all images
                l = 0
                for l in range(1,len(file_list)):
                    s = ""
                    dataEnc = BytesIO(file_obj[l])
                    im = Image.open(dataEnc)
                    if im._getexif() is not None:
                        for tag, value in im._getexif().items():
                            if tag in TAGS:
                                s = s + str(TAGS[tag]) + ": " + str(value) + " "
                    l1 = file_list[l].find("/")
                    l2 = file_list[l].find(".")
                    file_list[l] = "Name: " + (file_list[l][l1+1:l2]).upper() + "; " + s
                
                # Converting all image files into byte array for storing in database.
                for i in range(1,len(file_obj)):
                    file_binary = psycopg2.Binary(file_obj[i])
                    insert_script  = 'INSERT INTO image_data (byte_array,METADATA) VALUES (%s,%s)'
                    cur.execute(insert_script, (file_binary,file_list[i]))
                conn.commit()
                conn.close()
    except Exception as Error:
        print(Error)
    return {"file": file.filename}


@app.post("/get_face_info/")
async def get_face_info(image_id : int):
    try:
        # Establishing connection with database
        with psycopg2.connect(host = 'localhost',dbname = 'postgres',user = 'postgres',password = 'abhi',port = 5432) as conn:   
            # Using cursor for runnning queries.
            with conn.cursor() as cur:
                select_script = "SELECT METADATA FROM image_data WHERE img_id = %s"
                cur.execute(select_script,[image_id])
                METADATA = cur.fetchone() # fecthing metadata of corresponding image_id.
                conn.commit()
                conn.close()
    except Exception as Error:
        print(Error)
    return METADATA
    
