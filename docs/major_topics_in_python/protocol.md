핵심부터 말하면 `Protocol`은 다른 클래스를 직접 제어하거나 실행을 막지 않습니다.

> `Protocol`은 “이 역할을 하려면 이런 메서드를 가지고 있어야 한다”는 타입 계약을 정의하고, mypy나 Pyright 같은 정적 타입 검사기가 그 계약을 확인하도록 합니다.

그래서 `python app.py`로 실행만 하면 잘못된 구현도 바로 에러가 나지 않을 수 있습니다.

# 1. `Protocol`이 정의하는 계약

먼저 indentation을 정리하면 다음 코드입니다.

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

`Parser`의 의미는 다음과 같습니다.

> Parser 역할을 하는 객체는 `parse()` 메서드를 가져야 한다.  
> `parse()`는 문자열을 입력받고 `Record`를 반환해야 한다.

```text
method 이름: parse
입력:        raw: str
출력:        Record
```

`Sink`의 의미는:

> Sink 역할을 하는 객체는 `write()` 메서드를 가져야 한다.  
> `write()`는 `Record`를 받고 반환값은 없어야 한다.

# 2. 올바른 구현

```python
class StubParser:
    def parse(self, raw: str) -> Record:
        return Record(
            record_id=raw,
            value=100,
        )
```

`StubParser`는 `Parser`를 직접 상속하지 않았습니다.

그런데도 다음 조건을 만족합니다.

```text
✓ parse라는 메서드가 있음
✓ str을 받음
✓ Record를 반환함
```

따라서 타입 검사기는 `StubParser`가 `Parser` 역할을 할 수 있다고 판단합니다.

이것을 structural typing이라고 합니다.

> 어떤 클래스를 상속했는지가 아니라, 필요한 구조와 동작을 가지고 있는지를 확인한다.

# 3. 잘못된 반환 타입을 사용하면?

다음 구현은 잘못됐습니다.

```python
class BadParser:
    def parse(self, raw: str) -> None:
        print(raw)
```

`Parser`가 요구하는 반환 타입은 `Record`입니다.

```python
class Parser(Protocol):
    def parse(self, raw: str) -> Record:
        ...
```

그런데 `BadParser`는 `None`을 반환합니다.

```python
class BadParser:
    def parse(self, raw: str) -> None:
        ...
```

하지만 `BadParser` 클래스를 정의하는 순간 Python이 에러를 발생시키지는 않습니다.

```python
bad_parser = BadParser()
```

이것도 실행됩니다.

```python
result = bad_parser.parse("invoice-001")
print(result)
# None
```

왜냐하면 Python의 type hint는 기본적으로 runtime validation이 아니기 때문입니다.

# 4. 언제 에러를 발견하는가?

`BadParser`를 `Parser`가 필요한 곳에 전달할 때 정적 타입 검사기가 발견합니다.

```python
def process(parser: Parser, raw: str) -> Record:
    return parser.parse(raw)
```

올바른 사용:

```python
process(StubParser(), "invoice-001")
```

잘못된 사용:

```python
process(BadParser(), "invoice-001")
```

mypy나 Pyright를 실행하면 대략 다음과 같은 오류를 보여줍니다.

```text
Argument of type "BadParser" cannot be assigned to parameter "parser"
"BadParser.parse" has an incompatible return type

Expected:
    (raw: str) -> Record

Received:
    (raw: str) -> None
```

중요한 것은 일반 Python 실행과 타입 검사를 구분하는 것입니다.

```text
python app.py → 코드를 실제로 실행
mypy app.py  → 타입 계약을 정적으로 검사
Pyright      → IDE 또는 명령행에서 타입 검사
```

`Protocol`의 제재는 runtime에서 객체 생성을 막는 방식이 아니라, 개발 중에 타입 검사기가 오류를 표시하는 방식입니다.

# 5. 타입이 기대되는 위치가 있어야 검사된다

이 부분이 특히 중요합니다.

다음 코드만 있다면:

```python
class BadParser:
    def parse(self, raw: str) -> None:
        ...
```

타입 검사기는 이것을 오류라고 볼 이유가 없습니다.

`BadParser`가 꼭 `Parser` 역할을 해야 한다고 선언하지 않았기 때문입니다. `None`을 반환하는 parser가 의도된 클래스일 수도 있습니다.

문제가 드러나려면 `Parser`가 필요한 위치에 연결돼야 합니다.

## 함수 parameter로 연결

```python
def process(parser: Parser) -> None:
    ...


process(BadParser())
```

여기서 타입 오류가 발생합니다.

## 변수 타입으로 연결

```python
parser: Parser = BadParser()
```

여기서도 타입 오류가 발생합니다.

## Constructor parameter로 연결

