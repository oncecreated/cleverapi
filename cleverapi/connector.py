import aiohttp

class Connector():
    def __init__(self):
        self.session = None

    async def __aenter__(self):
        headers = {
            "User-Agent": str("Клевер/2.1.1 (Redmi Note 3; "
            "Android 23; Scale/3.00; VK SDK 1.6.8; com.vk.quiz)")
        }
        self.session = aiohttp.ClientSession(headers=headers)

    async def __aexit__(self, type, value, tarceback):
        await self.session.close()