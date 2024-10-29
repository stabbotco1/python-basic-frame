#!/bin/bash

# Define the end date as today in YYYY-MM-DD format
END_DATE=$(date +%Y-%m-%d)

# Define the start date as 60 days ago in YYYY-MM-DD format
START_DATE=$(date -v-60d +%Y-%m-%d)

# Retrieve cost data from AWS Cost Explorer, grouped by region and service
aws ce get-cost-and-usage \
    --time-period Start=$START_DATE,End=$END_DATE \
    --granularity DAILY \
    --metrics "UnblendedCost" \
    --group-by Type=DIMENSION,Key=REGION Type=DIMENSION,Key=SERVICE \
    --query 'ResultsByTime[].Groups[].[Keys[0], Keys[1], Metrics.UnblendedCost.Amount]' \
    --output text | \
    awk '{region_service_cost[$1 FS $2]+=$3} END {for (rs in region_service_cost) {split(rs, keys, FS); printf "%s | %s: %.2f\n", keys[1], keys[2], region_service_cost[rs]}}' | \
    sort
