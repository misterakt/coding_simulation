Senior Data Platform Engineer에게 필요한 OOP는 “상속 문법을 많이 아는 것”보다 다음 질문에 답할 수 있는 능력입니다.

```text
1. 이 객체의 책임은 무엇인가?
2. 어떤 상태를 객체가 소유해야 하는가?
3. 무엇을 변경 가능하게 하고 무엇을 고정할 것인가?
4. 외부 시스템과 내부 로직을 어떻게 분리할 것인가?
5. 구현체를 교체하고 테스트하기 쉬운가?
6. 실패와 resource lifecycle은 누가 책임지는가?
```

플랫폼 코드에서는 특히 **composition, interface, dependency injection, immutable value object, lifecycle 관리**가 중요합니다.

---

# 1. Class와 Object

클래스는 객체를 만들기 위한 설계이고, 객체는 그 설계로 생성된 실제 instance입니다.

```python
class Worker:
    def __init__(self, name: str) -> None:
        self.name = name

    def run(self) -> None:
        print(f"{self.name} is running")
```

각 객체는 독립적인 상태를 갖습니다.

```python
worker1 = Worker("worker-1")
worker2 = Worker("worker-2")

worker1.run()
worker2.run()
```

```text
Worker  → 클래스
worker1 → Worker의 첫 번째 객체
worker2 → Worker의 두 번째 객체
self    → 현재 method를 실행하는 객체
```

`worker1.run()`은 개념적으로 다음과 비슷합니다.

```python
Worker.run(worker1)
```

따라서 `self.name`은 현재 객체의 `name`입니다.

---

# 2. Instance attribute와 Class attribute

## Instance attribute

객체마다 별도로 존재하는 상태입니다.

```python
class Worker:
    def __init__(self, name: str) -> None:
        self.name = name
        self.processed = 0
```

```python
worker1 = Worker("worker-1")
worker2 = Worker("worker-2")

worker1.processed += 1

print(worker1.processed)  # 1
print(worker2.processed)  # 0
```

## Class attribute

모든 instance가 공유하는 클래스 수준의 값입니다.

```python
class Worker:
    worker_type = "batch"

    def __init__(self, name: str) -> None:
        self.name = name
```

```python
print(Worker.worker_type)
print(Worker("worker-1").worker_type)
```

상수나 클래스 전체에 공통인 설정에 사용할 수 있습니다.

## 자주 발생하는 실수

Mutable object를 class attribute로 만들면 모든 instance가 공유합니다.

```python
class BadWorker:
    tasks = []
```

```python
first = BadWorker()
second = BadWorker()

first.tasks.append("task-1")

print(second.tasks)
# ["task-1"]
```

대부분은 instance attribute로 만들어야 합니다.

```python
class Worker:
    def __init__(self) -> None:
        self.tasks: list[str] = []
```

---

# 3. Encapsulation: 상태와 규칙을 함께 관리하기

Encapsulation은 단순히 필드를 숨기는 것이 아닙니다.

> 객체가 자신의 상태와 그 상태를 유효하게 유지하는 규칙을 책임지는 것

다음 클래스에서는 `processed`와 `failed`를 누구나 마음대로 바꿀 수 있습니다.

```python
class JobStats:
    def __init__(self) -> None:
        self.processed = 0
        self.failed = 0
```

잘못된 상태도 만들 수 있습니다.

```python
stats = JobStats()
stats.failed = -100
```

객체가 상태 변경 규칙을 책임지게 만들 수 있습니다.

```python
class JobStats:
    def __init__(self) -> None:
        self._processed = 0
        self._failed = 0

    @property
    def processed(self) -> int:
        return self._processed

    @property
    def failed(self) -> int:
        return self._failed

    def record_success(self) -> None:
        self._processed += 1

    def record_failure(self) -> None:
        self._processed += 1
        self._failed += 1
```

사용자는 상태를 직접 조작하는 대신 의미 있는 행동을 호출합니다.

