from sqlalchemy.orm import Mapped, mapped_column

from source.db.models.extensions import BaseTable


class SphericalHorse(BaseTable):
    __tablename__ = "spherical_horses"

    name: Mapped[str] = mapped_column(index=True)
    radius: Mapped[float]
    color: Mapped[str]
