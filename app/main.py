from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

from .models import (ToDoListItem, ToDoListItemCreate, ToDoListItemRead,
                    ToDoListItemUpdate, Team, TeamCreate, TeamRead, TeamUpdate,
                    ToDoListItemReadWithTeam, TeamReadWithItems)


sqlite_file_name = "app/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


def get_session():
    with Session(engine) as session:
        yield session


@app.post("/items/", response_model=ToDoListItemRead)
def create_item(*, session: Session = Depends(get_session),
                item: ToDoListItemCreate):
    db_item = ToDoListItem.from_orm(item)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


@app.get("/items/", response_model=List[ToDoListItemRead])
def read_items(*, session: Session = Depends(get_session),
               offset: int = 0, limit: int = Query(default=100, lte=100)):
    items = session.exec(select(ToDoListItem).offset(offset).limit(limit)).all()
    return items


@app.get("/items/{item_id}", response_model=ToDoListItemReadWithTeam)
def read_item(*, session: Session = Depends(get_session), item_id: int):
    item = session.get(ToDoListItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.get("/items/urgent/", response_model=List[ToDoListItemRead])
def read_urgent_items(*, session: Session = Depends(get_session), date: str,
                      offset: int = 0,
                      limit: int = Query(default=100, lte=100)):
    statement = select(ToDoListItem).where(ToDoListItem.deadline <= date)
    items = session.exec(statement.offset(offset).limit(limit)).all()
    return items


@app.patch("/items/{item_id}", response_model=ToDoListItemRead)
def update_item(*, session: Session = Depends(get_session),
                item_id: int, item: ToDoListItemUpdate):
    db_item = session.get(ToDoListItem, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    item_data = item.dict(exclude_unset=True)
    for key, value in item_data.items():
        setattr(db_item, key, value)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


@app.delete("/items/{item_id}")
def delete_item(*, session: Session = Depends(get_session), item_id: int):
    item = session.get(ToDoListItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    session.delete(item)
    session.commit()
    return {"ok": True}


@app.post("/teams/", response_model=TeamRead)
def create_team(*, session: Session = Depends(get_session), team: TeamCreate):
    db_team = Team.from_orm(team)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


@app.get("/teams/", response_model=List[TeamRead])
def read_teams(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    teams = session.exec(select(Team).offset(offset).limit(limit)).all()
    return teams


@app.get("/teams/{team_id}", response_model=TeamReadWithItems)
def read_team(*, team_id: int, session: Session = Depends(get_session)):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@app.patch("/teams/{team_id}", response_model=TeamRead)
def update_team(
    *,
    session: Session = Depends(get_session),
    team_id: int,
    team: TeamUpdate,
):
    db_team = session.get(Team, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    team_data = team.dict(exclude_unset=True)
    for key, value in team_data.items():
        setattr(db_team, key, value)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


@app.delete("/teams/{team_id}")
def delete_team(*, session: Session = Depends(get_session), team_id: int):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    session.delete(team)
    session.commit()
    return {"ok": True}
