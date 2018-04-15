#!/usr/bin/python3

IDENTIFIER_DEFAULT_VALUE = -1
IDENTIFIER_ARRAY_VALUES = -2

INSTANCE_LIST = []
ARRAY_LIST = []

class BinaryTypeEnumeration:
	Primitive = 0
	String = 1
	Object = 2
	SystemClass = 3
	Class = 4
	ObjectArray = 5
	StringArray = 6
	PrimitiveArray = 7

class PrimitiveTypeEnumeration:
	Boolean = 1
	Byte = 2
	Char = 3
	#No value for 4
	Decimal = 5
	Double = 6
	Int16 = 7
	Int32 = 8
	Int64 = 9
	SByte = 10
	Single = 11
	TimeSpan = 12
	DateTime = 13
	UInt16 = 14
	UInt32 = 15
	UInt64 = 16
	Null = 17
	String = 18

class RecordTypeEnumeration:
	SerializedStreamHeader = 0
	ClassWithId = 1
	SystemClassWithMembers = 2
	ClassWithMembers = 3
	SystemClassWithMembersAndTypes = 4
	ClassWithMembersAndTypes = 5
	BinaryObjectString = 6
	BinaryArray = 7
	MemberPrimitiveTyped = 8
	MemberReference = 9
	ObjectNull = 10
	MessageEnd = 11
	BinaryLibrary = 12
	ObjectNullMultiple256 = 13
	ObjectNullMultiple = 14
	ArraySinglePrimitive = 15
	ArraySingleObject = 16
	ArraySingleString = 17
	MethodCall = 21
	MethodReturn = 22

class MemberReference:
	
	def __init__(self, idRef):
		self.idRef = idRef
	
	def resolve(self):
		for element in INSTANCE_LIST + ARRAY_LIST:
			if element.objectId == self.idRef:
				return element

class BinaryArrayTypeEnumeration:
	Single = 0
	Jagged = 1
	Rectangular = 2
	SingleOffset = 3
	JaggedOffset = 4
	RectangularOffset = 5

class BinaryLibrary:
	libraryId = 0
	libraryName = ""
	
	def __init__(self,  libraryId, libraryName):
		self.libraryId = libraryId
		self.libraryName = libraryName

class ClassTypeInfo:
	typeName = ""
	libraryId = 0
	
	def __init__(self, typeName, libraryId):
		self.typeName = typeName
		self.libraryId = libraryId
		
	def __repr__(self):
		return self.typeName + " : " + str(self.libraryId) 

class ClassInfo:
	objectId = 0
	name = ""
	memberCount = 0
	memberNames = []
	
	def __init__(self, objectId, name, memberCount, memberNames):
		self.objectId = objectId
		self.name = name
		self.memberCount = memberCount
		self.memberNames = memberNames
		
	def __repr__(self):
		return str(self.objectId) + " " + self.name + ",member count:" + str(self.memberCount) + " " + ",".join(self.memberNames)

class ClassWithMembersAndTypes:
	classInfo = None
	memberTypeInfo = None
	defaultValues = None
	
	def __init__(self, classInfo, memberTypeInfo):
		self.classInfo = classInfo
		self.memberTypeInfo = memberTypeInfo
		self.instances = []
		self.instances.append(ObjectInstance(IDENTIFIER_DEFAULT_VALUE, self.classInfo.objectId))
		self.instances[0].classBase = self
		
	def registerInstance(self, instance):
		instance.classBase = self
		self.instances.append(instance)

	def getInstance(self, index):
		instance = self.instances[index]
		if len(instance.values) != len(self.classInfo.memberNames) :
			print("ERR: Not enough data !")
			
		for i in range(0, len(self.classInfo.memberNames)):
			value = instance.values[i]
			if type(value) is MemberReference:
				value = value.resolve()
				
			print(self.classInfo.memberNames[i], "=>", value)

class ObjectInstance:
	objectId = 0
	classBase = None
	classBaseId = 0
		
	def __init__(self, objectId, classBaseId):
		INSTANCE_LIST.append(self)
		self.objectId  = objectId
		self.classBaseId = classBaseId
		self.values = {}
		self.addresses = []
		
	def __repr__(self):
		return "<instance of="+self.classBase.classInfo.name+">"
		
	def __getitem__(self, item):
		return self.values[item]
		
	def addValue(self, value, address = None):
		self.values[self.classBase.classInfo.memberNames[len(self.values)]] = value
		self.addresses.append(address)

class ArrayInstance(ObjectInstance):
	
	def __init__(self, arrayInfo, primitiveTypeEnum):
		ARRAY_LIST.append(self)
		self.arrayInfo = arrayInfo
		self.objectId = arrayInfo.objectId
		self.primitiveTypeEnum = primitiveTypeEnum
		self.values = []
		self.addresses = []
		
	def __repr__(self):
		return "<array, size="+str(self.arrayInfo.length)+", type="+str(self.primitiveTypeEnum)+">";

	def addValue(self, value, address = None):
		self.values.append(value)
		self.addresses.append(address)
	
		
class IdentifiableObject:
	objectId = 0
	extradata = None
	def __init__(self, objectId, extradata = None):
		self.objectId = objectId
		self.extradata = extradata

class ArrayInfo:
	objectId = 0
	length = 0
	
	def __init__(self, objectId, length):
		self.objectId = objectId
		self.length = length
		
	def __repr__(self):
		return str(self.objectId) + " " + str(self.length)
		
		
class BinaryObjectString:
	objectId = 0
	value = ""
	
	def __init__(self, objectId, value):
		self.objectId = objectId
		self.value = value
		
	def __repr__(self):
		return "<string, id=" + str(self.objectId) + ", val=\"" + self.value + "\">"