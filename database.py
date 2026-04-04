import aiosqlite


DB_PATH = "career_bot.db"


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_id INTEGER UNIQUE,
                age INTEGER,
                education TEXT,
                interests TEXT,
                subjects TEXT,
                skills TEXT,
                work_format TEXT,
                goal TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()


async def save_user_profile(
    tg_id: int,
    age: int,
    education: str,
    interests: str,
    subjects: str,
    skills: str,
    work_format: str,
    goal: str
):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO users (
                tg_id, age, education, interests, subjects,
                skills, work_format, goal
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(tg_id) DO UPDATE SET
                age=excluded.age,
                education=excluded.education,
                interests=excluded.interests,
                subjects=excluded.subjects,
                skills=excluded.skills,
                work_format=excluded.work_format,
                goal=excluded.goal
        """, (
            tg_id,
            age,
            education,
            interests,
            subjects,
            skills,
            work_format,
            goal
        ))
        await db.commit()


async def get_user_profile(tg_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("""
            SELECT tg_id, age, education, interests, subjects, skills, work_format, goal
            FROM users
            WHERE tg_id = ?
        """, (tg_id,))
        row = await cursor.fetchone()
        return row