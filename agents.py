
import asyncio
from presideo_guardrail import redact_text
from semantic_memory import update, query
from episodic_memory import add_to_memory
from agents_pydantic import synthesizer_agent, insight_agent, general_knowledge_agent,funny_bot_agent
from otel_setup import tracer


def research_agent(topic: str) -> str:
    with tracer.start_as_current_span("research_agent"):
        documents = query(topic, n_result=3)
        context = [doc["document"] for doc in documents]
        return '\n'.join(context)


def ask_second_brain(question: str) -> str:
    with tracer.start_as_current_span("ask_second_brain") as span:
        span.set_attribute("question.text", question)

        # Retrieve knowledge context
        context = research_agent(question)
        span.set_attribute("context.size", len(context))
        print("Context retrieved:\n", context)

        # Generate the main answer
        prompt = f"""You are an intelligent assistant.
        Use the following context to answer the question clearly and factually.

        Context:
        {context }

        Question:
            {question}
        """

        with tracer.start_as_current_span("generate_answer"):
            response = synthesizer_agent.run_sync(prompt).output
            answer = response.answer
            span.set_attribute("answer.confidence", response.confidence or 0)
            print("confidence score:", response.confidence, response.sources)

        # Store to episodic memory
        with tracer.start_as_current_span("update_episodic_memory"):
            add_to_memory("asked_question_answered", f"Q:{question}\nA:{answer}", {"question": question})

        # Generate insight
        with tracer.start_as_current_span("generate_insight"):
            insight_prompt = f"Generate one-sentence insight from the following answer:\n\n{answer}"
            insight_response = insight_agent.run_sync(insight_prompt).output
            redacted, _ = redact_text(insight_response.insight)
            update(redacted, metadata={"source": "insight"})

        return answer


def ask_internet(question: str) -> str:
    with tracer.start_as_current_span("ask_internet") as span:
        span.set_attribute("question.text", question)

        prompt = f"""You are an intelligent assistant.
        Use the following web search results to answer the question clearly and factually.

        Question:
            {question}
        """

        with tracer.start_as_current_span("generate_web_answer"):
            response = general_knowledge_agent.run_sync(prompt).output

        with tracer.start_as_current_span("update_web_memory"):
            update(response, metadata={"source": "web_search"})
       

        return response
    


async def ask_funny_joke() -> str:
    with tracer.start_as_current_span("ask_funny_joke") as span:
        span.set_attribute("agent.name", "funny_bot")

        prompt = "Tell me the joke you got get_joke mcp tool attached to you"

        with tracer.start_as_current_span("generate_joke"):
            result = await funny_bot_agent.run(prompt)
            response = result.output
        # --- Store result to memory ---
        with tracer.start_as_current_span("update_joke_memory"):
            span.set_attribute("joke.text", response)
            update(response, metadata={"source": "funny_joke"})

        return response