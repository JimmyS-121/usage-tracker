from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, conint
from typing import List, Optional
from datetime import date
import os
import asyncpg
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection pool
pool = None

async def get_db():
    global pool
    if pool is None:
        pool = await asyncpg.create_pool(
            dsn=os.getenv("DATABASE_URL"),
            min_size=1,
            max_size=10
        )
    return pool

# Pydantic models
class StaffCreate(BaseModel):
    name: str
    department: str
    email: str

class AIUsageCreate(BaseModel):
    staff_email: str
    tool_name: str
    duration_minutes: conint(gt=0)
    task_description: Optional[str] = None
    efficiency_rating: Optional[conint(ge=1, le=5)] = None

class AIUsageStats(BaseModel):
    tool_name: str
    total_uses: int
    total_minutes: int
    avg_rating: Optional[float]
    unique_users: int

class Recommendation(BaseModel):
    recommendation_text: str
    generated_at: date
    is_implemented: bool

# Database initialization
@app.on_event("startup")
async def startup():
    pool = await get_db()
    async with pool.acquire() as connection:
        await connection.execute('''
            CREATE TABLE IF NOT EXISTS staff (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                department VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            )
        ''')
        
        await connection.execute('''
            CREATE TABLE IF NOT EXISTS ai_usage (
                id SERIAL PRIMARY KEY,
                staff_id INTEGER REFERENCES staff(id),
                tool_name VARCHAR(100) NOT NULL,
                usage_date DATE NOT NULL DEFAULT CURRENT_DATE,
                duration_minutes INTEGER NOT NULL,
                task_description TEXT,
                efficiency_rating INTEGER CHECK (efficiency_rating BETWEEN 1 AND 5),
                created_at TIMESTAMP DEFAULT NOW()
            )
        ''')
        
        await connection.execute('''
            CREATE TABLE IF NOT EXISTS recommendations (
                id SERIAL PRIMARY KEY,
                staff_id INTEGER REFERENCES staff(id),
                recommendation_text TEXT NOT NULL,
                generated_at TIMESTAMP DEFAULT NOW(),
                is_implemented BOOLEAN DEFAULT FALSE
            )
        ''')

# API Endpoints
@app.post("/api/staff/", status_code=201)
async def create_staff(staff: StaffCreate, db=Depends(get_db)):
    async with db.acquire() as connection:
        try:
            staff_id = await connection.fetchval(
                '''INSERT INTO staff (name, department, email)
                   VALUES ($1, $2, $3) RETURNING id''',
                staff.name, staff.department, staff.email
            )
            return {"id": staff_id}
        except asyncpg.UniqueViolationError:
            raise HTTPException(status_code=400, detail="Email already registered")

@app.post("/api/usage/", status_code=201)
async def record_usage(usage: AIUsageCreate, db=Depends(get_db)):
    async with db.acquire() as connection:
        # Get staff member
        staff = await connection.fetchrow(
            "SELECT id FROM staff WHERE email = $1", 
            usage.staff_email
        )
        if not staff:
            raise HTTPException(status_code=404, detail="Staff member not found")
        
        # Record usage
        usage_id = await connection.fetchval(
            '''INSERT INTO ai_usage 
               (staff_id, tool_name, duration_minutes, task_description, efficiency_rating)
               VALUES ($1, $2, $3, $4, $5) RETURNING id''',
            staff['id'], usage.tool_name, usage.duration_minutes, 
            usage.task_description, usage.efficiency_rating
        )
        
        # Generate recommendation if efficiency is low
        if usage.efficiency_rating and usage.efficiency_rating < 3:
            await connection.execute(
                '''INSERT INTO recommendations 
                   (staff_id, recommendation_text)
                   VALUES ($1, $2)''',
                staff['id'], 
                f"Consider additional training on {usage.tool_name} (low efficiency rating)"
            )
        
        return {"id": usage_id}

@app.get("/api/stats/", response_model=List[AIUsageStats])
async def get_usage_stats(db=Depends(get_db)):
    async with db.acquire() as connection:
        stats = await connection.fetch('''
            SELECT 
                tool_name,
                COUNT(*) as total_uses,
                SUM(duration_minutes) as total_minutes,
                AVG(efficiency_rating) as avg_rating,
                COUNT(DISTINCT staff_id) as unique_users
            FROM ai_usage
            GROUP BY tool_name
            ORDER BY total_uses DESC
        ''')
        return stats

@app.get("/api/recommendations/{email}", response_model=List[Recommendation])
async def get_recommendations(email: str, db=Depends(get_db)):
    async with db.acquire() as connection:
        staff = await connection.fetchrow(
            "SELECT id FROM staff WHERE email = $1", 
            email
        )
        if not staff:
            raise HTTPException(status_code=404, detail="Staff member not found")
        
        recommendations = await connection.fetch(
            '''SELECT recommendation_text, generated_at, is_implemented
               FROM recommendations 
               WHERE staff_id = $1 
               ORDER BY generated_at DESC''',
            staff['id']
        )
        return recommendations
