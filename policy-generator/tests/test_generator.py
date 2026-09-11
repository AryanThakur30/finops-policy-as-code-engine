import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from generate_policies import generate_policy
from analyze_cost import analyze


def test_generator_creates_environment_budgets():
    config = {
        "budgets": {
            "development": {"monthly_limit": 100},
            "staging": {"monthly_limit": 250},
            "production": {"monthly_limit": 500},
        },
        "cost_increase": {
            "enabled": True,
            "max_percentage": 20,
        },
        "resources": {
            "ec2": {
                "enabled": True,
                "max_monthly_cost": 200,
            },
            "ebs": {
                "enabled": True,
                "max_monthly_cost": 100,
            },
        },
    }

    policy = generate_policy(config)

    assert "monthly-budget-development" in policy
    assert "monthly-budget-staging" in policy
    assert "monthly-budget-production" in policy
    assert "cost-increase-guardrail" in policy
    assert "resource-cost-ec2" in policy
    assert "resource-cost-ebs" in policy
    assert "default deny := set()" not in policy


def test_cost_analyzer_enriches_environment():
    data = {
        "totalMonthlyCost": "281.12",
        "pastTotalMonthlyCost": "250.00",
        "projects": [
            {
                "breakdown": {
                    "resources": [
                        {
                            "name": "aws_instance.web",
                            "monthlyCost": "220.00",
                        },
                        {
                            "name": "aws_ebs_volume.data",
                            "monthlyCost": "61.12",
                        },
                    ]
                }
            }
        ],
    }

    enriched, summary = analyze(data, "development")

    assert enriched["environment"] == "development"
    assert summary["current_monthly_cost"] == 281.12
    assert summary["previous_monthly_cost"] == 250.0
    assert round(summary["increase_percentage"], 2) == 12.45
    assert summary["resource_count"] == 2
    assert summary["top_resources"][0]["name"] == "aws_instance.web"
