import csv
import logging
import asyncio
from typing import Optional

from PyPDF2 import PdfReader

from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from browser_use.browser.browser import Browser, BrowserConfig
from browser_use import ActionResult, Agent, Controller
from browser_use.browser.context import BrowserContext

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

logger = logging.getLogger(__name__)
controller = Controller()
file_path = r"C:\Personal-LLM-Projects\Browser-Agents\data\Kavali_Kranthi_Kumar_ML_Engineer.pdf"


class Job(BaseModel):
    title: str
    link: str
    company: str
    fit_score: float
    location: Optional[str] = None
    salary: Optional[str] = None


@controller.action("Save jobs to file - with a score how well its fits to my profile", param_model=Job)
def save_jobs(job: Job):
    with open("data\jobs.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow([job.title, job.link, job.company, job.fit_score, job.location, job.salary])
    return "Saved job to file"


@controller.action("Ask me for help")
def ask_for_help(question: str):
    return input(f"\n{question}\nInput: ")


@controller.action("Read my cv for context to fill forms")
def read_cv():
    pdf = PdfReader(file_path)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    logger.info("Read cv with %s characters", len(text))
    return ActionResult(extracted_content=text, include_in_memory=True)


# @controller.action("close dialog")
# async def close_file_dialog(browser: BrowserContext):
#     page = await browser.get_current_page()
#     await page.keyboard.press("Escape")


@controller.action("Upload cv to element - call this function to upload if element is not found", requires_browser=True)
async def upload_cv(index: int, browser: BrowserContext):
    # await close_file_dialog(browser)

    dom_el = await browser.get_dom_element_by_index(index)

    if dom_el is None:
        return ActionResult(error=f"No element found at index {index}")

    file_upload_dom_el = dom_el.get_file_upload_element()

    if file_upload_dom_el is None:
        logger.error("No file upload element found at index %s", index)
        return ActionResult(error=f"No file upload element found at index {index}")

    file_upload_el = await browser.get_locate_element(file_upload_dom_el)

    if file_upload_el is None:
        logger.info(f'No file upload element found at index {index}')
        return ActionResult(error=f'No file upload element found at index {index}')

    try:
        await file_upload_el.set_input_files(file_path)
        msg = f'Successfully uploaded file to index {index}'
        logger.info(msg)
        return ActionResult(extracted_content=msg)
    except Exception as e:
        logger.debug(f'Error in set_input_files: {str(e)}')
        return ActionResult(error=f'Failed to upload file to index {index}')


browser = Browser(config=BrowserConfig(headless=False,
                                       chrome_instance_path=r"C:\Program Files (x86)\Google\Chrome\Application\chrome",
                                       disable_security=True))


async def main():
    # ground_task = (
    #     'You are a professional job finder. '
    #     '1. Read my cv with read_cv'
    #     '2. Open my LinkedIn and start applying to Senior GenAI developer jobs for atleast 3 companies'
    #     'You can navigate through pages e.g. by scrolling '
    #     'Make sure to be on the english version of the page'
    # )
    # ground_task = (
    #     'You are a professional job finder. '
    #     '1. Read my cv with read_cv'
    #     'find Senior GenAI developer jobs and save them to a file'
    #     'search at company:'
    # )
    # tasks = [
    #     # ground_task + '\n' + 'Google',
    #     # ground_task + '\n' + 'Amazon',
    #     # ground_task + '\n' + 'Apple',
    #     # ground_task + '\n' + 'Microsoft',
    #     ground_task
    #     # + '\n'
    #     # + 'go to https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite/job/Taiwan%2C-Remote/Fulfillment-Analyst---New-College-Graduate-2025_JR1988949/apply/autofillWithResume?workerSubType=0c40f6bd1d8f10adf6dae42e46d44a17&workerSubType=ab40a98049581037a3ada55b087049b7 NVIDIA',
    #     # ground_task + '\n' + 'Meta',
    # ]
    tasks = [("Read my cv and find Senior GenAI developer jobs for me."
              "start applying for them - please not via job portals like LinkedIn, indeed etc"
              "if you need more information of help, ask me")]
    model = ChatOpenAI(model="gpt-4o")

    agents = []
    for task in tasks:
        agent = Agent(task=task, llm=model, controller=controller, browser=browser)
        agents.append(agent)

    await asyncio.gather(*[agent.run() for agent in agents])


if __name__ == '__main__':
    asyncio.run(main())
