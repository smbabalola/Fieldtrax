from sqlalchemy import Column, String, Integer, ForeignKey, Float

from sqlalchemy.orm import relationship
from app.models.base import Base, BaseDBModel

class MudEquipmentDetail(BaseDBModel):
    __tablename__ = 'mud_equipment_details'

    report_id = Column(String(50), ForeignKey('daily_reports.id'), nullable=False)
    mud_equipment_id = Column(String(50), ForeignKey('mud_equipments.id'), nullable=False)
    hours_run = Column(Integer, nullable=True)
    screen_sizes = Column(String(25), nullable=True)
    active_volume_lost = Column(Float, nullable=True)
    reserve_volume_lost = Column(Float, nullable=True)
    other = Column(Float, nullable=True)

    daily_report = relationship('DailyReport', back_populates='mud_equipment_details')
    mud_equipment = relationship('MudEquipment', back_populates='mud_equipment_details') 

    def __repr__(self):
        return f"<MudEquipmentDetail: {self.mud_equipment_id}>"