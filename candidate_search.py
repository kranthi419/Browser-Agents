from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser, BrowserConfig, Controller
import asyncio

from pydantic import BaseModel
import csv
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

controller = Controller()
browser = Browser(config=BrowserConfig(headless=False,
                                       chrome_instance_path=r"C:\Program Files (x86)\Google\Chrome\Application\chrome"))


class CandidateInformation(BaseModel):
    name: str
    email: str
    phone: str


@controller.action("save candidates to file", param_model=CandidateInformation)
def save_candidates(candidate: CandidateInformation):
    with open(r"data\candidates_data.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow([candidate.name, candidate.email, candidate.phone])
    return "Saved job to file"


async def main():
    agent = Agent(
        task="You are professional HR. You help to find the right candidate for job."
             "You need to search for atleast 3 candidates for Machine Learning engineer job opening from linkedin."
             "Think step by step and plan the steps to find candidates from linkedin."
             "You can click on the candidate profile and click on 'Contact info' to get their information."
             "You have to save the each candidates information in a file.",
        controller=controller,
        llm=ChatOpenAI(model="gpt-4o"),
        browser=browser,
    )
    result = await agent.run()
    print(result)

asyncio.run(main())
