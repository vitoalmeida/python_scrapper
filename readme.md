# Convert GitHub Repository to Markdown - by Vito

This script converts all files in a GitHub repository to a single Markdown file. It clones the repository, reads all files and folders, and saves the content in Markdown format. The final Markdown file can be used to easily review all files in the repository.

## Prerequisites

- Python 3.6+
- A GitHub access token with `repo` scope

## Usage

1. Clone this repository and navigate to the cloned directory:
   ```
   git clone https://github.com/<username>/github-repo-to-markdown.git
   cd github-repo-to-markdown
   ```
2. Install the dependencies:

   ```
   pip install -r requeriments.txt
   ```

3. Create `.env` file and replace the `GITHUB_TOKEN` value with your GitHub access token.

4. Run the script with the desired repository name:

   ```
   python main.py
   ```

5. The script generates a folder `markdowns` with all Markdown files inside.

6. If you want convert another GitHub repository, replace `actix/examples` with the desired repository name in the `main.py` file.

## Notes

- The maximum character limit for each Markdown file is set to 6000. If the content of a file exceeds this limit, it will be split into multiple Markdown files.
- The script ignores some file extensions and folders by default. Modify the `ignored_files_extensions` variable to add or remove extensions.
- The script generates a `README.md` file at the beginning of the first Markdown file with the content of the original `README.md` file in the repository.
- The script was tested on Windows, Linux and macOS.
