import boto3
import datetime
import pandas as pd
import argparse

# get_cost_and_usage_with_resources API ref: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/get_cost_and_usage_with_resources.html

def get_cost_breakdown(start_date, end_date, by_day=False, by_region=False):
    """
    Get the cost breakdown by service, optionally by day and region.
    
    Parameters:
        start_date (str): The start date in 'YYYY-MM-DD' format.
        end_date (str): The end date in 'YYYY-MM-DD' format.
        by_day (bool): Whether to show a breakdown by day.
        by_region (bool): Whether to show a breakdown by region.
        
    Returns:
        pd.DataFrame: A DataFrame containing the cost breakdown.
    """
    try:
        # Create a Cost Explorer client
        ce_client = boto3.client('ce')
        
        # Configure GroupBy options
        group_by = [{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
        if by_region:
            group_by.insert(0, {'Type': 'DIMENSION', 'Key': 'REGION'})
        
        # Request parameters for Cost Explorer
        response = ce_client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='DAILY' if by_day else 'MONTHLY',
            Metrics=['UnblendedCost'],
            GroupBy=group_by
        )
        
        # Extract and process the data
        cost_data = []
        for result in response['ResultsByTime']:
            date = result['TimePeriod']['Start']
            for group in result['Groups']:
                if by_region:
                    region_name = group['Keys'][0]
                    service_name = group['Keys'][1] if len(group['Keys']) > 1 else 'N/A'
                else:
                    region_name = 'All Regions'
                    service_name = group['Keys'][0]
                    
                amount = float(group['Metrics']['UnblendedCost']['Amount'])
                
                cost_data.append({
                    'Region': region_name,
                    'Service': service_name,
                    'Date': date,
                    'Cost': amount
                })
        
        # Convert to a Pandas DataFrame
        df = pd.DataFrame(cost_data)
        
        # Sort the data for better readability (Region -> Service -> Date)
        df = df.sort_values(by=['Region', 'Service', 'Date'], ascending=[True, True, True])
        
        return df
    
    except Exception as e:
        print(f"Error occurred: {e}")
        return None


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='AWS Cost Breakdown Script')
    parser.add_argument('--days-back', type=int, default=30, help='Number of days to go back for the cost report (default: 30)')
    parser.add_argument('--by-day', action='store_true', help='Provide breakdown by day if set')
    parser.add_argument('--by-region', action='store_true', help='Provide breakdown by region if set')
    args = parser.parse_args()
    
    # Calculate start and end dates for the given number of days
    end_date = datetime.date.today().strftime('%Y-%m-%d')
    start_date = (datetime.date.today() - datetime.timedelta(days=args.days_back)).strftime('%Y-%m-%d')
    
    print(f"Fetching AWS cost data from {start_date} to {end_date}...")
    if args.by_day:
        print("Including daily breakdown.")
    if args.by_region:
        print("Including regional breakdown.")
    
    # Get the cost breakdown
    cost_df = get_cost_breakdown(start_date, end_date, by_day=args.by_day, by_region=args.by_region)
    
    if cost_df is not None:
        # Display the dataframe as a table
        print("\nAWS Cost Breakdown")
        print(cost_df)
        
        # Export to CSV (optional)
        csv_filename = 'aws_cost_breakdown.csv'
        cost_df.to_csv(csv_filename, index=False)
        print(f"\nData exported to {csv_filename}")
