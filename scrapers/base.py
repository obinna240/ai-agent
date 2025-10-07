from typing import List, Dict

class ScraperBase:
    name: str

    async def search(self, profile: Dict) -> List[Dict]:
        raise NotImplementedError
