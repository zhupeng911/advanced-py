from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    id: Optional[int]
    name: str
    email: str
    age: Optional[int]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "age": self.age,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @classmethod
    def from_row(cls, row):
        """从数据库行转换为 User 对象"""
        return cls(
            id=row[0],
            name=row[1],
            email=row[2],
            age=row[3],
            created_at=row[4],
            updated_at=row[5],
        )
