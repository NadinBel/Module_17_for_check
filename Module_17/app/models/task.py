from app.backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.models.user import User
class Task(Base):
    __tablename__ = 'task'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    priority = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    user_id = Column(String, ForeignKey('users.id'), nullable=False, index=True, onupdate='CASCADE')
    slug = Column(String, unique=True, index=True)

from sqlalchemy.schema import CreateTable
print(CreateTable(Task.__table__))