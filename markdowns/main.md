<p>import os
import stat
import tempfile
import shutil
import mistune
import chardet
from github import Github
from git import Repo
from dotenv import load_dotenv</p>
<p>def clone_repository(github_token, repo_name):
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    clone_url = repo.clone_url</p>
<pre><code>temp_dir = tempfile.mkdtemp()
cloned_repo = Repo.clone_from(clone_url, temp_dir)

return cloned_repo


</code></pre>
<p>def convert_files_to_markdown(repo_dir):
    markdown_renderer = mistune.create_markdown()</p>
<pre><code>print(&quot;Creating markdowns folder...&quot;)
markdowns_folder = os.path.join(os.getcwd(), 'markdowns')
os.makedirs(markdowns_folder, exist_ok=True)

print(&quot;Converting files to Markdown...&quot;)
for root, dirs, files in os.walk(repo_dir):
    for file in files:
        file_path = os.path.join(root, file)

        # Detect the file encoding
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            encoding = chardet.detect(raw_data)['encoding']

        # Read the file using the detected encoding
        with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
            content = f.read()

        markdown_content = markdown_renderer(content)

        # Compute the relative path of the file
        relative_path = os.path.relpath(root, repo_dir)
        if relative_path == '.':
            relative_path = ''

        # Save the Markdown file in the /markdowns folder with the same relative path
        md_file_path = os.path.join(
            markdowns_folder, relative_path, os.path.splitext(file)[0] + '.md')
        os.makedirs(os.path.dirname(md_file_path), exist_ok=True)
        with open(md_file_path, 'w', encoding='utf-8') as md_file:
            md_file.write(markdown_content)


</code></pre>
<p>def remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)</p>
<p>def main():
    try:
        print(&quot;Running script...&quot;)
        load_dotenv()</p>
<pre><code>    access_token = os.environ[&quot;GITHUB_TOKEN&quot;]
    # Replace with the desired repo name (format: username/repo)
    repo_name = &quot;vitoalmeida/python_scrapper&quot;

    # Clone the repository
    cloned_repo = clone_repository(access_token, repo_name)

    # Convert all files in the repository to Markdown
    convert_files_to_markdown(cloned_repo.working_dir)

    # Cleanup temporary directory
    shutil.rmtree(cloned_repo.working_dir, onerror=remove_readonly)

except Exception as e:
    print(f&quot;Error: {str(e)}&quot;)


</code></pre>
<p>if <strong>name</strong> == &quot;<strong>main</strong>&quot;:
    main()</p>
