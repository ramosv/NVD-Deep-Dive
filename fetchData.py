import requests
import json
import time
import os


def fetch_and_save_cves(api_key):
    base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0/"
    headers = {"X-Api-Key": api_key}
    params = {"resultsPerPage": 2000, "startIndex": 0}
    all_cves = []
    file_count = 0
    cve_count = 0

    output_folder = "all_data"

    while True:
        response = requests.get(base_url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            all_cves.extend(data.get("vulnerabilities", []))
            cve_count += len(data.get("vulnerabilities", []))
            print(f"Fetched {cve_count} of {data['totalResults']} total CVEs...")

            if len(all_cves) >= 10000:
                file_name = os.path.join(
                    output_folder, f"nvd_cves_part_{file_count + 1}.json"
                )
                with open(file_name, "w") as json_file:
                    json.dump(all_cves, json_file, indent=4)
                print(f"Data saved to {file_name}.")
                file_count += 1
                all_cves = []

            if params["startIndex"] + params["resultsPerPage"] >= data["totalResults"]:
                if all_cves:
                    file_name = os.path.join(
                        output_folder, f"nvd_cves_part_{file_count + 1}.json"
                    )
                    with open(file_name, "w") as json_file:
                        json.dump(all_cves, json_file, indent=4)
                    print(f"Data saved to {file_name}.")
                break

            params["startIndex"] += params["resultsPerPage"]
            time.sleep(6)
        else:
            print(
                f"Failed to fetch data. Status code: {response.status_code}, Detail: {response.text}"
            )
            break


api_key = "dd12d0e6-5f9a-4503-9828-b73989cdf27b"

fetch_and_save_cves(api_key)
