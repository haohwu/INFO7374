import streamlit as st
from PIL import Image
import requests
import os
from dotenv import load_dotenv
import openai
from azure import image_embedding, find_similar_images

def main():
    st.title("Clothing Style Recommender")
    st.write("Upload an image of clothing, and get similar style recommendations.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    st.write("")
    st.write("Generating recommendations...")

    # Save the uploaded image to a temporary file
    with open("temp_image.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Get the image embedding using azure.py function
    image_emb = image_embedding("temp_image.jpg")

    image_data = pd.DataFrame({
        'image_path': ["image1.jpg", "image2.jpg", "image3.jpg"],
        'embedding': [[0.1, 0.2], [0.3, 0.4], [0.5, 0.6]]  # Mock embeddings
    })
    
    st.subheader("Conversation History")
    for i, (user_prompt, image_urls) in enumerate(st.session_state.history):
        with st.container():
            print("hollalalal")
            print(user_prompt)
            st.write(f"**Prompt {i+1}:** {user_prompt}") 

            cols = st.columns(len(image_urls))
            for col, img_url in zip(cols, image_urls):
                col.image(img_url, use_column_width=True)

    # Find similar images (implement the actual logic in azure.py)
    similar_images = find_similar_images(image_emb, image_data)

    st.write("Similar styles:")
    for index, row in similar_images.iterrows():
        st.image(row['image_path'], caption=f"Similar Image {index + 1}")
        

if __name__ == "__main__":
    main()