<p>import os
import requests
from github import Github
from bs4 import BeautifulSoup
import mistune</p>
<h1>Set up your GitHub personal access token</h1>
<p>access_token = os.environ[&quot;GITHUB_TOKEN&quot;]
g = Github(access_token)</p>
<h1>Function to download file content from a URL</h1>
<p>def download_file(url):
    response = requests.get(url)
    return response.text</p>
<h1>Function to convert HTML to Markdown</h1>
<p>def html_to_markdown(html):
    soup = BeautifulSoup(html, &quot;html.parser&quot;)
    markdown = mistune.markdown(soup.get_text())
    return markdown</p>
<h1>Main function to get repository content in Markdown</h1>
<p>def get_repo_content_markdown(user, repo_name):
    repo = g.get_user(user).get_repo(repo_name)
    markdown_contents = []</p>
<pre><code>for content in repo.get_contents(&quot;&quot;):
    if content.type == &quot;file&quot; and content.path.endswith(&quot;.html&quot;):
        html_content = download_file(content.download_url)
        markdown_content = html_to_markdown(html_content)
        markdown_contents.append(markdown_content)

return markdown_contents


</code></pre>
<h1>Example usage</h1>
<p>user = &quot;username&quot;
repo_name = &quot;repository-name&quot;
markdown_contents = get_repo_content_markdown(user, repo_name)</p>
<p>for md_content in markdown_contents:
    print(md_content)</p>
