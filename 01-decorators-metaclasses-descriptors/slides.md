---
highlightTheme: monokai
---

<style>
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;400;600;700&display=swap');

:root {
	--r-code-font: "Fira Code";
}

.reveal .hljs {
	min-height: 50%;
}
</style>

%%

f7f7f7 background slide colour

%%


# Advanced Python

#### Decorators and Metaclasses and Descriptors &mdash; Oh My!

---

# Requirements

Python 3.8

[talks.leeming.dev/#advanced-python--01-decorators-metaclasses-descriptors](https://talks.leeming.dev/#advanced-python--01-decorators-metaclasses-descriptors)

notes:
- #TODO fill in GitHub link
- #TODO check Python version

---

# Inspiration

![[dabeaz-talk.png|640]] <!-- element class="fragment" -->

notes:
- This workshop is based on a talk given by David Beazley at Pycon 2013, titled Python 3 Metaprogramming

---

# Introduction

notes:
- Combining two great things

---
<!-- .slide: data-auto-animate -->

## Python 3

## Metaprogramming <!-- element class="fragment" -->

notes:
- Python 3, and metaprogramming

---
<!-- .slide: data-auto-animate -->

## Metaprogramming

![[code-transformer.excalidraw.svg]]  

notes:
- Metaprogramming is all about creating code that manipulates other code

---

### `@decorators`  <!-- element class="fragment" -->

### Metaclasses  <!-- element class="fragment" -->

### Descriptors  <!-- element class="fragment" -->

notes:
- Examples include decorators, metaclasses, and descriptors
- We'll be using all of these in today's talk

---

<split even gap="3">

	![[library.excalidraw.svg]]

	![[framework.excalidraw.svg]]

</split>

notes:
- Metaprogramming techniques are often used in libraries and frameworks to abstract detail away from the user

---

![[python.excalidraw.svg]]

notes:
- Understanding metaprogramming will give us a better understanding of how Python works under the hood

---

# DRY

Don't repeat yourself <!-- element class="fragment" -->

Don't repeat yourself <!-- element class="fragment" -->

Don't repeat yourself <!-- element class="fragment" -->

notes:
- Now, DRY
- Don't worry, I'm not referring to the humour in this talk
- Here we're saying Don't Repeat Yourself
- Don't Repeat Yourself
- Don't Repeat Yourself

---

# Why?

---

## Repetition harms code

---

# Hard to read

---

# **Slow** to write

---

# Difficult to modify

---

# Avoid repetition

notes:
- We'd like to avoid as much repetition and boilerplate as possible, especially in our user's code

---

# Building Blocks

notes:
- With that being said, let's begin!

---

```python
def linear_search(sequence: list, target: int) -> int:
	for index, item in enumerate(sequence):
		if item == target:
			return index
	return -1

if __name__ == '__main__':
	arr = [1, 2, 3, 4, 5]
	print(linear_search(arr, 4))
```

notes:
- I said earlier that metaprogramming is creating code to manipulate code
- But what are we manipulating?

---
<!-- .slide: data-auto-animate -->

# Statements

notes:
- Code is build from statements

---
<!-- .slide: data-auto-animate -->

# Statements

## do things

notes:
- And statements are the things that do stuff in our program

---
<!-- .slide: data-auto-animate -->

# Statements

## have scopes

notes:
- It's important to note that statements are executed in two scopes

---

# Global

The current module <!-- element class="fragment" -->

notes:
- The first of these is the global scope
	- For Python, this means the module (or file) the statement is in

---

# Local

The enclosing function or class <!-- element class="fragment" -->

notes:
- Then, there's the local scope
	- This is the class or function which contains the statement

---

# Functions

notes:
- Statements can then be combined into functions

---

```python
class List:
	def __init__(self, *items):
		self.items = items
	def __iter__(self):
		return iter(self.items)

def linear_search(sequence: List, target: int) -> int:
	for index, item in enumerate(sequence):
		if item == target:
			return index
	return -1

arr = List(1, 2, 3, 4, 5)
print(linear_search(arr, 4))
```

notes:
- Whilst statements are the building blocks, functions are the smallest units which can be easily manipulated

---

```python[1-2|4-5|6-7|1,8-9]
def add(x, y=0):
	return x + y

>>> add(1, 2)
3
>>> add(x=3, y=4)
7
>>> add(5)
5
```

notes:
- Functions can be called with either positional or keyword arguments
- We can supply default values for arguments


---

```python[1-3|5-6|7-8]
def append(item, array=[]):
	array.append(item)
	return array

>>> append(6)
[6]
>>> append(7)
[6, 7]
```

notes:
- We must be careful with default arguments as they're set at definition time

---

```python[1-3|7-8|9-10]
def append(item, array=None):
	if array is None:
		array = []
	array.append(item)
	return array

>>> append(6)
[6]
>>> append(7)
[7]
```

notes:
- Instead we can use something immutable to mark the default

---

```python
def compute(pos_only, /, pos, *args, kwd_only, **kwargs):
	print(pos_only, pos, args, kwd_only, kwargs)

>>> compute(0, 1, 2, 3, kwd_only=4, a=5, b=6)
0 1 (2, 3) 4 {'a': 5, 'b': 6}
```

notes:
- We can restrict arguments to be passes only positionally (before the `/`), or only by keyword (between `*args` and `**kwargs`)
- We can also collect positional and keyword arguments with `*` and `**` respectively

---

### Closures

```python[1-7|9|10-11|12-13]
def create_adder(x):
	z = 0
	def add(y):
		nonlocal z
		z += 1
		return x + y + z
	return add

>>> add_two = create_adder(2)
>>> add_two(3)
5
>>> add_two(3)
6
```

notes:
- In Python, functions are first class objects
- This means we can pass them around and return them from other functions
- Local variables are captured by inner functions

---

# Classes

notes:
- For the most part classes in Python are wrappers around dictionaries

---

```python[1-13|5|2|4-5]
class Foo:
	bar = 0

	def __init__(self, baz):
		self.baz = baz

	@classmethod
	def from_string(cls, string):
		return cls(cls.parse_string(string))

	@staticmethod
	def parse_string(string):
		return int(string.replace('_', ''), 16)
```

notes:
- In classes, we can attach variables to the instance or the class itself.
- Similarly, we can create instance methods, taking `self` as the first parameter, referring to the instance of the object the method was called on

---

```python[2-3|4-5|8-9]
class OtherSelf:
	def do_something(this, a, b, c):
		...

	def do_something_else(x, y, z):
		...

	def do_another_thing(self, sequence, item):
		...
```

notes:
- Side note: there's no requirement in Python to call this parameter `self`, so we _could_ adopt a similar standard to Java, C++, and others, and call this parameter `this`
- We _could_ even go crazy and make this name indistinguishable from the other parameters, though this is generally a bad idea
- However, it's always a good idea to name things well and part of that is conforming to expectations:
	- If you have one or two Python files in a large project in a  `this`-based language, calling it `this` is probably acceptable
	- If you're writing pure Python, `self` is a better choice

---

```python[7-9|11-13|4-5]
class Foo:
	bar = 0

	def __init__(self, baz):
		self.baz = baz

	@classmethod
	def from_string(cls, string):
		return cls(cls.parse_string(string))

	@staticmethod
	def parse_string(string):
		return int(string.replace('_', ''), 16)
```

notes:
- We can also use the `classmethod` decorator to attach the method not to an instance but the class.
	- We then use `cls` (short for class) as the first parameter, which refers to the type
- Finally, we can make the method static with the `staticmethod` decorator.
	- The method then has no reference to either the associated object or type
- Looking back at the `init` method, we see an example of so-called "dunder" methods (short for **d**ouble **under**score), which let us customise almost all parts of a class

---

```python
class Base:
	pass

class Child(Base):
	pass

class Grandchild(Child):
	pass

class Sibling(Base):
	pass

class Multiple(Sibling, Grandchild):
	pass
```

notes:
- 


---

# Basics

notes:
- Let's introduce the motivating example for this part of the talk: debugging.

---

```python
def add(x, y):
	return x + y
```

notes:
- We've all been there, we have a reasonably complex project with lots of interconnect modules and function calls
- And something doesn't work.

---

```python
def add(x, y):
	print(f'Calling add with arguments `x={x}` and `y={y}`')
	result = x + y
	print(f'add returned `{result}`')
	return result
```

notes:
- To try and solve the problem, we decide to add functionality to log the values passed to and returned from functions

---

```python
def sub(x, y):
	print(f'Calling sub with arguments `x={x}` and `y={y}`')
	result = x + y
	print(f'sub returned `{result}`')
	return result
```

notes:
- Let's add logging to our `sub` function as well.
- It's almost identical to the logging code in the `add` function...

---

```python
def mul(x, y):
	...

def div(x, y):
	...

def mod(x, y):
	...
```

notes:
- We've got lots of functions we want to add debug information to - and this is just in our maths module
- As the logging code is almost identical, it would be nice to abstract this away

---

# Decorators

notes:
- Decorators modify the behaviour of functions
- They originate from a pattern in the book Design Patterns: Elements of Reusable Object-Oriented Software, also known as the Gang of Four book
- Python has adopted them into the language

---

```python[1-14|3-14|5-12|4]
from functools import wraps

def log(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		print(
			f'Calling {func.__qualname__} with',
			args, kwargs
		)
		result = func(*args, **kwargs)
		print(f'{func.__qualname__} returned {result}')
		return result
		
	return wrapper
```

notes:
- Here, we're creating our decorator, `log`.
- It's a function which returns another function, `wrapper`
- Notice the call to `@wraps` on line 4
	- That's another decorator, which copies the name, doc strig, and some other attributes of `func` over to `wrapper`.
	- It's quite a useful tool to use, as it can lead to some weirdness otherwise
	- #demo

---

```python
@decorator
def foo(a, b, c):
	...
```

notes:
- We've seen how to define a decorator, and briefly how to use one, but what does it do?
- Let's have a look at this simple example, and see what Python does with it

---

```python
def foo(a, b, c):
	...

foo = decorator(foo)
```

notes:
- When it sees a decorator being used with the `@` syntax, Python converts it so this: using a decorator is syntactic sugar for defining the function, then reassigning it having passed it to the decorator
- Whilst you don't need to know this to use decorators, it's useful to keep in mind

---

```python[1,34,7,10]
@log
def add(x, y):
	return x + y
@log
def sub(x, y):
	return x - y
@log
def mul(x, y):
	return x / y
@log
def div(x, y):
	return x / y
```

notes:
- Here, we can see that the code is much cleaner, and with a lot less repetition
- We've done all this without changing the functionality: we can still use these methods as before #demo 
- We can also change the functionality of the decorator independently of the code using it.
	- Suppose we wanted to use the `logging` module to print things, or to enable logging only in a debug mode. We could do that! #example

---

## Logging needs prefixes

notes:
- But wait, logging needs prefixes, so we can easily find the output

---

```python[1-13|4-12|3,7,13]
from functool import wraps

def log(prefix='###'):
	def decorator(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			name = prefix + func.__qualname__
			print(f'Calling {name} with', args, kwargs)
			result = func(*args, **kwargs)
			print(f'{name} returned {result}')
			return result
		return wrapper
	return decorator
```

notes:
- We've got basically the same function here, but we've put a wrapper around it to take the prefix #demo

---

```python[1,34,7,10]
@log('+++ ')
def add(x, y):
	return x + y
@log('--- ')
def sub(x, y):
	return x - y
@log('*** ')
def mul(x, y):
	return x / y
@log('/// ')
def div(x, y):
	return x / y
```

notes:
- And to use it, it's almost identical
- However, we run into a problem: what if we want to use the default value of prefix?

---

```python[1,34,7,10]
@log()
def add(x, y):
	return x + y
@log()
def sub(x, y):
	return x - y
@log()
def mul(x, y):
	return x / y
@log()
def div(x, y):
	return x / y
```

notes:
- I don't know about you, but those brackets seem superfluous to me
- Can we do better?

---

```python[1-14|3-5]
from functool import partial, wraps

def log(func=None, /, *, prefix='###'):
	if func is None:
		return partial(log, prefix=prefix)

	@wraps(func)
	def wrapper(*args, **kwargs):
		name = prefix + func.__qualname__
		print(f'Calling {name} with', args, kwargs)
		result = func(*args, **kwargs)
		print(f'{name} returned {result}')
		return result
	return wrapper
```

notes:
- #demo 
- Again, this implementation is similar to the others.
- However, this time, we accept `func` as a _positional-only_ argument, and `prefix` as a _keyword-only_ argument
- If `func` isn't provided, we know we haven't been called as a decorator, so we can return a function which calls `log` again, this time with `prefix` filled in

---

```python[1,4|7,10]
@log(prefix='+++ ')
def add(x, y):
	return x + y
@log(prefix='--- ')
def sub(x, y):
	return x - y
@log
def mul(x, y):
	return x / y
@log
def div(x, y):
	return x / y
```

notes:
- We can now call it like before, only this time, we can omit the brackets if we don't want to pass a value for prefix
- The tradeoff is that we must pass prefix as a keyword argument if we do want to specify it
	- Here it increases readability, so it's not too much of an issue

---

# Class Decorators

notes:
- Decorators can not only be used to modify functions, but classes as well!

---

```python[]
def log_methods(cls):
	for name, value in vars(cls).items():
		if callable(value):
			setattr(cls, name, log(value))
	return cls
```

notes:
- #demo 
- Here, we iterate over all attributes of the class and, if they are callable, we wrap them with our log function
- We could extend this decorator to allow specifying the prefix
- Due to how Python implements them, this won't work class or static methods
	- You could try to modify it so it does

---

```python
def log_attributes(cls):
	original_getattribute = cls.__getattribute__
	
	def __getattribute__(self, name):
		value = original_getattribute(self, name)
		print(f'Get: {name} -> {value}')
		return value

	cls.__getattribute__ = __getattribute__
	return cls
```

notes:
- Here, we're creating another class decorator, this time to log when an attribute is accessed
- #demo 
- What if we want to use this for all subclasses as well?

---

```python
@log_attributes
class A:
	...

@log_attributes
class B(A):
	...

@log_attributes
class C(B):
	...
```

notes:
- That's not great...
- The point of inheritance is to pass things through the hierarchy...
- Solution: we can use a metaclass to apply `log_attribute` to each subclass as it is created

---

```python[1-9|1-6|8]
class BaseMeta(type):
	def __new__(mcs, name, bases, namespace, **kwds):
		cls = super().__new__(
			name, bases, namespace, **kwds
		)
		return log_attributes(cls)

class Base(metaclass=BaseMeta):
	pass
```

notes:
- What's going on here!?
- We define a class, `BaseMeta`, which inherits from `type` (more on that in a moment)
	- We give it a `__new__` method, which takes a variety of parameters and passes them to the `__new__` method of `type`
	- We then apply `log_attributes` to this result, and return it
- We've then got another class, `Base`, which seems to have a keyword argument where it's base classes should go?
- Before we get too confused, we should take a step back and look at things one at a time

---

# `type`

```python
>>> type(5) == int
```
<!-- element class="fragment" -->

```python
>>> type(int) == type
```
<!-- element class="fragment" -->

```python
>>> type(type) == type
```
<!-- element class="fragment" -->

notes:
- In Python, all values have a type
- If we pass a value to `type`, we can find out what that is
	- For example, `5` is of type `int`
- But `type` returns a value, which must therefore have a type
- So `int` is itself an instance of `type`...
- But what about `type` itself?
- This seems to be the end of the line
- Like many things that come built into Python, `type` looks like a function, but is actually a class
- To summarise, all classes are instances of the built-in `type`

---

```python
class Greeter(Base):
	def __init__(self, name):
		self.name = name

	def greet(self):
		print(f'Hello, {self.name}')
```

notes:
- So how is a class actually created?
- There's 4 main steps, as illustrated in the following pseudocode
- #demo

---

## 1) Isolate the body

```python
body = '''
def __init__(self, name):
	self.name = name

def greet(self):
	print(f'Hello, {self.name}')
'''
```

notes:
- First, Python isolates the body to be used later

---

## 2) Create the namespace

```python
namespace = metaclass.__prepare__('Greeter', (Base,))
```

notes:
- When creating a class, Python needs a dictionary to hold the contained items, known as the namespace
- This is where the `metaclass` first gets involved. We'll get on to what the variable represents soon
- `__prepare__` needs to return some kind of map; if `type` is used as the metaclass, this returns a standard dictionary

---

## 3) Execute the body

```python
exec(body, globals(), namespace)

>>> namespace
{
	'__init__': <function __init__ at 0x...>,
	'greet': <function greet at 0x...>,
}
```

notes:
- Python will then execute the body statements we isolated earlier, using the `namespace` we just created to store the local variables

---

## 4) Instantiate the type

```python
Greeter = type('Greeter', (Base,), namespace)

>>> Greeter
<class 'Greeter'>
>>> g = Greeter('world')
>>> g.greet()
Hello, world!
```

notes:
- The final step is to actually create the type
- We want to give it a name of `Greeter`, it has `Base` as a base class, and uses `namespace` as it's namespace
- Playing around with it, we see it behaves just as we would expect.

---
<!-- .slide: data-auto-animate -->

## `metaclass = ??`

notes:
- So, what was that `metaclass` variable we saw earlier?

---
<!-- .slide: data-auto-animate -->

## `metaclass = type`

notes:
- `metaclass` is a keyword argument to the `type` constructor - and it's default value is `type`
- Hence by default, most classes are defined with `type` as the metaclass, but we can provide our own to replace this
- Metaclasses should usually extend `type`, and override one of `__new__` or `__init__` to alter the behvaiour when we either create or instantiate the type

---

![[class-definition.excalidraw.svg]]

notes:
- Metaclasses get information about class definitions when the type is created
	- They can inspect and modify the data to alter how the class is created
	- In this way, they are similar to class decorators

---

![[inheritance.excalidraw.svg]] <!-- element class="fragment" -->

notes:
- The difference?
- Metaclasses are inherited, passing their traits across the object hierarchy.

---

# Recap

### Wrapping & Rewriting <!-- element class="fragment" -->

### Decorators for functions & classes <!-- element class="fragment" -->

### Metaclasses control inheritance <!-- element class="fragment" -->

notes:
- Before we carry on, lets have a look back at what we've covered so far
- We've mostly been concerned with wrapping and rewriting things
- We can use decorators to alter the behaviour of functions and classes
- We can use metaclasses to interfere with classes and their descendants, controlling inheritance

---

# Structures <!-- element class="fragment" -->

notes:
- Let's move on to a more complex example, something more common and with a lot more boilerplate: structures
- For the moment, we'll assume that the `dataclasses` module doesn't exist.
	- It's worth checking out if you've not heard of it before

---

```python
class Point:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

class Host:
	def __init__(self, address, port):
		self.address = address
		self.port = port
```

notes:
- We've got two classes here, `Point` and `Host`
- At the moment they seem quite different, but they're not particularly useful

---

```python
class Point:
	...
	def __repr__(self):
		name = type(self).__name__
		return f'{name}({self.x}, {self.y}, {self.z})'

class Host:
	...
	def __repr__(self):
		name = type(self).__name__
		return f'{name}({self.address}, {self.port})'
```

notes:
- So we can print instances nicely, we'll want a `repr` method
- They're almost identical...

---

```python
class Point:
	...
	def __eq__(self, other):
		if not isinstance(other, type(self)):
			return False
		return self.x == other.x and self.y == other.y and self.z == other.z

class Host:
	...
	def __eq__(self, other):
		if not isinstance(other, type(self)):
			return False
		return self.address == other.address and self.port == other.port
```

notes:
- Next we define a test for equality
	- The code doesn't entirely fit on the screen, but we're just checking each field in `self` against its opposite in `other`
- Again, these are almost identical

---

# Solution

notes:
- We'll start with a simple solution, and build it up to remove as much boilerplate as we can, heading for something a little more abstract when we take things too far for the final step
- #demo 

---

```python
class Structure:
	__fields__ = ()

	def __init__(self, *args):
		assert len(self.__fields__) == len(args)
		for field, arg in zip(self.__fields__, args):
			setattr(self, field, arg)
```

notes:
- For our first implementation, we'll create a class called `Structure`
- We're giving it a class attribute, `fields`, which will be overridden by subclasses
- In the initialiser, we check that `__fields__` and `args` are of the same length
	- We then set each field to the given value

---

```python
class Point(Structure):
	__fields__ = 'x', 'y', 'z'

class Host(Structure):
	__fields__ = 'address', 'port'
```

notes:
- That's already removed loads of boilerplate code
- Whilst we've not implemented all the methods we described before, we could very easily implement these in the `Structure` class
- However,
	- We can't pass keyword arguments
	- We have no clue what the signature of the function is supposed to be 
	- #demo `print(inspect.signature(Point))`

---

```python
from inspect import Parameter, Signature

def make_signature(*fields):
	return Signature([
		Parameter(name, Parameter.POSITIONAL_OR_KEYWORD)
		for name in fields
	])
```

```python
class Structure:
	__signature__ = None

	def __init__(self, *args, **kwargs):
		assert self.__signature__ is not None
		bound = self.__signature__.bind(*args, **kwargs)
		for name, value in bound.arguments.items():
			setattr(self, name, value)
```

notes:
- To solve these issues we create the `make_signature` function, which we'll use to generate so called signatures
	- A `Signature` is an ordered list of parameters, for each recording the name and how it can be passed
- We can then adjust the `Structure` class, replacing `__fields__` with `__signature__`
- In the initialiser, we then bind the arguments to the signature, which allows us to handle both arguments and keyword arguments easily and correctly
	- This will also ensure that a `Structure` cannot be created with the wrong number of arguments
- As before, we can then iterate over the arguments and populate our fields

---

```python
class Point(Structure):
	__signature__ = make_signature('x', 'y', 'z')

class Host(Structure):
	__signature__ = make_signature('address', 'host')
```

notes:
- Whilst it is cleaner than our original code, and more functional that the first solution, we've added some boilerplate
- Every structure we make must define `__signature__` which makes a call to `make_signature`
-  It's also harder to generate methods like `__repr__` and `__eq__`, as we no longer simply have a list of the fields
- We'd like to be able to just give the fields, and have the signature generated for us
- We could put it in the `Structure` initialiser, but it seems a waste to regenerate the signature every time
- That leaves us with two options to investigate:
	- A class decorator
	- Creating a metaclass

---

```python
class add_signature:
	def __init__(self, *fields):
		self.fields = fields

	def __call__(self, cls):
		cls.__signature__ = make_signature(self.fields)
		return cls
```

notes:
- Here, we create a simple decorator as a class
- This has the same effect as nesting functions, but is a bit neater
- A side note about the name of this function: it's in snake case

---

`PascalCase`

`snake_case`

`SHOUTING_SNAKE_CASE`

notes:
- There's two schools of thought about naming things in Python.
- The first states that things should follow the naming convention of what they are.
	- For Python, that means classes are named in `PascalCase`, variables and functions in `snake_case`, and constants in `SHOUTING_SNAKE_CASE`.
- The other idea is that things should base their names, not on what they are.
	- This means that, if we create a class in a function and assign the result to a variable, name that variable like a class.
	- If a class is supposed to look like a function or decorator (like ours from before), name it like a function.
- As you may be able to tell, I tend to follow this latter method: we write libraries for other people to use, and they don't need to know how we've implemented it.

---

```python
class StructureMeta(type):
	def __new__(mcs, name, bases, namespace, **kwds):
		cls = super().__new__(name, bases, namespace, **kwds)
		cls.__signature__ = make_signature(cls.__fields__)
		return cls

class Structure(metaclass=StructureMeta):
	__fields__ = ()

	def __init__(self, *args, **kwargs):
		bound = self.__signature__.bind(*args, **kwargs)
		for name, value in bound.arguments.items():
			setattr(self, name, value)
```

notes:
- Here, we're creating a metaclass, `StructureMeta`.
	- When the class itself is created, we create the signature and apply it to the class.
- We recreate the `Structure` class, now to use our metaclass.
- The initialiser remains the same.

---

### `@decorator`

## vs

### `(metaclass=...)`

notes:
- The decorator option is certainly the simplest, however...
- It doesn't store the fields, which we've seen is unhelpful for other methods
	- It could be added quite easily though
- The declaration of the fields is somewhat detached from the class, appearing in the decorator
- The utility of `Structure` doesn't get passed through the inheritance hierarchy if we use decorators
- Hence the metaclass seems to be a sensible way to go

---

