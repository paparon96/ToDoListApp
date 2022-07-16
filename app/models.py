from typing import List, Optional

import datetime

from sqlmodel import Field, Relationship, SQLModel


class TeamBase(SQLModel):
    name: str = Field(index=True)
    headquarters: str


class Team(TeamBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    items: List["ToDoListItem"] = Relationship(back_populates="team")


class TeamCreate(TeamBase):
    pass


class TeamRead(TeamBase):
    id: int


class TeamUpdate(SQLModel):
    id: Optional[int] = None
    name: Optional[str] = None
    headquarters: Optional[str] = None


class ToDoListItemBase(SQLModel):
    description: str = Field(index=True)
    priority: Optional[int] = Field(default=None, index=True)
    owner: str
    deadline: datetime.date = Field(default_factory=datetime.date.today,
                                        nullable=False)
    progress: str
    team_id: Optional[int] = Field(default=None, foreign_key="team.id")


class ToDoListItem(ToDoListItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    team: Optional[Team] = Relationship(back_populates="items")


class ToDoListItemCreate(ToDoListItemBase):
    pass


class ToDoListItemRead(ToDoListItemBase):
    id: int


class ToDoListItemUpdate(SQLModel):
    description: Optional[str] = None
    priority: Optional[int] = None
    owner: Optional[str] = None
    deadline: Optional[datetime.date] = None
    progress: Optional[str] = None
    team_id: Optional[int] = None


class ToDoListItemReadWithTeam(ToDoListItemRead):
    team: Optional[TeamRead] = None


class TeamReadWithItems(TeamRead):
    items: List[ToDoListItem] = []
