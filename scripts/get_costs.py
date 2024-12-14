import boto3
import datetime
import pandas as pd

def get_cost_breakdown_by_service(start_date, end_date):
    """
    Get the daily cost breakdown by service for the past 30 days, across all regions.
    
    Parameters:
        start_date (str): The start date in 'YYYY-MM-DD' format.
        end_date (str): The end date in 'YYYY-MM-DD' format.
        
    Returns:
        pd.DataFrame: A DataFrame containing the daily cost breakdown by service.
    """
    try:
        # Create a Cost Explorer client
        ce_client = boto3.client('ce')
        
        # Request parameters for Cost Explorer
        response = ce_client.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='DAILY',
            Metrics=['UnblendedCost'],
            GroupBy=[
                {'Type': 'DIMENSION', 'Key': 'SERVICE'}
            ]
        )
        
        # Extract and process the data
        cost_data = []
        for result in response['ResultsByTime']:
            date = result['TimePeriod']['Start']
            for group in result['Groups']:
                service_name = group['Keys'][0]
                amount = float(group['Metrics']['UnblendedCost']['Amount'])
                cost_data.append({
                    'Date': date,
                    'Service': service_name,
                    'Cost': amount
                })
        
        # Convert to a Pandas DataFrame
        df = pd.DataFrame(cost_data)
        
        # Sort the data for better readability
        df = df.sort_values(by=['Date', 'Service'], ascending=[True, True])
        
        return df
    
    except Exception as e:
        print(f"Error occurred: {e}")
        return None


if __name__ == "__main__":
    # Calculate start and end dates for the last 30 days
    end_date = datetime.date.today().strftime('%Y-%m-%d')
    start_date = (datetime.date.today() - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
    
    print(f"Fetching AWS cost data from {start_date} to {end_date}...")
    
    # Get the cost breakdown
    cost_df = get_cost_breakdown_by_service(start_date, end_date)
    
    if cost_df is not None:
        # Display the dataframe as a table
        print("\nAWS Cost Breakdown (Last 30 Days) - Daily by Service")
        print(cost_df)
        
        # Export to CSV (optional)
        csv_filename = 'aws_cost_breakdown_by_service.csv'
        cost_df.to_csv(csv_filename, index=False)
        print(f"\nData exported to {csv_filename}")
