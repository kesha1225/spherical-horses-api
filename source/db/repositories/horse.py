from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from source.db.models.horse import SphericalHorse


class HorseRepository(SQLAlchemyAsyncRepository[SphericalHorse]):
    model_type = SphericalHorse
