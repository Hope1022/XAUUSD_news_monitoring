from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv


load_dotenv()

brain = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile"
)
message = [
    ("system", """You are a gold market analyst assistant.
Your ONLY job is to decide if a news article is relevant to XAUUSD (Gold).
Relevant means:
- Directly mentions gold, XAUUSD, XAU
- High impact economic events that move gold (NFP, CPI, FOMC, interest rates, inflation, USD strength)
- Geopolitical events that affect gold (wars, sanctions, crises)
Not relevant means:
- Stocks, crypto, oil unrelated to gold
- Sports, entertainment, general news
Respond with ONLY this exact format:
RELEVANT: yes or no
REASON: one sentence why
URGENCY: high, medium, or low
"""),
    ("human", """Title: {title}
Content: {content}
Source: {source}
Is this relevant to gold trading?""")
]
prompt = ChatPromptTemplate.from_messages(message)
chain = prompt | brain | StrOutputParser()
def analyze_article(article):
    try:
            
        response = chain.invoke({
            "title": article["title"],
            "content": article["content"],
            "source": article["source"]
        })
        
        #strip means removing space from begging and end, split = spliti the string by new line then store it in a list
        lines = response.strip().split("\n")
        #jus better that result = {}, better than returning empty
        result = {
            "relevant": False,
            "reason": "unknown",
            "urgency": "low"
        }

        for line in lines:
            if "RELEVANT:" in line:
                result["relevant"] = "yes" in line.lower()
            #if a string "REASON:" is there inside the list,
            #replace REASON: with empty or nothing, or just remove  REASON: from the sentence
            if "REASON:" in line:
                result["reason"] = line.replace("REASON:", "").strip()
            #same like reason
            if "URGENCY:" in line:
                result["urgency"] = line.replace("URGENCY:", "").strip()

        return result
   


    except Exception as e:
        print(f"Analysis failed: {e}")
        return {"relevant": False, "reason": "error", "urgency": "low"}