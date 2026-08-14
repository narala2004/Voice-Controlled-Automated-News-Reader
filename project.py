import speech_recognition as sr
import requests
from gtts import gTTS
import os
from playsound import playsound  # For playing the mp3 file

# Configuration
NEWS_API_KEY = '3a9c15c659074dbeb28cd7736b1323d4'  # Get a free API key from https://newsapi.org/
LANGUAGE = 'en'

def fetch_news():
    url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        articles = response.json().get('articles', [])
        headlines = [article['title'] for article in articles[:5]]  # Get top 5 headlines
        return headlines
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return ["Error fetching news."]

def speak_text(text):
    tts = gTTS(text=text, lang=LANGUAGE, slow=False)
    filename = "news.mp3"
    tts.save(filename)
    playsound(filename)  # Use playsound to play the mp3 file
    os.remove(filename)  # Clean up the mp3 file after playing

def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for a command...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None
        except sr.RequestError as e:
            print(f"Sorry, there was an error with the request: {e}")
            return None

def main():
    while True:
        command = listen_for_command()
        if command:
            if 'news' in command:
                headlines = fetch_news()
                news_text = "Here are the top headlines: " + ", ".join(headlines)
                speak_text(news_text)
            elif 'stop' in command:
                print("Stopping...")
                break
            else:
                speak_text("Sorry, I didn't understand that command.")

if __name__ == "__main__":
    main()
