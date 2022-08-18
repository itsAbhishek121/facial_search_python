from fastapi.testclient import TestClient
from main import app
import requests

client = TestClient(app)

def test_search_face():
    response = client.post("http://127.0.0.1:8000/search_faces/",data={"k":2,"strictness":0.6},files={"file":("img1.jpg",open("img1.jpg", "rb"),"image/jpeg")})
    assert response.status_code == 200
    assert response.json() == [3,6,1,4]

def test_add_faces_in_bulk():
    with open("images.zip", "rb") as f:
        response = client.post("http://127.0.0.1:8000/add_faces_in_bulk/",files={"file": ("images.zip", f, "application/x-zip-compressed")})
        assert response.status_code == 200
        assert response.json() ==  {"file": "images.zip"}


def test_add_face():
    with open("img1.jpg", "rb") as f:
        response = client.post("http://127.0.0.1:8000/add_face/",files={"file": ("img1.jpg", f, "image/jpeg")})
        assert response.status_code == 200
        assert response.json() ==  {"file_name": "img1.jpg"}

def test_get_face_info():
    response = client.post("http://127.0.0.1:8000/get_face_info/",data={"image_id":2})
    assert response.status_code == 200
    assert response.json() == [
  "Name: biden; Artist: David Lienemann YCbCrPositioning: 1 ResolutionUnit: 2 XResolution: (72, 1) YResolution: (72, 1) Copyright: This official White House photograph is being made available only for publication by news organizations and/or for personal use printing by the subject(s) of the photograph. The photograph may not be manipulated in any way and may not be used in commercial or political materials, advertisements, emails, products, promotions that in any way suggests approval or endorsement of the President, the First Family, or the White House. ImageDescription: Official portrait of Vice President Joe Biden in his West Wing Office at the White House, Jan. 10, 2013. (Official White House Photo by David Lienemann)..This official White House photograph is being made available only for publication by news organizations and/or for personal use printing by the subject(s) of the photograph. The photograph may not be manipulated in any way and may not be used in commercial or political materials, advertisements, emails, products, promotions that in any way suggests approval or endorsement of the President, the First Family, or the White House. "
]
