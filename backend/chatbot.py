from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.utilities.serpapi import SerpAPIWrapper
from langchain.chains import LLMChain
from schema import ChatRequest  
import os
from dotenv import load_dotenv

load_dotenv()

# Load the LLM
llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation"
)
model = ChatHuggingFace(llm=llm)

# Summarizer prompt
template = PromptTemplate(
    template="Summarize the following text:\n\n{topic}",
    input_variables=["topic"]
)
parser = StrOutputParser()
summarizer = template | model | parser

# Start state
chat_state = {
    "history": [],
    "last_content": "",
    "last_summary": ""
}

def fallback_with_search(question: str, summary: str):
    SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
    if not SERPAPI_API_KEY:
        return "Fallback search is not available (missing SERPAPI_API_KEY)."

    search = SerpAPIWrapper()
    search_query = f"{question} (Based on this page: {summary})"
    search_result = search.run(search_query)

    fallback_prompt = PromptTemplate.from_template(
        "Given this info: {info}\nAnswer the question: {question}"
    )
    fallback_chain = LLMChain(llm=model, prompt=fallback_prompt)

    response = fallback_chain.invoke({
        "info": search_result,
        "question": question
    })

    return response["text"] if isinstance(response, dict) else response

async def handle_query(data: ChatRequest):
    content = data.content.strip()
    question = data.question.strip()

    if not content or len(content) < 300:
        fallback_answer = fallback_with_search(question, summary="")
        return {
            "summary": "Not enough content to summarize. Fallback search used.",
            "response": fallback_answer,
            "source": "search"
        }

    if content != chat_state["last_content"]:
        summary = summarizer.invoke({"topic": content})
        chat_state["history"] = [
            SystemMessage(content=summary),
            AIMessage(content="👋 Hi! You can ask me anything about this page.")
        ]
        chat_state["last_summary"] = summary
        chat_state["last_content"] = content

        return {
            "summary": summary,
            "response": "👋 Hi! You can ask me anything about this page.",
            "source": "welcome"
        }

    summary = chat_state["last_summary"]
    chat_state["history"].append(HumanMessage(content=question))
    response = model.invoke(chat_state["history"])
    model_answer = response.content.strip()

    fallback_triggers = [
        "i don't know", "unfortunately", "not mentioned", "no information",
        "not available", "check the official", "couldn’t find", "don’t have",
        "it appears", "not clear", "unclear", "no details"
    ]
    if any(trigger in model_answer.lower() for trigger in fallback_triggers):
        fallback_answer = fallback_with_search(question, summary)
        chat_state["history"].append(AIMessage(content=fallback_answer))
        combined = (
            "🔍 This information was not found in the text, but here's what I found from the web:\n\n"
            + fallback_answer
        )
        return {
            "summary": summary,
            "response": combined,
            "source": "search"
        }

    chat_state["history"].append(AIMessage(content=model_answer))
    return {
        "summary": summary,
        "response": model_answer,
        "source": "model"
    }
