"""
This module contains a class called SearchLinkedIn that allows you to search for the LinkedIn profile of a person using the OpenAI GPT-3.5 Turbo model.
"""

import os
import requests
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

# Load environment variables from .env file
load_dotenv()


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
        # self.agent = create_react_agent()
        # self.executor = AgentExecutor(self.agent)

        # Initialize the ChatOpenAI instance
        self.llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    def search_linkedin(self, query: str, by_name: bool = True) -> str:
        """
        Searches for the LinkedIn profile of a person based on either a name or a description.

        Args:
            query (str): The name or description of the person to search for.
            by_name (bool): If True, searches by name; if False, searches by description.

        Returns:
            str: The LinkedIn URL of the person's profile.
        """
        # Define the prompt template based on the search type
        if by_name:
            prompt = PromptTemplate(
                template="Search for the LinkedIn profile of {query}. Your response should only include the LinkedIn URL.",
                variables={
                    "query": query},
            )
        else:
            prompt = PromptTemplate(
                template="Search for the LinkedIn profile of a person described as: {query}. Your response should only include the LinkedIn URL.",
                variables={
                    "query": query},
            )

        # Create a list of tools for search
        tools_for_search = [
            Tool(
                name="LinkedIn",
                func=self._search_linkedin_profile,
                description="Search for the LinkedIn profile of the person based on query.",
                prompt=prompt,
            )]

        # Pull the react prompt from the hub
        react_prompt = hub.pull("hwchase17/react")

        # Create the agent with the specified parameters
        agent = create_react_agent(
            llm=self.llm,
            tools=tools_for_search,
            prompt=react_prompt,
        )

        # Execute the agent with the input prompt
        executor = AgentExecutor(
            agent=agent, tools=tools_for_search, verbose=True)
        result = executor.invoke(
            input={"input": prompt.format_prompt(query=query)})
        linkedin_url = result["output"]

        return linkedin_url

    def _search_linkedin_profile(
            self,
            linkedin_profile_url: str,
            mock: bool = False) -> dict:
        """
        Scrapes information from LinkedIn profiles.

        Args:
            linkedin_profile_url (str): The URL of the LinkedIn profile to scrape.
            mock (bool): If True, use a mock URL for testing purposes.

        Returns:
            dict: A dictionary containing the scraped profile information.
        """
        if mock:
            linkedin_profile_url = "https://gist.githubusercontent.com/emarco177/0d6a3f93dd06634d95e46a2782ed7490/raw/78233eb934aa9850b689471a604465b188e761a0/eden-marco.json"
            response = requests.get(
                linkedin_profile_url,
                timeout=10,
            )
        else:
            api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
            header_dic = {
                "Authorization": f'Bearer {
                    os.environ.get("PROXYCURL_API_KEY")}'}
            response = requests.get(
                api_endpoint,
                params={"url": linkedin_profile_url},
                headers=header_dic,
                timeout=10,
            )

        data = response.json()
        data = {
            k: v
            for k, v in data.items()
            if v not in ([], "", "", None)
            and k not in ["people_also_viewed", "certifications"]
        }
        if data.get("groups"):
            for group_dict in data.get("groups"):
                group_dict.pop("profile_pic_url")

        return data


if __name__ == "__main__":
    # Create an instance of the SearchLinkedIn class
    search_agent = SearchLinkedIn()

    # Call the search_linkedin method with a name
    linkedin_url_by_name = search_agent.search_linkedin(
        "Ed Mwanza", by_name=True)
    print(f"LinkedIn URL by name: {linkedin_url_by_name}")

    # Call the search_linkedin method with a description
    linkedin_url_by_description = search_agent.search_linkedin(
        "Experienced AI researcher and practitioner with more than 10 years experience with demonstrated technical leadership experience",
        by_name=False)
    print(f"LinkedIn URL by description: {linkedin_url_by_description}")

    # Scrape the LinkedIn profile information
    profile_info = search_agent._search_linkedin_profile(linkedin_url_by_name)
    print(f"Profile information: {profile_info}")
