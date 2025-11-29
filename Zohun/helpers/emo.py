from .emoji_logs import Emoji


class EMO:
    @staticmethod
    async def PROSES(client):
        emoji = Emoji(client)
        await emoji.get()
        return emoji.proses or "⏳ "
    
    @staticmethod
    async def GAGAL(client):
        emoji = Emoji(client)
        await emoji.get()
        return emoji.gagal or "❌ "
    
    @staticmethod
    async def BERHASIL(client):
        emoji = Emoji(client)
        await emoji.get()
        return emoji.sukses or "✅ "
    
    @staticmethod
    async def SUKSES(client):
        return await EMO.BERHASIL(client)
    
    @staticmethod
    async def PASIR(client):
        emoji = Emoji(client)
        await emoji.get()
        return emoji.robot or "⚙️ "
    
    @staticmethod
    async def BROADCAST(client):
        emoji = Emoji(client)
        await emoji.get()
        texts = await emoji.get_costum_text()
        return texts[4] if len(texts) > 4 else "📢 "
    
    @staticmethod
    async def PING(client):
        emoji = Emoji(client)
        await emoji.get()
        return emoji.ping or "🏓 "
    
    @staticmethod
    async def MSG(client):
        emoji = Emoji(client)
        await emoji.get()
        return emoji.msg or "✉️ "
    
    @staticmethod
    async def PROFIL(client):
        emoji = Emoji(client)
        await emoji.get()
        return emoji.profil or "👤 "
    
    @staticmethod
    async def OWNER(client):
        emoji = Emoji(client)
        await emoji.get()
        return emoji.owner or "⭐ "
    
    @staticmethod
    async def WARN(client):
        emoji = Emoji(client)
        await emoji.get()
        return emoji.warn or "⚠️ "
    
    @staticmethod
    async def BLOCK(client):
        emoji = Emoji(client)
        await emoji.get()
        return emoji.block or "⛔ "
    
    @staticmethod
    async def UPTIME(client):
        emoji = Emoji(client)
        await emoji.get()
        return emoji.uptime or "⏰ "
    
    @staticmethod
    async def ROBOT(client):
        emoji = Emoji(client)
        await emoji.get()
        return emoji.robot or "⚙️ "
    
    @staticmethod
    async def KLIP(client):
        emoji = Emoji(client)
        await emoji.get()
        return emoji.klip or "📎 "
    
    @staticmethod
    async def NET(client):
        emoji = Emoji(client)
        await emoji.get()
        return emoji.net or "🌐 "
    
    @staticmethod
    async def UP(client):
        emoji = Emoji(client)
        await emoji.get()
        return emoji.up or "⬆️ "
    
    @staticmethod
    async def DOWN(client):
        emoji = Emoji(client)
        await emoji.get()
        return emoji.down or "⬇️ "
    
    @staticmethod
    async def SPEED(client):
        emoji = Emoji(client)
        await emoji.get()
        return emoji.speed or "⚡️ "
