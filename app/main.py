from fastapi import FastAPI, Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy.orm import Session
from .database import get_db, engine, Base
from .models import ProductoDB, PedidoDB, PedidoProductoDB, Producto, PedidoCreate, PedidoProductoItem, Pedido

# Crear las tablas en la base de datos (solo la primera vez o si no existen)
# OJO: Esto es para desarrollo. En producción, usa migraciones (Alembic).
Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- Endpoints ---


@app.get("/productos", response_model=List[Producto])
def read_productos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtiene una lista de todos los productos disponibles.
    """
    productos = db.query(ProductoDB).offset(skip).limit(limit).all()
    if not productos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No se encontraron productos.")
    return productos


@app.post("/pedido", response_model=Pedido, status_code=status.HTTP_201_CREATED)
def create_pedido(pedido_data: PedidoCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo pedido. Calcula el total y guarda los ítems del pedido.
    """
    total_pedido = 0.0
    pedido_productos_db = []

    # Calcular el total y verificar la existencia de los productos
    for item in pedido_data.items:
        producto = db.query(ProductoDB).filter(
            ProductoDB.id == item.producto_id).first()
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {item.producto_id} no encontrado."
            )
        if item.cantidad <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"La cantidad para el producto {item.producto_id} debe ser mayor que cero."
            )
        total_pedido += float(producto.precio) * item.cantidad
        pedido_productos_db.append(
            PedidoProductoDB(producto_id=item.producto_id,
                             cantidad=item.cantidad)
        )

    # Crear el pedido principal
    db_pedido = PedidoDB(cliente=pedido_data.cliente, total=total_pedido)
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)  # Obtener el ID generado por la DB

    # Asociar los ítems al pedido recién creado
    for pp_db in pedido_productos_db:
        pp_db.pedido_id = db_pedido.id
        db.add(pp_db)
    db.commit()
    # Refrescar el pedido para incluir las relaciones si las usáramos directamente
    db.refresh(db_pedido)

    # Para la respuesta, obtener los productos asociados
    productos_en_pedido = []
    for item_data in pedido_data.items:
        producto_db = db.query(ProductoDB).filter(
            ProductoDB.id == item_data.producto_id).first()
        if producto_db:
            productos_en_pedido.append(Producto(id=producto_db.id, nombre=producto_db.nombre,
                                       precio=producto_db.precio, descripcion=producto_db.descripcion))

    # Construir la respuesta final del pedido
    response_pedido = Pedido(
        id=db_pedido.id,
        cliente=db_pedido.cliente,
        total=float(db_pedido.total),
        fecha=db_pedido.fecha,
        # Esta es una representación simplificada para el response_model
        items=productos_en_pedido
    )
    return response_pedido
