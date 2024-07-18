import streamlit as st
import re
import math

def parse_timecode_input(input_string):
    """Convierte una cadena de números sin separadores en formato HH:MM:SS:FF."""
    if re.match(r'^\d{1,8}$', input_string):
        input_string = input_string.zfill(8)
        return f"{input_string[:2]}:{input_string[2:4]}:{input_string[4:6]}:{input_string[6:8]}"
    return input_string

def timecode_to_seconds(timecode, frame_rate):
    """Convierte un timecode en formato `HH:MM:SS:FF` a segundos."""
    frame_rate = math.ceil(frame_rate)  # Redondear hacia arriba si tiene decimales
    timecode = parse_timecode_input(timecode)
    match = re.match(r'(\d{2}):(\d{2}):(\d{2}):(\d{2})', timecode)
    if not match:
        return 0
    hours, minutes, seconds, frames = map(int, match.groups())
    total_seconds = hours * 3600 + minutes * 60 + seconds + frames / frame_rate
    return total_seconds

def seconds_to_timecode(seconds, frame_rate):
    """Convierte una duración en segundos a un timecode `HH:MM:SS:FF` con un frame rate dado."""
    is_negative = seconds < 0
    seconds = abs(seconds)
    
    frame_rate = math.ceil(frame_rate)  # Redondear hacia arriba si tiene decimales
    total_frames = round(seconds * frame_rate)
    frames = total_frames % frame_rate
    total_seconds = total_frames // frame_rate
    
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    
    timecode = f"{hours:02}:{minutes:02}:{secs:02}:{frames:02}"
    return f"-{timecode}" if is_negative else timecode

def display_footer():
    footer = """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        color: black;
        text-align: center;
        padding: 10px;
        border-top: 1px solid #eaeaea;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .footer .logo {
        height: 60px; /* Increased size */
        margin-right: 20px;
    }
    .footer .separator {
        border-left: 2px solid #eaeaea;
        height: 120px;
        margin-right: 20px;
    }
    </style>
    <div class="footer">
        <img class="logo" src="http://vicherrera.net/wp-content/uploads/2023/05/VicHerrera_Logo.svg" alt="Vic Herrera Logo">
        <div class="separator"></div>
        <div>
            <p>Developed by Vic Herrera | <a href="https://vicherrera.net" target="_blank">Vic Herrera</a> | <a href="https://datawava.com" target="_blank">datawava</a></p>
            <p>© Version 1.3  - July, 2024</p>
        </div>
    </div>
    """
    st.markdown(footer, unsafe_allow_html=True)

def main():
    st.title("Timecode Calculator")

    frame_rate_options = [23.976, 24, 25, 29.97, 30, 48, 50, 59.94, 60]
    frame_rate = st.selectbox("Select Frame Rate (fps)", frame_rate_options, index=1)

    st.write("## Timecode to Seconds Conversion")
    if "timecode_input" not in st.session_state:
        st.session_state.timecode_input = "00:00:00:00"
    timecode_input = st.text_input("Enter Timecode or as a continuous string of numbers", key="timecode_input")
    formatted_timecode_input = parse_timecode_input(timecode_input)
    if st.button("Convert to Seconds"):
        st.session_state.timecode_input = formatted_timecode_input
        seconds = timecode_to_seconds(formatted_timecode_input, frame_rate)
        st.write(f"Total seconds: {seconds}")

    st.write("## Seconds to Timecode Conversion")
    seconds_input = st.number_input("Enter Seconds", min_value=0)
    if st.button("Convert to Timecode"):
        timecode = seconds_to_timecode(seconds_input, frame_rate)
        st.write(f"Timecode: {timecode}")

    st.write("## Timecode Addition/Subtraction")
    if "timecode1" not in st.session_state:
        st.session_state.timecode1 = "00:00:00:00"
    if "timecode2" not in st.session_state:
        st.session_state.timecode2 = "00:00:00:00"
    operation = st.selectbox("Select Operation", ["Add", "Subtract"])
    timecode1 = st.text_input("Timecode 1 format or as a continuous string of numbers", key="timecode1")
    timecode2 = st.text_input("Timecode 2 format or as a continuous string of numbers", key="timecode2")
    
    if operation == "Add":
        if st.button("Perform Operation"):
            formatted_timecode1 = parse_timecode_input(timecode1)
            formatted_timecode2 = parse_timecode_input(timecode2)
            st.session_state.timecode1 = formatted_timecode1
            st.session_state.timecode2 = formatted_timecode2
            total_seconds = timecode_to_seconds(formatted_timecode1, frame_rate) + timecode_to_seconds(formatted_timecode2, frame_rate)
            result_timecode = seconds_to_timecode(total_seconds, frame_rate)
            st.write(f"Result: {result_timecode}")
    elif operation == "Subtract":
        if st.button("Perform Operation"):
            formatted_timecode1 = parse_timecode_input(timecode1)
            formatted_timecode2 = parse_timecode_input(timecode2)
            st.session_state.timecode1 = formatted_timecode1
            st.session_state.timecode2 = formatted_timecode2
            total_seconds = timecode_to_seconds(formatted_timecode1, frame_rate) - timecode_to_seconds(formatted_timecode2, frame_rate)
            result_timecode = seconds_to_timecode(total_seconds, frame_rate)
            st.write(f"Result: {result_timecode}")

    display_footer()
            
if __name__ == "__main__":
    main()