"""Parse Synthea FHIR bundle JSON files into per-resource-type NDJSON files.

ELT boundary: this only splits bundles by resource type and writes the raw
resource JSON back out untouched (plus a couple of grain/join fields
pulled to the top level for convenience). All real transformation
(type casting, unnesting, business logic) happens later in dbt.

Cloud-agnostic on purpose — the output here is what a later, cloud-specific
upload step (GCS + BigQuery load) will consume.
"""

import argparse
import json
from pathlib import Path

# Maps FHIR resourceType -> raw table name, matching docs/data_dictionary.xlsx "Raw Tables" tab.
RESOURCE_TABLE_MAP = {
    "Patient": "raw_patient",
    "Condition": "raw_condition",
    "Encounter": "raw_encounter",
    "Observation": "raw_observation",
    "Claim": "raw_claim",
    "ExplanationOfBenefit": "raw_eob",
    "Coverage": "raw_coverage",
}


def iter_bundle_files(input_dir: Path):
    for path in sorted(input_dir.glob("*.json")):
        if path.name.startswith(("hospitalInformation", "practitionerInformation")):
            continue
        yield path


def _record(resource: dict, source_file: str) -> dict:
    return {
        "id": resource.get("id"),
        "source_file": source_file,
        "resource": resource,
    }


def extract_records(bundle_path: Path):
    """Yield (table_name, record) for each resource in a bundle we care about.

    Some resource types (e.g. Coverage) are not top-level bundle entries —
    Synthea nests them inside another resource's `contained[]` array (e.g.
    a Coverage contained within its ExplanationOfBenefit). Both places are
    checked so nothing is silently dropped.
    """
    with bundle_path.open(encoding="utf-8") as f:
        bundle = json.load(f)

    for entry in bundle.get("entry", []):
        resource = entry.get("resource", {})
        resource_type = resource.get("resourceType")
        table = RESOURCE_TABLE_MAP.get(resource_type)
        if table is not None:
            yield table, _record(resource, bundle_path.name)

        for contained in resource.get("contained", []):
            contained_table = RESOURCE_TABLE_MAP.get(contained.get("resourceType"))
            if contained_table is not None:
                yield contained_table, _record(contained, bundle_path.name)


def parse_bundles(input_dir: Path, output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    writers = {}
    counts = {table: 0 for table in RESOURCE_TABLE_MAP.values()}

    try:
        for bundle_path in iter_bundle_files(input_dir):
            for table, record in extract_records(bundle_path):
                if table not in writers:
                    writers[table] = (output_dir / f"{table}.ndjson").open("w", encoding="utf-8")
                writers[table].write(json.dumps(record) + "\n")
                counts[table] += 1
    finally:
        for f in writers.values():
            f.close()

    return counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default="raw_data_sample", help="Directory of bundle JSON files")
    parser.add_argument("--output", default="raw_data/staged", help="Directory to write NDJSON output")
    args = parser.parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output)

    counts = parse_bundles(input_dir, output_dir)

    print(f"Parsed bundles from {input_dir} -> {output_dir}")
    for table, count in counts.items():
        print(f"  {table}: {count} records")


if __name__ == "__main__":
    main()