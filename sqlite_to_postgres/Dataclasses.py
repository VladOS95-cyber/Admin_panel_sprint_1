import datetime
import uuid
from dataclasses import dataclass, field


@dataclass
class Film_work:
    title: str
    description: str
    creation_date: datetime
    certificate: str
    file_path: str
    rating: float
    type: str
    created_at: str = field(default_factory = lambda: datetime.datetime.now().isoformat())
    updated_at: str = field(default_factory = lambda: datetime.datetime.now().isoformat())
    id: uuid.UUID = field(default_factory=uuid.uuid4)

@dataclass
class Genre:
    name: str
    description: str
    created_at: str = field(default_factory = lambda: datetime.datetime.now().isoformat())
    updated_at: str = field(default_factory = lambda: datetime.datetime.now().isoformat())
    id: uuid.UUID = field(default_factory=uuid.uuid4)

@dataclass
class Genre_film_work:
    film_work_id: uuid.UUID = field(default_factory = lambda: Film_work.id)
    genre_id: uuid.UUID = field(default_factory = lambda: Genre.id)
    id: uuid.UUID = field(default_factory=uuid.uuid4)

@dataclass
class Person:
    full_name: str
    birth_date: datetime
    created_at: str = field(default_factory = lambda: datetime.datetime.now().isoformat())
    updated_at: str = field(default_factory = lambda: datetime.datetime.now().isoformat())
    id: uuid.UUID = field(default_factory=uuid.uuid4)

@dataclass
class Person_film_work:
    role: str
    film_work_id: uuid.UUID = field(default_factory = lambda: Film_work.id)
    person_id: uuid.UUID = field(default_factory = lambda: Person.id)
    created_at: str = field(default_factory = lambda: datetime.datetime.now().isoformat())
