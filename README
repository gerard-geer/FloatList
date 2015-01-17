FloatList
=========

You know, Python lists would just be more fun if you can peek in between elements.

Why
---

I had a list of values that were sampled from a waveform, and I needed a way to interpolate
between them. I also wanted to do something silly.

Examples
--------
```python
>>> from floatlist import FloatList
>>> f = FloatList([0, 4, 5, 6])
>>> f[.125]
0.5
>>> f[.75]
3.0
>>> f[3.0]
6.0
>>> f[-.5]
3.0
>>> f[10000.0]
0.0
>>> f[10001.0]
4.0
>>> f[0.0:1.0:.2]
[0.0, 0.8, 1.6, 2.4000000000000004, 3.2, 4.0]
>>> f
[0, 4, 5, 6]
>>> f[.5] = 2
>>> f
[1.0, 3.0, 5, 6]
>>> f[0] = 0
>>> f[1] = 4
>>> f
[0.0, 4.0, 5, 6]
>>> f[.75] = 1.0
>>> f
[0.25, 1.75, 5, 6]
```
