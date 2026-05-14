# Ashley's silly-project

## Overview:
An application in which one can keep track of their POPMART blind boxes purchases. There is also a feature in which you can upload images of figures for identification.

Users can:
1. Keep track of owned figures
2. Save figures onto a wishlist
3. Browse series
4. Identify unknown figures


## Dependencies
Python

PyTorch

Transformers

Streamlit

CLIP

PIL


## Functionality

The application uses the vision transfomer model CLIP to generate embeddings for the Hirono images and will perform a similarity-based retrival against a locally indexed dataset.

Data/saves persist locally in a .json file.


## To run locally:

``pip install -r requirements.txt``

``streamlit run app.py``


## access: 
https://myhironocollection.streamlit.app


## Future Work:
a lot
better storage clearly
improve similarity retrival cuz it messes up a lot. 
finish scraper! 
a better ui besides streamlit, even if i love streamlit
fix image sizes



