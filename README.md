# py-to-ts-interfaces
### Python to TypeScript Interfaces

## What is this?

A script for converting Python dataclasses with type annotations to TypeScript interfaces. This is a very similar 
project to [py-ts-interfaces](https://github.com/cs-cordero/py-ts-interfaces), and only exists because that project 
does not currently support enums. This is a utility for another project I am working on, and has the 
additional benefit of allowing me to generate the TypeScript output in compliance with my eslint configuration. This 
is a much more primitive approach compared to [py-ts-interfaces](https://github.com/cs-cordero/py-ts-interfaces) which 
comes with certain limitations (see [Usage](#Usage) for details).

## Installation

```
python --version  # requires 3.9+
pip install py-to-ts-interfaces
```

## Motivation

Just like [py-ts-interfaces](https://github.com/cs-cordero/py-ts-interfaces), this script is intended for cases 
where a web application is composed of a Python server and a TypeScript client. Setting up a language translator 
like this means that it is possible to define the message schemas once (in Python), and then guarantee that the 
TypeScript message schemas are in sync with the Python ones. This avoids the annoying task of maintaining two 
definition sets, and more importantly, bugs caused by forgetting to update both interfaces.

## Usage

This script takes a single input folder, and requires that all python files inside only contain the following:
- Module imports
- Newlines
- Spaces
- [Dataclasses](https://docs.python.org/3/library/dataclasses.html)
- Enums
- String definitions

If a dataclass contains an enum, the enum definition must be in the same folder also. 
This script also supports nullable types (see `MyNullableInterface` in the section below).
Functions in Enum definitions will be ignored (e.g. a `__str__` override).

### Example

1. Write your Python definitions.

```python
from dataclasses import dataclass
from enum import Enum
from typing import Final, Union, List, Dict


class MyEnum(Enum):
    FIRST = "Number One"
    SECOND = "Number Two"

    def __str__(self):
        return self.value

CONSTANT_STRING: Final = "example"
OTHER_STRING = "another example"
 
@dataclass(frozen=True)
class MyInterface:
    field: MyEnum
    
@dataclass(frozen=True)
class MyNullableInterface:
    field: Union[MyInterface, None] = None
    
@dataclass(frozen=True)
class MyInterface2:
    strange_type: Union[List[int], None]
    other_type: List[str]
    dict_type: Dict[int, Dict[str, MyEnum]]

```

2. In your shell, run the included command and pass in the path of the folder containing the files you want to convert, 
   and the path to the folder that the output should be written to. If the output folder path does not exist then it 
   will be created automatically. 
```
$ py-ts-interfaces example_folder output_folder
```

3. The resulting file will look like this:
```typescript
export enum MyEnum {
    FIRST = 'Number One',
    SECOND = 'Number Two',
}

export const CONSTANT_STRING = 'example';
export const OTHER_STRING = 'another example';

export interface MyInterface {
    field: MyEnum;
}

export interface MyNullableInterface {
    field?: MyInterface;
}

export interface MyInterface2 {
    strangeType?: number[];
    otherType: string[];
    dictType: Record<number, Record<string, MyEnum>>;

```

## Supported Type Mappings

| Python                          | Typescript                    |
|:-------------------------------:|:-----------------------------:|
| str                             | string                        |
| int                             | number                        |
| float                           | number                        |
| complex                         | number                        |
| bool                            | boolean                       |
| List[int]                       | number[]                      |
| List[str]                       | string[]                      |
| Dict[T, P]                      | Record<T, P>                  |

Where T and P are one of the listed supported types (this includes nested Dicts), or enums. 