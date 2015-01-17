#module: floatlist.py
"""
Decorates Python's standard list with the ability to index into it at 
floating point indices, with the option to interpret those floating point
indices as to be interpolated between surrounding values or as floored values.

Wraps infinitely as well.
"""
from math import floor, ceil

def flr(x):
	"""
	Floors a value to the greatest integer value lower than the
	given value. This is mainly to avoid ugly typecasting in-line.
	
	Parameters:
		x (Float): The value to floor.
	
	Returns:
		The first integer below this floating point value.
		
	Preconditions:
		None.
		
	Postconditions:
		None.
	"""
	return int(floor(x))
	
def cl(x):
	"""
	Returns the lowest integer value above the given value. This
	function exists to avoid typecasting inline.
	
	Parameters:
		x (Float): The value to ceil.
	
	Returns:
		The first integer above this floating point value.
		
	Preconditions:
		None.
		
	Postconditions:
		None.
	"""
	return int(ceil(x))
	
def _lerp(a, b, t):
	"""
	Linearly interpolates between A and B fractional distance t.
	
	Parameters:
		a (Any): The first of the two values to interpolate between.
		b (Any): The second of the two values to interpolate between.
		t (float): The fractional distance between the two to
			evaluate for.
	
	Returns:
		I'll be straight with you: a + (b-a)*t.
		
	Preconditions:
		The instances passed as a and b must define the "+", "-", and 
		"*"	operators.
		t must be within the range [0..1].
	
	Postconditions:
		None.
	
	"""
	return a + (b-a)*t

def _frange(start, stop, step=1):
	"""
	Returns a list containing all the terms at <step> intervals
	between start and stop. This expands upon the built-in range()
	as one can now use fractional values.
	
	Parameters:
		start (Numerical): The value to start the sequence at.
		stop (Numerical): The value to stop at or before.
		step (Numerical): The value to step by.
		
	Returns:
		A list defined as follows:
			{ [start, start+step*1, ... start+step*n] | start+step*n <= stop}
	
	Preconditions:
		None.
		
	Postconditions:
		Note that the values contained in the returned list may not
		contain stop as a value.
	"""
	if start == None:
		start = 0
	if step == None:
		step = 1

	lst = []
		
	while(start <= stop):
		lst.append(start)
		start += step
	return lst
		
