`dataclass`를 가장 쉽게 이해하면 다음과 같습니다.

> 데이터를 담는 클래스를 만들 때 반복적으로 작성하는 `__init__`, `__repr__`, `__eq__` 등을 Python이 자동으로 만들어주는 기능

Data Engineer 관점에서는 다음과 같은 “값을 표현하는 객체”에 특히 유용합니다.

- 하나의 데이터 레코드
- 파티션 키
- 작업 설정
- 처리 결과와 통계
- validation error
- API 요청과 응답의 내부 표현

# 1. 일반 클래스로 작성하면

레코드 ID와 payload를 가진 클래스를 일반적인 방식으로 작성해 보겠습니다.

```python
class Record:
    def __init__(self, record_id: str, payload: bytes) -> None:
        self.record_id = record_id
        self.payload = payload

    def __repr__(self) -> str:
        return (
            f"Record("
            f"record_id={self.record_id!r}, "
            f"payload={self.payload!r})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Record):
            return NotImplemented

        return (
            self.record_id == other.record_id
            and self.payload == other.payload
        )
```

두 개의 필드만 정의하는데도 코드가 많습니다.

`dataclass`를 사용하면 다음처럼 줄어듭니다.

```python
from dataclasses import dataclass


@dataclass
class Record:
    record_id: str
    payload: bytes
```

Python이 필드를 보고 필요한 method를 자동으로 생성합니다.

개념적으로는 다음과 같은 `__init__`이 생성됩니다.

```python
def __init__(
    self,
    record_id: str,
    payload: bytes,
) -> None:
    self.record_id = record_id
    self.payload = payload
```

따라서 객체를 만들 수 있습니다.

```python
record = Record(
    record_id="invoice-001",
    payload=b"hello",
)
```

`b"hello"`는 문자열이 아니라 `bytes` 값입니다. 파일, network message, serialized payload처럼 binary 데이터를 표현할 때 사용합니다.

# 2. `@dataclass`는 무엇인가?

```python
@dataclass
class Record:
    ...
```

`@dataclass`는 decorator입니다. 아래에 정의된 `Record` 클래스를 받아서 데이터 클래스에 필요한 기능을 추가합니다.

대략적인 의미는 다음과 같습니다.

```python
Record = dataclass(Record)
```

`@dataclass`를 붙이면 기본적으로 다음 method들이 생성됩니다.

- `__init__`: 객체 생성
- `__repr__`: 객체를 읽기 쉽게 출력
- `__eq__`: 필드 값을 기준으로 객체 비교

## 자동 생성되는 `__init__`

```python
record = Record("invoice-001", b"hello")
```

또는 keyword argument로:

```python
record = Record(
    record_id="invoice-001",
    payload=b"hello",
)
```

실무에서는 필드가 여러 개라면 keyword argument가 더 명확합니다.

## 자동 생성되는 `__repr__`

```python
print(record)
```

결과:

```text
Record(record_id='invoice-001', payload=b'hello')
```

일반 클래스를 만들었을 때 볼 수 있는 다음 결과보다 유용합니다.

```text
<__main__.Record object at 0x...>
```

## 자동 생성되는 `__eq__`

두 객체의 타입과 필드 값이 같으면 같은 것으로 비교합니다.

```python
first = Record("invoice-001", b"hello")
second = Record("invoice-001", b"hello")

print(first == second)
# True
```

일반 클래스는 `__eq__`를 직접 구현하지 않으면 보통 서로 다른 객체로 판단합니다.

# 3. 원래 코드 전체

올바른 indentation으로 작성하면 다음과 같습니다.

```python
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Record:
    record_id: str
    payload: bytes

    def __post_init__(self) -> None:
        if not self.record_id:
            raise ValueError("record_id must not be empty")
```

자연어로 바꾸면:

> `Record`는 `record_id`와 `payload`를 가진 데이터 객체다. 생성된 후에는 필드를 재할당할 수 없고, 필드는 정해진 것만 사용할 수 있다. 객체가 생성될 때 `record_id`가 비어 있으면 `ValueError`를 발생시킨다.

하나씩 살펴보겠습니다.

# 4. 필드 선언

```python
record_id: str
payload: bytes
```

두 개의 dataclass field를 선언한 것입니다.

