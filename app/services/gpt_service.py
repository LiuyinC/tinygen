from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def get_gpt_response(messages):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=4096,  # Adjust max tokens based on the model limit
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def generate_repo_summary(file_contents):
    summary = ""
    for file_path, content in file_contents:
        summary += f"\n\nFile: {file_path}\n{content}"
        if len(summary.encode('utf-8')) > 16000:  # Roughly accounting for token size
            summary = summary[:16000] + "\n\n... [Content truncated]"
            break
    return summary

def generate_git_diff(prompt, repo_summary):
    detailed_prompt = f"""You are a helpful assistant with expertise in programming and code refactoring. 
You have access to the following repository summary:
{repo_summary}

Please generate a git diff output based on the following request:
{prompt}

The output should be in the standard git diff format, starting with 'diff --git' and including the necessary metadata and changes in the format shown below:

diff --git a/file_path b/file_path
index old_hash..new_hash mode
--- a/file_path
+++ b/file_path
@@ -old_start,old_lines +new_start,new_lines @@
-lines removed
+lines added
 unchanged lines
"""

    messages = [
        {"role": "system", "content": "You are a helpful assistant with expertise in programming and code refactoring."},
        {"role": "user", "content": detailed_prompt}
    ]
    return get_gpt_response(messages)

def reflect_on_diff(reflection_prompt, repo_summary):
    detailed_reflection_prompt = f"""You are a helpful assistant with expertise in programming and code refactoring.
You have access to the following repository summary:
{repo_summary}

Here is the diff you generated:
{reflection_prompt}

Please review the diff and provide any corrections if needed. If the diff is correct, please confirm it. If there are corrections to be made, please provide an updated diff in the same format.
"""

    messages = [
        {"role": "system", "content": "You are a helpful assistant with expertise in programming and code refactoring."},
        {"role": "user", "content": detailed_reflection_prompt}
    ]
    return get_gpt_response(messages)
