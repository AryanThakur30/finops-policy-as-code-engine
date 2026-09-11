package infracost

import rego.v1


violations(input_data) := [
    violation |
    violation := deny[_] with input as input_data
]


test_development_cost_80_passes if {
    count(violations({
        "environment": "development",
        "totalMonthlyCost": "80.00",
        "pastTotalMonthlyCost": "75.00",
        "projects": []
    })) == 0
}


test_development_cost_99_passes if {
    count(violations({
        "environment": "development",
        "totalMonthlyCost": "99.00",
        "pastTotalMonthlyCost": "95.00",
        "projects": []
    })) == 0
}


test_development_cost_100_fails if {
    result := violations({
        "environment": "development",
        "totalMonthlyCost": "100.00",
        "pastTotalMonthlyCost": "95.00",
        "projects": []
    })

    some violation in result
    violation.policy == "monthly-budget-development"
    violation.failed == true
}


test_development_cost_281_fails if {
    result := violations({
        "environment": "development",
        "totalMonthlyCost": "281.12",
        "pastTotalMonthlyCost": "250.00",
        "projects": []
    })

    some violation in result
    violation.policy == "monthly-budget-development"
    violation.failed == true
}


test_cost_increase_12_5_percent_passes if {
    count(violations({
        "environment": "staging",
        "totalMonthlyCost": "112.50",
        "pastTotalMonthlyCost": "100.00",
        "projects": []
    })) == 0
}


test_cost_increase_30_percent_fails if {
    result := violations({
        "environment": "staging",
        "totalMonthlyCost": "130.00",
        "pastTotalMonthlyCost": "100.00",
        "projects": []
    })

    some violation in result
    violation.policy == "cost-increase-guardrail"
    violation.failed == true
}


test_staging_250_fails if {
    result := violations({
        "environment": "staging",
        "totalMonthlyCost": "250.00",
        "pastTotalMonthlyCost": "200.00",
        "projects": []
    })

    some violation in result
    violation.policy == "monthly-budget-staging"
}


test_production_500_fails if {
    result := violations({
        "environment": "production",
        "totalMonthlyCost": "500.00",
        "pastTotalMonthlyCost": "450.00",
        "projects": []
    })

    some violation in result
    violation.policy == "monthly-budget-production"
}


test_ec2_250_fails if {
    result := violations({
        "environment": "development",
        "totalMonthlyCost": "80.00",
        "pastTotalMonthlyCost": "80.00",
        "projects": [
            {
                "breakdown": {
                    "resources": [
                        {
                            "name": "aws_instance.ec2",
                            "monthlyCost": "250.00"
                        }
                    ]
                }
            }
        ]
    })

    some violation in result
    violation.policy == "resource-cost-ec2"
    violation.failed == true
}


test_ebs_120_fails if {
    result := violations({
        "environment": "development",
        "totalMonthlyCost": "80.00",
        "pastTotalMonthlyCost": "80.00",
        "projects": [
            {
                "breakdown": {
                    "resources": [
                        {
                            "name": "aws_ebs_volume.data",
                            "monthlyCost": "120.00"
                        }
                    ]
                }
            }
        ]
    })

    some violation in result
    violation.policy == "resource-cost-ebs"
    violation.failed == true
}
