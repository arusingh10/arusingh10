import streamlit as st
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column,String,Integer,Float
import pandas as pd
from database import Image as ImageModel
import cv2
from PIL import Image

# connect to database
engine = create_engine('sqlite:///db.sqlite3')
Session = sessionmaker(bind=engine)
sess = Session()

#Application operations
def addImage():
    st.header("Upload image to continue")
    img_name=st.text_input("Enter image name")

    img_file=st.file_uploader("Insert Image Here")
   
    if img_file:
        img=Image.open(img_file)
        st.image(img)
        img_path="./uploads/"+img_name+".png"
        img.save(img_path)
    
    add_btn=st.button("Save image")

    if add_btn and img_name and img_file:
        with st.spinner("Saving your Image"):
            img_data=ImageModel(name=img_name,path=img_path)
            sess.add(img_data)
            sess.commit()
            st.success("Image successfully saved") 

def maskImg():
    st.header("Create Masked Image")
    h=st.slider("H")
    s=st.slider("S")
    v=st.slider("V")



def trackObj():
    st.header("Webcam Live Feed")
    run = st.checkbox('Run')
    FRAME_WINDOW = st.image([])
    # camera = cv2.VideoCapture(0)

    # while run:
    #     _, frame = camera.read()
    #     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #     FRAME_WINDOW.image(frame)
    # else:
    #     st.write('Stopped')
    masked_images=ImageModel.query.all()
    st.text(masked_images)

def showsavedImg():
    saved_img=sess.query(ImageModel).all()
    for image in saved_img:
        st.text(image.name)
        st.image(image.path)
        st.button("Select Image",key=image.id)
    setupsliders()


def setupsliders():
    values=["v1_min", "v2_min", "v3_min", "v1_max", "v2_max", "v3_max"]
    cap_values={}
    for value in values:
        cap_values[value]=st.slider(value)



sidebar=st.sidebar
sidebar.header("Choose an option")
options=["Add image for masking","Create masked image", "Track Object with webcam"]
choice=sidebar.selectbox(options=options,label="Choose any option")


st.title("Camera Based Object Tracking System")

if choice==options[0]:
    addImage()
elif choice==options[1]:
    showsavedImg()
elif choice==options[2]:
    trackObj()




