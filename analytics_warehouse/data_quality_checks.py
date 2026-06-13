import json
from pathlib import Path

from analytics_warehouse.build_warehouse_reports import TABLES, load_data


def run_quality_checks():
    data = load_data()

    null_violations = []
    schema_violations = []
    freshness_violations = []

    for table, required_cols in TABLES.items():
        rows = data.get(table, [])

        for idx, row in enumerate(rows):
            missing_cols = [col for col in required_cols if col not in row]
            if missing_cols:
                schema_violations.append({
                    "table": table,
                    "row_index": idx,
                    "missing_columns": missing_cols
                })

            for col in required_cols:
                if row.get(col) in (None, ""):
                    null_violations.append({
                        "table": table,
                        "row_index": idx,
                        "column": col
                    })

            if "created_at" in required_cols and row.get("created_at", "") < "2026-05-01":
                freshness_violations.append({
                    "table": table,
                    "row_index": idx,
                    "created_at": row.get("created_at")
                })

    result = {
        "status": "pass" if not null_violations and not schema_violations and not freshness_violations else "fail",
        "null_violations": null_violations,
        "schema_violations": schema_violations,
        "freshness_violations": freshness_violations,
        "tables_checked": sorted(TABLES.keys())
    }

    Path("analytics_warehouse/reports/data_quality_report.json").write_text(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    print(json.dumps(run_quality_checks(), indent=2))
