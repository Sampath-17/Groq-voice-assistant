from openai import OpenAI
from groq import Groq
import speech_recognition as sr
import pyttsx3
import os

GROQ_API_KEY = <your-groq-api>

assi_mess=[{
            "role": "assistant",
            "content": 'You are a intelligent AI assistant which produces logical, honest and helpfull solutions to the user while being brief.'
                       'In response to the user prompts, you do not need to respond with formatting such as bold letter etc.'
            }]

opti_conv=('As an expert Al prompt engineer who knows how to interpret an average humans prompt and rewrite it in a '
            'way that increases the probability of the sodel generating the most useful possible response to any specific'
            ' human prompt. In response to the user prompts, you do not respond as an Al assistant. You only respond with an '
            'improved variation of the users prompt, with no explanations before or after the prompt of why it is better. Do '
            'not generate anything but the expert prompt engineers modified version of the users prompt.'
            'Do not generate anything besides the optimized prompt with no headers or explanations of the optimized prompt')

opti_mess=[{
            "role": "assistant",
            "content": opti_conv
            }]
            
recognizer = sr.Recognizer()
tts = pyttsx3.init()

def speak(text):
    tts.say(text)
    tts.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("Could not understand the audio.")
        speak("Sorry, I didn't catch that.")
        return None
    except sr.RequestError:
        print("Could not request results from Google Speech Recognition service.")
        speak("Speech recognition error.")
        return None

def Groq_response(mess):
    client = Groq(api_key = GROQ_API_KEY)
    completion = client.chat.completions.create(
        #Use your preferred model here 
        model="llama-3.3-70b-versatile",
        messages=mess,
    )
    response = completion.choices[0].message.content
    return response


print("Your Assistant is Ready. Say 'quit' to stop.")
while True:
    #commont the other to use in voice assistant mode.
    # query = listen()
    query = input("User: ")
    if query:
        print(f'\n You Said: {query}\n')
        if query.lower() in ["quit"]:
            speak("Goodbye!")
            break
        #Prompt Optimizer
        Optimized = Groq_response(opti_mess + [{"role": "user", "content": query}])
        print(f'Optimized Prompt: {Optimized}\n')
        
        assi_mess.append({"role": "user", "content": optimized})
        answer = Groq_response(assi_mess)        
        print(f'Assistant: {answer}\n')
        speak(answer)