```python
class Pipeline:
    def __init__(self, parser: Parser, sink: Sink) -> None:
        self._parser = parser
        self._sink = sink
```

```python
pipeline = Pipeline(
    parser=BadParser(),
    sink=InMemorySink(),
)
```

여기서 타입 검사기가 `BadParser`가 `Parser` contract와 맞지 않는다고 알려줍니다.

즉, `Protocol`은 혼자서 모든 클래스를 감시하지 않습니다.

> `Parser` 타입이 요구되는 경계에 어떤 객체가 들어왔을 때 그 객체가 계약을 만족하는지 확인합니다.

# 6. 메서드 이름을 잘못 작성하면?

`parse`가 아니라 `parser`로 작성했다고 해보겠습니다.

```python
class WrongParser:
    def parser(self, raw: str) -> Record:
        return Record(raw, 100)
```

사람이 보기에는 비슷하지만 `Parser` contract에는 맞지 않습니다.

```python
parser: Parser = WrongParser()
```

타입 검사 결과는 대략 다음과 같습니다.

```text
WrongParser is incompatible with Parser
"parse" is missing
```

필요한 method 이름이 `parse`인데 `parser`만 있기 때문입니다.

# 7. 입력 타입이 잘못된 경우

```python
class IntegerParser:
    def parse(self, raw: int) -> Record:
        return Record(str(raw), 100)
```

Protocol은 문자열을 전달할 수 있어야 한다고 정의했습니다.

```python
class Parser(Protocol):
    def parse(self, raw: str) -> Record:
        ...
```

하지만 `IntegerParser`는 `int`만 받는다고 선언했습니다.

```python
parser: Parser = IntegerParser()
```

따라서 타입 검사기는 계약이 맞지 않는다고 판단합니다.

# 8. Pipeline에서 어떻게 보호되는가?

전체 예제를 보겠습니다.

```python
class InMemorySink:
    def __init__(self) -> None:
        self.records: list[Record] = []

    def write(self, record: Record) -> None:
        self.records.append(record)


class Pipeline:
    def __init__(self, parser: Parser, sink: Sink) -> None:
        self._parser = parser
        self._sink = sink

    def run(self, raw_values: list[str]) -> None:
        for raw in raw_values:
            record = self._parser.parse(raw)
            self._sink.write(record)
```

올바른 연결:

```python
pipeline = Pipeline(
    parser=StubParser(),
    sink=InMemorySink(),
)
```

타입의 흐름은 다음과 같습니다.

```text
raw: str
   ↓
Parser.parse(raw)
   ↓
Record
   ↓
Sink.write(record)
```

잘못된 연결:

```python
pipeline = Pipeline(
    parser=BadParser(),
    sink=InMemorySink(),
)
```

`BadParser.parse()`는 `None`을 반환합니다.

```text
raw: str
   ↓
BadParser.parse(raw)
   ↓
None
   ↓
Sink.write(None)  ← 계약 위반
```

타입 검사기가 Pipeline을 실행하기 전에 이 연결 오류를 찾는 것입니다.

# 9. 타입 검사 없이 실행하면 어떻게 되는가?

Python은 타입 힌트를 강제하지 않으므로 다음 코드가 실행될 수 있습니다.

```python
pipeline = Pipeline(
    parser=BadParser(),
    sink=InMemorySink(),
)

pipeline.run(["invoice-001"])
```

더 위험한 점은 현재 `InMemorySink`가 내부적으로 단순히 list에 추가하기 때문에 runtime error조차 발생하지 않을 수 있다는 것입니다.

```python
self.records.append(record)
```

Python list에는 `None`도 들어갈 수 있습니다.

결과:

```python
print(pipeline._sink.records)
# [None]
```

즉, 즉시 실패하지 않고 잘못된 데이터가 흘러갈 수 있습니다.

이것이 타입 검사기를 사용하는 이유입니다.

```text
타입 검사 없음:
잘못된 None이 pipeline 내부로 들어갈 수 있음

타입 검사 있음:
BadParser를 Pipeline에 연결하는 시점에 발견
```

# 10. 직접 상속하면 달라지는가?

명시적으로 `Parser`를 상속할 수도 있습니다.

```python
class StubParser(Parser):
    def parse(self, raw: str) -> Record:
        return Record(raw, 100)
```

잘못된 override:

```python
class BadParser(Parser):
    def parse(self, raw: str) -> None:
        return None
```

타입 검사기는 클래스 정의에서 더 직접적으로 오류를 표시할 수 있습니다.

```text
Return type "None" is incompatible with return type "Record"
```

하지만 이것도 기본적으로 정적 타입 검사입니다. Python runtime이 return type annotation을 보고 반환값을 검사하는 것은 아닙니다.

`Protocol`의 장점은 반드시 명시적으로 상속하지 않아도 된다는 것입니다.

