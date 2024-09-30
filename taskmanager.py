from datetime import datetime
from tasklist import Task, TaskStatus
import json

class TaskManager:
    __database_path = "data.json"
    __last_id = 0
    __buffer = list()

    @property
    def last_id(self):
        return self.__last_id

    @property
    def database_path(self) -> str:
        return self.__database_path
    
    @property
    def buffer(self) -> list:
        return self.__buffer
    
    @database_path.setter
    def database_path(self, path) -> None:
        assert len(path) > 0, "The database path can't be nothing"
        self.__database_path = path

    def __init__(self):
        try:
            with open(self.__database_path, "r") as f:
                self.__buffer = json.loads(f.read())
                self.__last_id = max([x["id"] for x in self.__buffer])
        except Exception:
            print(f"The file {self.__database_path} was not found or isn't valid. Trying to create a new one...")
            
            try:
                with open(self.__database_path, "x") as f:
                    f.write(json.dumps(self.__buffer))
            except FileExistsError:
                    with open(self.__database_path, "w") as f:
                        f.write(json.dumps(self.__buffer))
        
    def save(self, task: Task) -> bool:
        if task.get_id() == 0:
            self.__last_id += 1
            task.set_id(self.__last_id)
        self.__buffer.append(task.to_dict())
        print(f"Task added successfully (ID: {task.get_id()})")
        return True

    def list(self, param: TaskStatus=None) -> None:
        try:
            for task in self.__buffer:
                if param is None or param.value == task["status"]:
                    print(
                        f"ID: {task["id"]}",
                        f"Description: {task["description"]}",
                        f"Status: {task["status"]}",
                        f"Created at: {task["created_at"]}",
                        f"Updated at: {task["updated_at"]}\n",
                        sep='\n'
                        )
        except KeyError:
            print(f"The file {self.__database_path} was edited and corrupted. Try to fix it manually")

    def delete(self, id: int) -> bool:
        try:
            assert id >= 1 and id <= self.__last_id, "The specified task id is not saved"
            
            task_to_delete = self.find_by_id(id)
            if task_to_delete is not None:
                print(task_to_delete)
                self.__buffer.remove(task_to_delete.to_dict())
                task_to_delete.set_status(TaskStatus.DELETED)
                print(f"Removing task\nID: {task_to_delete.get_id()}\t\tDescription: {task_to_delete.get_description()}\t\tStatus: {task_to_delete.get_status().value}")
                return True
            print(f"A task with id {id} was not found")
            return False
        except KeyError:
            print(f"The file {self.__database_path} was edited and corrupted. Try to fix it manually")

    def find_by_id(self, id: int) -> Task:
        try:
            assert id >= 1 and id <= self.__last_id, "The specified task id is not saved"
            
            for task in self.__buffer:
                if task["id"] == id:
                    created_at = datetime.strptime(task["created_at"], "%Y-%m-%d")
                    
                    if task["updated_at"] != "None":
                        updated_at = datetime.strptime(task["updated_at"], "%Y-%m-%d")
                    else:
                        updated_at = "Not updated"
                    status = TaskStatus._value2member_map_[task["status"]]
                    description = task["description"]
                    return Task(description, status, id, updated_at, created_at)
            print(f"A task with id {id} was not found")
            return None
        except KeyError:
            print(f"The file {self.__database_path} was edited and corrupted. Try to fix it manually")
    
    def update(self, id: int, description: str) -> bool:
        task = self.find_by_id(id)
        if task is None:
            return False
        index = self.__buffer.index(task.to_dict())
        task.set_description(description)
        self.__buffer[index] = task.to_dict()
        print(f"The task with id {id} was updated!")
        return True
    
    def update_status(self, id: int, status: TaskStatus) -> bool:
        task = self.find_by_id(id)
        if task is None:
            return False
        index = self.__buffer.index(task.to_dict())
        task.set_status(status)
        self.__buffer[index] = task.to_dict()
        print(f"The task with id {id} is marked as {status.value}!")
        return True

                
    def close(self):
        with open(self.__database_path, "w") as f:
            f.write(json.dumps(self.__buffer, indent=4))