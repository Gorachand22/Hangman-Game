import streamlit as st
from accessories import word_list, stages
import random
import string

session_state = st.session_state

# Function to reset the game
def reset_game():
    session_state.chosen_word = random.choice(word_list).lower()
    session_state.word_length = len(session_state.chosen_word)
    session_state.display = ['_'] * session_state.word_length
    session_state.lives = 6
    session_state.end_of_game = False

# Function to handle button click
def handle_button_click(letter):
    if not session_state.end_of_game:
        if letter in session_state.chosen_word:
            st.success(f'Good guess! {letter} is in the word.')
            for i in range(session_state.word_length):
                if session_state.chosen_word[i] == letter:
                    session_state.display[i] = letter
            # Display current state of the word with increased font size, boldness, and color
            st.markdown(f'<p style="font-size: 100px; font-weight: bold; color: blue;">{" ".join(session_state.display)}</p>', unsafe_allow_html=True)
        else:
            st.warning(f'Wrong guess! {letter} is not in the word.')
            session_state.lives -= 1

            # Ensure lives is within the valid range
            session_state.lives = max(0, min(session_state.lives, len(stages) - 1))

            st.image(stages[session_state.lives])

            # Check if the game should end after 6 wrong guesses
            if session_state.lives == 0:
                session_state.end_of_game = True
                st.write('You lose')
                st.write(f'The word was {session_state.chosen_word}')
                reset_game()

        # Check if the word has been guessed
        if '_' not in session_state.display:
            session_state.end_of_game = True
            st.success('Congratulations! You guessed the word.')
            st.success(f'The word was {session_state.chosen_word}')
            reset_game()

# Streamlit App
st.title('Welcome to Hangman Game')
st.sidebar.title('Hangman Game')

# Sidebar options
ln = st.sidebar.selectbox('Check this out', ['Tap to play', 'how to play', 'about'])

if ln == 'Tap to play':
    if 'chosen_word' not in st.session_state:
        reset_game()

    st.image("images/hangman_logo.png", caption="Hangman Game", use_column_width=False, width=300)  

    # Display current state of the word with increased font size, boldness, and color
    st.markdown(f'<p style="font-size: 100px; font-weight: bold; color: blue;">{" ".join(session_state.display)}</p>', unsafe_allow_html=True)

    # Create clickable buttons for each alphabet
    alphabet_buttons = list(string.ascii_lowercase)
    for letter in alphabet_buttons:
        if st.button(letter, key=f"button_{letter}"):
            handle_button_click(letter)

    # Check if the word has been guessed
    if '_' not in session_state.display:
        session_state.end_of_game = True
        st.success('Congratulations! You guessed the word.')
        st.success(f'The word was {session_state.chosen_word}')
        reset_game()

elif ln == 'how to play':
    st.write("Instructions on how to play the game:")
    st.markdown("- <span style='font-size:18px; font-weight:bold; color:blue;'>Click on 'Tap to play' in the sidebar.</span>", unsafe_allow_html=True)
    st.markdown("- <span style='font-size:18px; font-weight:bold; color:blue;'>Use the clickable alphabet buttons to guess letters.</span>", unsafe_allow_html=True)
    st.markdown("- <span style='font-size:18px; font-weight:bold; color:blue;'>Each correct guess reveals the corresponding letters in the word.</span>", unsafe_allow_html=True)
    st.markdown("- <span style='font-size:18px; font-weight:bold; color:blue;'>Incorrect guesses reduce your lives (displayed by the hangman stages).</span>", unsafe_allow_html=True)
    st.markdown("- <span style='font-size:18px; font-weight:bold; color:blue;'>The game ends when you guess the entire word or run out of lives.</span>", unsafe_allow_html=True)

elif ln == 'about':
    st.write("Information about the Hangman game:")
    st.markdown("- <span style='font-size:18px; font-weight:bold; color:green;'>Hangman is a classic word-guessing game.</span>", unsafe_allow_html=True)
    st.markdown("- <span style='font-size:18px; font-weight:bold; color:green;'>The player tries to guess a hidden word, letter by letter.</span>", unsafe_allow_html=True)
    st.markdown("- <span style='font-size:18px; font-weight:bold; color:green;'>Incorrect guesses lead to a visual representation of a hangman.</span>", unsafe_allow_html=True)
    st.markdown("- <span style='font-size:18px; font-weight:bold; color:green;'>Win by guessing the entire word before running out of lives.</span>", unsafe_allow_html=True)
    st.markdown("- <span style='font-size:18px; font-weight:bold; color:green;'>Have fun and enjoy the challenge!</span>", unsafe_allow_html=True)




else:
    # Reset the game if the user is not playing
    if 'chosen_word' in st.session_state:
        reset_game()
