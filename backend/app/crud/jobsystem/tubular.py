from typing import List, Optional, Any
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.jobsystem.tubular import Casing, Liner, Drillstring, Tubular
from app.schemas.jobsystem.tubular import (
    TubularCreate,
    TubularUpdate,
    TubularResponse,
    CasingCreate,
    CasingUpdate,
    LinerCreate,
    LinerUpdate,
    DrillstringCreate,
    DrillstringUpdate,
    TubularCreate
)

class CRUDTubular(CRUDBase[Tubular, TubularCreate, TubularUpdate]):
    async def get_by_type(
        self, db: Session, *, tubulartype_id: str
    ) -> List[Tubular]:
        """Get tubulars by type"""
        return db.query(Tubular).filter(Tubular.tubulartype_id == tubulartype_id).all()

    async def get_by_thread_type(
        self, db: Session, *, thread: str
    ) -> List[Tubular]:
        """Get tubulars by thread type"""
        return db.query(Tubular).filter(Tubular.thread == thread).all()

    async def get_by_diameter_range(
        self, db: Session, *, min_od: float, max_od: float
    ) -> List[Tubular]:
        """Get tubulars within outer diameter range"""
        return db.query(Tubular).filter(Tubular.outer_diameter >= min_od, Tubular.outer_diameter <= max_od).all()

    async def get_by_depth_range(
        self, db: Session, *, min_depth: float, max_depth: float
    ) -> List[Tubular]:
        """Get tubulars within depth range"""
        return db.query(Tubular).filter(Tubular.start_depth >= min_depth, Tubular.end_depth <= max_depth).all()

def create_crud_tubular(model: Any) -> CRUDTubular:
    return CRUDTubular(model)

class CRUDCasing(CRUDTubular):
    def create(self, db: Session, *, obj_in: CasingCreate) -> Casing:
        db_obj = Tubular(tubulartype_id="casing", **obj_in.model_dump(exclude={"cement_top", "cement_yield"}))
        db.add(db_obj)
        db.flush()
        db_casing = Casing(id=db_obj.id, cement_top=obj_in.cement_top, cement_yield=obj_in.cement_yield)
        db.add(db_casing)
        db.commit()
        db.refresh(db_casing)
        return db_casing

    def update(self, db: Session, *, db_obj: Casing, obj_in: CasingUpdate) -> Casing:
        tubular_data = obj_in.model_dump(exclude={"cement_top", "cement_yield"})
        for key, value in tubular_data.items():
            setattr(db_obj, key, value)
        db.add(db_obj)
        db.flush()
        casing_data = obj_in.model_dump(include={"cement_top", "cement_yield"})
        for key, value in casing_data.items():
            setattr(db_obj, key, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> Casing:
        obj = db.query(Casing).filter(Casing.id == id).first()
        tubular = db.query(Tubular).filter(Tubular.id == id).first()
        db.delete(obj)
        db.delete(tubular)
        db.commit()
        return obj

    async def get_by_cement_top_range(
        self, db: Session, *, min_top: float, max_top: float
    ) -> List[Casing]:
        return db.query(Casing).filter(Casing.cement_top >= min_top, Casing.cement_top <= max_top).all()


class CRUDLiner(CRUDTubular):
    def create(self, db: Session, *, obj_in: LinerCreate) -> Liner:
        db_obj = Tubular(tubulartype_id="liner", **obj_in.model_dump(exclude={"liner_top", "liner_bottom"}))
        db.add(db_obj)
        db.flush()
        db_liner = Liner(id=db_obj.id, liner_top=obj_in.liner_top, liner_bottom=obj_in.liner_bottom)
        db.add(db_liner)
        db.commit()
        db.refresh(db_liner)
        return db_liner

    def update(self, db: Session, *, db_obj: Liner, obj_in: LinerUpdate) -> Liner:
        tubular_data = obj_in.model_dump(exclude={"liner_top", "liner_bottom"})
        for key, value in tubular_data.items():
            setattr(db_obj, key, value)
        db.add(db_obj)
        db.flush()
        liner_data = obj_in.model_dump(include={"liner_top", "liner_bottom"})
        for key, value in liner_data.items():
            setattr(db_obj, key, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> Liner:
        obj = db.query(Liner).filter(Liner.id == id).first()
        tubular = db.query(Tubular).filter(Tubular.id == id).first()
        db.delete(obj)
        db.delete(tubular)
        db.commit()
        return obj

    async def get_by_overlap_range(
        self, db: Session, *, min_overlap: float, max_overlap: float
    ) -> List[Liner]:
        return db.query(Liner).filter(Liner.liner_Overlap >= min_overlap, Liner.liner_Overlap <= max_overlap).all()


class CRUDDrillstring(CRUDTubular):
    def create(self, db: Session, *, obj_in: DrillstringCreate) -> Drillstring:
        db_obj = Tubular(tubulartype_id="drillstring", **obj_in.model_dump(exclude={"component_type"}))
        db.add(db_obj)
        db.flush()
        db_drillstring = Drillstring(id=db_obj.id, component_type=obj_in.component_type)
        db.add(db_drillstring)
        db.commit()
        db.refresh(db_drillstring)
        return db_drillstring

    def update(self, db: Session, *, db_obj: Drillstring, obj_in: DrillstringUpdate) -> Drillstring:
        tubular_data = obj_in.model_dump(exclude={"component_type"})
        for key, value in tubular_data.items():
            setattr(db_obj, key, value)
        db.add(db_obj)
        db.flush()
        drillstring_data = obj_in.model_dump(include={"component_type"})
        for key, value in drillstring_data.items():
            setattr(db_obj, key, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> Drillstring:
        obj = db.query(Drillstring).filter(Drillstring.id == id).first()
        tubular = db.query(Tubular).filter(Tubular.id == id).first()
        db.delete(obj)
        db.delete(tubular)
        db.commit()
        return obj

    async def get_by_component_type(
        self, db: Session, *, component_type: str
    ) -> List[Drillstring]:
        return db.query(Drillstring).filter(Drillstring.component_type == component_type).all()

crud_tubular = CRUDTubular(Tubular)
crud_casing = CRUDCasing(Tubular)
crud_liner = CRUDLiner(Tubular)
crud_drillstring = CRUDDrillstring(Tubular)