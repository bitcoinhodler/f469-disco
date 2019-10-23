We tried running this, but it didn't work:

```
python gen_mpy.py -MD hello_mpy.json -MP uhello hello/hello.c
```

You also need to have this checked out in the proper place: https://github.com/eliben/pycparser/tree/e1a1d737be66308b633215fa26ac5ed30e890103

See this makefile for an example of the "proper way" to do all this ... https://github.com/littlevgl/lv_micropython/blob/2940838bf6d4999050efecb29a4152ab5796d5b3/py/py.mk#L22-L38
notes:
- last command run gen_mpy
- second-to-last command does some pycparser magic
