
from openai import OpenAI
import json
import re


def remove_json_markers(text):
    return text.replace("```json", "").replace("```", "").strip()

def deepseek(parm,from_date,to_date):
    system_prompt = (
        "Return the response strictly in the following JSON structure:\n"
        "{\n"
        "  \"goal_name\": \"" + parm + "\",\n"
        "  \"start_date\": \"" + from_date + "\",\n"
        "  \"end_date\": \"" + to_date + "\",\n"
        "  \"goal_template\": [\n"
        "    {\n"
        "      \"title\": \"<task title>\",\n"
        "      \"start_date\": \"<task start date>\",\n"
        "      \"end_date\": \"<task end date>\",\n"
        "      \"description\": \"<brief task description>\"\n"
        "    }\n"
        "  ]\n"
        "}\n"
        "No extra text. No explanation. Only return valid JSON."
    )
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="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",  # Replace with your actual API key
    )

    completion = client.chat.completions.create(
        extra_headers={},
        extra_body={},

        model="deepseek/deepseek-prover-v2:free",
       messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": f"Generate a roadmap for becoming a {parm} between {from_date} to {to_date}."
            }
        ]
    )

    roadmap = completion.choices[0].message.content
    data = remove_json_markers(roadmap)
    print(data)
    return data






