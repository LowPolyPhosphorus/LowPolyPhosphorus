import requests
import re
import sys
from datetime import datetime

token = sys.argv[1]
username = "LowPolyPhosphorus"

# GraphQL query for contribution stats
query = """
query($login: String!) {
  user(login: $login) {
    createdAt
    repositories(ownerAffiliations: OWNER, privacy: PUBLIC) {
      totalCount
    }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      totalRepositoriesWithContributedCommits
    }
  }
}
"""

resp = requests.post(
    "https://api.github.com/graphql",
    json={"query": query, "variables": {"login": username}},
    headers={"Authorization": f"bearer {token}"},
)
data = resp.json()["data"]["user"]

created = datetime.fromisoformat(data["createdAt"].replace("Z", "+00:00"))
years = (datetime.now().astimezone() - created).days // 365

commits = data["contributionsCollection"]["totalCommitContributions"]
prs = data["contributionsCollection"]["totalPullRequestContributions"]
issues = data["contributionsCollection"]["totalIssueContributions"]
repos = data["repositories"]["totalCount"]

line = f"I joined GitHub **{years} years ago**. This year I've pushed ~ **{commits} commits**, opened **{issues} issues**, submitted **{prs} pull requests** across **{repos} public repos**."

# Replace the placeholder in README.md
with open("README.md", "r") as f:
    content = f.read()

content = re.sub(r"<!-- STATS_LINE -->.*", f"<!-- STATS_LINE -->\n{line}", content)

with open("README.md", "w") as f:
    f.write(content)

print(line)
