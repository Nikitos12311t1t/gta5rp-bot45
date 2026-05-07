import aiosqlite

DB_NAME = "gta5rp.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            '''
            CREATE TABLE IF NOT EXISTS deals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                buy_price INTEGER,
                sell_price INTEGER,
                investments INTEGER,
                commission REAL,
                profit REAL,
                roi REAL
            )
            '''
        )
        await db.commit()

async def save_deal(user_id, buy, sell, inv, comm, profit, roi):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            '''
            INSERT INTO deals
            (
                user_id,
                buy_price,
                sell_price,
                investments,
                commission,
                profit,
                roi
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''',
            (user_id, buy, sell, inv, comm, profit, roi)
        )
        await db.commit()

async def get_history(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            '''
            SELECT buy_price, sell_price, profit
            FROM deals
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT 10
            ''',
            (user_id,)
        )

        return await cursor.fetchall()

async def get_stats(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            '''
            SELECT
                COUNT(*),
                COALESCE(SUM(profit), 0)
            FROM deals
            WHERE user_id = ?
            ''',
            (user_id,)
        )

        return await cursor.fetchone()