```python
stats = JobStats()

stats.record_success()
stats.record_failure()

print(stats.processed)  # 2
print(stats.failed)     # 1
```

Python에서 `_processed`는 강제 private이 아니라 다음 의미의 관례입니다.

> 이 값은 내부 구현이므로 외부에서 직접 변경하지 마세요.

Senior-level 설계에서는 getter/setter를 무조건 만드는 것보다, `record_success()`처럼 도메인 의미가 있는 동작을 제공하는 것이 좋습니다.

---

# 4. Dataclass와 Value Object

데이터 자체를 표현하는 객체에는 dataclass가 유용합니다.

```python
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PartitionKey:
    table: str
    partition_date: str

    def __post_init__(self) -> None:
        if not self.table:
            raise ValueError("table must not be empty")

        if not self.partition_date:
            raise ValueError("partition_date must not be empty")
```

이 객체는 변경되는 상태가 아니라 특정 partition을 나타내는 값입니다.

```python
key = PartitionKey(
    table="invoices",
    partition_date="2026-01-01",
)
```

다음은 가능합니다.

```python
print(key.table)
use_partition(key)
```

기존 객체 변경은 불가능합니다.

```python
key.table = "payments"  # FrozenInstanceError
```

다른 partition이 필요하다면 새로운 객체를 만듭니다.

```python
next_key = PartitionKey(
    table="invoices",
    partition_date="2026-01-02",
)
```

Value object는 보통 다음과 같은 성질을 가집니다.

- 자신의 필드 값으로 의미가 결정됨
- 같은 값을 가지면 같은 것으로 비교 가능
- 생성 후 변경되지 않는 편이 안전함
- validation을 통해 잘못된 상태를 방지함

적합한 예:

- `PartitionKey`
- `Record`
- `JobConfig`
- `ValidationError`
- `DateRange`
- `Checkpoint`

반면 계속 누적되는 통계는 mutable하게 만드는 것이 자연스럽습니다.

```python
@dataclass
class ProcessingStats:
    processed: int = 0
    succeeded: int = 0
    failed: int = 0
```

즉, 모든 dataclass가 `frozen=True`여야 하는 것은 아닙니다.

---

# 5. Abstraction: 필요한 동작만 정의하기

데이터 플랫폼에서는 source와 sink 구현이 자주 바뀝니다.

```text
Source: file, S3, Kafka, API
Sink: database, object storage, message queue
```

Pipeline이 특정 구현에 직접 의존하면 교체와 테스트가 어려워집니다.

```python
class Pipeline:
    def __init__(self) -> None:
        self._sink = ProductionDatabaseSink()
```

Python에서는 `Protocol`을 사용해 필요한 동작을 정의할 수 있습니다.

```python
from typing import Protocol


class Sink(Protocol):
    def write(self, record: "Record") -> None:
        ...
```

의미는 다음과 같습니다.

> `write(Record) -> None`을 제공하는 객체라면 Sink 역할을 수행할 수 있다.

구현 클래스가 `Sink`를 직접 상속할 필요도 없습니다.

```python
class DatabaseSink:
    def write(self, record: "Record") -> None:
        print(f"Writing {record.record_id} to database")
```

```python
class FileSink:
    def write(self, record: "Record") -> None:
        print(f"Writing {record.record_id} to file")
```

두 클래스 모두 `write()` contract를 만족하므로 `Sink`로 사용할 수 있습니다.

---

# 6. Polymorphism: 같은 인터페이스, 다른 동작

Polymorphism은 호출하는 쪽에서 구체적인 구현을 몰라도 동일한 방식으로 사용할 수 있다는 뜻입니다.

```python
def save_record(sink: Sink, record: "Record") -> None:
    sink.write(record)
```

다음 두 호출은 동일한 인터페이스를 사용합니다.

```python
save_record(DatabaseSink(), record)
save_record(FileSink(), record)
```

`save_record()`는 내부 구현이 database인지 file인지 알 필요가 없습니다.

