
from openai import OpenAI
import json
def deepseek(parm,from_date,to_date):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="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",  # Replace with your actual API key
    )

    completion = client.chat.completions.create(
        extra_headers={},
        extra_body={},

        model="deepseek/deepseek-prover-v2:free",
        messages=[
            {"role": "system", "content": "Provide a roadmap with only 'title', 'start_date', 'end_date', and 'description'. No additional text, no introduction, no AI-generated comments, no table format. The output should be in a structured JSON format."},
            {"role": "user", "content": f"Generate a roadmap for becoming a {parm} between {from_date} to {to_date}."}
        ]
    )

    roadmap = completion.choices[0].message.content
    # print(roadmap)
    return roadmap






