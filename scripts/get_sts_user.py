import boto3

def get_caller_identity():
    """
    Uses boto3 to get the caller identity equivalent to 'aws sts get-caller-identity'
    """
    try:
        # Create a session and STS client
        sts_client = boto3.client('sts')
        
        # Call get_caller_identity
        response = sts_client.get_caller_identity()
        
        print("Caller Identity Information:")
        print(f"Account: {response['Account']}")
        print(f"UserId: {response['UserId']}")
        print(f"ARN: {response['Arn']}")
        
        return response
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

if __name__ == "__main__":
    identity = get_caller_identity()
