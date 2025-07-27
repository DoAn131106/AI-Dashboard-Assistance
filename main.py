import pandas as pd
import streamlit as st
import openai
from dotenv import load_dotenv  # Place OPENAI_API_KEY inside .env then put .env into .gitignore to secure the API key
import os

import io
import contextlib
import matplotlib.pyplot as plt

load_dotenv()   # retrieve the API_KEY
openai.api_key = os.getenv("OPENAI_API_KEY")

# Processing database
st.title("AI Dashboard Assistant")
uploaded_file = st.file_uploader("Please provide your dataset", type = ["csv", "xlsx"])
if uploaded_file:
    if (uploaded_file.name.endswith(".csv")):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    st.write("Preview of the provided data: ", df.head())

    # Processing user's prompt
    st.write("What do you want to visualize from your data?\n")
    user_prompt = st.text_input("I want to: ")
    if user_prompt:
        sample_data = df.head(5).to_csv(index = False)
    
        # Call ChatGPT and make it learn the aggregate features of the database, e.g Column names, data types, etc
        messages = [
            {"role": "system", "content": "You are a data analyst who helps users visualize their data"},
            {"role": "user", "content": f"The dataset is:\n{sample_data}\nUser request is: {user_prompt}"}
        ]   #creating mesages to chatgpt
        
        #choosing the model, passing the message
        client = openai.OpenAI()
        response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.2 # to guarantee the little creativity and correctness of the response
        )
        generated_code = response.choices[0].message.content
        if st.checkbox("Show generated code"):
            st.code(generated_code)   # used for debugging, since it prints out what code ChatGPT responses with

        # execute the response of ChatGPT
        plt.clf()   # clean any previous matplotlib plots
        local_env = {"df": df, "plt": plt}
        output_buffer = io.StringIO()   # to create a temporary in-memory text buffer to capture anything printed

        with contextlib.redirect_stdout(output_buffer): # redirect any printed output to output_buffer instead of the terminal
            try:
                exec(generated_code, local_env)
                st.pyplot(plt)
            except Exception as e:
                st.error(f"Error running generated code\n{e}")

        std_output = output_buffer.getvalue()
        if std_output.strip():
            st.markdown(f"The above graph is based on: `{std_output.strip()}`")
        
else:
    st.write("No data provided yet")





    