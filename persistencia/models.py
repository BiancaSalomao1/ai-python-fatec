
from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from datetime import datetime


@dataclass
class Extracao:

    nome_arquivo: str
    produtos: list[dict]
    data_extracao: str = field(
        default_factory=lambda: datetime.now().isoformat()
    )
