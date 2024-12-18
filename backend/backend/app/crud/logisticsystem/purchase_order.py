# File: backend/app/crud/logisticssystem/crud_purchase_order.py
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from app.crud.base import CRUDBase
from app.models.logisticsystem.purchase_order import PurchaseOrder
from app.schemas.logisticsystem.purchase_order import PurchaseOrderCreate, PurchaseOrderUpdate

class CRUDPurchaseOrder(CRUDBase[PurchaseOrder, PurchaseOrderCreate, PurchaseOrderUpdate]):
    async def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[PurchaseOrder]:
        """Get multiple purchase orders with pagination and ordering"""
        try:
            query = db.query(self.model)
            
            if filters:
                for key, value in filters.items():
                    if hasattr(self.model, key):
                        query = query.filter(getattr(self.model, key) == value)
            
            return (query.order_by(self.model.po_date.desc())
                        .offset(skip)
                        .limit(limit)
                        .all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    async def get_by_po_number(
        self,
        db: Session,
        *,
        po_number: str
    ) -> Optional[PurchaseOrder]:
        """Get purchase order by number"""
        try:
            return db.query(self.model).filter(
                self.model.po_number == po_number
            ).first()
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    async def get_by_well(
        self,
        db: Session,
        *,
        well_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[PurchaseOrder]:
        """Get purchase orders by well ID"""
        try:
            return (db.query(self.model)
                    .filter(self.model.well_id == well_id)
                    .order_by(self.model.po_date.desc())
                    .offset(skip)
                    .limit(limit)
                    .all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    async def get_by_supplier(
        self,
        db: Session,
        *,
        supplier_name: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[PurchaseOrder]:
        """Get purchase orders by supplier"""
        try:
            return (db.query(self.model)
                    .filter(self.model.supplier_name == supplier_name)
                    .order_by(self.model.po_date.desc())
                    .offset(skip)
                    .limit(limit)
                    .all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    async def get_by_date_range(
        self,
        db: Session,
        *,
        start_date: datetime,
        end_date: datetime,
        well_id: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[PurchaseOrder]:
        """Get purchase orders within a date range"""
        try:
            query = db.query(self.model).filter(
                self.model.po_date >= start_date,
                self.model.po_date <= end_date
            )
            
            if well_id:
                query = query.filter(self.model.well_id == well_id)
                
            return (query.order_by(self.model.po_date.desc())
                        .offset(skip)
                        .limit(limit)
                        .all())
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

crud_purchase_order = CRUDPurchaseOrder(PurchaseOrder)