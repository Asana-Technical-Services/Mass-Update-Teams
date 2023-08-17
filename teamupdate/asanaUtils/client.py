import json
import requests as r
import time


def asana_client(method, url, **kwargs):
    backoff_seconds = 0.500
    retryError = 429
    attempt = 0

    base_url = "https://app.asana.com/api/1.0"
    full_url = base_url + url

    if "data" in kwargs:
        data = json.dumps(kwargs["data"])
    else:
        data = {}

    if "params" in kwargs:
        params = kwargs["params"]
    else:
        params = {}

    headers = {"Authorization": "Bearer " + kwargs["token"]}

    result = False

    while ((retryError == 429) or (retryError == 500)) and (attempt < 10):
        # pause execution before trying again

        if attempt == 6:
            print("hitting rate limits. slowing down calls...")

        if attempt == 8:
            print("thanks for your patience. still slow.")

        try:
            response = r.request(
                method, url=full_url, data=data, params=params, headers=headers
            )
            retryError = response.status_code

            if retryError >= 400:
                if (response.status_code != 429) and (response.status_code != 500):
                    error_json = response.json()
                    print(error_json["errors"][0]["message"])
                    print("HTTP Error: ", response.status_code)
                    return False
            else:
                response_content = response.json()
                return response_content

        except r.HTTPError as e:
            if (response.status_code != 429) and (response.status_code != 500):
                print("HTTP Error: ", response.status_code)
                error_json = response.json()
                print(error_json["errors"][0]["message"])
                return False

        # Exponential backoff in seconds = constant * attempt^2
        retry_time = backoff_seconds * attempt * attempt

        print(
            f"The script is hitting rate limits (too many calls/minute). Waiting for {retry_time} seconds before continuing"
        )
        time.sleep(retry_time)
        attempt += 1

    if attempt >= 10:
        print("too many requests hit rate limits - timed out")

    return result
