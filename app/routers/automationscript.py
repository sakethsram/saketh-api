import json

def po_to_json(file_path):
    """
    Simulates the processing of a file and returns sample JSON data.
    Args:
        file_path (str): Path to the file.
    Returns:
        dict: Sample JSON data.
    """
    # Sample JSON data (replace this with the actual logic later)
    sample_json_data = {
        "PAN NO": "56456456135154534",
        "Place of Delivery": "bangalore",
        "Order Date": "2025-01-17",
        "Order ID": "123-4567890-1234567"
    }
    return sample_json_data

# This block allows the script to work as a standalone program
if __name__ == "__main__":
    import sys
    file_path = sys.argv[1]  # Accept file path as a command-line argument

    # Get sample data for now
    data = process_file(file_path)
    
    # Print the JSON response (important for subprocess communication)
    print(json.dumps(data, ensure_ascii=False))
