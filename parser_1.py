import requests
from bs4 import BeautifulSoup

def parse_xml():
    url = "https://www.europarl.europa.eu/doceo/document/PV-9-2024-03-11-RCV_EN.xml"
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
        print("Failed to parse XML.")
        return None

result = parse_xml()
print(f"Results: {result}")