```text
호출자가 아는 것:
sink.write(record)를 호출할 수 있다.

호출자가 몰라도 되는 것:
어느 DB를 쓰는가?
파일 형식은 무엇인가?
인증은 어떻게 하는가?
```

이 분리가 polymorphism의 실질적인 가치입니다.

---

# 7. Composition over Inheritance

Composition은 객체가 필요한 다른 객체를 내부에 가지고 협력하는 방식입니다.

```text
Pipeline has a Parser
Pipeline has a Sink
```

예:

```python
class Pipeline:
    def __init__(self, parser: "Parser", sink: Sink) -> None:
        self._parser = parser
        self._sink = sink
```

Pipeline이 Parser나 Sink를 상속하는 것이 아닙니다.

```text
Pipeline is a Sink    → 이상함
Pipeline has a Sink   → 자연스러움
```

상속:

```python
class JsonPipeline(BasePipeline):
    ...
```

Composition:

```python
pipeline = Pipeline(
    parser=JsonParser(),
    sink=DatabaseSink(),
)
```

Composition은 component를 조합하므로 변경하기 쉽습니다.

```python
json_to_db = Pipeline(
    parser=JsonParser(),
    sink=DatabaseSink(),
)

csv_to_file = Pipeline(
    parser=CsvParser(),
    sink=FileSink(),
)
```

Pipeline 코드는 그대로이고 parser와 sink만 바뀝니다.

## 상속은 언제 사용하는가?

진정한 `is-a` 관계이고 base class의 contract를 안전하게 지킬 수 있을 때 사용합니다.

```python
class PipelineError(Exception):
    pass


class ParseError(PipelineError):
    pass


class SinkError(PipelineError):
    pass
```

`ParseError`와 `SinkError`는 실제로 `PipelineError`의 한 종류이므로 상속 관계가 자연스럽습니다.

반면 단순한 코드 재사용만을 위해 깊은 상속 구조를 만드는 것은 피하는 편이 좋습니다.

---

# 8. Dependency Injection

Dependency injection은 필요한 dependency를 객체 내부에서 직접 생성하지 않고 외부에서 전달하는 것입니다.

## 강하게 결합된 코드

```python
class Pipeline:
    def __init__(self) -> None:
        self._parser = JsonParser()
        self._sink = DatabaseSink()
```

문제점:

- JSON 외 다른 parser를 사용하기 어려움
- 실제 DB 없이 테스트하기 어려움
- Pipeline이 orchestration뿐 아니라 구현 선택까지 책임짐

## Dependency를 전달하는 코드

```python
class Pipeline:
    def __init__(self, parser: "Parser", sink: Sink) -> None:
        self._parser = parser
        self._sink = sink
```

사용:

```python
pipeline = Pipeline(
    parser=JsonParser(),
    sink=DatabaseSink(),
)
```

테스트:

```python
pipeline = Pipeline(
    parser=StubParser(),
    sink=InMemorySink(),
)
```

Dependency injection의 본질은 framework가 아닙니다.

> 객체가 필요한 협력자를 외부에서 받는 것

이를 통해 production 구현과 test 구현을 쉽게 교체할 수 있습니다.

---

# 9. Testability와 Test Double

외부 시스템에 의존하는 코드는 가짜 구현을 넣을 수 있어야 테스트하기 쉽습니다.

```python
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Record:
    record_id: str
    value: int


class Parser(Protocol):
    def parse(self, raw: str) -> Record:
        ...


class Sink(Protocol):
    def write(self, record: Record) -> None:
        ...
```

테스트용 구현:

```python
class StubParser:
    def parse(self, raw: str) -> Record:
        return Record(
            record_id=raw,
            value=100,
        )


class InMemorySink:
    def __init__(self) -> None:
        self.records: list[Record] = []

    def write(self, record: Record) -> None:
        self.records.append(record)
```

Pipeline:

```python
from collections.abc import Iterable


class Pipeline:
    def __init__(self, parser: Parser, sink: Sink) -> None:
        self._parser = parser
        self._sink = sink

    def run(self, lines: Iterable[str]) -> int:
        processed = 0

        for line in lines:
            record = self._parser.parse(line)
            self._sink.write(record)
            processed += 1

        return processed
```

