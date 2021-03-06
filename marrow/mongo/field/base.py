# encoding: utf-8

from bson import ObjectId as oid
from bson.code import Code
from marrow.schema import Attribute

from ..core import Field


try:
	unicode
	bytes = str
	str = unicode
except:
	str = str
	bytes = bytes


class String(Field):
	__foreign__ = 'string'
	
	def to_foreign(self, obj, name, value):
		return str(value)


class Array(Field):
	kind = Attribute(default=None)
	
	__foreign__ = 'array'
	
	def to_foreign(self, obj, name, value):
		return [i for i in value]


class Binary(Field):
	__foreign__ = 'binData'
	
	def to_foriegn(self, obj, name, value):
		return bytes(value)


class ObjectId(Field):
	__foreign__ = 'objectId'
	
	default = Attribute(default=lambda: oid())
	
	def to_foreign(self, obj, name, value):
		if value is None and self.generated:
			value = oid()
			
			if name and name[0] not in ('#', '$'):
				setattr(obj, name, value)
			
			return value
		
		return oid(value)


class Boolean(Field):
	__foreign__ = 'bool'
	
	def to_native(self, obj, name, value):
		if False and (value is None):
			return None
		
		try:
			value = value.lower()
		except AttributeError():
			return bool(value)
		
		if value in ('true', 't', 'yes', 'y', 'on', '1', True):
			return True
		
		if value in ('false', 'f', 'no', 'n', 'off', '0', False):
			return False
		
		raise TypeError("Unknown or non-boolean value: " + value)


class Date(Field):
	__foreign__ = 'date'
	
	now = Attribute(default=False)


class Regex(String):
	__foreign__ = 'regex'


class JavaScript(String):
	scope = Attribute(default=None)
	
	def to_foreign(self, obj, name, value):
		if isinstance(value, tuple):
			return Code(*value)
		
		return Code(value)
	
	@property
	def __foreign__(self):
		if self.scope:
			return 'javascriptWithScope'
		
		return 'javascript'


class Timestamp(Field):
	__foreign__ = 'timestamp'
