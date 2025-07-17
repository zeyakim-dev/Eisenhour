from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TaskAttributes(BaseModel):
    """작업의 기본 속성을 정의하는 모델.

    Attributes:
        title (str): 작업의 제목.
        is_important (bool): 작업의 중요도. 기본값은 False.
        is_urgent (bool): 작업의 긴급도. 기본값은 False.
    """

    title: str = Field(..., description="작업의 제목")
    is_important: bool = Field(False, description="작업의 중요도 (True: 중요)")
    is_urgent: bool = Field(False, description="작업의 긴급도 (True: 긴급)")


class TaskCreate(TaskAttributes):
    """작업 생성 요청에 사용되는 모델.

    TaskAttributes를 상속하며 생성 시 클라이언트가 전달하는 데이터를 정의합니다.
    """

    pass


class TaskUpdate(BaseModel):
    """작업 수정 요청에 사용되는 모델.

    모든 필드는 Optional이며 부분 업데이트를 지원합니다.
    `model_dump(exclude_unset=True)`로 전달된 필드만 추출할 수 있습니다.

    Attributes:
        title (Optional[str]): 작업의 제목.
        is_important (Optional[bool]): 작업의 중요 여부.
        is_urgent (Optional[bool]): 작업의 긴급 여부.
        is_completed (Optional[bool]): 작업 완료 여부.
    """

    title: str | None = Field(None, description="작업의 제목")
    is_important: bool | None = Field(None, description="중요 여부")
    is_urgent: bool | None = Field(None, description="긴급 여부")
    is_completed: bool | None = Field(None, description="완료 여부")


class TaskInDB(TaskAttributes):
    """데이터베이스 저장 및 조회 시 사용하는 작업 모델.

    TaskAttributes를 상속하며, DB 관련 필드를 포함합니다.

    Attributes:
        id (int): 작업 고유 ID.
        created_at (datetime): 작업 생성 시각.
        completed_at (Optional[datetime]): 작업 완료 시각.
        user_id (int): 작업을 생성한 사용자 ID.
        is_completed (bool): 작업 완료 여부.
    """

    id: int
    created_at: datetime
    completed_at: datetime | None = None
    user_id: int
    is_completed: bool = Field(False, description="완료 여부")

    model_config = ConfigDict(from_attributes=True)


class TaskResponse(TaskInDB):
    """API 응답에 사용되는 작업 모델.

    TaskInDB를 그대로 상속하며, 클라이언트에게 반환되는 구조입니다.
    필요에 따라 사용자 정보 등 추가 가공 가능.
    """

    pass
