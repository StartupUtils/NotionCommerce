from pydantic import BaseModel


class Parent(BaseModel):
    type: str
    database_id: str = None
    page_id: str = None

    @property
    def id(self):
        return self.page_id if self.type == "page_id" else self.database_id


class ObjectProperty(BaseModel):
    type: str


class NotionObject(BaseModel):
    object: str = None
    id: str = None
    created_time: str = None
    last_edited_time: str = None
    parent: Parent = None
    properties: dict = None

