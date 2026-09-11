import argparse
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined


REQUIRED_TOP_LEVEL_KEYS = {
    "budgets",
    "cost_increase",
    "resources",
}


def validate_config(config: dict) -> None:
    """Validate the FinOps policy configuration before rendering."""
    if not isinstance(config, dict):
        raise ValueError("Configuration must be a YAML mapping.")

    missing = REQUIRED_TOP_LEVEL_KEYS - config.keys()
    if missing:
        missing_keys = ", ".join(sorted(missing))
        raise ValueError(f"Missing required configuration keys: {missing_keys}")

    budgets = config["budgets"]
    if not isinstance(budgets, dict) or not budgets:
        raise ValueError("'budgets' must be a non-empty mapping.")

    for environment, values in budgets.items():
        if not isinstance(values, dict):
            raise ValueError(
                f"Budget configuration for '{environment}' must be a mapping."
            )

        if "monthly_limit" not in values:
            raise ValueError(f"Budget '{environment}' is missing 'monthly_limit'.")

        limit = values["monthly_limit"]

        if isinstance(limit, bool):
            raise ValueError(f"Budget '{environment}' monthly_limit must be numeric.")

        try:
            limit = float(limit)
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"Budget '{environment}' monthly_limit must be numeric."
            ) from exc

        if limit <= 0:
            raise ValueError(
                f"Budget '{environment}' monthly_limit must be greater than zero."
            )

    cost_increase = config["cost_increase"]

    if not isinstance(cost_increase, dict):
        raise ValueError("'cost_increase' must be a mapping.")

    if "enabled" not in cost_increase:
        raise ValueError("'cost_increase' is missing 'enabled'.")

    if not isinstance(cost_increase["enabled"], bool):
        raise ValueError("'cost_increase.enabled' must be true or false.")

    if cost_increase["enabled"]:
        if "max_percentage" not in cost_increase:
            raise ValueError(
                "'cost_increase' is enabled but 'max_percentage' is missing."
            )

        percentage = cost_increase["max_percentage"]

        if isinstance(percentage, bool):
            raise ValueError("'cost_increase.max_percentage' must be numeric.")

        try:
            percentage = float(percentage)
        except (TypeError, ValueError) as exc:
            raise ValueError("'cost_increase.max_percentage' must be numeric.") from exc

        if percentage < 0:
            raise ValueError("'cost_increase.max_percentage' cannot be negative.")

    resources = config["resources"]

    if not isinstance(resources, dict):
        raise ValueError("'resources' must be a mapping.")

    for resource_type, values in resources.items():
        if not isinstance(values, dict):
            raise ValueError(
                f"Resource configuration for '{resource_type}' must be a mapping."
            )

        if "enabled" not in values:
            raise ValueError(f"Resource '{resource_type}' is missing 'enabled'.")

        if not isinstance(values["enabled"], bool):
            raise ValueError(
                f"Resource '{resource_type}' enabled must be true or false."
            )

        if values["enabled"]:
            if "max_monthly_cost" not in values:
                raise ValueError(
                    f"Resource '{resource_type}' is enabled but "
                    "'max_monthly_cost' is missing."
                )

            limit = values["max_monthly_cost"]

            if isinstance(limit, bool):
                raise ValueError(
                    f"Resource '{resource_type}' max_monthly_cost must be numeric."
                )

            try:
                limit = float(limit)
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    f"Resource '{resource_type}' max_monthly_cost must be numeric."
                ) from exc

            if limit <= 0:
                raise ValueError(
                    f"Resource '{resource_type}' max_monthly_cost "
                    "must be greater than zero."
                )


def load_config(config_path: Path) -> dict:
    """Load and validate a YAML configuration file."""
    try:
        with config_path.open("r", encoding="utf-8") as file:
            config = yaml.safe_load(file)
    except yaml.YAMLError as exc:
        raise ValueError(f"Invalid YAML configuration: {exc}") from exc
    except OSError as exc:
        raise ValueError(
            f"Unable to read configuration file '{config_path}': {exc}"
        ) from exc

    validate_config(config)
    return config


def generate_policy(config: dict) -> str:
    """Render the FinOps configuration into Rego."""
    validate_config(config)

    template_dir = Path(__file__).resolve().parents[1] / "templates"

    environment = Environment(
        loader=FileSystemLoader(template_dir),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )

    template = environment.get_template("cost.rego.j2")

    return template.render(
        budgets=config["budgets"],
        cost_increase=config["cost_increase"],
        resources=config["resources"],
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate OPA/Rego FinOps policies from YAML configuration."
    )

    parser.add_argument(
        "--config",
        required=True,
        help="Path to the FinOps YAML configuration.",
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Output path for the generated Rego policy.",
    )

    args = parser.parse_args()

    config_path = Path(args.config)
    output_path = Path(args.output)

    config = load_config(config_path)
    policy = generate_policy(config)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(policy, encoding="utf-8")

    print(f"Generated policy: {output_path}")


if __name__ == "__main__":
    main()
