from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Categoria(Base):
    __tablename__ = "categorias"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    descripcion: Mapped[str | None] = mapped_column(String(80), nullable=True)

    equipos: Mapped[list["Equipo"]] = relationship(back_populates="categoria")


class Equipo(Base):
    __tablename__ = "equipos"
    __table_args__ = (
        CheckConstraint("precio_diario > 0", name="ck_equipo_precio"),
        CheckConstraint("stock_total >= 0", name="ck_stock_total"),
        CheckConstraint("stock_disponible >= 0", name="ck_stock_disponible"),
        CheckConstraint(
            "stock_disponible <= stock_total", name="ck_equipo_stock_disponible_valido"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    categoria_id: Mapped[int] = mapped_column(
        ForeignKey("categorias.id", ondelete="RESTRICT"), nullable=False
    )
    precio_diario: Mapped[float] = mapped_column(Float, nullable=False)
    stock_total: Mapped[int] = mapped_column(Integer, nullable=False)
    stock_disponible: Mapped[int] = mapped_column(Integer, nullable=False)
    tipo: Mapped[str] = mapped_column(String(50), nullable=False, default="general")

    categoria: Mapped["Categoria"] = relationship(back_populates="equipos")
    arriendos: Mapped[list["Arriendo"]] = relationship(back_populates="equipo")


class Cliente(Base):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    correo: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    telefono: Mapped[str | None] = mapped_column(String(30), nullable=True)

    arriendos: Mapped[list["Arriendo"]] = relationship(back_populates="cliente")


class Arriendo(Base):
    __tablename__ = "arriendos"
    __table_args__ = (
        CheckConstraint("cantidad > 0", name="ck_cantidad"),
        CheckConstraint("fecha_fin_prevista >= fecha_inicio", name="ck_fecha_valida"),
        CheckConstraint("estado IN ('ACTIVO', 'DEVUELTO')", name="ck_estado_arriendo"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    equipo_id: Mapped[int] = mapped_column(
        ForeignKey("equipos.id", ondelete="RESTRICT"), nullable=False
    )
    cliente_id: Mapped[int] = mapped_column(
        ForeignKey("clientes.id", ondelete="RESTRICT"), nullable=False
    )
    fecha_inicio: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    fecha_fin_prevista: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    estado: Mapped[str] = mapped_column(String(10), nullable=False, default="ACTIVO")
    fecha_devolucion: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    equipo: Mapped["Equipo"] = relationship(back_populates="arriendos")
    cliente: Mapped["Cliente"] = relationship(back_populates="arriendos")