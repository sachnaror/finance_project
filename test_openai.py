# # from langchain_openai import ChatOpenAI
# # import os

# # # Set OpenAI API Key
# # os.environ["OPENAI_API_KEY"] = "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"

# # # Use ChatOpenAI for chat models like gpt-3.5-turbo
# # llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

# # # Test OpenAI inference
# # response = llm.invoke("What is the capital of France?")
# # print("Response:", response.content)

# import requests
# from bs4 import BeautifulSoup

# ticker = "TSLA"
# url = f"https://finance.yahoo.com/quote/{ticker}/news"
# headers = {"User-Agent": "Mozilla/5.0"}
# response = requests.get(url, headers=headers)

# if response.status_code == 200:
#     soup = BeautifulSoup(response.content, "html.parser")
#     news_blocks = soup.select("h3 a")[:5]
#     for news in news_blocks:
#         print(news.get_text(strip=True), " -> ", news.get("href"))
# else:
#     print("Error fetching Yahoo Finance news.")
