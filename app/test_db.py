import asyncio
import asyncpg

async def main():
    conn = await asyncpg.connect(
        host="aws-1-ap-northeast-1.pooler.supabase.com",
        port=6543,
        user="postgres.pvccrzfsbbysqqxetfma",
        password="Pulse@2026#123",
        database="postgres",
    )
    print("CONNECTED!")
    await conn.close()

asyncio.run(main())