```text
record_id → 문자열을 기대
payload   → bytes를 기대
```

이 정보로 dataclass가 `__init__`을 생성합니다.

```python
record = Record(
    record_id="record-001",
    payload=b"data",
)
```

필드 순서대로 positional argument도 사용할 수 있습니다.

```python
record = Record("record-001", b"data")
```

하지만 다음 코드가 더 읽기 쉽습니다.

```python
record = Record(
    record_id="record-001",
    payload=b"data",
)
```

## 타입 힌트가 runtime validation을 하지는 않는다

다음 타입 힌트는:

```python
record_id: str
```

“문자열을 사용해야 한다”는 개발자와 타입 검사기를 위한 정보입니다. Python이 자동으로 실행 중 타입을 검사하지는 않습니다.

따라서 다음 코드도 생성 자체는 가능할 수 있습니다.

```python
record = Record(
    record_id=123,
    payload="not bytes",
)
```

mypy나 pyright는 이를 잘못된 사용으로 표시하지만, dataclass 자체가 자동으로 막아주지는 않습니다.

runtime validation이 필요하면 `__post_init__`에서 직접 검사하거나 Pydantic 같은 별도 도구를 사용합니다.

# 5. `__post_init__`이란?

dataclass가 자동 생성한 `__init__`이 필드 값을 설정한 후 호출하는 특별한 method입니다.

```python
def __post_init__(self) -> None:
    ...
```

실행 순서는 개념적으로 다음과 같습니다.

```text
Record(...) 호출
→ 자동 생성된 __init__ 실행
→ record_id 설정
→ payload 설정
→ __post_init__ 실행
→ 객체 생성 완료
```

현재 코드는:

```python
def __post_init__(self) -> None:
    if not self.record_id:
        raise ValueError("record_id must not be empty")
```

`record_id`가 비어 있으면 객체를 허용하지 않습니다.

정상:

```python
record = Record(
    record_id="record-001",
    payload=b"hello",
)
```

오류:

```python
record = Record(
    record_id="",
    payload=b"hello",
)
```

결과:

```text
ValueError: record_id must not be empty
```

즉, 잘못된 상태의 `Record` 객체가 만들어지는 것을 방지합니다.

## 좀 더 엄격하게 검증한다면

```python
@dataclass(frozen=True, slots=True)
class Record:
    record_id: str
    payload: bytes

    def __post_init__(self) -> None:
        if not isinstance(self.record_id, str):
            raise TypeError("record_id must be a string")

        if not self.record_id.strip():
            raise ValueError("record_id must not be empty")

        if not isinstance(self.payload, bytes):
            raise TypeError("payload must be bytes")
```

다만 내부 코드에서 타입 검사가 이미 보장된다면 모든 dataclass에 이런 runtime 검사를 반복할 필요는 없습니다. 외부 입력 경계에서 한 번 검증하고 내부에서는 타입 contract를 신뢰하는 설계도 가능합니다.

# 6. `frozen=True`란?

```python
@dataclass(frozen=True)
```

객체 생성 후 필드를 다시 할당하지 못하게 합니다.

```python
record = Record(
    record_id="record-001",
    payload=b"hello",
)

record.record_id = "record-002"
```

결과:

```text
FrozenInstanceError
```

왜 이렇게 할까요?

`Record`가 생성된 후 내용이 갑자기 바뀌지 않게 하기 위해서입니다.

예를 들어 record를 여러 함수에 전달했는데 중간 함수가 ID를 변경하면 추적하기 어려운 버그가 생길 수 있습니다.

```python
def process(record: Record) -> None:
    record.record_id = "different-id"  # frozen이면 방지
```

따라서 `frozen=True`는 다음과 같은 value object에 잘 맞습니다.

- 레코드
- configuration snapshot
- partition key
- 좌표
- 날짜 범위
- 처리 결과

## 완전한 불변성을 보장하지는 않는다

`frozen=True`는 필드 재할당을 막지만 필드 내부 객체까지 모두 immutable하게 만들지는 않습니다.

```python
@dataclass(frozen=True)
class Batch:
    records: list[str]
```

다음 재할당은 안 됩니다.

```python
batch.records = ["new"]  # 오류
```

하지만 list 자체는 mutable하기 때문에 다음은 가능합니다.

