from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def get_gpt_response(messages, response_format="text"):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        response_format={"type": response_format},
        max_tokens=4096,  # Adjust max tokens based on the model limit
        temperature=0.7
    )
    return response.choices[0].message.content

def notify_gpt_context_off():
    system_message = "The context window is now off. Next session will start fresh without history background."
    messages = [
        {"role": "system", "content": system_message}
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=50,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def generate_repo_summary(file_contents):
    summary = file_contents
    if len(summary.encode('utf-8')) > 16000:  # Roughly accounting for token size
        summary = summary[:16000] + "\n\n... [Content truncated]"
    return summary

def suggest_code_improvements(prompt, repo_summary):
    detailed_prompt = f"""
Based on the following request, please identify which files need to be updated, and provide the WHOLE updated codebase to replace for each changed file:
{prompt}

The expected format of the response should be a JSON-like structure as shown below:

{{
"file_path": "new_code_here",
"another_file_path": "another_new_code_here",
}}
The JSON structure should contain the file paths as keys, and the new codebase as values. Please ensure the json object is formatted correctly and contains the updated code for each file.
The code must be a new version of the file, not a diff and also contains a new line at the end of the file.
"""
    messages = [
        {"role": "system", "content": f"You are a helpful assistant with expertise in programming and code refactoring. Here is the repository structure:\n{repo_summary}"},
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": detailed_prompt}
    ]
    return get_gpt_response(messages, response_format="json_object")

def reflect_on_diff(diff, repo_summary):
    detailed_reflection_prompt = f"Here is the git diff:\n{diff}\nIs this correct, or would you like to make any corrections? Please don't make correction if the git diff is correct."

    detailed_prompt = f"""
Please review the code block and provide any corrections if needed. If the code block is correct, please confirm it. 
If there are corrections to be made, please provide an updated one, like the following example:

{{corrections:{{
"file_path": "new_code_here",
"another_file_path": "another_new_code_here",
}},
"confirm": true,
"feedback": "Why the code block is correct or incorrect."
}}
If there are no corrections to be made, set the "corrections" field to empty list and provide your feedback in the "feedback" field.
The JSON structure should contain the file paths as keys, and the new codebase as values. Please ensure the json object is formatted correctly and contains the updated code for each file.
The code must be a new version of the file, not a diff and also contains a new line at the end of the file.
"""
    messages = [
        {"role": "system", "content": "You are a helpful assistant with expertise in programming and code refactoring. Here is the repository structure:\n{repo_summary}"},
        {"role": "user", "content": detailed_reflection_prompt},
        {"role": "assistant", "content": detailed_prompt}
    ]
    return get_gpt_response(messages, response_format="json_object")
