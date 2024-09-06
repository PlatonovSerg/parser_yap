from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declared_attr, declarative_base
from sqlalchemy import create_engine


class PreBase:

    @declared_attr
    def __tablename__(cls):
        # В моделях-наследниках свойство __tablename__ будет создано
        # из имени модели, переведённого в нижний регистр.
        # Возвращаем это значение.
        return cls.__name__.lower()

    # В моделях-наследниках будет создана колонка id типа Integer
    id = Column(Integer, primary_key=True)


# Декларативная база включит в себя атрибуты,
# описанные в классе PreBase.
Base = declarative_base(cls=PreBase)


# Наследники класса Base теперь автоматически получат
# приватный атрибут __tablename__ и атрибут id.
class Pep(Base):
    pep_number = Column(Integer, unique=True)
    name = Column(String(200))
    status = Column(String(20))


if __name__ == "__main__":
    engine = create_engine("sqlite:///sqlite.db", echo=True)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