class FloatList(list):
	"""
	Decorates Python's standard list with the ability to comprehend floating
	point indices and optional relevant linear interpolation for transitive
	values.
	
	slots:
		lerp (Boolean): Whether or not to linearly interpolate between the
		nearest two indices when sampling or setting.
	"""
	
	__slots__= ("lerp")
	
	def __init__(self, list, interpolate=True):
		"""
		Constructor which accepts a pre-existing list type as initial
		data.
		
		Parameters:
			-list (List): An initial set of data.
			-interpolate (Boolean): Whether or not to interpolate on access
			and update. (Default: True)
			
		Returns:
			None.
			
		Preconditions:
			Every item in list must arithmetically define '+', '-', and '*'
			operations for interpolation purposes.
		
		Postconditions:
			None.
		"""
		super(FloatList, self).__init__(self)
		self.lerp = interpolate
		for i in list:
			self.append(i)
		
	def __len__(self):
		"""
		Returns the length of this FloatList instance, by simply calling
		the __len__() function of the decorated list.
		This defines the behavior of len() when passed an instance of
		FloatList.
		
		
		Parameters:
			None.
		
		Returns:
			The length of this FloatList.
		
		Preconditions:
			None.
			
		Postconditions:
			None.
		"""
		return super(FloatList, self).__len__()
		
	def __getitem__(self, key):
		"""
		Overrides the behavior of bracketed list access, allowing for
		floating point values to be used, and interpolated values to
		be returned.
		
		Parameters:
			key (Float, Slice): The floating point index of the value to 
			be returned.
			
		Returns:
			The item, or a NotFoundException, as defined by list.__getitem__().
			
		Preconditions:
			If the key given is a slice, it is allowed to contain floating point
			values, just as floating point values are allowed as indices.
		
		Postconditions:
			None.
		"""
		try:
			if isinstance(key, slice):
				return self.__get_slice(key)
			else:
				return self.__get_single(key)
		except TypeError as error:
			print("Could not retrieve key="+str(key)+". Key not integer, "+\
			"float, or slice."+str(error))
		
	def __get_slice(self, s):
		"""
		Returns a slice of this FloatList.
		
		Parameters:
			s (slice): The slice instance created to access the list.
			
		Returns:
			A list of values at the indices specified by the slice modulo the
			length of the list.
			
		Preconditions:
			The given slice may contain floating point values.
			
		Postconditions:
			A list is created, populated with the requested values, and finally
			returned.
		"""
		items = []
		for i in _frange(s.start, s.stop, s.step):
			items.append(self.__get_single(i))
		return items
		
	def __get_single(self, k):
		"""
		Returns a single element from the float list.
		
		Parameters:
			k (Float): The floating point index to sample.
			
		Returns:
			The value at that index.
			
		Preconditions:
			None.
			
		Postconditions:
			if interpolation is specified against, the index is simply floored.
			Otherwise the value returned is the interpolation of the elements
			on either integer side of the specified index.
		"""
		
		k %= super(FloatList, self).__len__()
		if self.lerp:
			return _lerp( super(FloatList, self).__getitem__(flr(k)),\
						super(FloatList, self).__getitem__(cl(k)%	\
						super(FloatList, self).__len__()),	k-flr(k))
		return super(FloatList, self).__getitem__(flr(k))
		
	def __setitem__(self, key, value):
		"""
		Assigns a value to pre-existing items.
		The nearest two values to the given index are updated proportionately
		to their distance to the given index.
		
		Parameters:
			key (Float, slice): The index (indices) to edit.
			value (Float): The value to store.
			
		Returns:
			None.
			
		Preconditions:
			If a slice is passed as key, it may contain floating point values.
		
		Postconditions:
			The values around each given index are updated with the value given.
		"""
		try:
			if isinstance(key, slice):
				self.__set_slice(key, value)
			else:
				return self.__set_single(key, value)
		except TypeError:
			print("Key not integer, float, or slice type.")
		
	def __set_slice(self, s, v):
		"""
		Sets a slice of this FloatList with the given value.
		
		Parameters:
			s (slice): The indices to edit.
			v (Float): The value to store.
			
		Returns:
			None.
			
		Preconditions:
			The slice may contain floating point values.
		
		Postconditions:
			The values around each given index are updated with the value given.
		"""
		for i in _frange(s.start, s.stop, s.step):
			self.__set_single(i, v.__get_single(i))
			
	def __set_single(self, k, v):
		"""
		Sets the nearest two indices to the given key.of the FloatList with the
		given value.
		
		Parameters:
			k (slice): The index to edit.
			v (Float): The value to store.
			
		Returns:
			None.
			
		Preconditions:
			None.
		
		Postconditions:
			The values around the given index are updated with the value given.
		
		
		"""
		k %= super(FloatList, self).__len__()
		if self.lerp:
			super(FloatList, self).__setitem__(floor(k), _lerp(v, \
								super(FloatList, self).__getitem__(flr(k)), \
								k-flr(k)) )
			super(FloatList, self).__setitem__(ceil(k),	\
							_lerp( super(FloatList, self).__getitem__(cl(k)), 
							v, 
							k-flr(k)) )
		else:
			super(FloatList, self).__setitem__(flr(k), v)
										
	def __contains__(self, item):
		"""
		Returns whether or not this FloatList contains the given item.
		
		Parameters:
			item (Any): The item to search for.
			
		Returns:
			Whether or not this FloatList contains the given item.
			
		Preconditions:
			None.
			
		Postconditions:
			None.
		"""
		if self.lerp:
			for i in range(super(FloatList, self).__len__()-1):
				if super(FloatList, self).__getitem__(i) <= item and 	\
					super(FloatList, self).__getitem__(i+1) >= item:
					return True
		else:
			return super().__contains__(item)
		return False
		
	def aslist(self):
		"""
		Returns the contents of this FloatList as a list.
		
		Parameters:
			None.
			
		Returns:
			The contents of this FloatList as a list.
			
		Preconditions:
			None.
			
		Postconditions:
			None.
		"""
		l = []
		for i in self:
			l.append(i)
		return l