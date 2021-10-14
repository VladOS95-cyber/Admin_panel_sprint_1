import datetime
from typing import Optional
import uuid
from dataclasses import dataclass, field
from psycopg2.extensions import AsIs, ISQLQuote


@dataclass
class Film_work:
    title: str
    description: str
    certificate: str
    file_path: str
    rating: float
    type: str
    created_at: datetime
    updated_at: datetime
    creation_date: Optional[datetime.datetime] = None
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __len__(self):
        return 1

    def __getitem__(self, key):
        return self

    def __conform__(self, protocol):
        if protocol is ISQLQuote:
            return AsIs("'{title}', '{description}', {creation_date}, {certificate}, {file_path}, '{rating}', '{type}', '{created_at}', '{updated_at}', '{id}'".format(
                title=self.title, description=self.description, creation_date=self.creation_date, certificate=self.certificate, file_path=self.file_path, rating=self.rating, 
                type=self.type, created_at=self.created_at, updated_at=self.updated_at, id=self.id))

        return None


@dataclass
class Genre:
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class Genre_film_work:
    created_at: datetime
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)
    genre_id: uuid.UUID = field(default_factory=uuid.uuid4)
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class Person:
    full_name: str
    birth_date: datetime
    created_at: datetime
    updated_at: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class Person_film_work:
    role: str
    created_at: datetime
    film_work_id: uuid.UUID = field(default_factory=uuid.uuid4)
    person_id: uuid.UUID = field(default_factory=uuid.uuid4)
    id: uuid.UUID = field(default_factory=uuid.uuid4)
