import json
import os
import requests
from datetime import datetime
from urllib.parse import urlparse
from wiz_sdk import WizAPIClient
from utilities.logger_master import logger, log_function_entry_exit
from utilities import wiz_config


@log_function_entry_exit(logger)
class WizMaster:
    def __init__(self):
        logger.info("WizReport - Start Wiz Client")
        self.client = WizAPIClient(conf={
            'wiz_env': wiz_config.WIZ_ENV,
            'wiz_client_id': wiz_config.WIZ_CLIENT_ID,
            'wiz_client_secret': wiz_config.WIZ_CLIENT_SECRET,
            'wiz_api_proxy': wiz_config.WIZ_API_PROXY
        })

    def create_dated_folder(self):
        current_date = datetime.now().strftime('%Y%m%d')
        dated_folder_path = os.path.join(wiz_config.OUTPUT_PATH, current_date)
        os.makedirs(dated_folder_path, exist_ok=True)
        logger.info(f"folder_path - {dated_folder_path}")
        return dated_folder_path

    def load_query(self, query_file):
        with open(query_file, 'r') as file:
            return file.read()

    def report_rerun(self):
        print(datetime.now(), f"QUERY_PATH_RUN_REPORT - {wiz_config.QUERY_PATH_RUN_REPORT}")
        print(datetime.now(), f"REPORT_ID: {wiz_config.REPORT_ID}")
        logger.info(f"QUERY_PATH_RUN_REPORT - {wiz_config.QUERY_PATH_RUN_REPORT}, REPORT_ID: {wiz_config.REPORT_ID}")
        self.query = self.load_query(wiz_config.QUERY_PATH_RUN_REPORT)
        self.variables = {
                "reportId": wiz_config.REPORT_ID
            }
        results = self.client.query(self.query, self.variables)
        logger.info(f"Wiz response : {results}")
        print(datetime.now(), f"results: {results}")

    def report_status(self):

        print(datetime.now(), f"QUERY_PATH_RUN_STATUS - {wiz_config.QUERY_PATH_RUN_STATUS}")
        logger.info(f"QUERY_PATH_RUN_STATUS - {wiz_config.QUERY_PATH_RUN_STATUS}")
        self.query = self.load_query(wiz_config.QUERY_PATH_RUN_STATUS)
        self.variables = {
                          "first": 20,
                          "filterBy": {
                            "search": "rk",
                            "scheduled": True
                          }
                        }

        results = self.client.query(self.query, self.variables)
        logger.info(f"QUERY_PATH_RUN_STATUS - results {results}")
        nodes = results.data.get('reports', {}).get('nodes', [])
        status = self.get_report_status(nodes)
        logger.info(f"get_report_status - status: {status}")
        print(datetime.now(), f"get_report_status - status: {status}")
        return status

    def get_report_status(self, nodes):
        print(datetime.now(), f"get_report_status - for report id {wiz_config.REPORT_ID}")
        logger.info(f"get_report_status - for report id {wiz_config.REPORT_ID}")
        for node in nodes:
            if node['id'] == wiz_config.REPORT_ID:
                return node.get('lastRun', {}).get('status', 'Status not available')
        return 'Report not found'

    def report_download_url(self):
        print(datetime.now(), f"QUERY_PATH_RUN_DOWNLOAD - {wiz_config.QUERY_PATH_RUN_DOWNLOAD}")
        print(datetime.now(), f"REPORT_ID: {wiz_config.REPORT_ID}")
        logger.info(f"QUERY_PATH_RUN_DOWNLOAD - {wiz_config.QUERY_PATH_RUN_DOWNLOAD}, REPORT_ID: {wiz_config.REPORT_ID}")

        self.query = self.load_query(wiz_config.QUERY_PATH_RUN_DOWNLOAD)
        self.variables = {"reportId": wiz_config.REPORT_ID}

        results = self.client.query(self.query, self.variables)
        logger.info(f"Wiz response : {results}")

        url = results.data.get('report', {}).get('lastRun', {}).get('url', None)
        if url:
            print(datetime.now(), f"url: {url}")
            self.download_file(url)
        else:
            logger.info(f"No URL to download")
            print(datetime.now(), f"No URL to download")

    def download_file(self, url):
        self.output_path = self.create_dated_folder()
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        save_file_path = os.path.join(self.output_path, filename)
        print(datetime.now(), f"download_file - url {url}")
        logger.info(f"download_file - url {url}")
        response = requests.get(url, stream=True)
        response.raise_for_status()

        logger.info(f"save_file : {save_file_path}")
        print(datetime.now(), f"save_file : {save_file_path}")
        with open(save_file_path, 'wb') as file:
            chunk_count = 0
            for chunk in response.iter_content(chunk_size=8192):
                chunk_count += 1
                if chunk:
                    file.write(chunk)
                    logger.info(f"save_file - chunk_count: {chunk_count}")
        print(datetime.now(), f"File downloaded successfully and saved as '{save_file_path}'")


