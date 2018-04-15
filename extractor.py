#!/usr/bin/python3
from datatypes import *
from vartypes import *
import sys, string, struct, time

BinaryLibraryRecord = []
MemberReferencesList = []
objectIds = []
typeStats = [0] * 22
parentlessObjects = {}

def registerObjectId(objectId):
	objectIds.append(objectId)
	
def getObjectFromId(objectId):
	for object in objectIds:
		if object.objectId == objectId:
			return object
	
def getBoolean(file):
	return MSBoolean(position=file.tell(), value=(file.read(1) == b'\x01'))

def getByte(file):
	return file.read(1)

def getChar(file):
	return file.read(1).decode('utf-8')

def getDecimal(file):
	print("ERR: not implemented")
	sys.exit(1)

def getDouble(file):
	print("ERR: not implemented getDouble")
	sys.exit(1)

def getInt(file, size = 1):
	return int.from_bytes(file.read(size), "little")
	
def getTypedInt32(file):
	position = file.tell()
	val = getInt(file, 4)
	return MSInteger32(val, position)
	
def getSByte(file):
	print("ERR: not implemented getSByte")
	sys.exit(1)

def getDecimal(file):
	print("ERR: not implemented getDecimal")
	sys.exit(1)

def getSingle(file):
	a1 = file.read(1)
	a2 = file.read(1)
	a3 = file.read(1)
	a4 = file.read(1)
	val = struct.unpack('f', a1 + a2 + a3 + a4)
	return val

def getTimeSpan(file):
	print("ERR: not implemented getTimeSpan")
	sys.exit(1)

def getDateTime(file):
	print("ERR: not implemented getDateTime")
	sys.exit(1)
	
def getUInt(file, size = 1):
	print("ERR: not implemented getUInt")
	sys.exit(1)
	
def getNull(file):
	print("ERR: should not happen")
	sys.exit(1)

def getString(file):
	return getLengthPrefixedString(file)
		
def getLengthPrefixedString(file, extend = False):
	length = int.from_bytes(file.read(1), "little")
	
	is_longer = (length >> 7) & 1	
	if is_longer == 1:
		old_length = length & 0b01111111
		length_2 = int.from_bytes(file.read(1), "little")
		length_2 = length_2 & 0b01111111
		length = (length_2 << 7) + old_length
		
	string = file.read(length).decode('utf-8')
	return string
	
def getObject(file):
	print("ERR: not implemented getObject")
	sys.exit(1)

def getSystemClass(file):
	print("ERR: not implemented getSystemClass")
	sys.exit(1)
	
def getClass(file):
	print("ERR: not implemented getClass")
	sys.exit(1)

def getObjectArray(file):
	print("ERR: not implemented getObjectArray")
	sys.exit(1)

def getStringArray(file):
	print("ERR: not implemented getStringArray")
	sys.exit(1)

def getPrimitiveArray(file):
	print("ERR: not implemented getPrimitiveArray")
	sys.exit(1)

def getValues(file, memberTypeInfos, instance : ObjectInstance):

	for i in range(0, len(memberTypeInfos[0])):
		memberTypeInfo = memberTypeInfos[0][i]
		additionalInfos = memberTypeInfos[1][i]
		
		if memberTypeInfo == BinaryTypeEnumeration.Primitive:
			if additionalInfos == PrimitiveTypeEnumeration.Boolean:
				instance.addValue(getBoolean(file))
			elif additionalInfos == PrimitiveTypeEnumeration.Byte:
				instance.addValue(getByte(file))
			elif additionalInfos == PrimitiveTypeEnumeration.Char:
				instance.addValue(getChar(file))
			elif additionalInfos == PrimitiveTypeEnumeration.Decimal:
				instance.addValue(getDecimal(file))
			elif additionalInfos == PrimitiveTypeEnumeration.Double:
				instance.addValue(getDouble(file))
			elif additionalInfos == PrimitiveTypeEnumeration.Int16:
				instance.addValue(getInt(file, 2))
			elif additionalInfos == PrimitiveTypeEnumeration.Int32:
				instance.addValue(getTypedInt32(file))
			elif additionalInfos == PrimitiveTypeEnumeration.Int64:
				instance.addValue(getInt(file, 8))
			elif additionalInfos == PrimitiveTypeEnumeration.SByte:
				instance.addValue(getSByte(file))
			elif additionalInfos == PrimitiveTypeEnumeration.Single:
				instance.addValue(getSingle(file))
			elif additionalInfos == PrimitiveTypeEnumeration.TimeSpan:
				instance.addValue(getTimeSpan(file))
			elif additionalInfos == PrimitiveTypeEnumeration.DateTime:
				instance.addValue(getDateTime(file))
			elif additionalInfos == PrimitiveTypeEnumeration.UInt16:
				instance.addValue(getUInt16(file, 2))
			elif additionalInfos == PrimitiveTypeEnumeration.UInt32:
				instance.addValue(getUInt32(file, 4))
			elif additionalInfos == PrimitiveTypeEnumeration.UInt64:
				instance.addValue(getUInt64W(file, 8))
			elif additionalInfos == PrimitiveTypeEnumeration.Null:
				instance.addValue(getNull(file))
			elif additionalInfos == PrimitiveTypeEnumeration.String:
				instance.addValue(getString(file))
			else:
				print("Unknown primitive type ", additionalInfos)
				sys.exit(1)
		elif memberTypeInfo == BinaryTypeEnumeration.String:
			instance.addValue(readRecordTypeEnumeration(file))
		elif memberTypeInfo == BinaryTypeEnumeration.Object:
			instance.addValue(readRecordTypeEnumeration(file))
		elif memberTypeInfo == BinaryTypeEnumeration.SystemClass:
			instance.addValue(readRecordTypeEnumeration(file))
		elif memberTypeInfo == BinaryTypeEnumeration.Class:
			instance.addValue(readRecordTypeEnumeration(file))
		elif memberTypeInfo == BinaryTypeEnumeration.ObjectArray:
			instance.addValue(readRecordTypeEnumeration(file))
		elif memberTypeInfo == BinaryTypeEnumeration.StringArray:
			instance.addValue(readRecordTypeEnumeration(file))
		elif memberTypeInfo == BinaryTypeEnumeration.PrimitiveArray:
			instance.addValue(readRecordTypeEnumeration(file))
		else:
			print("ERROR: memberTypeInfo is invalid")
			sys.exit(1)
	
