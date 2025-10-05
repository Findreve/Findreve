from pydantic import ConfigDict
from sqlmodel import SQLModel

class SQLModelBase(SQLModel):
    model_config = ConfigDict(use_attribute_docstrings=True)
