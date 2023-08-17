holdout_teams = ["1205289423803560"]

workspace_gid = "11915891072957"

import os
import sys
from .asanaUtils.client import asana_client


def teamupdate():
    """a function to mark all teams as private in Asana"""

    # get access token
    token = input("paste your Service Account token: ")

    # test the token to ensure it works
    user = asana_client(**{"method": "GET", "url": "/users/me", "token": token})
    if not user:
        sys.exit("invalid account token")

    confirmation = input("proceed? (Y/n)")

    if confirmation.lower() == "n":
        sys.exit("goodbye!")

    # get all teams

    has_more = True
    teams = []
    path = f"/teams?workspace={workspace_gid}&limit=10"
    while has_more == True:
        team_data = asana_client(
            **{
                "method": "GET",
                "url": path,
                "token": token,
            }
        )
        teams += team_data["data"]
        next_page = team_data["next_page"]
        if next_page:
            path = next_page["path"]
        else:
            has_more = False

    # for each team
    for team in teams:
        if team["gid"] not in holdout_teams:
            data = {
                "data": {"visibility": "secret", "name": f'ARCHIVE - {team["name"]}'}
            }
            asana_client(
                **{
                    "method": "PUT",
                    "url": f'/teams/{team["gid"]}',
                    "data": data,
                    "token": token,
                }
            )
            print(f'team {team["name"]} is now private')

    print(f"Complete!")

    return


## main function which is targeted by the CLI command
def main():
    """runs the team update function asynchronously"""

    try:
        teamupdate()
    except KeyboardInterrupt:
        print("\nInterrupted - goodbye")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


## if this file is run directly via Python:
if __name__ == "__main__":
    try:
        teamupdate()
    except KeyboardInterrupt:
        print("\nInterrupted - goodbye")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
