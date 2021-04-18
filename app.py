import streamlit as st
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column,String,Integer,Float
import pandas as pd
from database import Image as ImageModel
import cv2
from PIL import Image
from object_movement import Object_Tracker
import base64

# connect to database
engine = create_engine('sqlite:///db.sqlite3?check_same_thread=False')
Session = sessionmaker(bind=engine)
sess = Session()

st.title("Camera Based Object Tracking System")

sidebar=st.sidebar
sidebar.header("Choose an option")
options=["Add image for masking","Create masked image", "Track Object with webcam"]
choice=sidebar.selectbox(options=options,label="Choose any option")


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


def showMask(selObj, FRAME_WINDOW):
    st.markdown("### Adjust Sliders to create a mask for Tracking")
    sliders = setupsliders()
    save_btn = st.button('Save Mask Image')
    range_filter = 'HSV'

    if selObj.path:
        image = cv2.imread(selObj.path)
        frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    else:
        camera = cv2.VideoCapture(0)
    
    while True:
        
        # v1_min, v2_min, v3_min, v1_max, v2_max, v3_max = get_trackbar_values(range_filter)
        thresh = cv2.inRange(frame_to_thresh, (sliders['v1_min'], sliders['v2_min'], sliders['v3_min']), (sliders['v1_max'], sliders['v2_max'], sliders['v3_max']))

        if save_btn:
            try:
                cv2.imwrite('masks/thresh.jpg', thresh)
                st.success("Masked Image successfully saved") 
                return None
            except Exception as e:
                st.error('error occured in saving mask image')
                print(e)

        FRAME_WINDOW.image(thresh)

def trackObj():
    st.header("Live Object Tracking")
    run = st.checkbox('Run')
    FRAME_WINDOW = st.image([])
    camera = cv2.VideoCapture(0)

    frameobj = Object_Tracker((0, 63, 161, 215, 160, 245))
    cv2.imwrite('dsds.png', frameobj.track_object())
    while run:
        cv2.imshow('dsdsd', frameobj.track_object())
        FRAME_WINDOW.image(frameobj.track_object())


def showsavedImg():
    st.markdown("## Create Masked Image")
    saved_img=sess.query(ImageModel).all()
    image_names = [ image.name for image in saved_img ]
    sel_image_name = st.selectbox(options = image_names, label = 'Select Image to Mask')
    col1, col2 = st.beta_columns(2)
    org_image = col1.image([])
    masked_image = col2.image([])
    btn = st.checkbox("Use This Image to create Mask")

    selObj = sess.query(ImageModel).filter_by(name = sel_image_name).first()
    org_image.image(selObj.path)

    if btn:
        showMask(selObj, masked_image)


def setupsliders():
    values=["v1_min", "v2_min", "v3_min", "v1_max", "v2_max", "v3_max"]
    cap_values={}
    set1, set2 = st.beta_columns(2)
    for index, value in enumerate(values):
        if index<3:
            cap_values[value]=set1.slider(value, 0, 255)
        else:
            cap_values[value]=set2.slider(value, 0, 255, 255)

    return cap_values



if choice==options[0]:
    addImage()
elif choice==options[1]:
    showsavedImg()
elif choice==options[2]:
    trackObj()