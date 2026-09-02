"""A parser for java class files

This package contains classes for parsing java .class files.
This is useful to figure out when we need to recompile,
because most java class files contain a 'SourceFile'
attribute.
"""

from __future__ import annotations

import struct
import typing as t
from enum import Enum


class StructData:

    def __str__(self):
        return str(self.__dict__)

    def pp(self, indent=0):
        for field, value in self.__dict__.items():
            print("    " * indent + field + ":", end="")
            if any(
                    isinstance(value, t)
                    for t in [int, str, float, bytes, tuple]):
                print(" " + str(value))
            elif isinstance(value, StructData):
                print(" " + value.__class__.__name__)
                value.pp(indent + 1)
            elif isinstance(value, list):
                if len(value) == 0:
                    print(" empty list")
                else:
                    print(" " + value.__class__.__name__)
                    for i, item in enumerate(value, 1):
                        d = StructData()
                        d.__dict__[f"item {i}"] = item
                        d.pp(indent + 1)
            else:
                print("value: ", value)


class ClassFile(StructData):
    standart_attributes: dict[str, t.Callable[[bytes], Attribute]] = {}

    def __init__(self, stream: t.BinaryIO) -> None:
        self.raw_header = struct.unpack(">4sHH", stream.read(8))
        self.raw_constant_pool = constant_pool(stream)
        self.raw_access_flags = u2(stream)
        self.raw_this_class = u2(stream)
        self.raw_super_class = u2(stream)
        self.raw_interfaces = array(stream, u2)
        self.raw_fields = array(stream, FieldInfo)
        self.raw_methods = array(stream, MethodInfo)
        self.raw_attributes = array(stream, AttributeInfo)

        self.attributes: dict[str, Attribute] = {}
        for attribute in self.raw_attributes:
            name = self.string(attribute.raw_attribute_name_index)
            cls = self.standart_attributes.get(name, UnknownAttribute)
            self.attributes[name] = cls(attribute.raw_info)

    def string(self, index: int) -> str:
        constant = self.raw_constant_pool[index - 1]
        assert isinstance(constant, Utf8_info)
        return constant.raw_txt

    @property
    def source_file(self) -> t.Optional[str]:
        attr = self.attributes['SourceFile']
        if attr is None:
            return None

        assert isinstance(attr, SourceFile_attribute)
        return self.string(attr.sourcefile_index)

    @property
    def class_names(self) -> t.Generator[str]:
        for const in self.raw_constant_pool:
            if isinstance(const, Class_info):
                name = self.string(const.raw_name_index)
                yield name.replace("/", ".")


class FieldInfo(StructData):

    def __init__(self, stream: t.BinaryIO) -> None:
        self.raw_access_flags = u2(stream)
        self.raw_name_index = u2(stream)
        self.raw_descriptor_index = u2(stream)
        self.raw_attributes = array(stream, AttributeInfo)


class MethodInfo(StructData):

    def __init__(self, stream: t.BinaryIO) -> None:
        self.raw_access_flags = u2(stream)
        self.raw_name_index = u2(stream)
        self.raw_descriptor_index = u2(stream)
        self.raw_attributes = array(stream, AttributeInfo)


class AttributeInfo(StructData):

    def __init__(self, stream: t.BinaryIO) -> None:
        self.raw_attribute_name_index = u2(stream)
        self.raw_info = stream.read(u4(stream))


def u1(stream):
    return int.from_bytes(stream.read(1), byteorder='big')


def u2(stream):
    return int.from_bytes(stream.read(2), byteorder='big')


def u4(stream):
    return int.from_bytes(stream.read(4), byteorder='big')


def u8(stream):
    return int.from_bytes(stream.read(8), byteorder='big')


def array(stream, item, length=u2):
    return [item(stream) for _ in range(length(stream))]


def constant_pool(stream):
    constant_pool_count = u2(stream) - 1
    constant_pool = []
    while len(constant_pool) < constant_pool_count:
        entry = constant_pool_entry(stream)
        constant_pool.append(entry)
        if isinstance(entry, Long_info) or isinstance(entry, Double_info):
            constant_pool.append(None)
    return constant_pool


