from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, text
from src.core.session import Base
import enum


class GenderEnum(str, enum.Enum):
    male = "male"
    female = "female"


class ProfessionEnum(str, enum.Enum):
    employer = "employer"
    unemployer = "unemployer"


class User(Base):
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    profile: Mapped["Profile"] = relationship(
        "Profile",
        back_populates="user",
        uselist=False,
        lazy="joined",
        cascade="all, delete-orphan",
    )


class Profile(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    last_name: Mapped[str | None]
    age: Mapped[int]
    gender: Mapped[GenderEnum] = mapped_column(
        default=GenderEnum.male, server_default=text("'male'")
    )
    profession: Mapped[ProfessionEnum]
    user: Mapped["User"] = relationship("User", back_populates="profile", uselist=False)
