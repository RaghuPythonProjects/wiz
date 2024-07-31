import os
WIZ_ENV = None  # Set to "gov" or "fedramp", if applicable.
WIZ_CLIENT_ID = 'x624ue26z5bclpg6mocpasj4nz5tkqav5u7fxcngwjqfecjowxhxg'
WIZ_CLIENT_SECRET = 'JwlY8uATOijqLXnkGNAwz4g4RKa9C2sLBZJNCRZaHkbKYmBAbT8o4Ho1LYu3GCf0'
WIZ_API_PROXY = None

PROJECT_ID = "50264363-66ad-5ca2-b622-75df754e5439"
REPORT_ID = "cd9e3418-5927-406c-a06f-3e19dfd80e79"

OUTPUT_PATH = os.path.join('wiz_reports')

QUERY_PATH_RUN_REPORT = os.path.join('wiz_queries', 'query_report_rerun.txt')
QUERY_PATH_RUN_STATUS = os.path.join('wiz_queries', 'query_report_status.txt')
QUERY_PATH_RUN_DOWNLOAD = os.path.join('wiz_queries', 'query_report_download.txt')


