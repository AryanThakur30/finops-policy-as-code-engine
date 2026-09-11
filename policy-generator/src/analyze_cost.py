import argparse
import json
from pathlib import Path


def money(value):
    return float(value or 0)


def analyze(data, environment):
    current = money(data.get("totalMonthlyCost"))
    previous = money(data.get("pastTotalMonthlyCost"))

    if previous > 0:
        increase_pct = ((current - previous) / previous) * 100
    else:
        increase_pct = 0.0

    resources = []

    for project in data.get("projects", []):
        breakdown = project.get("breakdown", {})
        for resource in breakdown.get("resources", []):
            resources.append(
                {
                    "name": resource.get("name", "unknown"),
                    "monthly_cost": money(resource.get("monthlyCost")),
                }
            )

    resources.sort(key=lambda item: item["monthly_cost"], reverse=True)

    enriched = dict(data)
    enriched["environment"] = environment

    return enriched, {
        "environment": environment,
        "current_monthly_cost": current,
        "previous_monthly_cost": previous,
        "monthly_cost_delta": current - previous,
        "increase_percentage": increase_pct,
        "resource_count": len(resources),
        "top_resources": resources[:5],
    }


def write_report(report_path, summary):
    lines = [
        "# FinOps Cost Analysis",
        "",
        f"- Environment: `{summary['environment']}`",
        f"- Current monthly cost: `${summary['current_monthly_cost']:.2f}`",
        f"- Previous monthly cost: `${summary['previous_monthly_cost']:.2f}`",
        f"- Monthly delta: `${summary['monthly_cost_delta']:.2f}`",
        f"- Cost increase: `{summary['increase_percentage']:.2f}%`",
        f"- Resource count: `{summary['resource_count']}`",
        "",
        "## Top Resources",
        "",
        "| Resource | Monthly Cost |",
        "|---|---:|",
    ]

    for resource in summary["top_resources"]:
        lines.append(f"| `{resource['name']}` | `${resource['monthly_cost']:.2f}` |")

    Path(report_path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(
        description="Analyze and enrich an Infracost JSON result."
    )
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--environment", required=True)

    args = parser.parse_args()

    input_data = json.loads(Path(args.input).read_text(encoding="utf-8"))

    enriched, summary = analyze(input_data, args.environment)

    Path(args.output).write_text(
        json.dumps(enriched, indent=2),
        encoding="utf-8",
    )

    write_report(args.report, summary)

    print("FinOps Cost Analysis")
    print(f"Environment: {summary['environment']}")
    print(f"Current monthly cost: ${summary['current_monthly_cost']:.2f}")
    print(f"Previous monthly cost: ${summary['previous_monthly_cost']:.2f}")
    print(f"Monthly delta: ${summary['monthly_cost_delta']:.2f}")
    print(f"Cost increase: {summary['increase_percentage']:.2f}%")
    print(f"Resources analyzed: {summary['resource_count']}")


if __name__ == "__main__":
    main()
