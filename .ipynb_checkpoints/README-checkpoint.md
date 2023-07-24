# song-recommender

## Overview

This data science project aims to create a Song Recommender system utilizing the K-Means clustering algorithm. The project uses the Million Song Subset dataset, which contains a collection of song features and metadata. The data is retrieved and supplemented with additional information from the Spotify API to improve the recommendation process. Two clustering models, K-Means and DBSCAN, are considered for the recommendation system. The web application is deployed using Streamlit, allowing users to input a song of their choice and receive a set of song recommendations based on the selected clustering model.

## Dataset

The Million Song Subset dataset is used for this project. It can be accessed through the following link: Million Song Subset.

## Models

Two clustering models are considered for the song recommender system:

K-Means: K-Means is a popular unsupervised learning algorithm that groups data into K clusters based on their features. It allows the recommender system to identify songs that are similar to each other, making it an ideal choice for song recommendations.
DBSCAN: Density-Based Spatial Clustering of Applications with Noise (DBSCAN) is another clustering algorithm used for finding clusters in data. Unlike K-Means, it can discover clusters of various shapes and sizes and also detect outliers.
Data Gathering

To enhance the recommendation process, song data is enriched with additional features from the Spotify API. This API provides valuable information about each song, including audio features, popularity, release date, and more. Combining the Million Song Subset dataset with the Spotify API data allows for a more comprehensive representation of each song.

## Deployment

The Song Recommender web application is deployed using Streamlit. Streamlit is an interactive web framework that enables data scientists and developers to create and share data applications easily. The user can input a song of their choice, and based on the selected clustering model, the system will recommend a set of songs that share similar characteristics.

The web application is hosted at the following link: Song Recommender Web App

## Usage

To use the Song Recommender web application, follow these steps:

1. Access the Song Recommender Web App using the provided link.
2. On the main page, enter the name of a song (and optional artist) you like in the input field.
3. Click on the "Search" button.
4. Select the song you like from the list.
5. The web application will process your input and display a list of recommended songs that share similar characteristics to your chosen song based on the selected clustering model. You can also play around with the model option and the popularity filter get different results.
   
## Conclusion

The Song Recommender project demonstrates how the K-Means clustering algorithm can be used to create an effective recommendation system for songs. By utilizing the Million Song Subset dataset and augmenting it with data from the Spotify API, the system provides meaningful and relevant song recommendations to users.