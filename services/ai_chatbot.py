import os
import openai
import sqlite3
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# Load API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Chat Model
chat = ChatOpenAI(model_name="gpt-4", temperature=0.7)

def fetch_trend_summary():
    """Fetch latest social media trends from the database"""
    conn = sqlite3.connect("smm_tool.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TrendingData ORDER BY timestamp DESC LIMIT 5")
    trends = cursor.fetchall()
    conn.close()

    if not trends:
        return "No trending data available."

    summary = "Here are the latest social media trends:\n"
    for trend in trends:
        summary += f"📌 Hashtag: {trend[1]}, Keyword: {trend[2]}, Sentiment: {trend[3]}\n"

    return summary

def chatbot_response(user_query):
    """Generate AI response based on user queries"""
    system_message = SystemMessage(content="You are an AI assistant providing insights on social media trends.")
    human_message = HumanMessage(content=user_query + " " + fetch_trend_summary())

    response = chat([system_message, human_message])
    return response.content

# Test the chatbot
print(chatbot_response("What are the latest trends on Twitter?"))
