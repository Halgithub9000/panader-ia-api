from sqlalchemy import Column, Integer, String, Numeric, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

from .database import Base

# --- SQLAlchemy Models (para la base de datos) ---


class ProductoDB(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    precio = Column(Numeric(10, 2), nullable=False)
    descripcion = Column(Text, nullable=True)

    pedido_productos = relationship(
        "PedidoProductoDB", back_populates="producto")


class PedidoDB(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    cliente = Column(String(255), nullable=False)
    total = Column(Numeric(10, 2), nullable=False)
    fecha = Column(DateTime, default=datetime.now)

    pedido_productos = relationship(
        "PedidoProductoDB", back_populates="pedido")


class PedidoProductoDB(Base):
    __tablename__ = "pedido_productos"

    pedido_id = Column(Integer, ForeignKey("pedidos.id"), primary_key=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), primary_key=True)
    cantidad = Column(Integer, nullable=False)

    pedido = relationship("PedidoDB", back_populates="pedido_productos")
    producto = relationship("ProductoDB", back_populates="pedido_productos")


# --- Pydantic Models (para la API FastAPI) ---

class ProductoBase(BaseModel):
    nombre: str
    precio: float
    descripcion: Optional[str] = None


class ProductoCreate(ProductoBase):
    pass


class Producto(ProductoBase):
    id: int

    class Config:
        from_attributes = True  # O from_orm = True en Pydantic v1.x


class PedidoProductoItem(BaseModel):
    producto_id: int
    cantidad: int


class PedidoCreate(BaseModel):
    cliente: str
    items: List[PedidoProductoItem]  # Lista de productos en el pedido


class Pedido(BaseModel):
    id: int
    cliente: str
    total: float
    fecha: datetime
    # Esto es una simplificación, idealmente se mostraría PedidoProductoItem con más detalles
    items: List[Producto]

    class Config:
        from_attributes = True  # O from_orm = True en Pydantic v1.x
