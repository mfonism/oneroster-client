from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Type, TypeVar

StatusT = TypeVar("StatusT", bound="Status")
RoleT = TypeVar("RoleT", bound="Role")
BaseEntityT = TypeVar("BaseEntityT", bound="BaseEntity")
UserT = TypeVar("UserT", bound="User")
ClassT = TypeVar("ClassT", bound="Class")


class Status(Enum):
    ACTIVE = "active"
    TO_BE_DELETED = "tobedeleted"

    @classmethod
    def decode(cls: Type[StatusT], data: str) -> StatusT:
        return cls(data)


class Role(Enum):
    TEACHER = "teacher"
    STUDENT = "student"

    @classmethod
    def decode(cls: Type[RoleT], data: str) -> RoleT:
        return cls(data)


class BaseEntity:
    def __init__(
        self,
        sourced_id: str,
        status: Status,
        last_modified: datetime,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.sourced_id = sourced_id
        self.status = status
        self.last_modified = last_modified
        self.metadata = metadata if metadata is not None else {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sourcedId": str(self.sourced_id),
            "status": self.status.value,
            "dateLastModified": self.last_modified.isoformat(),
            "metadata": self.metadata,
        }

    @classmethod
    def decode(cls: Type[BaseEntityT], data: Dict[str, Any]) -> BaseEntityT:
        return cls(
            sourced_id=data["sourcedId"],
            status=Status.decode(data["status"]),
            last_modified=datetime.fromisoformat(data["dateLastModified"]),
            metadata=data.get("metadata"),
        )


class User(BaseEntity):
    def __init__(
        self,
        sourced_id: str,
        status: Status,
        last_modified: datetime,
        active: bool,
        username: str,
        firstname: str,
        middlename: Optional[str],
        lastname: str,
        role: Role,
        email: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(sourced_id, status, last_modified, metadata)
        self.active = active
        self.username = username
        self.firstname = firstname
        self.middlename = middlename
        self.lastname = lastname
        self.role = role
        self.email = email

    def to_dict(self) -> Dict[str, Any]:
        return {
            **super().to_dict(),
            "enabledUser": str(self.active).lower(),
            "username": self.username,
            "givenname": self.firstname,
            "middleName": self.middlename,
            "familyName": self.lastname,
            "role": self.role.value,
            "email": self.email,
        }

    @classmethod
    def decode(cls: Type[UserT], data: Dict[str, Any]) -> UserT:
        base_entity = BaseEntity.decode(data)
        return cls(
            sourced_id=base_entity.sourced_id,
            status=base_entity.status,
            last_modified=base_entity.last_modified,
            active=data["enabledUser"].lower() == "true",
            username=data["username"],
            firstname=data["givenName"],
            middlename=data.get("middleName"),
            lastname=data["familyName"],
            role=Role.decode(data["role"]),
            email=data.get("email"),
            metadata=base_entity.metadata,
        )


class Class(BaseEntity):
    def __init__(
        self,
        sourced_id: str,
        status: Status,
        last_modified: datetime,
        name: str,
        periods: List[str],
        metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(sourced_id, status, last_modified, metadata)
        self.name = name
        self.periods = periods

    def to_dict(self) -> Dict[str, Any]:
        return {
            **super().to_dict(),
            "title": self.name,
            "periods": self.periods,
        }

    @classmethod
    def decode(cls: Type[ClassT], data: Dict[str, Any]) -> ClassT:
        base_entity = BaseEntity.decode(data)
        return cls(
            sourced_id=base_entity.sourced_id,
            status=base_entity.status,
            last_modified=base_entity.last_modified,
            name=data["title"],
            periods=data["periods"],
            metadata=base_entity.metadata,
        )
