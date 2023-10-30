from adapters.image_processor_adapter import ImageProcessorAdapter

class ImageProcessorService:
    
    def __init__(self) -> None:
        self.image_processor_adapter = ImageProcessorAdapter()

    async def get_defect_details(self, file):
        return await self.image_processor_adapter.get_defect_details(file=file)
    
    
    async def get_defect_file(self, file):
        return await self.image_processor_adapter.get_defect_file(file=file)