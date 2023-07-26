from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import relationship, mapped_column, Mapped

from src.database import Base


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(index=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(length=12), nullable=False)
    image: Mapped[str]
    registered_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)
    events = relationship('Event', back_populates='organizer')

    def __str__(self):
        return self.username
