"""레포지터리 패턴 구현."""
from __future__ import annotations
from typing import Optional, Union, Literal, Any, cast
from contextlib import ContextDecorator
import abc

from sqlalchemy.orm import Session

from ..domain.models import Batch, OrderLine


class AbstractRepository(abc.ABC, ContextDecorator):
    """Repository 패턴 추상 인터페이스."""
    def __enter__(self) -> AbstractRepository:
        """`module`:contextmanager`의 필수 인터페이스 구현."""
        return self

    def __exit__(self,
                 typ: Any = None,
                 value: Any = None,
                 traceback: Any = None) -> Literal[False]:
        self.close()
        return False

    @abc.abstractmethod
    def close(self) -> None:
        pass

    @abc.abstractmethod
    def add(self, batch: Batch) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference: str) -> Optional[Batch]:
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> list[Batch]:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, item: Union[Batch, OrderLine]) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def clear(self) -> None:
        """레포지터리 내의 모든 엔티티 데이터를 지웁니다"""
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, db: Session):
        self.db = db

    def close(self) -> None:
        self.db.close()

    def add(self, batch: Batch) -> None:
        self.db.add(batch)
        self.db.commit()

    def get(self, reference: str) -> Optional[Batch]:
        return cast(
            Optional[Batch],
            self.db.query(Batch).filter_by(reference=reference).first())

    def delete(self, item: Union[Batch, OrderLine]) -> None:
        self.db.delete(item)
        self.db.commit()

    def list(self) -> list[Batch]:
        return cast(list[Batch], self.db.query(Batch).all())

    def clear(self) -> None:
        self.db.execute('DELETE FROM allocation')
        self.db.execute('DELETE FROM batch')
        self.db.execute('DELETE FROM order_line')
        self.db.commit()
