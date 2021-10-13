import os
import shutil

from py_to_ts_interfaces.__main__ import python_to_typescript_folder

PYTHON_DEFINITIONS = """from dataclasses import dataclass
from enum import Enum
from typing import Union, List


class MyEnum(Enum):
    FIRST = "Number One"
    SECOND = "Number Two"


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
    
"""

TYPESCRIPT_DEFINITIONS = """enum MyEnum {
    FIRST = 'Number One',
    SECOND = 'Number Two',
}

export interface MyInterface {
    field: MyEnum;
}

export interface MyNullableInterface {
    field?: MyInterface;
}

export interface MyInterface2 {
    strangeType?: number[];
    otherType: string[];
}
"""


class TestPyToTsInterfaces:
    def test_success(self):
        """Primitive 'catch-all' test."""

        input_path = "temp_testing"
        output_path = "temp_testing_2"

        if not os.path.isdir(input_path):
            os.makedirs(input_path)
        with open(os.path.join(input_path, "temp.py"), "w+", encoding="utf-8") as writer:
            writer.write(PYTHON_DEFINITIONS)

        python_to_typescript_folder(input_path, output_path)

        with open(os.path.join(output_path, "temp.ts"), "r",  encoding="utf-8") as reader:
            output = reader.read()

        shutil.rmtree(input_path)
        shutil.rmtree(output_path)

        output_split = output.split("\n")
        expected_split = TYPESCRIPT_DEFINITIONS.split("\n")
        print("\n\nOutput:\n\"{}\"".format(output))

        for i in range(max(len(output_split), len(expected_split))):
            assert output_split[i] == expected_split[i]