테스트:

```python
def test_pipeline_writes_all_records() -> None:
    sink = InMemorySink()

    pipeline = Pipeline(
        parser=StubParser(),
        sink=sink,
    )

    processed = pipeline.run(["record-1", "record-2"])

    assert processed == 2
    assert sink.records == [
        Record(record_id="record-1", value=100),
        Record(record_id="record-2", value=100),
    ]
```

실제 DB를 실행하지 않고도 Pipeline의 책임을 테스트했습니다.

```text
StubParser
→ 입력을 예측 가능한 Record로 변환

InMemorySink
→ 저장 요청을 memory에 기록

Pipeline test
→ parser 결과를 sink에 전달했는지 검증
```

이것이 OOP와 테스트가 연결되는 지점입니다.

---

# 10. Method 종류

## Instance method

객체 상태를 사용하거나 변경합니다.

```python
class Worker:
    def __init__(self) -> None:
        self.processed = 0

    def process(self) -> None:
        self.processed += 1
```

첫 번째 parameter는 `self`입니다.

## Class method

클래스 자체를 받고 alternative constructor에 자주 사용합니다.

```python
@dataclass
class JobConfig:
    batch_size: int
    timeout_seconds: int

    @classmethod
    def from_dict(cls, values: dict[str, int]) -> "JobConfig":
        return cls(
            batch_size=values["batch_size"],
            timeout_seconds=values["timeout_seconds"],
        )
```

사용:

```python
config = JobConfig.from_dict(
    {
        "batch_size": 100,
        "timeout_seconds": 30,
    }
)
```

`cls`는 현재 클래스를 의미합니다.

## Static method

객체나 클래스 상태가 필요 없는 관련 utility입니다.

```python
class JobName:
    @staticmethod
    def is_valid(value: str) -> bool:
        return bool(value.strip())
```

하지만 클래스와 밀접한 관계가 없다면 일반 함수가 더 간단합니다.

```python
def is_valid_job_name(value: str) -> bool:
    return bool(value.strip())
```

---

# 11. Property

`@property`는 method를 attribute처럼 읽게 합니다.

```python
class ProcessingStats:
    def __init__(self) -> None:
        self._processed = 0
        self._failed = 0

    @property
    def failure_rate(self) -> float:
        if self._processed == 0:
            return 0.0

        return self._failed / self._processed
```

사용:

```python
stats.failure_rate
```

호출자는 다음처럼 쓰지 않습니다.

```python
stats.failure_rate()
```

Property는 다음 상황에 적합합니다.

- 다른 상태에서 계산되는 값
- 읽기 전용으로 보여주고 싶은 값
- attribute 접근 뒤에 간단한 validation이 필요한 경우

단순히 Java 스타일의 getter/setter를 만들기 위해 남용할 필요는 없습니다.

---

# 12. Equality와 Hashability

Dataclass는 기본적으로 필드 값으로 equality를 비교합니다.

```python
@dataclass(frozen=True)
class PartitionKey:
    table: str
    partition_date: str
```

```python
first = PartitionKey("invoices", "2026-01-01")
second = PartitionKey("invoices", "2026-01-01")

print(first == second)
# True
```

중요한 규칙:

```text
a == b라면 hash(a) == hash(b)여야 한다.
```

Frozen value object는 set이나 dictionary key에 사용하기 좋습니다.

```python
completed = {
    PartitionKey("invoices", "2026-01-01"),
}
```

```python
key = PartitionKey("invoices", "2026-01-01")

print(key in completed)
# True
```

Mutable 객체를 dictionary key로 사용하면 저장 이후 의미가 변경될 수 있으므로 위험합니다.

---

# 13. Inheritance, `super()`, MRO

문법적으로는 알아야 하지만 데이터 플랫폼의 기본 설계 수단으로 먼저 선택하지는 않습니다.

