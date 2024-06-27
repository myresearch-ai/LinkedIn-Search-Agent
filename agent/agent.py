"""
This module contains a class called SearchLinkedIn that allows you to search for the LinkedIn profile of a person using the OpenAI GPT-3.5 Turbo model.
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub


class SearchLinkedIn:
    """
    A class that represents a LinkedIn search agent.

    Attributes:
        agent (Agent): The react agent used for executing tools.
        executor (AgentExecutor): The executor for the react agent.
        llm (ChatOpenAI): The ChatOpenAI instance for language generation.
    """

    def __init__(self):
        """
        Initializes the SearchLinkedIn class by creating the react agent, executor, and ChatOpenAI instance.
        """
        # Create the react agent and executor
        self.agent = create_react_agent()
        self.executor = AgentExecutor(self.agent)

        # Initialize the ChatOpenAI instance
        self.llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    def search_linkedin(self, name: str) -> str:
        """
        Searches for the LinkedIn profile of a person.

        Args:
            name (str): The name of the person to search for.

        Returns:
            str: The LinkedIn URL of the person's profile.
        """
        # Define the prompt template
        prompt = PromptTemplate(
            template="Search for the LinkedIn profile of {name}. Your response should only include the LinkedIn URL.",
            variables={"name": name},
        )

        # Create a list of tools for search
        tools_for_search = [
            Tool(
                name="LinkedIn",
                func="",  # Add the function to search for LinkedIn profile
                description="Search for the LinkedIn profile of the person.",
                prompt=prompt,
            )
        ]

        # Pull the react prompt from the hub
        react_prompt = hub.pull("hwchase17/react")

        # Create the agent with the specified parameters
        agent = create_react_agent(
            llm=self.llm,
            tools=tools_for_search,
            react_prompt=react_prompt,
        )

        # Execute the agent with the input prompt
        executor = AgentExecutor(agent, verbose=True)
        result = executor.invoke(input={"input": prompt.format_prompt(name=name)})
        linkedin_url = result["output"]

        return linkedin_url


if __name__ == "__main__":
    # Create an instance of the SearchLinkedIn class
    search_agent = SearchLinkedIn()

    # Call the search_linkedin method with a name
    linkedin_url = search_agent.search_linkedin("John Doe")

    # Print the LinkedIn URL
    print(linkedin_url)
