import asyncio
from pydantic_evals import Case, Dataset
from pydantic_evals.evaluators import EqualsExpected, LLMJudge
from agents_pydantic import synthesizer_agent, general_knowledge_agent, funny_bot_agent


async def synthesizer_main(prompt: str) -> str:
    result = await synthesizer_agent.run(prompt)
    return result.output if hasattr(result, "output") else str(result)


async def general_main(prompt: str) -> str:
    result = await general_knowledge_agent.run(prompt)
    return result.output if hasattr(result, "output") else str(result)

async def funny_bot_main(prompt:str)-> str:
    result= await funny_bot_agent.run(prompt)
    print(result)
    return result.output if hasattr(result, "output") else str(result)


synth_dataset = Dataset[str, str, str](
    name="synthesizer_answer_quality",
    cases=[
        Case(
            name="Wake up time kundapur",
            inputs=f"What time people in kundapur wake up? context=no_context_provided",
            expected_output=(
                "The model should refuse to answer due to missing context, "
                "stating clearly that it cannot provide factual information without context."
            ),
            evaluators=[LLMJudge(rubric=(
                    "Score 1.0 if the model *refuses* to answer because of missing context "
                "or lack of data (e.g., says it cannot determine without context). "
                "Score 0.0 if it tries to guess or fabricate an answer."
         ),
                                                   model="google-gla:gemini-2.5-pro"
                                                   )],
        ),
       Case(
    name="food_in_kundapur",
    inputs="People in Kundapur often eat what? context=Fish is more eaten in kundapur",
    expected_output="People in Kundapur often eat fish.",
    evaluators=[
        LLMJudge(
            rubric=     "Evaluate if the model's answer correctly identifies fish as a commonly eaten food in Kundapur based on the provided context.",
            model="google-gla:gemini-2.5-pro",
        )
    ],
)
    ],
    evaluators=[],
)


web_dataset = Dataset[str, str, str](
    name="web_search_eval",
    cases=[
        Case(
            name="olympics_winner",
            inputs="Who won the 2024 Olympics?",
            expected_output="France won the most medals at the 2024 Olympics.",
            evaluators=[ LLMJudge(rubric="Judge factual correctness for the Olympic winner.",
                                                   model="google-gla:gemini-2.5-pro"
                                                   
                                                   )],
        ),
        Case(
            name="capital_japan",
            inputs="Capital of Japan?",
            expected_output="Tokyo",
            evaluators=[ LLMJudge(rubric="Check if the capital of Japan is correct.",
                                                   model="google-gla:gemini-2.5-pro"
                                                   
                                                   )],
        ),
    ],
    evaluators=[],
)

funny_dataset=Dataset[str,str,str](
    name="funny_bot",
    cases=[
        
        Case(
            name="simple_joke",
            inputs="Tell me the joke you got get_joke mcp tool attached to you",
            expected_output="A funny joke should be returned.",
            evaluators=[
                LLMJudge(
                    rubric=(
                        "Check if the response is indeed a joke or humorous statement. "
                      
                    ),
                    model="google-gla:gemini-2.5-pro"
                )
            ],
            
            
        )
    ],
     evaluators=[],
    
)


async def main():
    print(" Running evaluation: Synthesizer Agent Eval\n")
    synth_report = await synth_dataset.evaluate(synthesizer_main)
    synth_report.print()

    print(" Running evaluation: General Knowledge Agent Eval\n")
    web_report = await web_dataset.evaluate(general_main)
    web_report.print()
    
    print(" Running evaluation: MCP Fun bot Agent Eval\n")
    web_report = await funny_dataset.evaluate(funny_bot_main)
    web_report.print()



if __name__ == "__main__":
    asyncio.run(main())
