# 示例1
def upper_attr(future_class_name, future_class_parents, future_class_attr):
	print('future_class_name: ',future_class_name)
	print('future_class_parents: ', future_class_parents)
	print('future_class_attr: ', future_class_attr)
	uppercase_attr = {}
	for name, val in future_class_attr.items():
		if not name.startswith('__'):
			uppercase_attr[name.upper()] = val
		else:
			uppercase_attr[name] = val

	return type(future_class_name, future_class_parents, uppercase_attr)

# __metaclass__ = upper_attr

class Foo(object, metaclass=upper_attr):
	bar = 'bip'

print(hasattr(Foo, 'bar'))
print(hasattr(Foo, 'BAR'))

f = Foo()
print(f.BAR)

print(f.__class__)

print('-'*40)
# 示例2
class UpperAttrMetaclass(type):
	# bar = 'bipp'
	def __new__(cls, clsname, 
				bases, dct):
		print('upperattr_metaclass: ',cls)
		print('future_class_name: ',clsname)
		print('future_class_parents: ', bases)
		print('future_class_attr: ', dct)
		uppercase_attr = {}
		for name, val in dct.items():
			if not name.startswith('__'):
				uppercase_attr[name.upper()] = val
			else:
				uppercase_attr[name] = val

		return super(UpperAttrMetaclass, cls).__new__(cls, clsname, bases, dct)


class Foo(object, metaclass=UpperAttrMetaclass):
	bar = 'bipp'

print(hasattr(Foo, 'bar'))
print(hasattr(Foo, 'BAR'))
print(Foo.__class__)




# print(uam.bar)
print('-'*40)
# 示例3

class Field(object):
	def __init__(self, name, column_type):
		self.name = name
		self.column_type = column_type

	def __str__(self):
		return '<%s:%s>' % (self.__class__.__name__, self.name)

class StringField(Field):
	def __init__(self, name):
		super(StringField, self).__init__(name, 'varchar(100)')

class IntegerField(Field):
	def __init__(self, name):
		super(IntegerField, self).__init__(name, 'bigint')

class ModelMetaclass(type):
	def __new__(cls, name, bases, attrs):
		if name == 'Model':
			return type.__new__(cls, name, bases, attrs)
		mappings = dict()
		for k, v in attrs.items():
			if isinstance(v, Field):
				print('Found mapping: %s ==> %s' % (k, v))
				mappings[k] = v
		for k in mappings.keys():
			attrs.pop(k)
		attrs['__table__'] = name
		attrs['__mappings__'] = mappings
		print(attrs)
		return type.__new__(cls, name, bases, attrs)

class Model(dict, metaclass=ModelMetaclass):
	# __metaclass__ = ModelMetaclass 

	def __init__(self, **kw):
		super(Model, self).__init__(**kw)

	def __getattr__(self, key):
		try:
			print(1)
			return self[key]
		except KeyError:
			raise AttributeError(r"'Model' object has no attribute '%s'" % key)

	def __setattr__(self, key, value):
		self[key] = value

	def save(self):
		fields = []
		params = []
		args = []
		print(self.__mappings__)

		for k, v in self.__mappings__.items():
			print(v)
			fields.append(k)
			# params.append("'%s'" % v)
			params.append('?')
			args.append(getattr(self, k, None))
		sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(fields), ','.join(params))
		print('SQL: %s' % sql)
		print('ARGS: %s' % str(args))


# class Model(dict):
# 	# __metaclass__ = ModelMetaclass 

# 	def __init__(self, *args, **kwargs):
# 		super(Model, self).__init__(*args, **kwargs)

# 	def __getattr__(self, key):
# 		try:
# 			print(1)
# 			return self[key]
# 		except KeyError:
# 			raise AttributeError(r"'Model' object has no attribute '%s'" % key)

# 	def __setattr__(self, key, value):
# 		self[key] = value

# 	def save(self):
# 		fields = []
# 		params = []
# 		args = []
# 		print(self)
# 		print(getattr(self, 'id', None))
# 		print(type(self))
# 		for k, v in self.items():
# 			print(v)
# 			fields.append(k)
# 			# params.append("'%s'" % v)
# 			params.append('?')
# 			args.append(getattr(self, k, None))
# 		sql = 'insert into %s (%s) values (%s)' % (self.__class__.__name__, ','.join(fields), ','.join(params))
# 		print('SQL: %s' % sql)
# 		print('ARGS: %s' % str(args))

class User(Model):
	id = IntegerField('id')
	name = StringField('username')
	email = StringField('email')
	password = StringField('password')

u = User(id=12345, name='Michael', email='test@orm.org', password='123456')
# print(u)
u.save()

