import datetime
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String
from config import DB_URL


engine = create_async_engine(DB_URL, echo=True)

Base = declarative_base()

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True)
    birth_date = Column(String, nullable=False)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
async def add_user(user_id: int, birth_date: str):
    async with async_session() as session: 
        user = User(user_id=user_id, birth_date=birth_date)
        session.add(user)
        await session.commit()
        
async def get_user(user_id: int): 
    async with async_session() as session:
        result = await session.get(User, user_id)
        return result.birth_date if result else None
    
def calculate_weeks_left(birth_date: str, life_expectancy: int = 75): 
    birth_date = datetime.datetime.strptime(birth_date, "%Y-%m-%d")
    today = datetime.datetime.today()
    
    weeks_lived = (today - birth_date).days // 7
    total_weeks = life_expectancy * 52
    weeks_left = max(total_weeks - weeks_lived, 0)
    
    return weeks_lived, weeks_left