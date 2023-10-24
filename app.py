import streamlit as st
from src.pipeline.prediction import PredictionPipeline, imageFile

st.set_page_config(page_title='Blood Cancer Detection', page_icon=':drop_of_blood:', layout='wide')

with st.container():
    # st.title('🩸 Blood Cancer Detection')
    st.markdown("<h1 style='text-align: center; color: black;'>🩸 Blood Cancer Detection</h2>", unsafe_allow_html=True)
    st.write('---')

leftCol, rightCol = st.columns(2)

with leftCol:
    st.markdown('This AI model analyzes **Peripheral Blood Smear (PBS)** images to detect and classify 4 stages of **Acute Lymphoblastic Leukemia** - **Benign (Normal Stage)**, **Malignant Early**, **Malignant Pre**, and **Malignant Pro** stages.')
    st.write('Upload a PBS image and click on the "Predict" button to get predictions.')

    st.warning('The prediction will take a few seconds for the first time as the model is being loaded.')
with rightCol:
    try:
        file = st.file_uploader(label='Upload a PBS image')
        if file:
            predButton = st.button('Predict')
            st.image(file, width=224)
            
            if predButton:
                imgObj = imageFile(file)
                arr = imgObj.getArr()

                predict = PredictionPipeline()
                className, confidence = predict.predict(arr)

                st.markdown(f'''
                            * Class Name: **{className}**
                            * Confidence: **{confidence} %**
                            ''')
    
    except:
        st.warning('Oops! An error occured. Please upload a valid image file.')