```python
class BaseSink:
    def __init__(self, name: str) -> None:
        self.name = name


class FileSink(BaseSink):
    def __init__(self, name: str, path: str) -> None:
        super().__init__(name)
        self.path = path
```

`super()`는 method resolution order, 즉 MRO상 다음 구현을 호출합니다.

확인:

```python
print(FileSink.mro())
```

Multiple inheritance에서는 특히 MRO가 중요하지만, 일반적인 pipeline 설계에서는 깊고 복잡한 상속을 피하는 것이 좋습니다.

Senior 인터뷰에서 중요한 것은 다음 판단입니다.

> 상속은 강한 결합을 만들기 때문에 진짜 subtype 관계에만 사용하고, 구현 교체가 목적이라면 composition과 Protocol을 우선 검토하겠습니다.

---

# 14. Resource Lifecycle

플랫폼 객체는 파일, DB connection, lock 같은 resource를 다룰 수 있습니다. 생성만큼 정리 책임도 중요합니다.

```python
class ManagedFile:
    def __init__(self, path: str) -> None:
        self._path = path
        self._file = None

    def __enter__(self):
        self._file = open(self._path, "r")
        return self._file

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if self._file is not None:
            self._file.close()
```

사용:

```python
with ManagedFile("records.txt") as file:
    for line in file:
        process(line)
```

중간에 exception이 발생해도 `__exit__`가 호출됩니다.

실무에서는 파일 자체가 이미 context manager이므로 이렇게 사용하면 됩니다.

```python
with open("records.txt") as file:
    ...
```

핵심은 다음입니다.

> 이 객체가 resource를 열었다면 누가, 언제, 실패 시에도 어떻게 닫는가?

---

# 15. SOLID를 실무적으로 이해하기

SOLID를 암기식으로 설명하기보다 앞의 Pipeline 예제와 연결하는 것이 좋습니다.

## Single Responsibility

각 객체의 변경 이유를 하나로 제한합니다.

```text
Parser   → parsing 규칙 변경
Sink     → 저장 방식 변경
Pipeline → 처리 순서 변경
Record   → 데이터 모델 변경
```

## Open/Closed

Pipeline을 수정하지 않고 새로운 구현을 추가할 수 있습니다.

```python
Pipeline(CsvParser(), DatabaseSink())
Pipeline(JsonParser(), FileSink())
```

## Liskov Substitution

어떤 `Sink` 구현을 넣어도 `write()` contract를 지켜야 합니다.

예를 들어 어떤 Sink는 조용히 데이터를 버린다면 같은 contract라고 보기 어렵습니다.

## Interface Segregation

너무 큰 인터페이스를 강요하지 않습니다.

좋지 않은 예:

```python
class Storage(Protocol):
    def read(self): ...
    def write(self): ...
    def delete(self): ...
    def compact(self): ...
    def create_table(self): ...
```

Pipeline에 `write()`만 필요하다면 작은 인터페이스가 낫습니다.

```python
class Sink(Protocol):
    def write(self, record: Record) -> None:
        ...
```

## Dependency Inversion

상위 수준 Pipeline이 구체적인 `DatabaseSink`가 아니라 `Sink` abstraction에 의존합니다.

```python
class Pipeline:
    def __init__(self, sink: Sink) -> None:
        self._sink = sink
```

---

# 16. Platform Engineer에게 유용한 패턴

패턴 이름 자체보다 어떤 문제를 해결하는지가 중요합니다.

## Strategy

교체 가능한 정책입니다.

```text
RetryPolicy
PartitionStrategy
DeduplicationStrategy
SerializationStrategy
```

```python
class PartitionStrategy(Protocol):
    def partition_for(self, record: Record) -> PartitionKey:
        ...
```

## Adapter

외부 시스템의 서로 다른 API를 내부의 동일한 interface로 감쌉니다.

```text
S3 SDK ────┐
GCS SDK ───┼─→ ObjectStore interface
Azure SDK ─┘
```

## Factory

설정에 따라 적절한 구현을 생성합니다.

