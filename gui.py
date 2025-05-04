import time
from threading import Thread
from tkinter import font as tkfont
from tkinter import scrolledtext
from tkinter import *
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()  # Load .env variables

genai.configure(api_key=os.environ['GEMINI_API_KEY'])

model = genai.GenerativeModel("gemini-2.0-flash")
chat = model.start_chat(
    history=[
        {"role": "user", "parts": "Hello"},
        {"role": "model", "parts": "Great to meet you. What would you like to know?"}
    ]
)


# Initialize the main window
window = Tk()
window.geometry("650x500")
window.title("AI ChatBot")
window.configure(bg="#e0f7fa")  # Light teal background


def send():
    """Send the user's question to the AI and display the response."""
    user_input = questionEntry.get()
    if user_input.strip() == "":
        return  # Ignore empty input

    # Display user's question in the response area
    responseText.insert(END, f"You: {user_input}\n")
    questionEntry.delete(0, END)  # Clear the entry field

    # Get AI's response
    response = chat.send_message(user_input, stream=True)
    responseText.insert(END, "AI is thinking...\n")
    for chunk in response:
        responseText.insert(END, f"{chunk.text}\n")
        responseText.see(END)  # Scroll to the end of the text area
    questionEntry.delete(0, END)  # Clear the entry field


def sendStream():
    t = Thread(target=send)
    t.start()


# Define custom fonts
title_font = tkfont.Font(family="Helvetica", size=18, weight="bold")
text_font = tkfont.Font(family="Arial", size=12)
button_font = tkfont.Font(family="Verdana", size=10, weight="bold")

# Title label
title_label = Label(window, text="Welcome to AI ChatBot 🤖", bg="#e0f7fa",
                    fg="#006064", font=title_font)
title_label.grid(column=0, row=0, columnspan=2, pady=(15, 5))

# Response display area
responseText = scrolledtext.ScrolledText(
    window, wrap=WORD, width=60, height=15, bg="#fffde7", font=text_font)
responseText.grid(column=0, row=1, columnspan=2, padx=10, pady=10)

# Entry for user input
questionEntry = Entry(window, width=45, bg="#ffffff", font=text_font)
questionEntry.grid(column=0, row=2, padx=10, pady=10, sticky=W)

# Send button
sendButton = Button(window, text="Send", bg="#00796b", fg="white",
                    font=button_font, width=10, height=1, command=sendStream)
sendButton.grid(column=1, row=2, padx=10, pady=10, sticky=E)

window.mainloop()
