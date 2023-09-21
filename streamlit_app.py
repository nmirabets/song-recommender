import streamlit as st
import utils.functions as f

# Define model to use
model_name = 'kmeans_17'

def update_popularity():
    
    # Dictionary to convert popularity slider values to min and max values
    pop_dict = {'Hidden Gem': 0,
                'Underrated': 25,
                'Trending': 50,
                'Popular': 75,
                'Super hit': 100}
    
    st.session_state['popularity_min'] = pop_dict[st.session_state['pop_slider'][0]]
    st.session_state['popularity_max'] = pop_dict[st.session_state['pop_slider'][1]]

    option_song_clicked() # Call function to update recommendations

def start_again():
    for key in st.session_state.keys():
        del st.session_state[key]

def like_song_clicked():

    track_name = st.session_state['track_name']
    artist = st.session_state['artist']

    if track_name != "":
        sp_song_data = f.search_song(track_name, artist)
        st.session_state['sp_song_data'] = sp_song_data

        if len(sp_song_data) == 0:
            st.session_state['current_page'] = 1
            st.info('No songs found.') 
        else:
            st.session_state['current_page'] = 2

def option_song_clicked():
    
    for item in st.session_state.items():
        if (item[1] == True) & (item[0][:2] == 'so'): # if it is search option button and its true
            st.session_state['selected_song_index'] = int(item[0][-1])
            st.session_state['current_page'] = 3

    st.session_state['track_id'] = st.session_state['sp_song_data'][st.session_state['selected_song_index']]['track_id']

    st.session_state['recommended_songs'] = f.recommend_song(model_name,
                                                             st.session_state['track_id'], 
                                                             st.session_state['popularity_min'], 
                                                             st.session_state['popularity_max']).to_dict(orient="records")

def main():

    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 1

    if 'track_name' not in st.session_state:
        st.session_state['track_name'] = ""

    if 'artist' not in st.session_state:
        st.session_state['artist'] = ""

    if 'sp_song_data' not in st.session_state:
        st.session_state['sp_song_data'] = []
        
    if 'popularity_min' not in st.session_state:
        st.session_state['popularity_min'] = 0
        st.session_state['popularity_max'] = 100

    # Logo
    st.image('./resources/melodymind_logo_v5.png', width=150)

    st.divider()
    
    # --- PAGE 1 ---
    if st.session_state['current_page'] == 1:

        # Track name input box
        st.text_input('Type a song that you like', key='track_name')
    
        # Artist input box
        st.text_input('Type the artist (optional)', key='artist')
        
        # Search button
        search_button = st.button('Search song', on_click=like_song_clicked)

        if search_button:
            if st.session_state['track_name'] == "":
                st.error("You must input a song.")

    # --- PAGE 2 ---
    elif st.session_state['current_page'] == 2:
        
        # --- HEADER ---
        st.subheader('Choose a song...')
        st.caption("Click on 'I like this song!' to get recommendations.")

        st.divider()

        # --- SONG SEARCH RESULTS ---
        for index, song in enumerate(st.session_state['sp_song_data']):
            col1, col2 = st.columns(2)

            with col1:
                st.subheader(song['track_name'])
                st.caption(song['artist'])
                st.write(f.convert_seconds_to_min_seconds(song['track_duration']))
                st.write('Album: *'+str(song['album_name'])+'*')
                st.write('Released: ', song['album_release_year'])

            with col2:
                st.image(song['album_image'],width=125)
                st.button('I like this song!', on_click=option_song_clicked, key='so_button_'+str(index))

            st.divider()

    # --- PAGE 3 ---
    elif st.session_state['current_page'] == 3:

        # --- HEADER ---
        col1, col2 = st.columns([3, 1])

        with col1:
            st.subheader('You will also like these songs!')
            st.caption('Find below a list of recommended songs based on your selection.')
            
        with col2:
            st.button('Start again', on_click=start_again)

        # --- POPULARITY FILTER ---
        st.caption('Use the popularity filter to narrow down your results:')
        st.select_slider('',
                                          options=['Hidden Gem', 'Underrated', 'Trending', 'Popular', 'Super hit'],
                                          value=('Hidden Gem', 'Super hit'),
                                         on_change=update_popularity,
                                         key='pop_slider')

        st.divider()

        # --- RECOMMENDED SONGS ---
        recommended_songs = st.session_state['recommended_songs']

        if len(recommended_songs) == 0:
            st.info('No recommendations available. Consider widening the popularity filter.')
        for index, song in enumerate(recommended_songs):
            col1, col2 = st.columns(2)
    
            with col1:
                st.subheader(song['track_name'])
                st.caption(song['artist'])
                st.write(f.convert_seconds_to_min_seconds(song['track_duration']))
                st.write('Album: *'+str(song['album_name'])+'*')
                st.write('Released: ', song['album_release_year'])
                st.write('Popularity: ', song['popularity'])
    
            with col2:
                st.image(song['album_image'], width=125)
                st.markdown('[Listen on Spotify!](' + song['track_link'] + ')')

            st.divider()
                    
if __name__ == "__main__":
    main()