```python
class StubParser:
    def parse(self, raw: str) -> Record:
        ...
```

구조만 맞으면 `Parser` 역할을 할 수 있습니다.

# 11. Runtime에서도 검사하고 싶다면?

`@runtime_checkable`을 사용할 수 있습니다.

```python
from typing import Protocol, runtime_checkable


@runtime_checkable
class Parser(Protocol):
    def parse(self, raw: str) -> Record:
        ...
```

이제:

```python
isinstance(StubParser(), Parser)
# True
```

메서드가 없는 객체는:

```python
class NoParser:
    pass


isinstance(NoParser(), Parser)
# False
```

하지만 큰 제한이 있습니다.

`runtime_checkable`은 기본적으로 필요한 attribute가 존재하는지를 검사할 뿐, method의 parameter와 return type을 완전하게 검사하지 않습니다.

```python
class BadParser:
    def parse(self, raw: str) -> None:
        return None
```

`parse` 메서드 자체는 존재하기 때문에:

```python
isinstance(BadParser(), Parser)
# True일 수 있음
```

`Record`를 실제로 반환하는지는 검사하지 않습니다.

따라서 `runtime_checkable`은 완전한 runtime type validation 도구가 아닙니다.

# 12. ABC는 runtime에서 막아주지 않나?

`ABC`와 `abstractmethod`를 사용하면 필수 메서드를 구현하지 않은 subclass의 생성을 막을 수 있습니다.

```python
from abc import ABC, abstractmethod


class ParserABC(ABC):
    @abstractmethod
    def parse(self, raw: str) -> Record:
        raise NotImplementedError
```

구현하지 않은 클래스:

```python
class MissingParser(ParserABC):
    pass
```

객체를 만들려고 하면 runtime error가 발생합니다.

```python
MissingParser()
```

```text
TypeError: Can't instantiate abstract class MissingParser
```

하지만 이것도 반환값이 실제로 `Record`인지까지 runtime에서 검사하지는 않습니다.

```python
class BadParser(ParserABC):
    def parse(self, raw: str) -> None:
        return None
```

메서드를 구현했기 때문에 객체 생성은 가능할 수 있습니다. 반환 타입 오류는 여전히 정적 타입 검사기의 역할입니다.

비교하면:

| 기능                         | Protocol       | ABC       |
| ---------------------------- | -------------- | --------- |
| 명시적 상속 필요             | 아니요         | 예        |
| 구조가 맞으면 호환           | 예             | 아니요    |
| 정적 타입 검사               | 강점           | 가능      |
| 누락 method로 객체 생성 차단 | 기본 목적 아님 | 가능      |
| 실제 반환값 runtime 검사     | 하지 않음      | 하지 않음 |

# 13. 실제로 어떻게 사용해야 하는가?

일반적인 workflow는 다음과 같습니다.

## 코드에 Protocol을 정의

```python
class Parser(Protocol):
    def parse(self, raw: str) -> Record:
        ...
```

## 사용하는 쪽에 타입을 명시

```python
class Pipeline:
    def __init__(self, parser: Parser) -> None:
        self._parser = parser
```

## 구현체 작성

```python
class JsonParser:
    def parse(self, raw: str) -> Record:
        ...
```

## IDE에서 Pyright를 사용하거나 mypy 실행

```text
mypy application.py
```

또는 프로젝트 전체:

```text
mypy src tests
```

CI에서도 type check를 실행할 수 있습니다.

```text
test
lint
type check
```

그래야 Protocol 계약 위반이 merge 전에 발견됩니다.

# 핵심 정리

`Protocol`은 다음처럼 작동하지 않습니다.

```text
Protocol이 다른 클래스를 감시한다
→ 잘못된 클래스 정의를 runtime에서 막는다
```

실제로는 다음처럼 작동합니다.

```text
Parser가 필요한 위치가 있다
→ StubParser를 그 위치에 전달한다
→ 타입 검사기가 StubParser의 구조를 확인한다
→ parse(str) -> Record 계약과 비교한다
→ 맞으면 통과, 다르면 type error를 표시한다
```

질문하신 경우:

```python
class BadParser:
    def parse(self, raw: str) -> None:
        ...
```

결론은 다음과 같습니다.

```text
Python으로 그냥 실행:
클래스 정의 가능, 객체 생성 가능

Parser 타입이 필요한 곳에 전달:
mypy/Pyright가 타입 오류로 표시

runtime_checkable:
parse 메서드 존재 여부 정도만 확인

실제 반환값 runtime 검증:
Protocol이 하지 않음
```

한 문장으로 정리하면:

> `Protocol`은 runtime 경찰이 아니라, 서로 다른 객체를 연결하기 전에 인터페이스가 맞는지 검사해주는 설계도이자 정적 타입 검사 계약입니다.
