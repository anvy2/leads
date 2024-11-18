import codecs
import csv
from typing import Annotated, Iterable

from fastapi import APIRouter, Depends, Request, Response, UploadFile, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import DB, get_db
from src.models.lead import Lead, LeadInterestLevel, LeadSource, LeadStatus
from src.services.lead import LeadService

router = APIRouter(prefix="/leads", tags=["leads"])


@router.post("/uploads")
async def lead_uploads(
    request: Request, db: Annotated[AsyncSession, Depends(get_db(DB.APP))], csv_file: UploadFile
) -> Response:
    lead_service = LeadService(db=db)
    # lead_records = await input_file.read()
    record_reader = csv.DictReader(codecs.iterdecode(csv_file.file, "utf-8"), delimiter=",")
    salesperson_records = []
    salesperson_seen = set()
    lead_records = []
    for record in record_reader:
        lead_records.append(
            lead_service.make_lead(
                lead_id=int(record["Lead ID"]),
                name=record["Lead Name"],
                email=record["Contact Information"],
                source=LeadSource(
                    record["Source"].lower().replace(" ", "_")
                ),  # I am assuming that the csv will have the same formatting but we can transform it to fit the formatting we are using
                interest_level=LeadInterestLevel(
                    record["Interest Level"].lower().replace(" ", "_")
                ),
                status=LeadStatus(record["Status"].lower().replace(" ", "_")),
                assigned_salesperson=record["Assigned Salesperson"],
            )
        )
        if record["Assigned Salesperson"].lower() not in salesperson_seen:
            salesperson_records.append(
                lead_service.make_salesperson(name=record["Assigned Salesperson"])
            )
            salesperson_seen.add(record["Assigned Salesperson"].lower())
    try:
        await lead_service.bulk_insert_salesperson(salesperson_records)
        await db.flush()
        await lead_service.bulk_insert_lead(lead_records)
        await db.commit()
    except IntegrityError as exc:
        return Response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=str(exc._message())
        )
    return Response()


@router.get("/all")
async def get_all_leads(
    db: Annotated[AsyncSession, Depends(get_db(DB.APP))],
    lead_status: LeadStatus | None = None,
    interest_level: LeadInterestLevel | None = None,
    lead_source: LeadSource | None = None,
) -> Iterable[Lead]:
    lead_service = LeadService(db=db)
    return await lead_service.get_all_leads(
        source=lead_source, interest_level=interest_level, status=lead_status
    )


@router.get("/all/pages")
async def get_all_leads_pages(
    db: Annotated[AsyncSession, Depends(get_db(DB.APP))],
    lead_status: LeadStatus | None = None,
    interest_level: LeadInterestLevel | None = None,
    lead_source: LeadSource | None = None,
    page: int = 1,
    limit: int = 20,
) -> Iterable[Lead]:
    lead_service = LeadService(db=db)
    return await lead_service.get_all_leads_paginated(
        source=lead_source,
        interest_level=interest_level,
        status=lead_status,
        limit=limit,
        page=page,
    )
