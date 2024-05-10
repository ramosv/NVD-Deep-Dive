import json
import os
from datetime import datetime


def categorize_cve_by_type(cve_description, clientSearch):
    parts = clientSearch.split(" ")

    for part in parts:
        cve_description = cve_description.lower()
        if part not in cve_description:
            return None

    return True


def load_categorized_cve_data(directory, clientSearch):
    cve_details = []
    for filename in os.listdir(directory):

        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            with open(file_path, "r") as file:
                data = json.load(file)
                for item in data:
                    cve_id = item["cve"]["id"]
                    for desc in item["cve"]["descriptions"]:
                        if desc["lang"] == "en":

                            if (
                                categorize_cve_by_type(desc["value"], clientSearch)
                                == None
                            ):
                                continue

                            # pub_date = datetime.strptime(
                            #     item["cve"]["published"], "%Y-%m-%dT%H:%M:%S.%f"
                            # )
                            pub_date = item["cve"]["published"]
                            cve_status = item["cve"]["vulnStatus"]

                            if "cvssMetricV31" in item["cve"]["metrics"]:
                                cve_metrics = item["cve"]["metrics"]["cvssMetricV31"][0]

                                exploitability_score = cve_metrics.get(
                                    "exploitabilityScore"
                                )
                                impact_score = cve_metrics.get("impactScore")
                                attack_vector = cve_metrics["cvssData"].get(
                                    "attackVector"
                                )
                                base_severity = cve_metrics["cvssData"].get(
                                    "baseSeverity"
                                )
                            elif "cvssMetricV30" in item["cve"]["metrics"]:
                                cve_metrics = item["cve"]["metrics"]["cvssMetricV30"][0]

                                exploitability_score = cve_metrics.get(
                                    "exploitabilityScore"
                                )
                                impact_score = cve_metrics.get("impactScore")
                                attack_vector = cve_metrics["cvssData"].get(
                                    "attackVector"
                                )
                                base_severity = cve_metrics["cvssData"].get(
                                    "baseSeverity"
                                )
                            elif "cvssMetricV2" in item["cve"]["metrics"]:
                                cve_metrics = item["cve"]["metrics"]["cvssMetricV2"][0]

                                exploitability_score = cve_metrics.get(
                                    "exploitabilityScore"
                                )
                                impact_score = cve_metrics.get("impactScore")
                                attack_vector = cve_metrics["cvssData"].get(
                                    "accessVector"
                                )
                                base_severity = cve_metrics.get("baseSeverity")
                            else:
                                cve_metrics = None
                                exploitability_score = None
                                impact_score = None
                                attack_vector = None
                                base_severity = None

                            cve_details.append(
                                {
                                    "id": cve_id,
                                    "description": desc["value"],
                                    "pub_date": pub_date,
                                    "cve_status": cve_status,
                                    "exploitability_score": exploitability_score,
                                    "impact_score": impact_score,
                                    "attack_vector": attack_vector,
                                    "base_severity": base_severity,
                                }
                            )

    return cve_details


def save_cve_data_by_type_to_json(cve_details, output_filename):
    cve_by_type = {}

    for cve_type, (cve_id, pub_date) in cve_details:
        if cve_type not in cve_by_type:
            cve_by_type[cve_type] = []
        cve_by_type[cve_type].append(
            {"id": cve_id, "published_date": pub_date.isoformat()}
        )

    with open(output_filename, "w") as file:
        json.dump(cve_by_type, file, indent=4)


def analyze_search_string(clientSearch):
    directory = "all_data"
    cve_details = load_categorized_cve_data(directory, clientSearch)

    return cve_details
