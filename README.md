# LinkedIn Search Agent

This module contains a class called `SearchLinkedIn` that allows you to search for the LinkedIn profile of a person using the OpenAI GPT-3.5 Turbo model.

## Features

- Uses OpenAI's GPT-3.5 Turbo model for language generation.
- Utilizes `langchain` for creating a react agent and executing tools.
- Provides a simple interface to search for LinkedIn profiles by name.

## Repository Structure

```bash
.
├── agent
│ ├── __init__.py
│ └── agent.py
├── tools
│ ├── __init__.py
│ └── tools.py
├── .env
├── .gitignore
├── .pre-commit-config.yaml
├── config.yaml
├── LICENSE
├── poetry.lock
├── pyproject.toml
└── README.md
```

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/linkedin-search-agent.git
    cd linkedin-search-agent
    ```

2. **Install dependencies using Poetry**:

    ```bash
    poetry install
    ```

3. **Set up environment variables**:

    Create a `.env` file in the root directory and add your OpenAI API key:

    ```env
    OPENAI_API_KEY=your_openai_api_key
    ```

## Usage

You can use the `SearchLinkedIn` class to search for LinkedIn profiles. Here is an example usage:

```python
from agent.agent import SearchLinkedIn

if __name__ == "__main__":
    # Create an instance of the SearchLinkedIn class
    search_agent = SearchLinkedIn()

    # Call the search_linkedin method with a name
    linkedin_url_by_name = search_agent.search_linkedin("John Doe", by_name=True)
    print(f"LinkedIn URL by name: {linkedin_url_by_name}")

    # Call the search_linkedin method with a description
    linkedin_url_by_description = search_agent.search_linkedin("mid-level computer scientist with more than 3 years of AI relevant skills", by_name=False)
    print(f"LinkedIn URL by description: {linkedin_url_by_description}")

    # Scrape the LinkedIn profile information
    profile_info = search_agent._search_linkedin_profile(linkedin_url_by_name)
    print(f"Profile information: {profile_info}")
```
## Pre-commit Hooks
This project uses pre-commit to ensure code quality. The configuration for autopep8 and black is included in the .pre-commit-config.yaml file.

## To set up pre-commit hooks:

1. Install pre-commit:
```bash
poetry add --dev pre-commit
```

2. Install the pre-commit hooks:
```bash
poetry run pre-commit install
```

3. Update the pre-commit hooks:
```bash
poetry run pre-commit autoupdate
```

## License
This project is licensed under the MIT License. See the LICENSE file for more details.


## Contributing

Feel free to open issues or submit pull requests if you find any bugs or have suggestions for improvements.

## Acknowledgements

- [OpenAI](https://www.openai.com/)
- [LangChain](https://github.com/langchain-ai/langchain)

## Business Use Case
Using Language Models (LLMs) like GPT-3.5 Turbo to automate LinkedIn searches offers significant business advantages over manual searches. Automated searches are more efficient and scalable, allowing organizations to process a high volume of queries quickly and accurately. LLMs can understand and process complex descriptions, ensuring more precise and relevant search results. This capability is crucial for tasks such as talent acquisition, lead generation, and market research, where finding the right profiles efficiently can save time and resources. By integrating LLM-powered search into their workflows, businesses can enhance their operational efficiency, reduce human error, and stay ahead in a competitive landscape.

## Improvements Over the Original
This repository provides several improvements over the original by [Marco177](https://github.com/emarco177/ice_breaker/commits?author=emarco177), notably:

Enhanced Search Flexibility: Supports searching LinkedIn profiles by both name and detailed descriptions, offering more versatility.
## References

This project was inspired by the original [repository](https://github.com/emarco177/ice_breaker/commits?author=emarco177) by emarco177.
