# game.py
import streamlit as st
import random

# Set page configuration
st.set_page_config(
    page_title="Guess the Number Game",
    page_icon="🎮",
    layout="centered"
)

# Initialize session state variables
if 'number' not in st.session_state:
    st.session_state.number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.session_state.guesses = []
    st.session_state.message = "I'm thinking of a number between 1 and 100. Take a guess!"

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 20px;
    }
    .stButton > button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 12px;
        border-radius: 8px;
        font-size: 16px;
        font-weight: bold;
        margin-top: 10px;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background-color: #45a049;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    .new-game-btn > button {
        background-color: #FF5722 !important;
    }
    .new-game-btn > button:hover {
        background-color: #E64A19 !important;
    }
    .message-box {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 20px 0;
        text-align: center;
        font-size: 18px;
        min-height: 100px;
        display: flex;
        align-items: center;
        justify-content: center;
        backdrop-filter: blur(10px);
    }
    .win-message {
        color: #FFD700;
        font-weight: bold;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    .attempts-counter {
        font-size: 20px;
        font-weight: bold;
        text-align: center;
        margin: 15px 0;
    }
    .guesses-history {
        margin-top: 20px;
        padding: 15px;
        background-color: rgba(0, 0, 0, 0.1);
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Main game UI
st.title("🎮 Guess the Number Game")
st.markdown("---")

# Game state display
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Attempts", st.session_state.attempts)
with col2:
    st.metric("Guesses", len(st.session_state.guesses))
with col3:
    status = "Playing" if not st.session_state.game_over else "Won! 🎉"
    st.metric("Status", status)

# Message display
st.markdown('<div class="message-box">' + st.session_state.message + '</div>', unsafe_allow_html=True)

# Game controls (only show if game isn't over)
if not st.session_state.game_over:
    # Input for guess
    col1, col2 = st.columns([3, 1])
    with col1:
        guess = st.number_input(
            "Enter your guess (1-100):",
            min_value=1,
            max_value=100,
            value=50,
            step=1,
            key="guess_input"
        )
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        submit_guess = st.button("🚀 Submit Guess")
    
    # Handle guess submission
    if submit_guess:
        st.session_state.attempts += 1
        st.session_state.guesses.append(guess)
        
        if guess < 1 or guess > 100:
            st.session_state.message = "⚠️ Please enter a number between 1 and 100!"
        elif guess < st.session_state.number:
            st.session_state.message = f"📈 Too low! Try a number higher than {guess}."
        elif guess > st.session_state.number:
            st.session_state.message = f"📉 Too high! Try a number lower than {guess}."
        else:
            st.session_state.message = f"""
            <div class="win-message">
            🎉 CONGRATULATIONS! 🎉<br>
            You guessed the number {st.session_state.number} correctly!<br>
            It took you {st.session_state.attempts} attempts.
            </div>
            """
            st.session_state.game_over = True
        
        # Force rerun to update UI
        st.rerun()

# Show guesses history
if st.session_state.guesses:
    with st.expander("📊 Guesses History"):
        for i, g in enumerate(st.session_state.guesses, 1):
            if g < st.session_state.number:
                st.write(f"Attempt {i}: {g} ➡️ Too low")
            elif g > st.session_state.number:
                st.write(f"Attempt {i}: {g} ➡️ Too high")
            else:
                st.write(f"Attempt {i}: {g} ➡️ ✅ Correct!")

# New Game Button
st.markdown("<div class='new-game-btn'>", unsafe_allow_html=True)
if st.button("🔄 Start New Game", key="new_game"):
    # Reset session state
    st.session_state.number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.session_state.guesses = []
    st.session_state.message = "New game started! I'm thinking of a number between 1 and 100. Take a guess!"
    st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# Instructions sidebar
with st.sidebar:
    st.header("📖 How to Play")
    st.markdown("""
    1. **I've picked** a random number between 1 and 100
    2. **Enter your guess** in the number input
    3. **Click Submit** to make your guess
    4. **I'll tell you** if it's too high or too low
    5. **Keep guessing** until you find the number!
    6. **Try to win** in as few attempts as possible
    """)
    
    st.header("🎯 Tips")
    st.markdown("""
    - Start with the middle number (50)
    - Use binary search strategy
    - Keep track of your previous guesses
    - Don't guess the same number twice!
    """)
    
    st.header("📈 Statistics")
    if st.session_state.guesses:
        avg_guess = sum(st.session_state.guesses) / len(st.session_state.guesses)
        st.metric("Average Guess", f"{avg_guess:.1f}")
    st.metric("Target Number", "???" if not st.session_state.game_over else st.session_state.number)
    
    # Add a fun progress bar for attempts
    st.progress(min(st.session_state.attempts / 20, 1.0))
    st.caption(f"Difficulty: {'Easy' if st.session_state.attempts < 10 else 'Medium' if st.session_state.attempts < 15 else 'Hard'}")

# Footer
st.markdown("---")
st.caption("Made with ❤️ using Streamlit | Try to beat your high score!")
