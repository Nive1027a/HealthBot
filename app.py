import os
import sqlite3
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

app = Flask(__name__)

# llm setup


groq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    api_key=groq_api_key,
    model="openai/gpt-oss-20b"
)

prompt = ChatPromptTemplate.from_messages([
    ("system","You are a helpful AI health assistant.You can use bold text and tables where appropriate."),
    ("human","{question}")
])

chain = prompt | llm

# DATABASE

def init_db():
    conn = sqlite3.connect("healthbot.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chats(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT,
    answer TEXT
    )
    """)
    conn.commit()
    conn.close()
init_db()    

# starting

@app.route("/")
def home():
    return render_template("index.html")

# question

@app.route("/chat", methods=["POST"])
def chat():

    user_message = request.json.get("message")
    user_message = user_message.capitalize()
    
    response = chain.invoke({"question":user_message})
    bot_message = response.content

    conn = sqlite3.connect("healthbot.db")
    c = conn.cursor()
    c.execute("INSERT INTO chats(question,answer) VALUES(?,?)",(user_message,bot_message))
    conn.commit()
    conn.close()

    return jsonify({"response":bot_message})

# history

@app.route("/history")
def history():

    conn=sqlite3.connect("healthbot.db")
    c=conn.cursor()

    c.execute("SELECT question, answer FROM chats ORDER BY id DESC")
    data =c.fetchall()

    conn.close()
    return jsonify(data)

# running web

if __name__ == "__main__":
    app.run(debug=True)