def getArrayInfo(file):
	objectId = getInt(file, 4)
	length = getInt(file, 4)
	
	return ArrayInfo(objectId, length)
	
def getClassInfo(file, extend = False):

	objectId = getInt(file, 4)
	name = getLengthPrefixedString(file, True)
	memberCount = getInt(file, 4)
	memberNames = []
	for i in range(0, memberCount):
		val = getLengthPrefixedString(file)
		memberNames.append(val)
			
	return ClassInfo(objectId, name, memberCount, memberNames)
	
def getSystemClassTypeInfo(file):
	typeName = getString(file)
	
def getClassTypeInfo(file):
	typeName = getLengthPrefixedString(file)
	libraryId = getInt(file, 4)
	isValidLibraryId = False
	for binaryLibrary in BinaryLibraryRecord:
		if binaryLibrary.libraryId == libraryId:
			isValidLibraryId = True
			break
	if not isValidLibraryId:
		print("ERR: class", typeName, "does not have a valid libraryId (", libraryId, ")")
		sys.exit(1)
		
	return ClassTypeInfo(typeName, libraryId)
	
def getMemberTypeInfo(file, classInfo):
	binaryTypeEnums = []
	
	for i in range(0, classInfo.memberCount):
		binaryTypeEnums.append(getInt(file))
		
	additionalInfos = []
	for type in binaryTypeEnums:
		if type == 0 or type == 7:
			additionalInfos.append(getInt(file))
		elif type == 1 or type == 2 or type == 5 or type == 6 :
			additionalInfos.append(None)
		elif type == 3 :
			additionalInfos.append(getSystemClassTypeInfo(file))
		elif type == 4 :
			additionalInfos.append(getClassTypeInfo(file))

	return (binaryTypeEnums, additionalInfos)
			
#Type value 0
def readSerializedStreamHeader(file):
	rootId = getInt(file, 4)
	headerId = getInt(file, 4)
	majorVersion = getInt(file, 4)
	minorVersion = getInt(file, 4)
	
	print("==== LOADING ====")
	print("=> HEADER VERIFICATION SUCCESS")

#Type value 1
def getClassWithId(file):
	objectId = getInt(file, 4)
	metadataId = getInt(file, 4)
	updateObject = getObjectFromId(metadataId)
	if updateObject == None:
		print("ERR: unable to find object to update")
		
	newInstance = ObjectInstance(objectId, metadataId)
	updateObject.extradata.registerInstance(newInstance)
	getValues(file, updateObject.extradata.memberTypeInfo, newInstance)
	
	return newInstance
	
#Type value 2
def readSystemClassWithMembers(file):
	print(file.tell())
	classInfo = getClassInfo(file, True) 

#Type value 5
def getClassWithMembersAndTypes(file):
	classInfo = getClassInfo(file) 
	memberTypeInfo = getMemberTypeInfo(file, classInfo)
	libraryId = getInt(file, 4)
	classObject = ClassWithMembersAndTypes(classInfo, memberTypeInfo)
	getValues(file, memberTypeInfo, classObject.instances[0])
	registerObjectId(IdentifiableObject(classInfo.objectId, classObject))
	return classObject.instances[0]
	
#Type value 4
def getSystemClassWithMembersAndTypes(file):
	classInfo = getClassInfo(file) 
	memberTypeInfo = getMemberTypeInfo(file, classInfo)
	classObject = ClassWithMembersAndTypes(classInfo, memberTypeInfo)
	values = getValues(file, memberTypeInfo, classObject.instances[0])
	registerObjectId(IdentifiableObject(classInfo.objectId, classObject))
	return classObject.instances[0]

#Type value 6
def readBinaryObjectString(file):
	objectId = getInt(file, 4)
	value = getLengthPrefixedString(file)
	return BinaryObjectString(objectId, value)
	
