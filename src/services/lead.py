from datetime import datetime
from typing import Any, Iterable

from sqlalchemy import desc, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.lead import Lead, LeadInterestLevel, LeadSource, LeadStatus, SalesPerson


class LeadService:
    def __init__(self, db: AsyncSession):
        self.__db = db

    def make_lead(
        self,
        lead_id: int,
        name: str,
        email: str,
        source: LeadSource,
        interest_level: LeadInterestLevel,
        status: LeadStatus,
        assigned_salesperson: str,
    ) -> dict[str, Any]:
        return dict(
            created_at=datetime.now(),
            updated_at=datetime.now(),
            lead_id=lead_id,
            name=name,
            email=email,
            source=source,
            interest_level=interest_level,
            status=status,
            assigned_salesperson=assigned_salesperson,
        )

    def make_salesperson(self, name: str) -> dict[str, Any]:
        return dict(name=name, created_at=datetime.now(), updated_at=datetime.now())

    async def bulk_insert_salesperson(self, salespersons: Iterable[dict[str, Any]]):
        existing_salespersons_records = (await self.__db.scalars(select(SalesPerson))).all()
        existing_salespersons = set(
            [record.name.lower() for record in existing_salespersons_records]
        )
        records_to_insert = [
            record for record in salespersons if record["name"].lower() not in existing_salespersons
        ]
        if len(records_to_insert) > 0:
            await self.__db.execute(insert(SalesPerson).values(records_to_insert))

    async def bulk_insert_lead(self, leads: Iterable[dict[str, Any]]):
        if len(list(leads)) > 0:
            await self.__db.execute(insert(Lead).values(list(leads)))

    async def get_all_leads(
        self,
        source: LeadSource | None = None,
        interest_level: LeadInterestLevel | None = None,
        status: LeadStatus | None = None,
    ) -> Iterable[Lead]:
        query = select(Lead)
        if source is not None:
            query = query.where(Lead.source == source)  # pyright: ignore
        if interest_level is not None:
            query = query.where(Lead.interest_level == interest_level)  # pyright: ignore
        if status is not None:
            query = query.where(Lead.status == status)  # pyright: ignore
        return (await self.__db.scalars(query.order_by(desc(Lead.created_at)))).all()  # pyright: ignore

    async def get_all_leads_paginated(
        self,
        source: LeadSource | None = None,
        interest_level: LeadInterestLevel | None = None,
        status: LeadStatus | None = None,
        page: int = 1,
        limit: int = 20,
    ) -> Iterable[Lead]:
        page = max(page, 1)
        limit = max(5, limit)
        offset = (page - 1) * limit
        query = select(Lead).limit(limit).offset(offset)
        if source is not None:
            query = query.where(Lead.source == source)  # pyright: ignore
        if interest_level is not None:
            query = query.where(Lead.interest_level == interest_level)  # pyright: ignore
        if status is not None:
            query = query.where(Lead.status == status)  # pyright: ignore
        return (await self.__db.scalars(query.order_by(desc(Lead.created_at)))).all()  # pyright: ignore
