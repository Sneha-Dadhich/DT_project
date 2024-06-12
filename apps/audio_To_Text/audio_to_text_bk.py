import speech_recognition as sr
from flask import render_template
from urllib.request import urlretrieve

def audio_to_text(audio_file):
    print("reached backend")
    print("Loading...........")

    recognizer = sr.Recognizer()
    
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        return text
    
def global_audio_to_text(url):
    audio_file=urlretrieve(url,"C:\\Sneha\\audio.wav")
    print(audio_to_text("C:\\Sneha\\audio.wav"))
    return audio_to_text("C:\\Sneha\\audio.wav")

if __name__ == "__main__":
    audio_file = 'C:\\Sneha\\Programs1\\Python\\Internship\\DreamTeam\\FLASK\\apps\\audio_To_Text\\harvard.wav'
