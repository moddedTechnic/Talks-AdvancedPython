---
highlightTheme: monokai
---

<style>
:root {
	--r-code-font: "JetBrains Mono";
}

.reveal .hljs {
	min-height: 50%;
}
</style>

%%

f7f7f7 background slide colour

%%


# TITLE SLIDE

---

# Requirements

Python 3.3

[github.com/moddedTechnic/Talks-LibraryDev](https://github.com/moddedTechnic/Talks-LibraryDev)

notes:
	#TODO fill in GitHub link
	#TODO check Python version

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
def foo(a, b, c):
	d = a + b
	return (d + c) / d
```

notes:
- Whilst statements are the building blocks, functions are a 