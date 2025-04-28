# preprocessor/data_formatter.py
import csv
import json

class DataFormatter:
    def __init__(self, data):
        self.data = data
    
    def to_stream(self):
        """Convert data to a standard format stream"""
        if isinstance(self.data, dict):
            return json.dumps(self.data)
        else:
            return ",".join(map(str, self.data))
    
    def to_csv(self, output_path):
        """Save data to CSV file"""
        if isinstance(self.data, dict):
            with open(output_path, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=self.data.keys())
                writer.writeheader()
                writer.writerow(self.data)
        else:
            with open(output_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(self.data)