def constant_pool_entry(stream):
    tag = ConstantTag(u1(stream))
    match tag:
        case ConstantTag.Class:
            return Class_info(stream)

        case ConstantTag.Fieldref:
            return Fieldref_info(stream)

        case ConstantTag.Methodref:
            return Methodref_info(stream)

        case ConstantTag.InterfaceMethodref:
            return InterfaceMethodref_info(stream)

        case ConstantTag.String:
            return String_info(stream)

        case ConstantTag.Integer:
            return Integer_info(stream)

        case ConstantTag.Float:
            return Float_info(stream)

        case ConstantTag.Long:
            return Long_info(stream)

        case ConstantTag.Double:
            return Double_info(stream)

        case ConstantTag.NameAndType:
            return NameAndType_info(stream)

        case ConstantTag.Utf8:
            return Utf8_info(stream)

        case ConstantTag.MethodHandle:
            return MethodHandle_info(stream)

        case ConstantTag.MethodType:
            return MethodType_info(stream)

        case ConstantTag.InvokeDynamic:
            return InvokeDynamic_info(stream)


class Class_info(StructData):

    def __init__(self, stream: t.BinaryIO) -> None:
        self.raw_name_index = u2(stream)


class Fieldref_info(StructData):

    def __init__(self, stream: t.BinaryIO) -> None:
        self.raw_class_index = u2(stream)
        self.raw_name_and_type_index = u2(stream)


class Methodref_info(StructData):

    def __init__(self, stream: t.BinaryIO) -> None:
        self.raw_class_index = u2(stream)
        self.raw_name_and_type_index = u2(stream)


class InterfaceMethodref_info(StructData):

    def __init__(self, stream: t.BinaryIO) -> None:
        self.raw_class_index = u2(stream)
        self.raw_name_and_type_index = u2(stream)


class String_info(StructData):

    def __init__(self, stream: t.BinaryIO) -> None:
        self.raw_string_index = u2(stream)


class Integer_info(StructData):

    def __init__(self, stream: t.BinaryIO) -> None:
        self.raw_value = u4(stream)  # TODO: signed


class Float_info(StructData):

    def __init__(self, stream: t.BinaryIO) -> None:
        self.raw_value = struct.unpack(">f", stream.read(4))[0]


class Long_info(StructData):

    def __init__(self, stream: t.BinaryIO) -> None:
        self.raw_value = u8(stream)  # TODO: signed


class Double_info(StructData):

    def __init__(self, stream: t.BinaryIO) -> None:
        self.raw_value = struct.unpack(">d", stream.read(8))[0]


class NameAndType_info(StructData):

    def __init__(self, stream: t.BinaryIO) -> None:
        self.raw_name_index = u2(stream)
        self.raw_descriptor_index = u2(stream)


class Utf8_info(StructData):

    def __init__(self, stream: t.BinaryIO) -> None:
        length = u2(stream)
        self.raw_txt = stream.read(length).decode("utf-8")


class MethodHandle_info(StructData):

    def __init__(self, stream: t.BinaryIO) -> None:
        self.raw_reference_kind = ReferenceKind(u1(stream))
        self.raw_reference_index = u2(stream)


class MethodType_info(StructData):

    def __init__(self, stream: t.BinaryIO) -> None:
        self.raw_descriptor_index = u2(stream)


class InvokeDynamic_info(StructData):

    def __init__(self, stream: t.BinaryIO) -> None:
        self.raw_bootstrap_method_attr_index = u2(stream)
        self.raw_name_and_type_index = u2(stream)


class Attribute(StructData):

    @classmethod
    def register(cls, C: t.Callable[[bytes], Attribute]):
        name = C.__name__.removesuffix("_attribute")
        ClassFile.standart_attributes[name] = C
        return C


class UnknownAttribute(Attribute):

    def __init__(self, info: bytes):
        self.info = info


@Attribute.register
class SourceFile_attribute(Attribute):

    def __init__(self, info: bytes):
        self.sourcefile_index = struct.unpack(">h", info)[0]


class ConstantTag(Enum):
    Class = 7
    Fieldref = 9
    Methodref = 10
    InterfaceMethodref = 11
    String = 8
    Integer = 3
    Float = 4
    Long = 5
    Double = 6
    NameAndType = 12
    Utf8 = 1
    MethodHandle = 15
    MethodType = 16
    InvokeDynamic = 18


class ReferenceKind(Enum):
    REF_getField = 1
    REF_getStatic = 2
    REF_putField = 3
    REF_putStatic = 4
    REF_invokeVirtual = 5
    REF_invokeStatic = 6
    REF_invokeSpecial = 7
    REF_newInvokeSpecial = 8
    REF_invokeInterface = 9
