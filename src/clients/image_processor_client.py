import requests
from os import getenv

class ImageProcessorApiClient:

    def __init__(self):
        self.baseUrl = getenv("IMAGE_PROCESSOR_BASE_API_URL")
    
    async def get_defect_details(self, file):
        files = {'file': file}
        defects_details = requests.post(url=self.baseUrl + '/report/details/from-file', files=files)
        defects_details.raise_for_status()
        return defects_details.json()
    
    async def get_defect_file(self, file):
        files = {'file': file}
        defects_file = requests.post(url=self.baseUrl + '/report/file/from-file', files=files)
        defects_file.raise_for_status()
        return defects_file.content