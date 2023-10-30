from clients.image_processor_client import ImageProcessorApiClient

class ImageProcessorAdapter:
    
    def __init__(self) -> None:
        self.image_processor_client = ImageProcessorApiClient()

    async def get_defect_details(self, file):
        return await self.image_processor_client.get_defect_details(file=file)
    
    async def get_defect_file(self, file):
        return await self.image_processor_client.get_defect_file(file=file)