```python
batch.records.append("new")
```

정말 불변하게 만들고 싶다면 `list` 대신 `tuple`을 사용할 수 있습니다.

```python
@dataclass(frozen=True)
class Batch:
    records: tuple[str, ...]
```

# 7. `slots=True`란?

일반적인 Python 객체는 필드들을 내부적으로 `__dict__`에 보관합니다.

```python
@dataclass
class Record:
    record_id: str
    payload: bytes
```

```python
record = Record("record-001", b"hello")

print(record.__dict__)
```

대략 다음처럼 나옵니다.

```python
{
    "record_id": "record-001",
    "payload": b"hello",
}
```

`__dict__`는 유연하지만 객체마다 dictionary가 필요합니다.

```python
@dataclass(slots=True)
```

를 사용하면 선언한 필드를 위한 고정된 저장 공간을 사용하고, 일반적인 instance `__dict__` 생성을 피할 수 있습니다.

장점:

- 객체당 memory overhead를 줄일 수 있음
- 선언하지 않은 attribute가 실수로 추가되는 것을 방지
- 경우에 따라 attribute access가 개선될 수 있음

예:

```python
record = Record("record-001", b"hello")

record.source = "api"
```

`source`가 선언되지 않았기 때문에 오류가 발생합니다.

```text
AttributeError
```

## 언제 유용한가?

수많은 작은 객체를 생성할 때 도움이 될 수 있습니다.

```text
Record 객체 10개       → 큰 차이 없을 수 있음
Record 객체 5,000,000개 → memory 차이가 중요할 수 있음
```

그러나 습관적으로 모든 클래스에 `slots=True`를 붙일 필요는 없습니다. 동적인 attribute가 필요하거나 특정 상속 구조가 있다면 제약이 될 수 있습니다.

먼저 단순한 `@dataclass`로 시작하고, 다음 상황에서 고려하는 것이 좋습니다.

- 객체가 매우 많이 생성됨
- 필드가 고정돼 있음
- 메모리 측정 결과 객체 overhead가 문제임
- dynamic attribute가 필요하지 않음

# 8. 이 객체가 만들어지는 전체 과정

다음 코드를 실행한다고 해보겠습니다.

```python
record = Record(
    record_id="record-001",
    payload=b"hello",
)
```

개념적으로는 다음 순서입니다.

```text
1. Record 객체 공간 생성
2. record_id에 "record-001" 할당
3. payload에 b"hello" 할당
4. __post_init__ 호출
5. record_id validation 통과
6. 완성된 Record 반환
```

다음 입력은:

```python
Record(
    record_id="",
    payload=b"hello",
)
```

이렇게 처리됩니다.

```text
1. 필드 할당
2. __post_init__ 실행
3. 빈 record_id 발견
4. ValueError 발생
5. 유효한 Record 객체를 호출자에게 반환하지 않음
```

# 9. 기본값 사용하기

필드에 기본값을 줄 수 있습니다.

```python
@dataclass
class Record:
    record_id: str
    payload: bytes
    source: str = "unknown"
```

이제 `source`를 생략할 수 있습니다.

```python
record = Record(
    record_id="record-001",
    payload=b"hello",
)

print(record.source)
# unknown
```

직접 전달할 수도 있습니다.

```python
record = Record(
    record_id="record-001",
    payload=b"hello",
    source="kafka",
)
```

주의할 점은 기본값이 없는 필드가 기본값이 있는 필드보다 먼저 나와야 한다는 것입니다.

올바른 순서:

```python
@dataclass
class Record:
    record_id: str
    payload: bytes
    source: str = "unknown"
```

잘못된 순서:

```python
@dataclass
class Record:
    source: str = "unknown"
    record_id: str
```

# 10. Mutable 기본값과 `default_factory`

다음처럼 list를 기본값으로 직접 사용하면 안 됩니다.

```python
@dataclass
class Batch:
    records: list[Record] = []  # 잘못된 방식
```

여러 객체가 같은 list를 공유할 위험이 있기 때문입니다. Dataclass는 이런 일반적인 실수를 방지하기 위해 오류를 발생시킵니다.

`field(default_factory=...)`를 사용합니다.

