import subprocess
import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from generate_policies import generate_policy, load_config, validate_config
from analyze_cost import analyze


VALID_CONFIG = {
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


def test_generator_creates_environment_budgets():
    policy = generate_policy(VALID_CONFIG)

    assert "monthly-budget-development" in policy
    assert "monthly-budget-staging" in policy
    assert "monthly-budget-production" in policy
    assert "cost-increase-guardrail" in policy
    assert "resource-cost-ec2" in policy
    assert "resource-cost-ebs" in policy
    assert "default deny := set()" not in policy


def test_generator_ignores_disabled_resource():
    config = VALID_CONFIG.copy()
    config["resources"] = {
        "ec2": {
            "enabled": False,
            "max_monthly_cost": 200,
        }
    }

    policy = generate_policy(config)

    assert "resource-cost-ec2" not in policy


def test_generator_disables_cost_increase_policy():
    config = VALID_CONFIG.copy()
    config["cost_increase"] = {
        "enabled": False,
        "max_percentage": 20,
    }

    policy = generate_policy(config)

    assert "cost-increase-guardrail" not in policy


def test_missing_required_config_key():
    config = VALID_CONFIG.copy()
    del config["resources"]

    with pytest.raises(ValueError, match="Missing required configuration keys"):
        validate_config(config)


def test_missing_budget_limit():
    config = {
        **VALID_CONFIG,
        "budgets": {
            "development": {}
        },
    }

    with pytest.raises(ValueError, match="monthly_limit"):
        validate_config(config)


def test_invalid_budget_value():
    config = {
        **VALID_CONFIG,
        "budgets": {
            "development": {
                "monthly_limit": "not-a-number"
            }
        },
    }

    with pytest.raises(ValueError, match="must be numeric"):
        validate_config(config)


def test_malformed_yaml(tmp_path):
    config_path = tmp_path / "invalid.yml"
    config_path.write_text(
        "budgets:\n  development:\n    monthly_limit: [100\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Invalid YAML"):
        load_config(config_path)


def test_cli_generates_policy(tmp_path):
    config_path = tmp_path / "policies.yml"
    output_path = tmp_path / "generated" / "cost.rego"

    config_path.write_text(
        yaml.safe_dump(VALID_CONFIG),
        encoding="utf-8",
    )

    generator = Path(__file__).resolve().parents[1] / "src" / "generate_policies.py"

    result = subprocess.run(
        [
            sys.executable,
            str(generator),
            "--config",
            str(config_path),
            "--output",
            str(output_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert output_path.exists()
    assert "Generated policy:" in result.stdout

    policy = output_path.read_text(encoding="utf-8")
    assert "monthly-budget-development" in policy


def test_cli_requires_arguments():
    generator = Path(__file__).resolve().parents[1] / "src" / "generate_policies.py"

    result = subprocess.run(
        [sys.executable, str(generator)],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode != 0
    assert "--config" in result.stderr
    assert "--output" in result.stderr


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
