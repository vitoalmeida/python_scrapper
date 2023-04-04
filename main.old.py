import os
from dotenv import load_dotenv
import requests
from github import Github
from bs4 import BeautifulSoup
import mistune

load_dotenv()

# Set up your GitHub personal access token
access_token = os.environ["GITHUB_TOKEN"]
g = Github(access_token)

# Function to download file content from a URL


def download_file(url):
    response = requests.get(url)
    return response.text

# Function to convert HTML to Markdown


def html_to_markdown(html):
    soup = BeautifulSoup(html, "html.parser")
    markdown = mistune.markdown(soup.get_text())
    return markdown

# Main function to get repository content in Markdown


def get_repo_content_markdown(user, repo_name):
    repo = g.get_user(user).get_repo(repo_name)
    markdown_contents = []

    for content in repo.get_contents(""):
        if content.type == "file" and content.path.endswith(".html"):
            html_content = download_file(content.download_url)
            markdown_content = html_to_markdown(html_content)
            markdown_contents.append(markdown_content)

    return markdown_contents


# Example usage
user = "vitoalmeida"
repo_name = "python_scrapper"
markdown_contents = get_repo_content_markdown(user, repo_name)

for md_content in markdown_contents:
    print(md_content)
