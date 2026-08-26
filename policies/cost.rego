package infracost

deny contains out if {
    maxCost := 100.0
    actualCost := to_number(input.totalMonthlyCost)

    msg := sprintf(
        "Monthly infrastructure cost must be less than $%.2f (actual cost is $%.2f)",
        [maxCost, actualCost],
    )

    out := {
        "msg": msg,
        "failed": actualCost >= maxCost,
    }
}