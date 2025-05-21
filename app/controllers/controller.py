from googleapiclient.discovery import build

from ..models.deepseekapi import deepseek
def google_custom_search(api_key, cse_id, query, num_results=10):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=query, cx=cse_id, num=num_results).execute()

    results = []
    if 'items' in res:
        for item in res['items']:
            results.append({
                'title': item.get('title'),
                'link': item.get('link'),
                'snippet': item.get('snippet')
            })
    return results



def get_goal_template(query,startdate,end_date):
    result = deepseek(query,startdate,end_date)
    return result 

# === Replace these with your credentials ===


# # === Command-line input ===
# query = input("Enter your search query: ")

# if query:
#     try:
#         results = google_custom_search(API_KEY, CSE_ID, query)
#         for i, r in enumerate(results, 1):
#             print(f"\nResult {i}")
#             print(f"Title  : {r['title']}")
#             print(f"Link   : {r['link']}")
#             print(f"Snippet: {r['snippet']}")
#     except Exception as e:
#         print("Error:", e)
# else:
#     print("No query entered.")