#Type value 7
def readBinaryArray(file):
	objectId = getInt(file, 4)
	binaryTypeEnum = getInt(file)
	rank = getInt(file, 4)
	lengths = []
	for i in range(0, rank):
		lengths.append(getInt(file, 4))
		
	if binaryTypeEnum in [BinaryArrayTypeEnumeration.SingleOffset, BinaryArrayTypeEnumeration.JaggedOffset, BinaryArrayTypeEnumeration.RectangularOffset]:
		lowerBounds = []
		for i in range(0, rank):
			lowerBounds.append(getInt(file, 4))
		
	typeEnum = getInt(file)
	if typeEnum == 0 or typeEnum == 7:
		getInt(file)
	elif typeEnum == 1 or typeEnum == 2 or typeEnum == 5 or typeEnum == 6 :
		pass
	elif typeEnum == 3 :
		getSystemClassTypeInfo(file)
	elif typeEnum == 4 :
		getClassTypeInfo(file)
	
#Type value 9
def getMemberReference(file):
	idRef = getInt(file, 4)
	return MemberReference(idRef)
	
#Type value 12
def readBinaryLibrary(file):
	libraryId = getInt(file, 4)
	libraryName = getLengthPrefixedString(file)
	
	BinaryLibraryRecord.append(BinaryLibrary(libraryId, libraryName))

#Type value 14
def readObjectNullMultiple256(file):
	nullCount = getInt(file)
	
#Type value 14
def readObjectNullMultiple(file):
	nullCount = getInt(file, 4)
	
#Type value 15
def readArraySinglePrimitive(file):
	arrayInfo = getArrayInfo(file)
	primitiveTypeEnum = getInt(file, 1)
	
	values = ArrayInstance(arrayInfo, primitiveTypeEnum)

	for i in range(0, arrayInfo.length):
		getValues(file, ([BinaryTypeEnumeration.Primitive], [primitiveTypeEnum]), values)
	return 
	
#Type value 16
def readArraySingleObject(file):
	arrayInfo = getArrayInfo(file)

#Type value 16
def readArraySingleString(file):
	arrayInfo = getArrayInfo(file)
	
def readRecordTypeEnumeration(file, topLevel = False):

	global parentlessObjects

	type = getInt(file)
	typeStats[type] += 1
		
	if type == RecordTypeEnumeration.ClassWithId:
		return getClassWithId(file)
	elif type == RecordTypeEnumeration.SystemClassWithMembersAndTypes:
		return getSystemClassWithMembersAndTypes(file)
	elif type == RecordTypeEnumeration.SystemClassWithMembers:
		return readSystemClassWithMembers(file)
	elif type == RecordTypeEnumeration.ClassWithMembersAndTypes:
		val = getClassWithMembersAndTypes(file)
		if topLevel:
			parentlessObjects[val.classBase.classInfo.name] = val
		return val
	elif type == RecordTypeEnumeration.BinaryObjectString:
		return readBinaryObjectString(file)
	elif type == RecordTypeEnumeration.BinaryArray:
		return readBinaryArray(file)
	elif type == RecordTypeEnumeration.MemberReference:
		return getMemberReference(file)
	elif type == RecordTypeEnumeration.ObjectNull: 
		pass
	elif type == RecordTypeEnumeration.BinaryLibrary:
		return readBinaryLibrary(file)
	elif type == RecordTypeEnumeration.ObjectNullMultiple256:
		return readObjectNullMultiple256(file)
	elif type == RecordTypeEnumeration.ObjectNullMultiple:
		return readObjectNullMultiple(file)
	elif type == RecordTypeEnumeration.ArraySinglePrimitive:
		return readArraySinglePrimitive(file)
	elif type == RecordTypeEnumeration.ArraySingleObject:
		return readArraySingleObject(file)
	elif type == RecordTypeEnumeration.ArraySingleString:
		return readArraySingleString(file)
	elif type == RecordTypeEnumeration.MessageEnd:
		return False
	else:
		print("ERR: unknown type ", type)
		print("I read", (file.tell()), " bytes")
		exit(1)
			
def dumpClass(target, level = 1):
	targetClass = target.classBase
	print("="*level + ">DUMPING", targetClass.classInfo.name, "WITH", len(targetClass.instances), "ELEMENTS")
				
	print("="*level + "> VALUES")			
	print("="*level + str(targetClass.classInfo.memberNames))
	
def parseSaveFile(filename):
	with open(filename, mode='rb') as inspected_file:

		dataArray = bytearray(inspected_file.read())
		inspected_file.seek(0)

		startTime = time.time()
		#Read file header
		headerCheck = getInt(inspected_file)
		assert(headerCheck == 0) #The SerializedStreamHeader must be the first record
		readSerializedStreamHeader(inspected_file)
		
		while readRecordTypeEnumeration(inspected_file, True) != False:
			continue
		print("==== FINISHED ====")
		print("=> Loading took ", time.time() - startTime, "seconds")

			
	return (parentlessObjects, dataArray)
	
def writeSaveFile(outputfilename, dataArray):
	with open(outputfilename, mode="wb+") as newfile:
			newfile.write(dataArray)