```python
from dataclasses import dataclass, field


@dataclass
class Batch:
    batch_id: str
    records: list[Record] = field(default_factory=list)
```

각 `Batch` 객체마다 새로운 list가 생성됩니다.

```python
first = Batch(batch_id="batch-1")
second = Batch(batch_id="batch-2")

first.records.append(
    Record("record-001", b"hello")
)

print(first.records)
# [Record(...)]

print(second.records)
# []
```

이 문법은 반드시 기억하는 것이 좋습니다.

```python
field(default_factory=list)
field(default_factory=dict)
field(default_factory=set)
```

# 11. 자주 사용하는 `field()` 옵션

```python
from dataclasses import dataclass, field
```

## 출력에서 감추기

비밀번호나 큰 payload를 `repr`에서 제외할 수 있습니다.

```python
@dataclass
class Credentials:
    username: str
    password: str = field(repr=False)
```

```python
credentials = Credentials("user", "secret")
print(credentials)
```

결과:

```text
Credentials(username='user')
```

`repr=False`가 보안 전체를 보장하는 것은 아니지만, 로그에 실수로 표시될 가능성을 줄입니다.

## 비교에서 제외하기

```python
@dataclass
class JobResult:
    job_id: str
    row_count: int
    duration_seconds: float = field(compare=False)
```

두 객체를 비교할 때 `duration_seconds`를 제외합니다.

```python
first = JobResult("job-1", 100, 1.2)
second = JobResult("job-1", 100, 1.5)

print(first == second)
# True
```

이 옵션은 equality의 의미가 도메인적으로 명확할 때만 사용합니다.

## 생성자에서 제외하기

```python
@dataclass
class Batch:
    records: list[Record]
    record_count: int = field(init=False)

    def __post_init__(self) -> None:
        self.record_count = len(self.records)
```

호출자는 `record_count`를 전달하지 않습니다.

```python
batch = Batch(records=[record])
print(batch.record_count)
# 1
```

`record_count`는 다른 필드로부터 계산됩니다.

# 12. Data Engineer에게 유용한 예제

## Partition key

```python
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class PartitionKey:
    table: str
    partition_date: date
```

사용:

```python
partition = PartitionKey(
    table="invoices",
    partition_date=date(2026, 9, 8),
)
```

`frozen=True`이므로 dictionary와 set의 key로 사용하기에도 적합할 수 있습니다.

```python
processed_partitions = {
    PartitionKey("invoices", date(2026, 9, 8)),
}
```

## 처리 통계

```python
@dataclass
class ProcessingStats:
    processed: int = 0
    succeeded: int = 0
    failed: int = 0

    def record_success(self) -> None:
        self.processed += 1
        self.succeeded += 1

    def record_failure(self) -> None:
        self.processed += 1
        self.failed += 1
```

이 객체는 실행 중 상태가 바뀌어야 하므로 `frozen=True`를 사용하지 않습니다.

```python
stats = ProcessingStats()

stats.record_success()
stats.record_failure()

print(stats)
# ProcessingStats(processed=2, succeeded=1, failed=1)
```

이 예제가 중요한 이유는 `dataclass`라고 항상 frozen이어야 하는 것은 아니기 때문입니다.

- 변하지 않는 값 객체 → `frozen=True` 고려
- 실행 중 변하는 상태 객체 → 일반 dataclass 고려

## Validation error

```python
@dataclass(frozen=True, slots=True)
class ValidationError:
    record_index: int
    field: str
    code: str
    message: str
```

문자열만 반환하는 것보다 구조화된 오류를 반환할 수 있습니다.

```python
error = ValidationError(
    record_index=3,
    field="invoice_id",
    code="MISSING_VALUE",
    message="invoice_id is required",
)
```

# 13. Dataclass는 언제 쓰면 좋은가?

다음 질문에 “예”라면 좋은 후보입니다.

```text
이 클래스의 핵심 목적이 몇 개의 관련된 데이터를 함께 표현하는 것인가?
필드의 이름과 타입이 객체 의미의 중요한 부분인가?
필드 기준 equality/repr가 유용한가?
반복적인 __init__ 코드를 줄이고 싶은가?
```

대표적인 사용 사례:

- record/DTO
- configuration
- value object
- command/event
- statistics/result
- partition identifier
- validation error
- 내부 API의 구조화된 반환값

