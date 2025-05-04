

while True:
    question = input("What would you like tpo know? :")
    print("----------------")
    response = chat.send_message(question)
    print(response.text)
    print("----------------")
