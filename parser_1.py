import requests
from bs4 import BeautifulSoup

import requests
from bs4 import BeautifulSoup
import datetime

def generate_urls(start_year, end_year, end_month, end_day):
    urls = []
    current_date = datetime.date(start_year, 1, 1)
    end_date = datetime.date(end_year, end_month, end_day)

    while current_date <= end_date:
        url = f"https://www.europarl.europa.eu/doceo/document/PV-9-{current_date.year}-{current_date.month:02d}-{current_date.day:02d}-RCV_EN.xml"
        urls.append(url)
        current_date += datetime.timedelta(days=1)

    return urls

def parse_xml(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "lxml-xml")

        roll_call_vote_descriptions = soup.find_all("RollCallVote.Description.Text")

        votes = []

        for roll_call_vote_description in roll_call_vote_descriptions:
            vote_name = roll_call_vote_description.text.strip()

            result_for_tag = roll_call_vote_description.find_previous("Result.For")
            result_against_tag = roll_call_vote_description.find_previous("Result.Against")

            if result_for_tag:
                for_identifiers = {}
                for political_group_list in result_for_tag.find_all("Result.PoliticalGroup.List"):
                    identifier = political_group_list["Identifier"]
                    members = political_group_list.find_all("PoliticalGroup.Member.Name")
                    for_identifiers[identifier] = len(members)
            else:
                for_identifiers = {}

            if result_against_tag:
                against_identifiers = {}
                for political_group_list in result_against_tag.find_all("Result.PoliticalGroup.List"):
                    identifier = political_group_list["Identifier"]
                    members = political_group_list.find_all("PoliticalGroup.Member.Name")
                    against_identifiers[identifier] = len(members)
            else:
                against_identifiers = {}

            vote = {
                "name": vote_name,
                "for": for_identifiers,
                "against": against_identifiers,
            }

            votes.append(vote)

        return votes
    else:
        print(f"Failed to parse XML (Status code: {response.status_code}): {url}")
        return []

urls = generate_urls(2019, 2024, 3, 15)

all_votes = []

for url in urls:
    result = parse_xml(url)
    all_votes.extend(result)

print(f"Results: {all_votes}")



url="https://www.europarl.europa.eu/doceo/document/PV-9-2024-03-04-RCV_EN.xml"
def getUrl(url):
    response = requests.get(url)
    return response.status_code

res = getUrl(url)
print(f"Results: {res}")