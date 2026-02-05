# Database

This project uses [SQLAlchemy](https://www.sqlalchemy.org/) as its

## Configuration

Database configuration is managed through Pydantic settings with the following environment variable:

- **DATABASE_URL**: Database connection string (default: `sqlite:///./test.db`)
  - SQLite: `sqlite:///./database.db` (local file) or `sqlite:///:memory:` (in-memory)
  - PostgreSQL: `postgresql://user:password@localhost:5432/dbname`

The database service automatically transforms the connection string for async operations:

- `sqlite` → `sqlite+aiosqlite` (async SQLite driver)
- `postgresql` → `postgresql+asyncpg` (async PostgreSQL driver)

## Database API

This project uses the modern SQLAlchemy 2.0 API with full async/await support:

- **Async Engine**: Provides asynchronous database connections
- **AsyncSession**: Manages database transactions asynchronously
- **Future-compatible**: Uses the `future=True` flag for forward compatibility

### Supported Databases

- **SQLite**: Perfect for development and testing, supports both file-based and in-memory databases
- **PostgreSQL**: Recommended for production, provides full relational database features

## Defining Models

Models are defined in the `f1_api/models` directory and inherit from the declarative base.

### Basic Model Structure

```python
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from f1_api.models.base import Base

class User(Base):
    """User model."""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    bio: Mapped[str | None] = mapped_column(String(500))
```

### Column Types

SQLAlchemy provides a rich set of column types:

```python
import datetime
from typing import Any
from sqlalchemy import String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(Text)
    is_published: Mapped[bool] = mapped_column(default=False)
    view_count: Mapped[int] = mapped_column(default=0)
    rating: Mapped[float | None]
    metadata: Mapped[dict[str, Any] | None]
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime.datetime | None] = mapped_column(onupdate=func.now())
```

### Constraints and Indexes

```python
from sqlalchemy import String, UniqueConstraint, Index, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[str] = mapped_column(String(50), unique=True)
    name: Mapped[str] = mapped_column(String(200))
    price: Mapped[float]
    category: Mapped[str] = mapped_column(String(100))

    __table_args__ = (
        # Composite unique constraint
        UniqueConstraint("name", "category", name="uq_product_name_category"),
        # Multi-column index for better query performance
        Index("idx_category_price", "category", "price"),
        # Check constraint
        CheckConstraint("price > 0", name="ck_product_price_positive"),
    )
```

## Relationships

SQLAlchemy provides powerful relationship patterns for connecting models.

### One-to-Many Relationship

```python
from typing import List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    # Relationship to books (one author has many books)
    books: Mapped[List["Book"]] = relationship(back_populates="author", cascade="all, delete-orphan")


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id", ondelete="CASCADE"))

    # Relationship to author (many books belong to one author)
    author: Mapped["Author"] = relationship(back_populates="books")
```

### Many-to-Many Relationship

```python
from typing import List
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Association table for many-to-many relationship
student_course_association = Table(
    "student_courses",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id", ondelete="CASCADE")),
    Column("course_id", Integer, ForeignKey("courses.id", ondelete="CASCADE")),
)


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    # Many-to-many relationship to courses
    courses: Mapped[List["Course"]] = relationship(
        secondary=student_course_association,
        back_populates="students"
    )


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))

    # Many-to-many relationship to students
    students: Mapped[List["Student"]] = relationship(
        secondary=student_course_association,
        back_populates="courses"
    )
```

### Self-Referential Relationship

```python
from typing import List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    manager_id: Mapped[int | None] = mapped_column(ForeignKey("employees.id"))

    # Self-referential relationship
    manager: Mapped["Employee | None"] = relationship(
        remote_side="Employee.id",
        back_populates="subordinates"
    )
    subordinates: Mapped[List["Employee"]] = relationship(back_populates="manager")
```

## Session Management

The database service provides async context managers for session management.

### Basic Session Usage

```python
from f1_api.providers.db import get_session

async def create_user(name: str, email: str):
    """Create a new user."""
    async with get_session() as session:
        user = User(name=name, email=email)
        session.add(user)
        await session.commit()
        await session.refresh(user)  # Get generated ID
        return user
```

### Querying Data

```python
from sqlalchemy import select

async def get_user_by_email(email: str):
    """Find a user by email."""
    async with get_session() as session:
        result = await session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()


async def get_all_users():
    """Get all users."""
    async with get_session() as session:
        result = await session.execute(select(User))
        return result.scalars().all()


async def get_users_by_name(name: str):
    """Find users by name pattern."""
    async with get_session() as session:
        result = await session.execute(
            select(User).where(User.name.like(f"%{name}%"))
        )
        return result.scalars().all()
```

### Updating Data

```python
async def update_user_email(user_id: int, new_email: str):
    """Update a user's email."""
    async with get_session() as session:
        result = await session.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one()
        user.email = new_email
        await session.commit()
        return user
```

### Deleting Data

```python
async def delete_user(user_id: int):
    """Delete a user."""
    async with get_session() as session:
        result = await session.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalar_one()
        await session.delete(user)
        await session.commit()
```

### Transaction Management

```python
async def transfer_credits(from_user_id: int, to_user_id: int, amount: int):
    """Transfer credits between users with transaction safety."""
    async with get_session() as session:
        try:
            # Get both users
            from_user = (await session.execute(
                select(User).where(User.id == from_user_id)
            )).scalar_one()

            to_user = (await session.execute(
                select(User).where(User.id == to_user_id)
            )).scalar_one()

            # Perform transfer
            if from_user.credits < amount:
                raise ValueError("Insufficient credits")

            from_user.credits -= amount
            to_user.credits += amount

            await session.commit()

        except Exception:
            await session.rollback()
            raise
```

## FastAPI Integration

The `get_session_depends` function integrates seamlessly with FastAPI's dependency injection system.

### Using Database Sessions in Endpoints

```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from f1_api.providers.db import get_session_depends

@app.get("/users/{user_id}")
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_session_depends)
):
    """Get a user by ID."""
    result = await session.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/users")
async def create_user(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session_depends)
):
    """Create a new user."""
    user = User(**user_data.dict())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
```

### Testing with Database Fixtures

The test suite provides database fixtures that override the dependency:

```python
def test_create_user(fastapi_client):
    """Test creating a user via API."""
    response = fastapi_client.post(
        "/users",
        json={"name": "Test User", "email": "test@example.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test User"
```

See [Testing Documentation](./testing.md#testing-database-operations) for more details on testing with databases.

## Common CRUD Patterns

### Create

```python
async def create_record(data: dict):
    """Create a new record."""
    async with get_session() as session:
        record = MyModel(**data)
        session.add(record)
        await session.commit()
        await session.refresh(record)
        return record
```

### Read

```python
from sqlalchemy import select

async def get_record_by_id(record_id: int):
    """Get a single record by ID."""
    async with get_session() as session:
        result = await session.execute(
            select(MyModel).where(MyModel.id == record_id)
        )
        return result.scalar_one_or_none()


async def get_all_records(skip: int = 0, limit: int = 100):
    """Get paginated records."""
    async with get_session() as session:
        result = await session.execute(
            select(MyModel).offset(skip).limit(limit)
        )
        return result.scalars().all()


async def get_filtered_records(status: str):
    """Get records with filtering."""
    async with get_session() as session:
        result = await session.execute(
            select(MyModel).where(MyModel.status == status)
        )
        return result.scalars().all()
```

### Update

```python
async def update_record(record_id: int, updates: dict):
    """Update a record."""
    async with get_session() as session:
        result = await session.execute(
            select(MyModel).where(MyModel.id == record_id)
        )
        record = result.scalar_one()

        for key, value in updates.items():
            setattr(record, key, value)

        await session.commit()
        await session.refresh(record)
        return record
```

### Delete

```python
async def delete_record(record_id: int):
    """Delete a record."""
    async with get_session() as session:
        result = await session.execute(
            select(MyModel).where(MyModel.id == record_id)
        )
        record = result.scalar_one()
        await session.delete(record)
        await session.commit()
```

## Testing Database Operations

The test suite provides fixtures for database testing with isolated, in-memory databases.

### Using the db_session Fixture

```python
import pytest
from sqlalchemy import select

@pytest.mark.asyncio
async def test_create_user(db_session):
    """Test creating a user."""
    user = User(name="Test User", email="test@example.com")
    db_session.add(user)
    await db_session.commit()

    # Verify creation
    result = await db_session.execute(
        select(User).where(User.email == "test@example.com")
    )
    saved_user = result.scalar_one()
    assert saved_user.name == "Test User"
```

See [Testing Documentation](./testing.md) for comprehensive testing patterns.

## Best Practices

1. **Always use async/await**: This project uses async SQLAlchemy exclusively

   ```python
   # Good
   async with get_session() as session:
       result = await session.execute(query)

   # Bad - will not work
   with get_session() as session:
       result = session.execute(query)
   ```

2. **Use context managers for sessions**: Ensures proper cleanup and connection management

   ```python
   # Good
   async with get_session() as session:
       # operations here

   # Bad - manual session management
   session = create_session()
   # operations
   session.close()  # Easy to forget!
   ```

3. **Use select() for queries**: Modern SQLAlchemy 2.0 style

   ```python
   # Good - SQLAlchemy 2.0 style
   result = await session.execute(select(User).where(User.id == 1))
   user = result.scalar_one()

   # Old - SQLAlchemy 1.x style (avoid)
   user = session.query(User).filter(User.id == 1).one()
   ```

4. **Handle exceptions properly**: Always be prepared for database errors

   ```python
   from sqlalchemy.exc import IntegrityError

   try:
       session.add(user)
       await session.commit()
   except IntegrityError:
       await session.rollback()
       # Handle duplicate email, etc.
   ```

5. **Use scalar_one_or_none() for single results**: Prevents exceptions on missing data

   ```python
   # Good - returns None if not found
   user = result.scalar_one_or_none()
   if user is None:
       # handle not found

   # Bad - raises exception if not found
   user = result.scalar_one()  # Will raise if no result
   ```

6. **Refresh after commit to get generated values**: Get auto-generated IDs and defaults

   ```python
   session.add(user)
   await session.commit()
   await session.refresh(user)  # Now user.id is populated
   ```

7. **Use relationships for related data**: Let SQLAlchemy handle joins

   ```python
   # Good - use relationships
   author = result.scalar_one()
   books = author.books  # SQLAlchemy handles the query

   # Less efficient - manual joins
   books = await session.execute(
       select(Book).where(Book.author_id == author.id)
   )
   ```

8. **Index frequently queried columns**: Improve query performance

   ```python
   email = Column(String(255), unique=True, index=True)  # Indexed for fast lookups
   ```

## Development vs Production

### Development Configuration

```bash
# SQLite for local development (fast and simple)
export DATABASE_URL="sqlite:///./dev.db"

# Or in-memory for testing
export DATABASE_URL="sqlite:///:memory:"
```

### Production Configuration

```bash
# PostgreSQL for production (recommended)
export DATABASE_URL="postgresql://username:password@hostname:5432/database"

# With connection pool settings
export DATABASE_URL="postgresql://username:password@hostname:5432/database?pool_size=20&max_overflow=0"
```

### Database Initialization

In production, ensure migrations are run before starting the application:

```bash
# Run all pending migrations
make run_migrations

# Start your application
python -m f1_api.www  # or celery, etc.
```

## Schema Documentation

This schema is automatically generated with [Paracelsus](https://github.com/tedivm/paracelsus). To update:

```bash
make document_schema
```

<!-- BEGIN_SQLALCHEMY_DOCS -->
```mermaid
erDiagram
  chassis {
    VARCHAR(100) id PK
    VARCHAR(100) constructor_id FK
    VARCHAR(100) full_name
    VARCHAR(100) name
  }

  circuit {
    VARCHAR(100) id PK
    VARCHAR(100) country_id FK
    VARCHAR(14) direction
    VARCHAR(100) full_name
    NUMERIC(10-6) latitude
    NUMERIC(6-3) length
    NUMERIC(10-6) longitude
    VARCHAR(100) name
    VARCHAR(100) place_name
    VARCHAR(255) previous_names "nullable"
    INTEGER total_races_held
    INTEGER turns
    VARCHAR(6) type
  }

  constructor {
    VARCHAR(100) id PK
    VARCHAR(100) country_id FK
    INTEGER best_championship_position "nullable"
    INTEGER best_race_result "nullable"
    INTEGER best_sprint_race_result "nullable"
    INTEGER best_starting_grid_position "nullable"
    VARCHAR(100) full_name
    VARCHAR(100) name
    INTEGER total_1_and_2_finishes
    NUMERIC(8-2) total_championship_points
    INTEGER total_championship_wins
    INTEGER total_fastest_laps
    INTEGER total_podium_races
    INTEGER total_podiums
    NUMERIC(8-2) total_points
    INTEGER total_pole_positions
    INTEGER total_race_entries
    INTEGER total_race_laps
    INTEGER total_race_starts
    INTEGER total_race_wins
    INTEGER total_sprint_race_starts
    INTEGER total_sprint_race_wins
  }

  constructor_chronology {
    VARCHAR(100) constructor_id PK,FK
    INTEGER position_display_order PK
    VARCHAR(100) other_constructor_id FK
    INTEGER year_from
    INTEGER year_to "nullable"
  }

  continent {
    VARCHAR(100) id PK
    VARCHAR(2) code UK
    VARCHAR(100) demonym
    VARCHAR(100) name UK
  }

  country {
    VARCHAR(100) id PK
    VARCHAR(100) continent_id FK
    VARCHAR(2) alpha2_code UK
    VARCHAR(3) alpha3_code UK
    VARCHAR(100) demonym "nullable"
    VARCHAR(3) ioc_code "nullable"
    VARCHAR(100) name UK
  }

  driver {
    VARCHAR(100) id PK
    VARCHAR(100) country_of_birth_country_id FK
    VARCHAR(100) nationality_country_id FK
    VARCHAR(100) second_nationality_country_id FK "nullable"
    VARCHAR(3) abbreviation
    INTEGER best_championship_position "nullable"
    INTEGER best_race_result "nullable"
    INTEGER best_sprint_race_result "nullable"
    INTEGER best_starting_grid_position "nullable"
    DATE date_of_birth
    DATE date_of_death "nullable"
    VARCHAR(100) first_name
    VARCHAR(100) full_name
    VARCHAR(6) gender
    VARCHAR(100) last_name
    VARCHAR(100) name
    VARCHAR(2) permanent_number "nullable"
    VARCHAR(100) place_of_birth
    NUMERIC(8-2) total_championship_points
    INTEGER total_championship_wins
    INTEGER total_driver_of_the_day
    INTEGER total_fastest_laps
    INTEGER total_grand_slams
    INTEGER total_podiums
    NUMERIC(8-2) total_points
    INTEGER total_pole_positions
    INTEGER total_race_entries
    INTEGER total_race_laps
    INTEGER total_race_starts
    INTEGER total_race_wins
    INTEGER total_sprint_race_starts
    INTEGER total_sprint_race_wins
  }

  driver_family_relationship {
    VARCHAR(100) driver_id PK,FK
    INTEGER position_display_order PK
    VARCHAR(100) other_driver_id FK
    VARCHAR(50) type
  }

  driver_of_the_day_result {
    VARCHAR(100) constructor_id "nullable"
    VARCHAR(100) driver_id "nullable"
    VARCHAR(3) driver_number "nullable"
    VARCHAR(100) engine_manufacturer_id "nullable"
    NUMERIC(4-1) percentage "nullable"
    INTEGER position_display_order "nullable"
    INTEGER position_number "nullable"
    VARCHAR(4) position_text "nullable"
    INTEGER race_id "nullable"
    VARCHAR(100) tyre_manufacturer_id "nullable"
  }

  engine {
    VARCHAR(100) id PK
    VARCHAR(100) engine_manufacturer_id FK
    VARCHAR(100) aspiration "nullable"
    NUMERIC(2-1) capacity "nullable"
    VARCHAR(100) configuration "nullable"
    VARCHAR(100) full_name
    VARCHAR(100) name
  }

  engine_manufacturer {
    VARCHAR(100) id PK
    VARCHAR(100) country_id FK
    INTEGER best_championship_position "nullable"
    INTEGER best_race_result "nullable"
    INTEGER best_sprint_race_result "nullable"
    INTEGER best_starting_grid_position "nullable"
    VARCHAR(100) name
    NUMERIC(8-2) total_championship_points
    INTEGER total_championship_wins
    INTEGER total_fastest_laps
    INTEGER total_podium_races
    INTEGER total_podiums
    NUMERIC(8-2) total_points
    INTEGER total_pole_positions
    INTEGER total_race_entries
    INTEGER total_race_laps
    INTEGER total_race_starts
    INTEGER total_race_wins
    INTEGER total_sprint_race_starts
    INTEGER total_sprint_race_wins
  }

  entrant {
    VARCHAR(100) id PK
    VARCHAR(100) name
  }

  fastest_lap {
    VARCHAR(100) constructor_id "nullable"
    VARCHAR(100) driver_id "nullable"
    VARCHAR(3) driver_number "nullable"
    VARCHAR(100) engine_manufacturer_id "nullable"
    VARCHAR(20) gap "nullable"
    INTEGER gap_millis "nullable"
    VARCHAR(20) interval "nullable"
    INTEGER interval_millis "nullable"
    INTEGER lap "nullable"
    INTEGER position_display_order "nullable"
    INTEGER position_number "nullable"
    VARCHAR(4) position_text "nullable"
    INTEGER race_id "nullable"
    VARCHAR(20) time "nullable"
    INTEGER time_millis "nullable"
    VARCHAR(100) tyre_manufacturer_id "nullable"
  }

  free_practice_1_result {
    VARCHAR(100) constructor_id "nullable"
    VARCHAR(100) driver_id "nullable"
    VARCHAR(3) driver_number "nullable"
    VARCHAR(100) engine_manufacturer_id "nullable"
    VARCHAR(20) gap "nullable"
    INTEGER gap_millis "nullable"
    VARCHAR(20) interval "nullable"
    INTEGER interval_millis "nullable"
    INTEGER laps "nullable"
    INTEGER position_display_order "nullable"
    INTEGER position_number "nullable"
    VARCHAR(4) position_text "nullable"
    INTEGER race_id "nullable"
    VARCHAR(20) time "nullable"
    INTEGER time_millis "nullable"
    VARCHAR(100) tyre_manufacturer_id "nullable"
  }

  free_practice_2_result {
    VARCHAR(100) constructor_id "nullable"
    VARCHAR(100) driver_id "nullable"
    VARCHAR(3) driver_number "nullable"
    VARCHAR(100) engine_manufacturer_id "nullable"
    VARCHAR(20) gap "nullable"
    INTEGER gap_millis "nullable"
    VARCHAR(20) interval "nullable"
    INTEGER interval_millis "nullable"
    INTEGER laps "nullable"
    INTEGER position_display_order "nullable"
    INTEGER position_number "nullable"
    VARCHAR(4) position_text "nullable"
    INTEGER race_id "nullable"
    VARCHAR(20) time "nullable"
    INTEGER time_millis "nullable"
    VARCHAR(100) tyre_manufacturer_id "nullable"
  }

  free_practice_3_result {
    VARCHAR(100) constructor_id "nullable"
    VARCHAR(100) driver_id "nullable"
    VARCHAR(3) driver_number "nullable"
    VARCHAR(100) engine_manufacturer_id "nullable"
    VARCHAR(20) gap "nullable"
    INTEGER gap_millis "nullable"
    VARCHAR(20) interval "nullable"
    INTEGER interval_millis "nullable"
    INTEGER laps "nullable"
    INTEGER position_display_order "nullable"
    INTEGER position_number "nullable"
    VARCHAR(4) position_text "nullable"
    INTEGER race_id "nullable"
    VARCHAR(20) time "nullable"
    INTEGER time_millis "nullable"
    VARCHAR(100) tyre_manufacturer_id "nullable"
  }

  free_practice_4_result {
    VARCHAR(100) constructor_id "nullable"
    VARCHAR(100) driver_id "nullable"
    VARCHAR(3) driver_number "nullable"
    VARCHAR(100) engine_manufacturer_id "nullable"
    VARCHAR(20) gap "nullable"
    INTEGER gap_millis "nullable"
    VARCHAR(20) interval "nullable"
    INTEGER interval_millis "nullable"
    INTEGER laps "nullable"
    INTEGER position_display_order "nullable"
    INTEGER position_number "nullable"
    VARCHAR(4) position_text "nullable"
    INTEGER race_id "nullable"
    VARCHAR(20) time "nullable"
    INTEGER time_millis "nullable"
    VARCHAR(100) tyre_manufacturer_id "nullable"
  }

  grand_prix {
    VARCHAR(100) id PK
    VARCHAR(100) country_id FK "nullable"
    VARCHAR(3) abbreviation
    VARCHAR(100) full_name
    VARCHAR(100) name
    VARCHAR(100) short_name
    INTEGER total_races_held
  }

  pit_stop {
    VARCHAR(100) constructor_id "nullable"
    VARCHAR(100) driver_id "nullable"
    VARCHAR(3) driver_number "nullable"
    VARCHAR(100) engine_manufacturer_id "nullable"
    INTEGER lap "nullable"
    INTEGER position_display_order "nullable"
    INTEGER position_number "nullable"
    VARCHAR(4) position_text "nullable"
    INTEGER race_id "nullable"
    INTEGER stop "nullable"
    VARCHAR(20) time "nullable"
    INTEGER time_millis "nullable"
    VARCHAR(100) tyre_manufacturer_id "nullable"
  }

  pre_qualifying_result {
    VARCHAR(100) constructor_id "nullable"
    VARCHAR(100) driver_id "nullable"
    VARCHAR(3) driver_number "nullable"
    VARCHAR(100) engine_manufacturer_id "nullable"
    VARCHAR(20) gap "nullable"
    INTEGER gap_millis "nullable"
    VARCHAR(20) interval "nullable"
    INTEGER interval_millis "nullable"
    INTEGER laps "nullable"
    INTEGER position_display_order "nullable"
    INTEGER position_number "nullable"
    VARCHAR(4) position_text "nullable"
    INTEGER race_id "nullable"
    VARCHAR(20) time "nullable"
    INTEGER time_millis "nullable"
    VARCHAR(100) tyre_manufacturer_id "nullable"
  }

  qualifying_1_result {
    VARCHAR(100) constructor_id "nullable"
    VARCHAR(100) driver_id "nullable"
    VARCHAR(3) driver_number "nullable"
    VARCHAR(100) engine_manufacturer_id "nullable"
    VARCHAR(20) gap "nullable"
    INTEGER gap_millis "nullable"
    VARCHAR(20) interval "nullable"
    INTEGER interval_millis "nullable"
    INTEGER laps "nullable"
    INTEGER position_display_order "nullable"
    INTEGER position_number "nullable"
    VARCHAR(4) position_text "nullable"
    INTEGER race_id "nullable"
    VARCHAR(20) time "nullable"
    INTEGER time_millis "nullable"
    VARCHAR(100) tyre_manufacturer_id "nullable"
  }

  qualifying_2_result {
    VARCHAR(100) constructor_id "nullable"
    VARCHAR(100) driver_id "nullable"
    VARCHAR(3) driver_number "nullable"
    VARCHAR(100) engine_manufacturer_id "nullable"
    VARCHAR(20) gap "nullable"
    INTEGER gap_millis "nullable"
    VARCHAR(20) interval "nullable"
    INTEGER interval_millis "nullable"
    INTEGER laps "nullable"
    INTEGER position_display_order "nullable"
    INTEGER position_number "nullable"
    VARCHAR(4) position_text "nullable"
    INTEGER race_id "nullable"
    VARCHAR(20) time "nullable"
    INTEGER time_millis "nullable"
    VARCHAR(100) tyre_manufacturer_id "nullable"
  }

  qualifying_result {
    VARCHAR(100) constructor_id "nullable"
    VARCHAR(100) driver_id "nullable"
    VARCHAR(3) driver_number "nullable"
    VARCHAR(100) engine_manufacturer_id "nullable"
    VARCHAR(20) gap "nullable"
    INTEGER gap_millis "nullable"
    VARCHAR(20) interval "nullable"
    INTEGER interval_millis "nullable"
    INTEGER laps "nullable"
    INTEGER position_display_order "nullable"
    INTEGER position_number "nullable"
    VARCHAR(4) position_text "nullable"
    VARCHAR(20) q1 "nullable"
    INTEGER q1_millis "nullable"
    VARCHAR(20) q2 "nullable"
    INTEGER q2_millis "nullable"
    VARCHAR(20) q3 "nullable"
    INTEGER q3_millis "nullable"
    INTEGER race_id "nullable"
    VARCHAR(20) time "nullable"
    INTEGER time_millis "nullable"
    VARCHAR(100) tyre_manufacturer_id "nullable"
  }

  race {
    INTEGER id PK
    VARCHAR(100) circuit_id FK
    VARCHAR(100) grand_prix_id FK
    INTEGER year FK
    VARCHAR(6) circuit_type
    BOOLEAN constructors_championship_decider
    NUMERIC(6-3) course_length
    DATE date
    VARCHAR(14) direction
    NUMERIC(6-3) distance
    BOOLEAN drivers_championship_decider
    DATE free_practice_1_date "nullable"
    VARCHAR(5) free_practice_1_time "nullable"
    DATE free_practice_2_date "nullable"
    VARCHAR(5) free_practice_2_time "nullable"
    DATE free_practice_3_date "nullable"
    VARCHAR(5) free_practice_3_time "nullable"
    DATE free_practice_4_date "nullable"
    VARCHAR(5) free_practice_4_time "nullable"
    INTEGER laps
    VARCHAR(100) official_name
    DATE pre_qualifying_date "nullable"
    VARCHAR(5) pre_qualifying_time "nullable"
    DATE qualifying_1_date "nullable"
    VARCHAR(5) qualifying_1_time "nullable"
    DATE qualifying_2_date "nullable"
    VARCHAR(5) qualifying_2_time "nullable"
    DATE qualifying_date "nullable"
    VARCHAR(20) qualifying_format
    VARCHAR(5) qualifying_time "nullable"
    INTEGER round
    NUMERIC(6-3) scheduled_distance "nullable"
    INTEGER scheduled_laps "nullable"
    DATE sprint_qualifying_date "nullable"
    VARCHAR(20) sprint_qualifying_format "nullable"
    VARCHAR(5) sprint_qualifying_time "nullable"
    DATE sprint_race_date "nullable"
    VARCHAR(5) sprint_race_time "nullable"
    VARCHAR(5) time "nullable"
    INTEGER turns
    DATE warming_up_date "nullable"
    VARCHAR(5) warming_up_time "nullable"
  }

  race_constructor_standing {
    INTEGER position_display_order PK
    INTEGER race_id PK,FK
    VARCHAR(100) constructor_id FK
    VARCHAR(100) engine_manufacturer_id FK
    BOOLEAN championship_won
    NUMERIC(8-2) points
    INTEGER position_number "nullable"
    VARCHAR(4) position_text
    INTEGER positions_gained "nullable"
  }

  race_data {
    INTEGER position_display_order PK
    INTEGER race_id PK,FK
    VARCHAR(50) type PK
    VARCHAR(100) constructor_id FK
    VARCHAR(100) driver_id FK
    VARCHAR(100) engine_manufacturer_id FK
    VARCHAR(100) tyre_manufacturer_id FK
    VARCHAR(3) driver_number
    NUMERIC(4-1) driver_of_the_day_percentage "nullable"
    VARCHAR(20) fastest_lap_gap "nullable"
    INTEGER fastest_lap_gap_millis "nullable"
    VARCHAR(20) fastest_lap_interval "nullable"
    INTEGER fastest_lap_interval_millis "nullable"
    INTEGER fastest_lap_lap "nullable"
    VARCHAR(20) fastest_lap_time "nullable"
    INTEGER fastest_lap_time_millis "nullable"
    INTEGER pit_stop_lap "nullable"
    INTEGER pit_stop_stop "nullable"
    VARCHAR(20) pit_stop_time "nullable"
    INTEGER pit_stop_time_millis "nullable"
    INTEGER position_number "nullable"
    VARCHAR(4) position_text
    VARCHAR(20) practice_gap "nullable"
    INTEGER practice_gap_millis "nullable"
    VARCHAR(20) practice_interval "nullable"
    INTEGER practice_interval_millis "nullable"
    INTEGER practice_laps "nullable"
    VARCHAR(20) practice_time "nullable"
    INTEGER practice_time_millis "nullable"
    VARCHAR(20) qualifying_gap "nullable"
    INTEGER qualifying_gap_millis "nullable"
    VARCHAR(20) qualifying_interval "nullable"
    INTEGER qualifying_interval_millis "nullable"
    INTEGER qualifying_laps "nullable"
    VARCHAR(20) qualifying_q1 "nullable"
    INTEGER qualifying_q1_millis "nullable"
    VARCHAR(20) qualifying_q2 "nullable"
    INTEGER qualifying_q2_millis "nullable"
    VARCHAR(20) qualifying_q3 "nullable"
    INTEGER qualifying_q3_millis "nullable"
    VARCHAR(20) qualifying_time "nullable"
    INTEGER qualifying_time_millis "nullable"
    BOOLEAN race_driver_of_the_day "nullable"
    BOOLEAN race_fastest_lap "nullable"
    VARCHAR(20) race_gap "nullable"
    INTEGER race_gap_laps "nullable"
    INTEGER race_gap_millis "nullable"
    BOOLEAN race_grand_slam "nullable"
    INTEGER race_grid_position_number "nullable"
    VARCHAR(2) race_grid_position_text "nullable"
    VARCHAR(20) race_interval "nullable"
    INTEGER race_interval_millis "nullable"
    INTEGER race_laps "nullable"
    INTEGER race_pit_stops "nullable"
    NUMERIC(8-2) race_points "nullable"
    BOOLEAN race_pole_position "nullable"
    INTEGER race_positions_gained "nullable"
    INTEGER race_qualification_position_number "nullable"
    VARCHAR(4) race_qualification_position_text "nullable"
    VARCHAR(100) race_reason_retired "nullable"
    BOOLEAN race_shared_car "nullable"
    VARCHAR(20) race_time "nullable"
    INTEGER race_time_millis "nullable"
    VARCHAR(20) race_time_penalty "nullable"
    INTEGER race_time_penalty_millis "nullable"
    VARCHAR(20) starting_grid_position_grid_penalty "nullable"
    INTEGER starting_grid_position_grid_penalty_positions "nullable"
    INTEGER starting_grid_position_qualification_position_number "nullable"
    VARCHAR(4) starting_grid_position_qualification_position_text "nullable"
    VARCHAR(20) starting_grid_position_time "nullable"
    INTEGER starting_grid_position_time_millis "nullable"
  }

  race_driver_standing {
    INTEGER position_display_order PK
    INTEGER race_id PK,FK
    VARCHAR(100) driver_id FK
    BOOLEAN championship_won
    NUMERIC(8-2) points
    INTEGER position_number "nullable"
    VARCHAR(4) position_text
    INTEGER positions_gained "nullable"
  }

  race_result {
    VARCHAR(100) constructor_id "nullable"
    VARCHAR(100) driver_id "nullable"
    VARCHAR(3) driver_number "nullable"
    BOOLEAN driver_of_the_day "nullable"
    VARCHAR(100) engine_manufacturer_id "nullable"
    BOOLEAN fastest_lap "nullable"
    VARCHAR(20) gap "nullable"
    INTEGER gap_laps "nullable"
    INTEGER gap_millis "nullable"
    BOOLEAN grand_slam "nullable"
    INTEGER grid_position_number "nullable"
    VARCHAR(2) grid_position_text "nullable"
    VARCHAR(20) interval "nullable"
    INTEGER interval_millis "nullable"
    INTEGER laps "nullable"
    INTEGER pit_stops "nullable"
    NUMERIC(8-2) points "nullable"
    BOOLEAN pole_position "nullable"
    INTEGER position_display_order "nullable"
    INTEGER position_number "nullable"
    VARCHAR(4) position_text "nullable"
    INTEGER positions_gained "nullable"
    INTEGER qualification_position_number "nullable"
    VARCHAR(4) qualification_position_text "nullable"
    INTEGER race_id "nullable"
    VARCHAR(100) reason_retired "nullable"
    BOOLEAN shared_car "nullable"
    VARCHAR(20) time "nullable"
    INTEGER time_millis "nullable"
    VARCHAR(20) time_penalty "nullable"
    INTEGER time_penalty_millis "nullable"
    VARCHAR(100) tyre_manufacturer_id "nullable"
  }

  season {
    INTEGER year PK
  }

  season_constructor {
    VARCHAR(100) constructor_id PK,FK
    INTEGER year PK,FK
    INTEGER best_race_result "nullable"
    INTEGER best_sprint_race_result "nullable"
    INTEGER best_starting_grid_position "nullable"
    INTEGER position_number "nullable"
    VARCHAR(4) position_text "nullable"
    INTEGER total_1_and_2_finishes
    INTEGER total_fastest_laps
    INTEGER total_podium_races
    INTEGER total_podiums
    NUMERIC(8-2) total_points
    INTEGER total_pole_positions
    INTEGER total_race_entries
    INTEGER total_race_laps
    INTEGER total_race_starts
    INTEGER total_race_wins
    INTEGER total_sprint_race_starts
    INTEGER total_sprint_race_wins
  }

  season_constructor_standing {
    INTEGER position_display_order PK
    INTEGER year PK,FK
    VARCHAR(100) constructor_id FK
    VARCHAR(100) engine_manufacturer_id FK
    BOOLEAN championship_won
    NUMERIC(8-2) points
    INTEGER position_number "nullable"
    VARCHAR(4) position_text
  }

  season_driver {
    VARCHAR(100) driver_id PK,FK
    INTEGER year PK,FK
    INTEGER best_race_result "nullable"
    INTEGER best_sprint_race_result "nullable"
    INTEGER best_starting_grid_position "nullable"
    INTEGER position_number "nullable"
    VARCHAR(4) position_text "nullable"
    INTEGER total_driver_of_the_day
    INTEGER total_fastest_laps
    INTEGER total_grand_slams
    INTEGER total_podiums
    NUMERIC(8-2) total_points
    INTEGER total_pole_positions
    INTEGER total_race_entries
    INTEGER total_race_laps
    INTEGER total_race_starts
    INTEGER total_race_wins
    INTEGER total_sprint_race_starts
    INTEGER total_sprint_race_wins
  }

  season_driver_standing {
    INTEGER position_display_order PK
    INTEGER year PK,FK
    VARCHAR(100) driver_id FK
    BOOLEAN championship_won
    NUMERIC(8-2) points
    INTEGER position_number "nullable"
    VARCHAR(4) position_text
  }

  season_engine_manufacturer {
    VARCHAR(100) engine_manufacturer_id PK,FK
    INTEGER year PK,FK
    INTEGER best_race_result "nullable"
    INTEGER best_sprint_race_result "nullable"
    INTEGER best_starting_grid_position "nullable"
    INTEGER position_number "nullable"
    VARCHAR(4) position_text "nullable"
    INTEGER total_fastest_laps
    INTEGER total_podium_races
    INTEGER total_podiums
    NUMERIC(8-2) total_points
    INTEGER total_pole_positions
    INTEGER total_race_entries
    INTEGER total_race_laps
    INTEGER total_race_starts
    INTEGER total_race_wins
    INTEGER total_sprint_race_starts
    INTEGER total_sprint_race_wins
  }

  season_entrant {
    VARCHAR(100) entrant_id PK,FK
    INTEGER year PK,FK
    VARCHAR(100) country_id FK
  }

  season_entrant_chassis {
    VARCHAR(100) chassis_id PK,FK
    VARCHAR(100) constructor_id PK,FK
    VARCHAR(100) engine_manufacturer_id PK,FK
    VARCHAR(100) entrant_id PK,FK
    INTEGER year PK,FK
  }

  season_entrant_constructor {
    VARCHAR(100) constructor_id PK,FK
    VARCHAR(100) engine_manufacturer_id PK,FK
    VARCHAR(100) entrant_id PK,FK
    INTEGER year PK,FK
  }

  season_entrant_driver {
    VARCHAR(100) constructor_id PK,FK
    VARCHAR(100) driver_id PK,FK
    VARCHAR(100) engine_manufacturer_id PK,FK
    VARCHAR(100) entrant_id PK,FK
    INTEGER year PK,FK
    VARCHAR(100) rounds "nullable"
    VARCHAR(100) rounds_text "nullable"
    BOOLEAN test_driver
  }

  season_entrant_engine {
    VARCHAR(100) constructor_id PK,FK
    VARCHAR(100) engine_id PK,FK
    VARCHAR(100) engine_manufacturer_id PK,FK
    VARCHAR(100) entrant_id PK,FK
    INTEGER year PK,FK
  }

  season_entrant_tyre_manufacturer {
    VARCHAR(100) constructor_id PK,FK
    VARCHAR(100) engine_manufacturer_id PK,FK
    VARCHAR(100) entrant_id PK,FK
    VARCHAR(100) tyre_manufacturer_id PK,FK
    INTEGER year PK,FK
  }

  season_tyre_manufacturer {
    VARCHAR(100) tyre_manufacturer_id PK,FK
    INTEGER year PK,FK
    INTEGER best_race_result "nullable"
    INTEGER best_sprint_race_result "nullable"
    INTEGER best_starting_grid_position "nullable"
    INTEGER total_fastest_laps
    INTEGER total_podium_races
    INTEGER total_podiums
    INTEGER total_pole_positions
    INTEGER total_race_entries
    INTEGER total_race_laps
    INTEGER total_race_starts
    INTEGER total_race_wins
    INTEGER total_sprint_race_starts
    INTEGER total_sprint_race_wins
  }

  sprint_qualifying_result {
    VARCHAR(100) constructor_id "nullable"
    VARCHAR(100) driver_id "nullable"
    VARCHAR(3) driver_number "nullable"
    VARCHAR(100) engine_manufacturer_id "nullable"
    VARCHAR(20) gap "nullable"
    INTEGER gap_millis "nullable"
    VARCHAR(20) interval "nullable"
    INTEGER interval_millis "nullable"
    INTEGER laps "nullable"
    INTEGER position_display_order "nullable"
    INTEGER position_number "nullable"
    VARCHAR(4) position_text "nullable"
    VARCHAR(20) q1 "nullable"
    INTEGER q1_millis "nullable"
    VARCHAR(20) q2 "nullable"
    INTEGER q2_millis "nullable"
    VARCHAR(20) q3 "nullable"
    INTEGER q3_millis "nullable"
    INTEGER race_id "nullable"
    VARCHAR(20) time "nullable"
    INTEGER time_millis "nullable"
    VARCHAR(100) tyre_manufacturer_id "nullable"
  }

  sprint_race_result {
    VARCHAR(100) constructor_id "nullable"
    VARCHAR(100) driver_id "nullable"
    VARCHAR(3) driver_number "nullable"
    VARCHAR(100) engine_manufacturer_id "nullable"
    VARCHAR(20) gap "nullable"
    INTEGER gap_laps "nullable"
    INTEGER gap_millis "nullable"
    INTEGER grid_position_number "nullable"
    VARCHAR(2) grid_position_text "nullable"
    VARCHAR(20) interval "nullable"
    INTEGER interval_millis "nullable"
    INTEGER laps "nullable"
    NUMERIC(8-2) points "nullable"
    INTEGER position_display_order "nullable"
    INTEGER position_number "nullable"
    VARCHAR(4) position_text "nullable"
    INTEGER positions_gained "nullable"
    INTEGER qualification_position_number "nullable"
    VARCHAR(4) qualification_position_text "nullable"
    INTEGER race_id "nullable"
    VARCHAR(100) reason_retired "nullable"
    VARCHAR(20) time "nullable"
    INTEGER time_millis "nullable"
    VARCHAR(20) time_penalty "nullable"
    INTEGER time_penalty_millis "nullable"
    VARCHAR(100) tyre_manufacturer_id "nullable"
  }

  sprint_starting_grid_position {
    VARCHAR(100) constructor_id "nullable"
    VARCHAR(100) driver_id "nullable"
    VARCHAR(3) driver_number "nullable"
    VARCHAR(100) engine_manufacturer_id "nullable"
    VARCHAR(20) grid_penalty "nullable"
    INTEGER grid_penalty_positions "nullable"
    INTEGER position_display_order "nullable"
    INTEGER position_number "nullable"
    VARCHAR(4) position_text "nullable"
    INTEGER qualification_position_number "nullable"
    VARCHAR(4) qualification_position_text "nullable"
    INTEGER race_id "nullable"
    VARCHAR(20) time "nullable"
    INTEGER time_millis "nullable"
    VARCHAR(100) tyre_manufacturer_id "nullable"
  }

  starting_grid_position {
    VARCHAR(100) constructor_id "nullable"
    VARCHAR(100) driver_id "nullable"
    VARCHAR(3) driver_number "nullable"
    VARCHAR(100) engine_manufacturer_id "nullable"
    VARCHAR(20) grid_penalty "nullable"
    INTEGER grid_penalty_positions "nullable"
    INTEGER position_display_order "nullable"
    INTEGER position_number "nullable"
    VARCHAR(4) position_text "nullable"
    INTEGER qualification_position_number "nullable"
    VARCHAR(4) qualification_position_text "nullable"
    INTEGER race_id "nullable"
    VARCHAR(20) time "nullable"
    INTEGER time_millis "nullable"
    VARCHAR(100) tyre_manufacturer_id "nullable"
  }

  tyre_manufacturer {
    VARCHAR(100) id PK
    VARCHAR(100) country_id FK
    INTEGER best_race_result "nullable"
    INTEGER best_sprint_race_result "nullable"
    INTEGER best_starting_grid_position "nullable"
    VARCHAR(100) name
    INTEGER total_fastest_laps
    INTEGER total_podium_races
    INTEGER total_podiums
    INTEGER total_pole_positions
    INTEGER total_race_entries
    INTEGER total_race_laps
    INTEGER total_race_starts
    INTEGER total_race_wins
    INTEGER total_sprint_race_starts
    INTEGER total_sprint_race_wins
  }

  warming_up_result {
    VARCHAR(100) constructor_id "nullable"
    VARCHAR(100) driver_id "nullable"
    VARCHAR(3) driver_number "nullable"
    VARCHAR(100) engine_manufacturer_id "nullable"
    VARCHAR(20) gap "nullable"
    INTEGER gap_millis "nullable"
    VARCHAR(20) interval "nullable"
    INTEGER interval_millis "nullable"
    INTEGER laps "nullable"
    INTEGER position_display_order "nullable"
    INTEGER position_number "nullable"
    VARCHAR(4) position_text "nullable"
    INTEGER race_id "nullable"
    VARCHAR(20) time "nullable"
    INTEGER time_millis "nullable"
    VARCHAR(100) tyre_manufacturer_id "nullable"
  }

  constructor ||--o{ chassis : constructor_id
  country ||--o{ circuit : country_id
  country ||--o{ constructor : country_id
  constructor ||--o| constructor_chronology : constructor_id
  constructor ||--o{ constructor_chronology : other_constructor_id
  continent ||--o{ country : continent_id
  country ||--o{ driver : country_of_birth_country_id
  country ||--o{ driver : nationality_country_id
  country ||--o{ driver : second_nationality_country_id
  driver ||--o| driver_family_relationship : driver_id
  driver ||--o{ driver_family_relationship : other_driver_id
  engine_manufacturer ||--o{ engine : engine_manufacturer_id
  country ||--o{ engine_manufacturer : country_id
  country ||--o{ grand_prix : country_id
  season ||--o{ race : year
  grand_prix ||--o{ race : grand_prix_id
  circuit ||--o{ race : circuit_id
  race ||--o| race_constructor_standing : race_id
  constructor ||--o{ race_constructor_standing : constructor_id
  engine_manufacturer ||--o{ race_constructor_standing : engine_manufacturer_id
  race ||--o| race_data : race_id
  driver ||--o{ race_data : driver_id
  constructor ||--o{ race_data : constructor_id
  engine_manufacturer ||--o{ race_data : engine_manufacturer_id
  tyre_manufacturer ||--o{ race_data : tyre_manufacturer_id
  race ||--o| race_driver_standing : race_id
  driver ||--o{ race_driver_standing : driver_id
  season ||--o| season_constructor : year
  constructor ||--o| season_constructor : constructor_id
  season ||--o| season_constructor_standing : year
  constructor ||--o{ season_constructor_standing : constructor_id
  engine_manufacturer ||--o{ season_constructor_standing : engine_manufacturer_id
  season ||--o| season_driver : year
  driver ||--o| season_driver : driver_id
  season ||--o| season_driver_standing : year
  driver ||--o{ season_driver_standing : driver_id
  season ||--o| season_engine_manufacturer : year
  engine_manufacturer ||--o| season_engine_manufacturer : engine_manufacturer_id
  season ||--o| season_entrant : year
  entrant ||--o| season_entrant : entrant_id
  country ||--o{ season_entrant : country_id
  season ||--o| season_entrant_chassis : year
  entrant ||--o| season_entrant_chassis : entrant_id
  constructor ||--o| season_entrant_chassis : constructor_id
  engine_manufacturer ||--o| season_entrant_chassis : engine_manufacturer_id
  chassis ||--o| season_entrant_chassis : chassis_id
  season ||--o| season_entrant_constructor : year
  entrant ||--o| season_entrant_constructor : entrant_id
  constructor ||--o| season_entrant_constructor : constructor_id
  engine_manufacturer ||--o| season_entrant_constructor : engine_manufacturer_id
  season ||--o| season_entrant_driver : year
  entrant ||--o| season_entrant_driver : entrant_id
  constructor ||--o| season_entrant_driver : constructor_id
  engine_manufacturer ||--o| season_entrant_driver : engine_manufacturer_id
  driver ||--o| season_entrant_driver : driver_id
  season ||--o| season_entrant_engine : year
  entrant ||--o| season_entrant_engine : entrant_id
  constructor ||--o| season_entrant_engine : constructor_id
  engine_manufacturer ||--o| season_entrant_engine : engine_manufacturer_id
  engine ||--o| season_entrant_engine : engine_id
  season ||--o| season_entrant_tyre_manufacturer : year
  entrant ||--o| season_entrant_tyre_manufacturer : entrant_id
  constructor ||--o| season_entrant_tyre_manufacturer : constructor_id
  engine_manufacturer ||--o| season_entrant_tyre_manufacturer : engine_manufacturer_id
  tyre_manufacturer ||--o| season_entrant_tyre_manufacturer : tyre_manufacturer_id
  season ||--o| season_tyre_manufacturer : year
  tyre_manufacturer ||--o| season_tyre_manufacturer : tyre_manufacturer_id
  country ||--o{ tyre_manufacturer : country_id

```
<!-- END_SQLALCHEMY_DOCS -->

## References

- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/en/20/)
- [SQLAlchemy ORM Documentation](https://docs.sqlalchemy.org/en/20/orm/)
- [SQLAlchemy Async Documentation](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
