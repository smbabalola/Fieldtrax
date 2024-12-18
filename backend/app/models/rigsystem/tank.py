from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship


from app.models.base import Base, BaseDBModel

class Tank(BaseDBModel):
    __tablename__ = 'tanks'

    rig_id = Column(String(50), ForeignKey('rigs.id'), nullable=False)
    tank_name = Column(String(10), nullable=True)
    capacity = Column(Float, nullable=True)
    shape = Column(String(20), nullable=True)
    length = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    width_top = Column(Float, nullable=True)
    width_bottom = Column(Float, nullable=True)

    rig = relationship('Rig', back_populates='tanks') 

    def __repr__(self):
        return f"<Tank: {self.tank_name}>"
