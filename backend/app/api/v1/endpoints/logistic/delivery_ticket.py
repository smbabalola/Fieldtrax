# File: backend/app/api/v1/endpoints/logistics/delivery_ticket.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.crud.logisticsystem.delivery_ticket import crud_delivery_ticket
from app.crud.logisticsystem.delivery_ticket_item import crud_delivery_ticket_item
from app.schemas.logisticsystem.delivery_ticket import (
    DeliveryTicketResponse,
    DeliveryTicketCreate,
    DeliveryTicketUpdate
)
from app.schemas.logisticsystem.delivery_ticket_item import (
    DeliveryTicketItemResponse,
    DeliveryTicketItemCreate
)
from app.core.deps import get_db, get_current_user
from app.schemas.authsystem.user import UserResponse as User

router = APIRouter()

@router.post("/", response_model=DeliveryTicketResponse)
async def create_delivery_ticket(
    ticket_in: DeliveryTicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new delivery ticket"""
    return await crud_delivery_ticket.create(db=db, obj_in=ticket_in)

@router.get("/{ticket_id}", response_model=DeliveryTicketResponse)
async def get_delivery_ticket(
    ticket_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get delivery ticket by ID"""
    ticket = await crud_delivery_ticket.get(db=db, id=ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Delivery ticket not found"
        )
    return ticket

@router.get("/number/{ticket_number}", response_model=DeliveryTicketResponse)
async def get_by_ticket_number(
    ticket_number: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get delivery ticket by number"""
    ticket = await crud_delivery_ticket.get_by_ticket_number(
        db=db,
        ticket_number=ticket_number
    )
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Delivery ticket not found"
        )
    return ticket

@router.get("/wellbore/{wellbore_id}", response_model=List[DeliveryTicketResponse])
async def get_wellbore_tickets(
    wellbore_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all delivery tickets for a wellbore"""
    return await crud_delivery_ticket.get_by_wellbore(db=db, wellbore_id=wellbore_id)

@router.get("/purchase-order/{po_id}", response_model=List[DeliveryTicketResponse])
async def get_po_tickets(
    po_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all delivery tickets for a purchase order"""
    return await crud_delivery_ticket.get_by_purchase_order(
        db=db,
        purchase_order_id=po_id
    )

@router.put("/{ticket_id}", response_model=DeliveryTicketResponse)
async def update_delivery_ticket(
    ticket_id: str,
    ticket_in: DeliveryTicketUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update delivery ticket"""
    ticket = await crud_delivery_ticket.get(db=db, id=ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Delivery ticket not found"
        )
    return await crud_delivery_ticket.update(db=db, db_obj=ticket, obj_in=ticket_in)

@router.post("/{ticket_id}/items", response_model=DeliveryTicketItemResponse)
async def add_ticket_item(
    ticket_id: str,
    item_in: DeliveryTicketItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add item to delivery ticket"""
    ticket = await crud_delivery_ticket.get(db=db, id=ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Delivery ticket not found"
        )
    return await crud_delivery_ticket_item.create(db=db, obj_in=item_in)

@router.get("/{ticket_id}/items", response_model=List[DeliveryTicketItemResponse])
async def get_ticket_items(
    ticket_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all items for a delivery ticket"""
    return await crud_delivery_ticket_item.get_by_delivery_ticket(
        db=db,
        delivery_ticket_id=ticket_id
    )

@router.get("/date-range", response_model=List[DeliveryTicketResponse])
async def get_tickets_by_date(
    start_date: datetime,
    end_date: datetime,
    wellbore_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get delivery tickets within date range"""
    return await crud_delivery_ticket.get_by_date_range(
        db=db,
        start_date=start_date,
        end_date=end_date,
        wellbore_id=wellbore_id
    )