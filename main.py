import os
import stat
import tempfile
import shutil
import mistune
import chardet
import logging
import datetime
from github import Github
from git import Repo
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO,
                    format='[%(levelname)s - %(asctime)s]: %(message)s', datefmt='%H:%M:%S')

ignored_files_extensions = ('.git', '.exe')


def clone_repository(github_token, repo_name):
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    clone_url = repo.clone_url

    temp_dir = tempfile.mkdtemp()
    cloned_repo = Repo.clone_from(clone_url, temp_dir)

    return cloned_repo


def convert_files_to_markdown(repo_dir):
    markdown_renderer = mistune.create_markdown()

    readme_content = None
    markdown_content = ""

    markdowns_folder = os.path.join(os.getcwd(), 'markdowns')

    if os.path.exists(markdowns_folder):
        logging.info("Deleting existing markdowns folder...")
        shutil.rmtree(markdowns_folder)

    logging.info("Creating markdowns folder...")
    os.makedirs(markdowns_folder, exist_ok=True)

    logging.info("Fetching README.md...")
    readme_file_path = os.path.join(repo_dir, 'README.md')
    if os.path.exists(readme_file_path):
        with open(readme_file_path, 'r', encoding='utf-8') as f:
            readme_content = f.read()

    logging.info(
        "Looping through all files and folders and converting to markdown...")

    total_length = 0
    file_num = 1
    curr_file_content = ""
    last_file_readme = False

    # Checkpoint 5 #
    def save_curr_file():
        nonlocal curr_file_content, file_num
        if len(curr_file_content) > 0:
            curr_file_path = os.path.join(
                markdowns_folder, f'single_markdown_{file_num}.md')
            with open(curr_file_path, 'w', encoding='utf-8') as md_file:
                md_file.write(curr_file_content)
            logging.info(
                f"Single markdown file {file_num} successfully generated!")
            curr_file_content = ""
            file_num += 1

    for root, dirs, files in os.walk(repo_dir):
        # Ignore any folders with ignored names
        dirs[:] = [d for d in dirs if d not in ignored_files_extensions]
        for file in files:
            file_path = os.path.join(root, file)

            # Check if file extension is ignored
            if file.endswith(ignored_files_extensions) or (file.lower() == 'readme.md' and root == repo_dir):
                continue

            # Detect the file encoding
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                encoding = chardet.detect(raw_data)['encoding']

            # Read the file using the detected encoding
            with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
                content = f.read()

            # Compute the relative path of the file
            relative_path = os.path.relpath(file_path, repo_dir)

            # Save the file content in Markdown format
            markdown_content += f"\n\n### FILE: {relative_path}\n"
            markdown_content += "```sh\n"
            markdown_content += content
            markdown_content += "\n```\n"

            total_length += len(content)

            if total_length > 10000:
                if last_file_readme:
                    save_curr_file()
                    curr_file_content += markdown_content
                    markdown_content = ""
                    total_length = len(markdown_content)
                    last_file_readme = False
                else:
                    save_curr_file()
                    curr_file_content += markdown_content
                    markdown_content = ""
                    total_length = 0
                    last_file_readme = True

    logging.info("Adding readme content to single_markdown file beginning...")
    if readme_content:
        markdown_content = f"### README\n\n{readme_content}\n\n" + \
            markdown_content

    # Save the last Markdown content to a file
    curr_file_content += markdown_content
    save_curr_file()

    logging.info(
        "\033[92mMarkdown single file(s) successfully generated!\033[0m")


def remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def main():
    try:
        logging.info("Running script...")
        load_dotenv()

        access_token = os.environ["GITHUB_TOKEN"]
        # Replace with the desired repo name (format: username/repo)
        repo_name = "vitoalmeida/python_scrapper"

        # Clone the repository
        cloned_repo = clone_repository(access_token, repo_name)

        # Convert all files in the repository to a single Markdown
        convert_files_to_markdown(cloned_repo.working_dir)

        markdown_file_path = os.path.join(
            os.getcwd(), 'markdowns', 'single_markdown.md')

        # Test if the Markdown file was generated
        if os.path.exists(markdown_file_path):
            logging.info(
                "\033[92mMarkdown single file successfully generated!\033[0m")
        else:
            logging.error(
                "\033[91mFailed to generate markdown single file!\033[0m")

        # Cleanup temporary directory
        shutil.rmtree(cloned_repo.working_dir, onerror=remove_readonly)

    except Exception as e:
        logging.info(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
