from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser, BrowserConfig
import asyncio


browser = Browser(config=BrowserConfig(headless=False,
                                       chrome_instance_path=r"C:\Program Files (x86)\Google\Chrome\Application\chrome"))


async def main():
    agent = Agent(
        task="Open my LinkedIn and send message 'I'm browser agent' to ABHINAV CHINNA LACHANNAGARI.",
        llm=ChatOpenAI(model="gpt-4o"),
        browser=browser,
    )
    result = await agent.run()
    print(result)

asyncio.run(main())
