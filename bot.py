
# -*- coding: utf-8 -*-
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
top = {'Brand': 'M&S', 'type': 'shirt', 'Size': 'Medium','Color':'Blue','Price':'30$'}
bottom = {'Brand': 'M&S', 'type': 'short', 'Size': 'Medium','Color':'white','Price':'20$'}

var=7
chatbot = ChatBot("luis")
conversation = [
    "Hello",
    "Hi there!",
    "How are you doing?",
    "I'm doing great.",
    "That is good to hear",
    "Thank you.",
    "You're welcome.",
    "bye",
    "See you"
]

chatbot.set_trainer(ListTrainer)
chatbot.train(conversation)


chatbot.train([
    "Hi there!",
    "Hello",
])

chatbot.train([
    "Hi there!",
    "Hello",
])

chatbot.train([
    "Greetings!",
    "Hello",
])

chatbot.train([
    "How many people have seen you today?",
    var
]) 

chatbot.train([
    "What are you wearing?",
    "im wearing a %s %s" %(top['Color'],top['type'])
]) 



chatbot.train([
    "Greetings!",
    "Hello",
])

say = raw_input("Ask something : ")
while(say!="bye"):
    response = chatbot.get_response(say)
    print(response)
    say = raw_input("Ask something : ")
    
response = chatbot.get_response(say)
print(response)