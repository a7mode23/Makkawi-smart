"""
Makkawi Smart - Router Model
"""
import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, ForeignKey
from app.database import Base


class ConnectionStatus(str, enum.Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    UNKNOWN = "unknown"


class Router(Base):
    __tablename__ = "routers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    vpn_ip_address = Column(String(45), nullable=False)
    api_username = Column(String(50), nullable=False)
    api_password = Column(String(255), nullable=False)
    api_port = Column(Integer, default=8728)
    connection_status = Column(
        Enum(ConnectionStatus), default=ConnectionStatus.UNKNOWN, nullable=False
    )
    is_active = Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_seen = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Router(id={self.id}, name='{self.name}', ip='{self.vpn_ip_address}')>"
