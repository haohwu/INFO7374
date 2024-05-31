from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
import os
from openai import OpenAI
import openai
import streamlit as st
os.environ['OPENAI_API_KEY'] = 'sk-proj-xhciNXC1j7affb7gGXIGT3BlbkFJiYQ2e57BzdlmwVeRGz5J'
model = SentenceTransformer('all-MiniLM-L6-v2')


os.environ['PINECONE_API_KEY'] = '6af43f47-f2bd-4ef5-9a3c-315257881c1f'

index = "boston-restaurants"
client = OpenAI()
pc=Pinecone(api_key='6af43f47-f2bd-4ef5-9a3c-315257881c1f',)

def find_match(input):
    input_em = model.encode(input).tolist()
    result = index.query(input_em, top_k=2, includeMetadata=True)
    return result.matches[0].metadata.text+"\n"+result.matches[1].metadata.text

def query_refiner(conversation, query):
    completion = client.completions.create(model='gpt-3.5-turbo-instruct',prompt= f'Given the following user query and conversation log, formulate a question that would be the most relevant to provide the user with an answer from a knowledge base.\n\nCONVERSATION LOG: \n{conversation}\n\nQuery: {query}\n\nRefined Query:')
    #print(completion.choices[0].text)
    response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": 'user',
            "content": f'Given the following user query and conversation log, formulate a question that would be the most relevant to provide the user with an answer from a knowledge base.\n\nCONVERSATION LOG: \n{conversation}\n\nQuery: {query}\n\nRefined Query:',
            #"temperature":0.7,
            #"max_tokens":256,
            #"top_p":1,
            #"frequency_penalty":0,
            #"presence_penalty":0
            },
    
    ],
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
),

    return completion.choices[0].text

def get_conversation_string():
    conversation_string = ""
    for i in range(len(st.session_state['responses'])-1):
        
        conversation_string += "Human: "+st.session_state['requests'][i] + "\n"
        conversation_string += "Bot: "+ st.session_state['responses'][i+1] + "\n"
    return conversation_string