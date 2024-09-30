from datetime import datetime
from enum import Enum

class TaskStatus(Enum):
    TO_DO = "To Do"
    IN_PROGRESS = "In Progress"
    DONE = "Done"
    DELETED = "Deleted"

    @property
    def __dict__(self):
        return {self.__class__.__name__: self.value}

class Task:
    def __init__(
            self,
            description: str,
            status: TaskStatus,
            id: int=0,
            updated_at: datetime=None,
            created_at: datetime=None
        ):
        # Checking if there is no invalid data
        assert id >= 0, "The id must be a non-negative number"
        assert len(description) > 0, "The description can't be nothing"
        assert isinstance(status, TaskStatus), "The status has to be TODO, IN_PROGRESS or DONE from Task class"
    
        self.__id = id
        self.__description = description
        self.__status = status
        self.__updated_at = updated_at

        if created_at is None:
            self.__created_at = datetime.now()
        else:
            self.__created_at = created_at

    def get_id(self) -> int:
        return self.__id
    
    def get_description(self) -> str:
        return self.__description

    def get_update_time(self) -> datetime:
        return self.__updated_at
    
    def get_creation_time(self) -> datetime:
        return self.__created_at

    def get_status(self) -> TaskStatus:
        return self.__status
        
    
    def set_description(self, description: str) -> None:
        assert len(description) > 0, "The description can't be nothing"
        self.__description = description
        self.set_update_time(datetime.now())
    
    def set_id(self, id: int) -> None:
        assert id >= 0, "The id must be a non-negative number"
        self.__id = id
        self.set_update_time(datetime.now())
    
    def set_update_time(self, updated_at: datetime) -> None:
        self.__updated_at = updated_at

    def set_creation_time(self, created_at: datetime) -> None:
        self.__created_at = created_at
        self.set_update_time(datetime.now())
    
    def set_status(self, status: TaskStatus) -> None:
        assert isinstance(status, TaskStatus), "The status has to be TODO, IN_PROGRESS or DONE from Task class"
        self.__status = status
        self.set_update_time(datetime.now())
    
    def __repr__(self) -> str:
        return f"Task({self.__id}, \"{self.__description}\", {self.__status}, {self.__created_at.date()}, {self.__updated_at.date()})"
    
    def to_dict(self) -> dict:
        return {
            "id": self.__id,
            "description": self.__description,
            "status": self.__status.value,
            "created_at": f"{self.__created_at.year}-{self.__created_at.month}-{self.__created_at.day}",
            "updated_at": f"{self.__updated_at.year}-{self.__updated_at.month}-{self.__updated_at.day}"
        }