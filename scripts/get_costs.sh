#!/bin/bash

# Define the end date as today in YYYY-MM-DD format
END_DATE=$(date +%Y-%m-%d)

# Define the start date as 60 days ago in YYYY-MM-DD format
START_DATE=$(date -v-60d +%Y-%m-%d)

# Retrieve cost data from AWS Cost Explorer, filter by region, and sum the costs
aws ce get-cost-and-usage \
    --time-period Start=$START_DATE,End=$END_DATE \
    --granularity DAILY \
    --metrics "UnblendedCost" \
    --group-by Type=DIMENSION,Key=REGION \
    --query 'ResultsByTime[].Groups[].[Keys[0], Metrics.UnblendedCost.Amount]' \
    --output text | \
    awk '{region_cost[$1]+=$2} END {for (region in region_cost) printf "%s: %.2f\n", region, region_cost[region]}' | \
    sort
