from enum import Enum
from pydantic import BaseModel, Field


class Criticidad(str, Enum):
    baja = "baja"
    media = "media"
    alta = "alta"


class ExtraccionTecnica(BaseModel):
    tecnologias: list[str] = Field(
        min_length=1,
        description="Tecnologías, herramientas o servicios mencionados en el texto.",
    )
    nivel_de_criticidad: Criticidad = Field(
        description="Qué tan grave es la situación descrita: baja, media o alta."
    )
    resumen_tecnico: str = Field(
        description="Resumen técnico del texto en una o dos oraciones."
    )
