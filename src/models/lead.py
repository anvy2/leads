import enum

from sqlmodel import Field

from src.models.base import BaseModel


class LeadSource(enum.StrEnum):
    REFERRAL = "referral"
    WEBSITE = "website"
    COLD_CALL = "cold_call"
    EVENT = "event"


class LeadInterestLevel(enum.StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class LeadStatus(enum.StrEnum):
    NEW = "new"
    CLOSED = "closed"
    QUALIFIED = "qualified"
    CONTACTED = "contacted"


class SalesPerson(BaseModel, table=True):
    __tablename__: str = "salespersons"
    name: str = Field(primary_key=True, unique=True)


class Lead(BaseModel, table=True):
    __tablename__: str = "leads"
    lead_id: int = Field(primary_key=True, unique=True)
    name: str = Field()
    email: str = Field()
    source: LeadSource = Field()
    interest_level: LeadInterestLevel = Field()
    status: LeadStatus = Field()
    assigned_salesperson: str = Field(foreign_key="salespersons.name")
