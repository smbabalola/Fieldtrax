# File: backend/app/crud/base.py
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from app.db.base_class import Base

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        """
        self.model = model

    async def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """Get a single record by ID with error handling"""
        try:
            obj = db.query(self.model).filter(self.model.id == id).first()
            if not obj:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"{self.model.__name__} not found"
                )
            return obj
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    async def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> List[ModelType]:
        """Get multiple records with filtering, ordering and active status"""
        try:
            query = db.query(self.model)
            
            if filters:
                for key, value in filters.items():
                    if hasattr(self.model, key):
                        query = query.filter(getattr(self.model, key) == value)
            
            # Add is_active filter if the model has this attribute
            if is_active is not None and hasattr(self.model, 'is_active'):
                query = query.filter(self.model.is_active == is_active)
            
            if order_by and hasattr(self.model, order_by.lstrip('-')):
                if order_by.startswith('-'):
                    query = query.order_by(getattr(self.model, order_by[1:]).desc())
                else:
                    query = query.order_by(getattr(self.model, order_by).asc())
            else: 
                # Default ordering if order_by is not provided 
                query = query.order_by(self.model.id.asc())
            return query.offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    async def get_all(self, db: Session, order_by: str = "id") -> List[ModelType]:
        """Alias for get_multi method"""
        return await self.get_multi(db=db,
                                    order_by=order_by)

    async def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """Create a new record with error handling"""
        try:
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = self.model(**obj_in_data)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    async def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """Update a record with error handling"""
        try:
            obj_data = jsonable_encoder(db_obj)
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.dict(exclude_unset=True)
                
            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
                    
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    async def remove(self, db: Session, *, id: Any, soft_delete: bool = True) -> ModelType:
        """Delete a record with soft delete support"""
        try:
            obj = await self.get(db=db, id=id)
            
            if soft_delete and hasattr(obj, 'is_active'):
                obj.is_active = False
                db.add(obj)
            else:
                db.delete(obj)
                
            db.commit()
            return obj
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    # Add this alias method
    async def delete(self, db: Session, *, id: Any, soft_delete: bool = True) -> ModelType:
        """Alias for remove method for backward compatibility"""
        return await self.remove(db=db, id=id, soft_delete=soft_delete)

    async def count(
        self,
        db: Session,
        filters: Optional[Dict[str, Any]] = None
    ) -> int:
        """Count total records with optional filtering"""
        try:
            query = select(func.count()).select_from(self.model)
            
            if filters:
                for key, value in filters.items():
                    if hasattr(self.model, key):
                        query = query.where(getattr(self.model, key) == value)
                        
            return db.execute(query).scalar()
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )

    async def get_by_field(
        self,
        db: Session,
        field: str,
        value: Any
    ) -> Optional[ModelType]:
        """Get a record by any field"""
        try:
            if not hasattr(self.model, field):
                raise ValueError(f"Field {field} does not exist in model {self.model.__name__}")
            
            obj = db.query(self.model).filter(getattr(self.model, field) == value).first()
            if not obj:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"{self.model.__name__} not found"
                )
            return obj
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )


    async def get_by_type(
        self, 
        db: Session, 
        *,
        type_value: Any,
        type_field: Optional[str] = None
    ) -> Optional[ModelType]:
        """
        Get record by type field
        Args:
            db: Database session
            type_value: Value to search for
            type_field: Field name to search in. If not provided, 
                       will try to infer from model name and common patterns
        """
        try:
            # Infer type field if not provided
            if not type_field:
                model_name = self.model.__name__.lower()
                common_patterns = [
                    f'{model_name}_type',      # e.g., well_type
                    f'{model_name}_type_name',  # e.g., well_type_name
                    f'{model_name}_name',       # e.g., well_name
                    'type',                     # generic type field
                    'name',                     # generic name field
                    'code'                      # generic code field
                ]
                
                # Find the first matching field in the model
                for pattern in common_patterns:
                    if hasattr(self.model, pattern):
                        type_field = pattern
                        break
                
            if not type_field or not hasattr(self.model, type_field):
                raise ValueError(
                    f"Could not find appropriate type field in model {self.model.__name__}. "
                    f"Please specify the type_field parameter."
                )
            
            # Query the database
            obj = db.query(self.model).filter(
                getattr(self.model, type_field) == type_value
            ).first()
            
            if not obj:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"{self.model.__name__} with {type_field}='{type_value}' not found"
                )
                
            return obj
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )