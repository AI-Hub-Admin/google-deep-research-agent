import requests
import json
from typing import List, Any

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Replace with your actual API key and Search Engine ID
# https://developers.google.com/custom-search/v1/introduction

CX = "b148d4aa1418c4059"

LOG_ENABLE = False

def google_search(query: str, num: int = 10, start: int = 0) -> List[Any]:
    """
        query: Query to search
        num: int, return results
        start: int, pagination start index of item at the number of 0,  [0, 30], [30,60]
    """
    if query is None or query == "":
        return []
    try:
        api_key = os.environ.get("GOOGLE_SEARCH_ACCESS_KEY")
        if api_key is None or api_key == "":
            raise ValueError("Input Google Search Access Key Should not be empy.. SET GOOGLE_SEARCH_ACCESS_KEY in the .env")

        url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={CX}&q={query}&start={start}&num={num}"
        response = requests.get(url)
        # Raise an exception for bad status codes
        response.raise_for_status()
        results = response.json()
        # Process the results (e.g., print titles and links)
        items = results.get("items", [])
        return_fields = ["title", "link", "snippet"]
        KEY_RANK = "rank"
        items_return = []
        if 'items' in results:
                for i, item in enumerate(results['items']):
                    item_return_dict = {}
                    for key in return_fields:
                        item_return_dict[key] = item.get(key, "")
                    item_return_dict[KEY_RANK] = (i + 1)
                    items_return.append(item_return_dict)
                    if LOG_ENABLE:
                        print(f"Item: {item}")
                        print(f"Title: {item['title']}")
                        print(f"Link: {item['link']}")
                        print("-" * 20)
        else:
                print("No results found.")
        return items_return
    except requests.exceptions.RequestException as e:
        print(f"Google Search API error occurred: {e}")
        return []
    except Exception as e:
        print(f"Google Search API error : {e}")
        return []

"""
Item: {'kind': 'customsearch#result', 'title': 'The official site of the NBA for the latest NBA Scores, Stats & News ...', 'htmlTitle': 'The official site of the <b>NBA</b> for the latest <b>NBA</b> Scores, Stats &amp; <b>News</b> ...', 'link': 'https://www.nba.com/', 'displayLink': 'www.nba.com', 'snippet': 'Follow the action on NBA scores, schedules, stats, news, teams, and players. Buy tickets or watch the games anywhere with NBA League Pass.', 'htmlSnippet': 'Follow the action on <b>NBA</b> scores, schedules, stats, <b>news</b>, teams, and players. Buy tickets or watch the games anywhere with <b>NBA</b> League Pass.', 'formattedUrl': 'https://www.nba.com/', 'htmlFormattedUrl': 'https://www.<b>nba</b>.com/', 'pagemap': {'cse_thumbnail': [{'src': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR08VgMcNg8oJVHJ5unKjKglIsdFwH6SHykS0FAt6PWE4eSfiXk-MqIEmw&s', 'width': '259', 'height': '194'}], 'metatags': [{'msapplication-tilecolor': '#da532c', 'og:image': 'https://cdn.nba.com/next/fallback.jpg', 'next-head-count': '27', 'og:type': 'website', 'twitter:card': 'summary_large_image', 'twitter:site': '@NBA', 'og:site_name': 'NBA', 'viewport': 'width=device-width,initial-scale=1,minimum-scale=1,maximum-scale=1,user-scalable=no', 'og:title': 'The official site of the NBA for the latest NBA Scores, Stats & News. | NBA.com', 'og:locale': 'en_US', 'og:url': 'https://www.nba.com', 'twitter:image': 'https://cdn.nba.com/logos/nba/fallback/NBA.Com-National-Basketball-Association.png'}], 'cse_image': [{'src': 'https://cdn.nba.com/next/fallback.jpg'}]}}
Title: The official site of the NBA for the latest NBA Scores, Stats & News ...
Link: https://www.nba.com/
--------------------
Item: {'kind': 'customsearch#result', 'title': 'NBA | NBA News, Scores, Highlights, Stats, Standings, and Rumors ...', 'htmlTitle': 'NBA | <b>NBA News</b>, Scores, Highlights, Stats, Standings, and Rumors ...', 'link': 'https://bleacherreport.com/nba', 'displayLink': 'bleacherreport.com', 'snippet': 'Be the best NBA fan you can be with Bleacher Report. Keep up with the latest storylines, expert analysis, highlights, scores and more.', 'htmlSnippet': 'Be the best <b>NBA</b> fan you can be with Bleacher Report. Keep up with the latest storylines, expert analysis, highlights, scores and more.', 'formattedUrl': 'https://bleacherreport.com/nba', 'htmlFormattedUrl': 'https://bleacherreport.com/<b>nba</b>', 'pagemap': {'cse_thumbnail': [{'src': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR7Ed__F_LE0WWjxbtlHVt9a9QJrZqSk_vke50votm4dyb6yY8rp2BJ2DU&s', 'width': '225', 'height': '225'}], 'thumbnail': [{'src': 'https://publish-bleacher-report-gsp-cms.wmsports.io/sites/bleacher-report/files/styles/media_library/todays_newsletter.png'}], 'metatags': [{'p:domain_verify': '0c768466449ebb550411234d6d4ffc30', 'og:image': 'https://publish-bleacher-report-gsp-cms.wmsports.io/sites/bleacher-report/files/styles/media_library/todays_newsletter.png', 'theme-color': '#000', 'og:image:width': '562', 'twitter:card': 'summary_large_image', 'al:android:package': 'com.bleacherreport.android.teamstream', 'al:ipad:app_store_id': '484725748', 'section': 'NBA', 'og:description': 'Be the best NBA fan you can be with Bleacher Report. Keep up with the latest storylines, expert analysis, highlights, scores and more.', 'twitter:creator': '@bleacherreport', 'twitter:image': 'https://publish-bleacher-report-gsp-cms.wmsports.io/sites/bleacher-report/files/styles/media_library/todays_newsletter.png', 'al:iphone:app_name': 'Bleacher Report', 'twitter:site': '@bleacherreport', 'thumbnail': 'https://publish-bleacher-report-gsp-cms.wmsports.io/sites/bleacher-report/files/styles/media_library/todays_newsletter.png', 'og:type': 'website', 'twitter:title': 'NBA | NBA News, Scores, Highlights, Stats, Standings, and Rumors | Bleacher Report', 'og:title': 'NBA | NBA News, Scores, Highlights, Stats, Standings, and Rumors | Bleacher Report', 'og:image:height': '421', 'color-scheme': 'dark light', 'al:iphone:url': 'teamstream://', 'al:ipad:url': 'teamstream://', 'viewport': 'width=device-width, initial-scale=1', 'twitter:description': 'Be the best NBA fan you can be with Bleacher Report. Keep up with the latest storylines, expert analysis, highlights, scores and more.', 'al:iphone:app_store_id': '418075935', 'al:ipad:app_name': 'Bleacher Report', 'og:locale': 'en_US', 'og:url': 'https://bleacherreport.com/nba', 'al:android:app_name': 'Bleacher Report'}], 'cse_image': [{'src': 'https://publish-bleacher-report-gsp-cms.wmsports.io/sites/bleacher-report/files/styles/media_library/todays_newsletter.png'}]}}
Title: NBA | NBA News, Scores, Highlights, Stats, Standings, and Rumors ...
Link: https://bleacherreport.com/nba
--------------------
"""

def main():
    items = google_search(query="NBA News", num=10)
    print (items)

if __name__ == '__main__':
    main()
