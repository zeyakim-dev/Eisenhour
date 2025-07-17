from datetime import datetime

import pytest
from pydantic import ValidationError

from src.models.task.schemas import TaskAttributes, TaskCreate, TaskInDB, TaskUpdate


def test_task_attributes_creation():
    """
    TaskAttributes 모델이 입력값으로 올바르게 생성되는지 확인합니다.

    Arrange: 제목, 중요도, 긴급도를 포함한 입력 데이터를 준비합니다.
    Act: TaskAttributes 인스턴스를 생성합니다.
    Assert: 각 필드가 기대한 값으로 설정되어 있는지 확인합니다.
    """
    task = TaskAttributes(title="할 일 테스트", is_important=True, is_urgent=False)

    assert task.title == "할 일 테스트"
    assert task.is_important is True
    assert task.is_urgent is False


def test_task_attributes_default_values():
    """
    TaskAttributes 모델이 기본값을 올바르게 적용하는지 확인합니다.

    Arrange: 필수 필드(title)만 포함된 입력 데이터를 준비합니다.
    Act: TaskAttributes 인스턴스를 생성합니다.
    Assert: is_important 및 is_urgent 필드가 기본값(False)으로 설정되어 있는지 확인합니다.
    """
    task = TaskAttributes(title="기본값 테스트")

    assert task.title == "기본값 테스트"
    assert task.is_important is False
    assert task.is_urgent is False


def test_task_attributes_validation_error():
    """
    필수 필드(title)가 누락될 경우 ValidationError가 발생하는지 확인합니다.

    Arrange: 필수 필드가 누락된 입력 데이터를 준비합니다.
    Act: TaskAttributes 인스턴스를 생성하면서 예외를 트리거합니다.
    Assert: ValidationError가 발생하는지 확인합니다.
    """
    with pytest.raises(ValidationError):
        TaskAttributes(is_important=True)


def test_task_create_inherits_attributes():
    """
    TaskCreate 모델이 TaskAttributes를 상속받아 올바르게 동작하는지 확인합니다.

    Arrange: 일부 필드만 포함된 입력 데이터를 준비합니다.
    Act: TaskCreate 인스턴스를 생성합니다.
    Assert: 누락된 필드는 기본값으로 설정되며, 제공된 필드는 반영되는지 확인합니다.
    """
    task = TaskCreate(title="생성 테스트", is_urgent=True)

    assert task.title == "생성 테스트"
    assert task.is_important is False
    assert task.is_urgent is True


def test_task_update_partial_fields():
    """
    TaskUpdate 모델이 부분 업데이트 용도로 작동하는지 확인합니다.

    Arrange: 일부 필드만 포함된 입력 데이터를 준비합니다.
    Act: TaskUpdate 인스턴스를 여러 조합으로 생성합니다.
    Assert: 제공된 필드는 설정되고, 나머지는 None으로 유지되는지 확인합니다.
    """
    update = TaskUpdate(is_completed=True)

    assert update.is_completed is True
    assert update.title is None
    assert update.is_important is None
    assert update.is_urgent is None

    partial = TaskUpdate(title="변경", is_important=True)
    assert partial.title == "변경"
    assert partial.is_important is True
    assert partial.is_urgent is None


def test_task_in_db_creation():
    """
    TaskInDB 모델이 모든 필드를 포함해 올바르게 생성되는지 확인합니다.

    Arrange: 전체 필드가 포함된 입력 데이터를 준비합니다.
    Act: TaskInDB 인스턴스를 생성합니다.
    Assert: 모든 필드가 입력값과 일치하는지 확인합니다.
    """
    now = datetime.now()
    task_data = {
        "id": 10,
        "title": "DB 저장 테스트",
        "is_important": True,
        "is_urgent": False,
        "created_at": now,
        "completed_at": None,
        "user_id": 999,
        "is_completed": False,
    }

    task = TaskInDB(**task_data)

    assert task.id == 10
    assert task.title == "DB 저장 테스트"
    assert task.created_at == now
    assert task.completed_at is None
    assert task.user_id == 999
    assert task.is_completed is False
