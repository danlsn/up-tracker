from http import HTTPMethod, HTTPStatus
from typing import Optional

from const import BASE_URL, DEFAULT_PAGE_SIZE, RATE_LIMIT_HEADER
from models import AccountType, OwnershipType, ErrorObject, Account
from pydantic import AnyHttpUrl
import requests


class UpTrackerClient:
    def __init__(self, token: str, base_url: AnyHttpUrl = BASE_URL):
        self.token = token
        self.base_url = base_url

    def list_accounts(
            self,
            account_type: Optional[AccountType],
            ownership_type: Optional[OwnershipType],
            page_size: int = DEFAULT_PAGE_SIZE
    ):
        # Create the request URL
        url = f"{self.base_url}/accounts"

        # Create the request headers
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json"
        }

        # Create the request parameters if any
        params = {
            "page[size]": page_size
        }

        if account_type:
            params["filter[accountType]"] = account_type.value

        if ownership_type:
            params["filter[ownershipType]"] = ownership_type.value

        # Make the request
        response = requests.request(
            HTTPMethod.GET,
            url,
            headers=headers,
            params=params
        )

        # Check the response status code
        if response.status_code != HTTPStatus.OK:
            raise ErrorObject(response)
        res_json = response.json()
        accounts = [Account(**account) for account in res_json["data"]]
        # Return the response as an Account object
        return accounts

    def retrieve_account(self, account_id: str):
        # Create the request URL
        url = f"{self.base_url}/accounts/{account_id}"

        # Create the request headers
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json"
        }

        # Make the request
        response = requests.request(
            HTTPMethod.GET,
            url,
            headers=headers
        )

        # Check the response status code
        if response.status_code != HTTPStatus.OK:
            raise ErrorObject(response)

        # Return the response as an Account object
        return Account(**response.json()["data"])



def main():
    import configparser
    import os

    # Read the config file
    config = configparser.ConfigParser()
    config.read(os.path.join('..', "config.ini"))
    UP_TOKEN = config["DEFAULT"]["UP_TOKEN"]
    # Create an instance of the client
    client = UpTrackerClient(UP_TOKEN)

    # List all accounts
    accounts = client.list_accounts(account_type=AccountType.TRANSACTIONAL, ownership_type=OwnershipType.JOINT)
    for account in accounts:
        acc = client.retrieve_account(account.id)
    # Print the accounts
    ...

if __name__ == "__main__":
    main()

