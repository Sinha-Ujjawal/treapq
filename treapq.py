import random

''' ADT Treapq:
		len() O(1)
  		isEmpty() O(1)
		put(k, prior) Exp. O(lg n)
		get(k) Exp. O(1)
		pop(k) Exp. O(1)
		min() O(1)
		extractMin() Exp. O(1)
		max() O(1)
		extractMax() Exp. O(1)
		items(desc = False) O(n)
'''

class Wrapper:
	def __init__(self, k, prior):
		self._k = k
		self._prior = prior

	def __repr__(self):
		return '{}: {}'.format(self._k, self._prior)

	@property
	def k(self):
		return self._k

	@property
	def prior(self):
		return self._prior

class Treapq:
	class __Node:
		def __init__(self, k, prior):
			self.object = Wrapper(k, prior)
			self.prior = random.getrandbits(32)
			self.left = self.right = self.p = self.next = self.prev = None

		@staticmethod
		def minPriorNode(node):
			m = node
			left = node.left
			right = node.right
			if left != None and left.prior < m.prior:
				m = left
			if right != None and right.prior < m.prior:
				m = right
			return m

		@staticmethod
		def getObject(node):
			return node.object if node else None

	def __init__(self):
		self._root = self._min = self._max = None
		self._map = {}

	def __len__(self):
		return len(self._map)

	def len(self):
		return len(self._map)

	def __iter__(self):
		return self.items()

	def __repr__(self):
		x = "Treapq ({"
		p = self._min
		while p != None:
			x += p.object.__repr__()
			if p.next != None:
				x += ", "
			p = p.next
		return x + "})"

	def __setitem__(self, k, prior):
		self.put(k, prior)

	def __getitem__(self, k):
		return self.get(k)

	def __delitem__(self, k):
		self.pop(k)

	def __contains__(self, k):
		return self.contains(k)

	def isEmpty(self):
		return self._root == None

	def clear(self):
		self._root = self._min = self._max = None
		self._map.clear()

	def min(self):
		return self.__Node.getObject(self._min)

	def extractMin(self):
		if self._min != None:
			p = self._min
			self.__transplant(self, p, p.right)
			self._min = p.next
			if self._min:
				self._min.prev = None
			self._map.pop(p.object.k)
			return p.object

	def extractMax(self):
		if self._max != None:
			p = self._max
			self.__transplant(self, p, p.left)
			self._max = p.prev
			if self._max:
				self._max.next = None
			self._map.pop(p.object.k)
			return p.object

	def max(self):
		return self.__Node.getObject(self._max)

	@staticmethod
	def __leftRotate(self, x):
		if x:
			y = x.right
			x.right = y.left
			if x.right:
				x.right.p = x
			self.__transplant(self, x, y)
			y.left = x
			x.p = y

	@staticmethod
	def __rightRotate(self, x):
		if x:
			y = x.left
			x.left = y.right
			if x.left:
				x.left.p = x
			self.__transplant(self, x, y)
			y.right = x
			x.p = y

	@staticmethod
	def __transplant(self, x, y):
		if x.p == None:
			self._root = y
		elif x.p.left == x:
			x.p.left = y
		else:
			x.p.right = y
		if y != None:
			y.p = x.p

	@staticmethod 
	def __maintainMinHeapProperty(self, p):
		while p != None:
			q = p.p
			m = self.__Node.minPriorNode(p)
			if m == p.left:
				self.__rightRotate(self, p)
			elif m == p.right:
				self.__leftRotate(self, p)
			p = q

	def put(self, k, prior):
		try:
			if prior != self._map[k].object.prior:
				self.pop(k)
			else:
				return
		except:
			p = self._root
			a = b = q = None
			while p != None:
				q = p
				if prior < p.object.prior:
					a = p
					p = p.left
				else:
					b = p
					p = p.right
			node = self.__Node(k, prior)
			self._map[k] = node
			node.next = a
			node.prev = b
			if a:
				a.prev = node
			if b:
				b.next = node
			if self._min == None or prior < self._min.object.prior:
				self._min = node
			if self._max == None or prior >= self._max.object.prior:
				self._max = node
			node.p = q
			if q:
				if prior < q.object.prior:
					q.left = node
				else:
					q.right = node
				self.__maintainMinHeapProperty(self, node)
			else:
				self._root = node

	def get(self, k):
		return self._map[k].object

	def contains(self, k):
		return k in self._map

	def pop(self, k):
		p = self._map.pop(k)
		if p == self._min:
			self._min = p.next
		if self._min:
			self._min.prev = None
		if p == self._max:
			self._max = p.prev
		if self._max:
			self._max.next = None
		a = p.next
		b = p.prev
		if a:
			a.prev = b
		if b:
			b.next = a
		p.next = p.prev = None
		if p.left == None:
			self.__transplant(self, p, p.right)
		elif p.right == None:
			self.__transplant(self, p, p.left)
		else:
			if a != p.right:
				self.__transplant(self, a, a.right)
				a.right = p.right
				a.right.p = a
			a.left = p.left
			a.left.p = a
			self.__transplant(self, p, a)
			a.prior = p.prior
			p.left = p.right = p.p = None
		return p.object

	def items(self, desc = False):
		if not desc:
			p = self._min
			while p != None:
				yield p.object
				p = p.next
		else:
			p = self._max
			while p != None:
				yield p.object
				p = p.prev
