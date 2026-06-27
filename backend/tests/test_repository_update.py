import pytest

from app.core.exceptions import NotFoundError
from app.repository.base_repository import BaseRepository


class DummySchema:
    def dict(self, exclude_none=True):
        return {"name": "x"}


class DummyQuery:
    def __init__(self, existing=True):
        self.updated = False
        self.existing = existing

    def filter(self, *args, **kwargs):
        return self

    def first(self):
        return self.existing and object()

    def update(self, data):
        self.updated = True
        return 0


class DummySession:
    def __init__(self, existing=True):
        self.query_obj = DummyQuery(existing=existing)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def query(self, model):
        return self.query_obj

    def commit(self):
        pass


class DummyModel:
    id = None


def test_update_raises_not_found_when_row_does_not_exist(monkeypatch):
    session = DummySession(existing=False)
    repository = BaseRepository(lambda: session, DummyModel)

    def fail_read_by_id(self, id):
        raise AssertionError("read_by_id should not be called when no row is updated")

    monkeypatch.setattr(repository, "read_by_id", fail_read_by_id)

    with pytest.raises(NotFoundError):
        repository.update(1, DummySchema())
