# script to wait for NZ case numbers for today to appear on MOH official dataset.

import pandas as pd
import time
from datetime import datetime
import urllib

# HTTP headers to emulate curl
curl_headers = {'user-agent': 'curl/7.64.1'}

def moh_updated_today():
    """Check if NZ MOH dataset for today exists yet, return True if it does"""
    today = datetime.now().strftime('%Y-%m-%d')
    URL = f"https://www.health.govt.nz/system/files/documents/pages/covid_cases_{today}.csv"

    for suffix in ['', '_0', '_1', '_2', '_3']:
        try:
            pd.read_csv(
                URL.replace('.csv', f'{suffix}.csv'), storage_options=curl_headers
            )
            return True
        except urllib.error.HTTPError:
            # Try again with _<n> appended to the filename
            continue
        except pd.errors.ParserError:
            return False
        except Exception as e:
            print(e)
            return False
        return False

if __name__ == '__main__':
    # Hit MoH once every 15 minutes checking if it's updated:
    while not moh_updated_today():
        time.sleep(900)
    print("ready!")
