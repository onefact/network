"""
Classes / Functions for loading CMS Ownership Data

TODO:
- Load multiple time slice
- Check for new data availability (populate DATASET_TO_LOAD)
"""

import sqlite3
from dataclasses import dataclass
import requests
import pandas as pd


@dataclass
class CMSDataset:
    title: str
    target_table: str
    distro: dict = None

DATASETS_TO_LOAD = [
    # Owners
    CMSDataset('Hospital All Owners', 'hospital_all_owners'),
    CMSDataset('Home Health Agency All Owners', 'hha_all_owners'),
    CMSDataset('Hospice All Owners', 'hospice_all_owners'),
    CMSDataset('Skilled Nursing Facility All Owners', 'snf_all_owners'),
    CMSDataset('Federally Qualified Health Center All Owners', 'fqhc_all_owners'),
    CMSDataset('Rural Health Clinic All Owners', 'rhc_all_owners'),

    # Enrollments
    CMSDataset('Hospital Enrollments', 'hospital_enrollments'),
    CMSDataset('Home Health Agency Enrollments', 'hha_enrollments'),
    CMSDataset('Hospice Enrollments', 'hospice_enrollments'),
    CMSDataset('Skilled Nursing Facility Enrollments', 'snf_enrollments'),
    CMSDataset('Federally Qualified Health Center Enrollments', 'fqhc_enrollments'),
    CMSDataset('Rural Health Clinic Enrollments', 'rhc_enrollments')
]

# Core Big Dawgs
class CMSDataAPILoader():
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.dataset_obj = None

    def retrieve_dataset(self, dataset_obj: CMSDataset):
        """
        Example in Python
        Paginates through the Opt Out Affidavits data
        https://data.cms.gov/provider-characteristics/medicare-provider-supplierenrollment/opt-out-affidavits
        """
        self.dataset_obj = dataset_obj
        url = "https://data.cms.gov/data.json"
        response = requests.request("GET", url)
        response = response.json()
        dataset = response['dataset']
        for set in dataset:
            if dataset_obj.title == set['title']:
                for distro in set['distribution']:
                    if 'format' in distro.keys() and 'description' in distro.keys():
                        if distro['format'] == "API" and distro['description'] == "latest":
                            dataset_obj.distro = distro
                            break

        stats_endpoint = dataset_obj.distro["accessURL"] + "/stats"
        stats_response = requests.request("GET", stats_endpoint)
        stats_response = stats_response.json()
        total_rows = stats_response['total_rows']

        if self.check_table_exists():
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT COUNT(1) FROM {dataset_obj.target_table} WHERE distro_title = '{dataset_obj.distro['title']}'")
            rows = cursor.fetchall()
            if len(rows) > 0 and rows[0][0] == total_rows:
                print(f"Skipping, {dataset_obj.distro['title']} already loaded")
                return None
            elif rows[0][0] != total_rows:
                print(f"Data mismatch, reloading {dataset_obj.distro['title']}")
                self.conn.execute(f"DELETE FROM {dataset_obj.target_table} WHERE distro_title = '{dataset_obj.distro['title']}'")

        i = 0
        loaded_count = 0
        while i < total_rows:
            size = 5000
            offset_url = f"{dataset_obj.distro["accessURL"]}?size={size}&offset={i}"
            offset_response = requests.request("GET", offset_url)
            df = self.prepare_data(pd.DataFrame(offset_response.json()))
            df.to_sql(dataset_obj.target_table, self.conn, if_exists='append', index=False)
            loaded_count += df.shape[0]
            i = i+size
        assert loaded_count == total_rows, "Not all records were loaded"
        print("Loaded ", loaded_count, " records")

    def prepare_data(self, df: pd.DataFrame):
        df.replace("", pd.NA, inplace=True)
        df.replace("N/A", pd.NA, inplace=True)
        df.rename(columns=lambda x: x.lower().replace(' ', '_').replace('-', ''), inplace=True)
        df['distro_access_url'] = self.dataset_obj.distro['accessURL']
        df['distro_title'] = self.dataset_obj.distro['title']
        df['distro_modified'] = self.dataset_obj.distro['modified']
        df['_load_ts'] = pd.Timestamp.now()
        return df

    def check_table_exists(self):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.dataset_obj.target_table}'")
        return cursor.fetchone()
        
    def load_all_datasets(self):
        for dataset in DATASETS_TO_LOAD:
            print("Processing dataset: ", dataset.title)
            self.retrieve_dataset(dataset)

if __name__ == '__main__':
    loader = CMSDataAPILoader('data/raw/cms_data_api_raw.db')
    loader.load_all_datasets()
