import requests
from google import genai
# ------------------ CONFIG ------------------
GEMINI_API_KEY = "AIzaSyCf8CoovwApwhXh6Va4IAfsMheswxvwYyQ"
GOOGLE_API_KEY = "AIzaSyBO-1Jw5bdez946MA2EOEm-GYcBa8MhF54"
SEARCH_ENGINE_ID = "465ac168d52b94466"

client = genai.Client(api_key=GEMINI_API_KEY)

# ---------------- GOOGLE SEARCH ----------------
def get_real_links(topic, num=10):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": topic,
        "num": num
    }

    response = requests.get(url)
    data = response.json()

    links = []
    for item in data.get("items", []):
        links.append(item["link"])

    return links

# ---------------- GEMINI FILTER ----------------
def filter_links_with_gemini(topic, links):
    if not links:
        return "No links found."

    prompt = f"""
Topic: {topic}

Select ONLY high-quality educational links.
Prefer:
- Wikipedia
- Britannica
- IBM
- Microsoft
- University / research sites

Remove ads, blogs, and shopping sites.

Links:
{chr(10).join(links)}

Return only the final links.
"""

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )

    return response.text

# ---------------- MAIN ----------------
topic = input("Enter a topic to search: ")

print("\n🔍 Fetching REAL Google links...\n")
links = get_real_links(topic)

print("📄 Links found:")
for link in links:
    print(link)

print("\n🤖 Gemini AI filtering best links...\n")
final_links = filter_links_with_gemini(topic, links)

print("\n✅ Final Educational Links:\n")
print(final_links)