```python
def create_sink(kind: str) -> Sink:
    if kind == "file":
        return FileSink()

    if kind == "database":
        return DatabaseSink()

    raise ValueError(f"Unsupported sink: {kind}")
```

## Repository

저장소 접근을 도메인 로직에서 분리할 때 사용할 수 있습니다. 하지만 단순한 CRUD wrapper를 과도하게 만드는 것은 피합니다.

---

# 17. OOP에서 흔히 하는 실수

## God object

```python
class PipelineManager:
    # parsing
    # validation
    # retry
    # DB write
    # metrics
    # configuration
    # scheduling
```

한 클래스가 모든 책임을 가집니다.

## 과도한 상속

```text
BasePipeline
└─ CloudPipeline
   └─ AwsPipeline
      └─ S3JsonPipeline
         └─ RetryingS3JsonPipeline
```

작은 변경이 전체 계층에 영향을 줍니다.

## 필요 없는 interface

구현이 하나이고 교체·테스트 필요도 없는데 모든 것에 ABC와 Factory를 추가하면 복잡도만 늘어납니다.

## Dataclass를 단순 dictionary처럼 남용

도메인 의미나 안정된 schema가 없는 임시 데이터라면 dictionary가 더 간단할 수 있습니다.

## Constructor에서 외부 I/O 실행

```python
class Client:
    def __init__(self):
        self.connection = connect_to_database()
```

객체 생성이 느리고 실패 가능하며 테스트하기 어려워집니다. 가능하면 명시적인 lifecycle이나 dependency injection을 검토합니다.

## 모든 것을 mutable하게 만들기

여러 component가 동일한 객체를 변경하면 데이터 흐름과 bug 원인을 추적하기 어렵습니다.

## 모든 것을 frozen으로 만들기

통계, cache, worker state처럼 변경 자체가 책임인 객체까지 frozen으로 만들 필요는 없습니다.

---

# 18. 인터뷰에서 OOP 문제를 받았을 때 접근 순서

클래스부터 만들지 말고 다음 순서로 정리하세요.

```text
1. Use case
   시스템이 실제로 해야 하는 동작은 무엇인가?

2. Domain/value objects
   어떤 데이터가 고정된 의미를 갖는가?

3. Responsibilities
   parsing, validation, storage, orchestration을 누가 담당하는가?

4. Boundaries
   DB, API, file, queue 같은 외부 시스템은 어디인가?

5. Variation points
   무엇이 교체되거나 확장될 가능성이 있는가?

6. Failure/lifecycle
   exception, retry, cleanup은 누가 책임지는가?

7. Testability
   실제 외부 시스템 없이 어떻게 테스트할 것인가?
```

인터뷰에서 설명한다면:

> `Record`는 immutable value object로 표현하겠습니다. Parser와 Sink는 외부 구현이 교체될 수 있으므로 작은 Protocol로 정의하겠습니다. Pipeline은 두 component를 composition하고 constructor injection을 사용하겠습니다. 이렇게 하면 Pipeline orchestration을 실제 DB 없이 테스트할 수 있습니다.

이 정도면 OOP 개념을 나열하지 않고 설계 결정에 연결한 좋은 답변입니다.

# 최종 우선순위

Senior Data Platform Engineer라면 다음 순서로 확실히 이해하는 것을 추천합니다.

```text
1. Class, object, instance state
2. Encapsulation과 invariant
3. Dataclass와 mutable/immutable value object
4. Composition over inheritance
5. Protocol과 polymorphism
6. Dependency injection과 testability
7. Exception hierarchy와 lifecycle
8. Property, classmethod, staticmethod
9. Equality와 hashability
10. Inheritance, super, MRO
11. Strategy, Adapter, Factory
12. SOLID를 실제 trade-off에 적용
```

가장 중요한 한 문장으로 압축하면:

> 플랫폼 엔지니어에게 OOP는 클래스를 많이 만드는 기술이 아니라, 데이터·정책·외부 시스템·실행 흐름의 책임을 분리해서 변경과 테스트가 안전하도록 만드는 기술입니다.
