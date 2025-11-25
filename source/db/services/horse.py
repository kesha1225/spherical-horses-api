from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from source.db.models.horse import SphericalHorse
from source.db.repositories.horse import HorseRepository


class HorseService(SQLAlchemyAsyncRepositoryService[SphericalHorse]):
    repository_type = HorseRepository
