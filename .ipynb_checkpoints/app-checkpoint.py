import pandas as pd
import streamlit as st
from datetime import datetime

import functions

def update_popularity():
    
    pop_dict = {'Hidden Gem': 0,
                'Underrated': 25,
                'Trending': 50,
                'Popular': 75,
                'Super hit': 100}
    
    st.session_state['popularity_min'] = pop_dict[st.session_state['pop_slider'][0]]
    st.session_state['popularity_max'] = pop_dict[st.session_state['pop_slider'][1]]

def update_model():
    st.session_state['current_model'] = st.session_state['sm_radio']

def start_again():
    for key in st.session_state.keys():
        del st.session_state[key]

def option_song_clicked():
    # Load data
    df = pd.read_csv('./data/songs_and_features_kmeans_clustered.csv', sep=';')

    # Define selected features
    selected_features = ['energy','danceability','mode', 'speechiness', 
                         'tempo', 'acousticness', 'instrumentalness', 'valence']

    # Load models
    kmeans_9 = functions.read_pickle_file('./models/{}.pkl'.format('kmeans_9'))
    kmeans_27 = functions.read_pickle_file('./models/{}.pkl'.format('kmeans_27'))

    # Store models in a dictionary
    models = {'kmeans_9': kmeans_9,
             'kmeans_27': kmeans_27}

    
    for item in st.session_state.items():
        if (item[1] == True) & (item[0][:2] == 'so'): # if it is search option button and its true
            st.session_state['selected_song_index'] = int(item[0][-1])
            st.session_state['current_page'] = 2

    st.session_state['track_id'] = st.session_state['sp_song_data'][st.session_state['selected_song_index']]['track_id']

    selected_model = st.session_state['current_model']

    st.session_state['recommended_songs'] = functions.recommend_song(df, selected_model, models, selected_features, 
                                                                     st.session_state['track_id'], 
                                                                     st.session_state['popularity_min'], 
                                                                     st.session_state['popularity_max']).to_dict(orient="records")

def main():

    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 1
        
    if 'current_model' not in st.session_state:
        st.session_state['current_model'] = 'kmeans_9'
        
    if 'popularity_min' not in st.session_state:
        st.session_state['popularity_min'] = 0
        st.session_state['popularity_max'] = 100

    #'st.session_state object:', st.session_state

    # Application Title
    st.image('./resources/gnod_logo.png', width=150)
    st.header('MelodyMind')
    st.caption('Song Recommender Beta 1.0')

    st.divider()
    

    
    # Page rendering
    if st.session_state['current_page'] == 1:

        # Model Selection
        st.radio("Select model ", ("kmeans_9","kmeans_27"), horizontal=True, key='sm_radio', on_change=update_model)

        st.divider()
    
        # Track name input box
        track_name = st.text_input('Type a song that you like')
    
        # Artist input box
        artist = st.text_input('Type the artist (optional)')
        
        # Search button
        search_button = st.button('Search song')
        
        if search_button:
            
            if (track_name == "") & (track_name == ""):
                # Error message if nothing as input
                st.error("You must input a song.")
            else:
                # Get spotify data including track_id
                sp_song_data = functions.search_song(track_name, artist)
                st.session_state['sp_song_data'] = sp_song_data
                
                if len(sp_song_data) > 0:
                    for index, song in enumerate(sp_song_data):
                        col1, col2 = st.columns(2)

                        with col1:
                            st.subheader(song['track_name'])
                            st.caption(song['artist'])
                            st.write(functions.convert_seconds_to_min_seconds(song['track_duration']))
                            st.write('Album: *'+str(song['album_name'])+'*')
                            st.write('Released: ', song['album_release_year'])

                        with col2:
                            st.image(song['album_image'],width=125)
                            search_button = st.button('I like this song!', on_click=option_song_clicked, key='so_button_'+str(index))


                        st.divider()
                else:
                    st.info('No songs found.')

    elif st.session_state['current_page'] == 2:
        st.select_slider('Select a range of popularity',
                                          options=['Hidden Gem', 'Underrated', 'Trending', 'Popular', 'Super hit'],
                                          value=('Hidden Gem', 'Super hit'),
                                         on_change=update_popularity,
                                         key='pop_slider')
        
        col1, col2 = st.columns(2)
        with col1:
            st.button('Recommend again', on_click=option_song_clicked)
            
        with col2:
            st.button('Start again', on_click=start_again)
            
        st.divider()
        
        st.subheader('You will also like...')
        
        st.divider()
        recommended_songs = st.session_state['recommended_songs']
        if len(recommended_songs) == 0:
            st.info('No recommendations available. Consider widening the popularity filter.')
        for index, song in enumerate(recommended_songs):
            col1, col2 = st.columns(2)
    
            with col1:
                st.subheader(song['track_name'])
                st.caption(song['artist'])
                st.write(functions.convert_seconds_to_min_seconds(song['track_duration']))
                st.write('Album: *'+str(song['album_name'])+'*')
                st.write('Released: ', song['album_release_year'])
                st.write('Popularity: ', song['popularity'])
    
            with col2:
                st.image(song['album_image'], width=125)
                #st.image('./resources/images/listen-on-spotify-3.png', width=125)
                st.markdown('[Listen on Spotify!](' + song['track_link'] + ')')

            st.divider()
                    
if __name__ == "__main__":
    main()