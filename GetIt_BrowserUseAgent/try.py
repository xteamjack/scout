"""
Simple try of the agent.

@dev You need to add ANTHROPIC_API_KEY to your environment variables.
"""

import os
import sys

from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import argparse
import asyncio

from browser_use import Agent
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.controller.service import Controller


def get_llm(provider: str):
	if provider == 'anthropic':
		return ChatAnthropic(
			model_name='claude-3-5-sonnet-20240620', timeout=25, stop=None, temperature=0.0
		)
	elif provider == 'openai':
		return ChatOpenAI(
			base_url="https://models.inference.ai.azure.com", 
			model='gpt-4o', 
			temperature=0.0,
			api_key=os.environ["GITHUB_TOKEN"],
		)
	else:
		raise ValueError(f'Unsupported provider: {provider}')


# task = 'Show the solution of y"(z) + sin(y(z)) = 0 from wolframalpha https://www.wolframalpha.com/'
task = """
	Using https://www.zaubacorp.com/company/BRANE-ENTERPRISES-PRIVATE-LIMITED/U72900TG2020PTC141392 
  	extract information like CIN, Legal Entity Name, Stock market listing, current status, date of incoporation,  board of directors, list of directors
	in a json format"""


parser = argparse.ArgumentParser()
parser.add_argument('--query', type=str, help='The query to process', default=task)
parser.add_argument(
	'--provider',
	type=str,
	choices=['openai', 'anthropic'],
	default='openai',
	help='The model provider to use (default: openai)',
)

args = parser.parse_args()

# llm = get_llm(args.provider)
llm = get_llm('openai')


browser = Browser(
	config=BrowserConfig(
		# chrome_instance_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
		# chrome_instance_path='C:\Program Files\Google\Chrome\Application\chrome.exe',
		chrome_instance_path="D:\\bin\\Chrome\\131.0.6778.108\\chrome-win64\\chrome.exe",
	)
)

agent = Agent(
	task=args.query, llm=llm, controller=Controller(), browser=browser, validate_output=True
)


async def main():
	await agent.run(max_steps=25)

	await browser.close()


asyncio.run(main())