# 14. 언제 사용하지 않는 것이 좋은가?

## 단순히 값 하나만 전달하는 경우

```python
@dataclass
class UserId:
    value: str
```

도메인 의미가 특별하지 않다면 그냥 `str`로 충분할 수 있습니다.

## 외부 입력을 강하게 검증해야 하는 경우

외부 JSON에서 다음을 자동으로 변환하고 검증해야 한다면:

- 문자열을 날짜로 변환
- nested object validation
- 상세한 validation error
- serialization/deserialization

Pydantic 같은 validation library가 더 적합할 수 있습니다.

```text
dataclass → 내부 Python 데이터 모델에 적합
Pydantic  → 신뢰할 수 없는 외부 입력 검증에 강함
```

## 복잡한 lifecycle이나 resource를 관리하는 객체

DB connection pool, thread pool, network client 같은 객체는 단순한 data container가 아닙니다. 일반 class와 context manager가 더 자연스러울 수 있습니다.

## 필드 기반 equality가 적절하지 않은 경우

서비스 객체나 repository 객체를 모든 내부 필드로 비교하는 것은 의미가 없을 수 있습니다.

# 15. 일반 class, dataclass, dictionary 비교

| 선택           | 적합한 상황                                       |
| -------------- | ------------------------------------------------- |
| `dict`         | 일회성 데이터, 구조가 단순하거나 동적임           |
| `TypedDict`    | dictionary 형태를 유지하면서 정적 타입을 표현     |
| `dataclass`    | 명확한 내부 데이터 모델과 동작이 필요             |
| 일반 `class`   | 복잡한 lifecycle, behavior, custom initialization |
| Pydantic model | 외부 입력 parsing과 runtime validation이 중요     |

예를 들어:

```python
record["record_id"]
```

보다:

```python
record.record_id
```

가 도메인 객체로서 더 명확할 수 있습니다. 또한 dictionary에서는 key 오타가 런타임까지 발견되지 않을 수 있습니다.

```python
record["recrod_id"]  # 오타
```

Dataclass와 타입 검사기를 사용하면 IDE가 더 잘 도와줄 수 있습니다.

# 16. 주요 syntax 요약

## 가장 기본적인 형태

```python
@dataclass
class Record:
    record_id: str
    payload: bytes
```

## 기본값

```python
@dataclass
class Record:
    record_id: str
    payload: bytes = b""
```

## Mutable 기본값

```python
@dataclass
class Batch:
    records: list[Record] = field(default_factory=list)
```

## 생성 후 validation

```python
def __post_init__(self) -> None:
    if not self.record_id:
        raise ValueError("record_id must not be empty")
```

## 생성 후 변경 방지

```python
@dataclass(frozen=True)
```

## Instance memory 구조 최적화

```python
@dataclass(slots=True)
```

## 출력과 비교 제어

```python
secret: str = field(repr=False)
timestamp: float = field(compare=False)
```

# 마지막으로 원래 코드를 한 줄씩 읽으면

```python
from dataclasses import dataclass
```

> 표준 라이브러리에서 dataclass decorator를 가져온다.

```python
@dataclass(frozen=True, slots=True)
```

> 반복 코드를 자동 생성하고, 생성 후 필드 재할당을 막으며, 필드를 고정된 slot에 저장한다.

```python
class Record:
```

> `Record`라는 데이터 객체를 정의한다.

```python
record_id: str
payload: bytes
```

> 생성할 때 문자열 ID와 bytes payload가 필요하다.

```python
def __post_init__(self) -> None:
```

> 자동 생성된 `__init__`이 필드를 설정한 직후 실행한다.

```python
if not self.record_id:
```

> `record_id`가 빈 문자열처럼 falsy한 값인지 확인한다.

```python
raise ValueError("record_id must not be empty")
```

> 유효하지 않으면 객체 생성을 실패시킨다.

우선 실전에서 반드시 익혀야 할 dataclass 문법은 네 가지면 충분합니다.

```python
@dataclass
@dataclass(frozen=True)
field(default_factory=list)
def __post_init__(self): ...
```

`slots=True`, `repr=False`, `compare=False`, `order=True` 같은 옵션은 이 기본기를 이해한 다음 필요할 때 추가하면 됩니다.
