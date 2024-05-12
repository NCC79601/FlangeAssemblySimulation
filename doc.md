# 开发文档
## 通讯协议
通过 socket 进行通讯，格式为 JSON。具体流程如下：

```mermaid
graph LR
    A[comm]--->|cmd_data|B[ANSYS]
```

### `cmd_data`:
- `'cmd'`: 命令类型
  - 若为 `exit`，则退出程序
  - 若为 `solve`，则根据设置的预紧力进行求解
- `'pretensions'`：各个螺栓的预紧力，对应的值为一个数组

# 试验记录
## 2024-5-12
### 初次测试
1. 同轴度：0.0238；拧紧B、C、E

```python
data = [
    {
        'dis_to_up_up': 40e-3,
        'readings': [385e-6, 382e-6, 382e-6, 382e-6, 376e-6, 375e-6]
    },
    {
        'dis_to_up_up': 50e-3,
        'readings': [383e-6, 390e-6, 390e-6, 390e-6, 388e-6, 388e-6]
    },
    {
        'dis_to_up_up': 60e-3,
        'readings': [382e-6, 387e-6, 387e-6, 387e-6, 382e-6, 382e-6]
    }
]
```
2. 同轴度：0.0137；拧紧A、B、E、F
```python
data = [
    {
        'dis_to_up_up': 40e-3,
        'readings': [385e-6, 382e-6, 382e-6, 382e-6, 375e-6, 375e-6]
    },
    {
        'dis_to_up_up': 50e-3,
        'readings': [382e-6, 387e-6, 387e-6, 384e-6, 380e-6, 380e-6]
    },
    {
        'dis_to_up_up': 60e-3,
        'readings': [380e-6, 382e-6, 382e-6, 381e-6, 375e-6, 374e-6]
    }
]
```

---

3. 同轴度：0.0256；拧紧A、B、C、D、F
```python
data = [
    {
        'dis_to_up_up': 40e-3,
        'readings': [413e-6, 413e-6, 413e-6, 413e-6, 413e-6, 413e-6]
    },
    {
        'dis_to_up_up': 50e-3,
        'readings': [404e-6, 409e-6, 409e-6, 409e-6, 405e-6, 404e-6]
    },
    {
        'dis_to_up_up': 60e-3,
        'readings': [407e-6, 412e-6, 412e-6, 412e-6, 408e-6, 408e-6]
    }
]
```

4. 同轴度：0.0226，拧紧A、B、E、F
```python
data = [
    {
        'dis_to_up_up': 40e-3,
        'readings': [411e-6, 412e-6, 412e-6, 412e-6, 412e-6, 411e-6]
    },
    {
        'dis_to_up_up': 50e-3,
        'readings': [407e-6, 410e-6, 410e-6, 410e-6, 408e-6, 407e-6]
    },
    {
        'dis_to_up_up': 60e-3,
        'readings': [399e-6, 404e-6, 404e-6, 404e-6, 401e-6, 399e-6]
    }
]
```

5. 同轴度：0.0216
```python
data = [
    {
        'dis_to_up_up': 40e-3,
        'readings': [392e-6, 396e-6, 396e-6, 396e-6, 392e-6, 392e-6]
    },
    {
        'dis_to_up_up': 50e-3,
        'readings': [382e-6, 385e-6, 385e-6, 385e-6, 383e-6, 382e-6]
    },
    {
        'dis_to_up_up': 60e-3,
        'readings': [374e-6, 382e-6, 382e-6, 382e-6, 380e-6, 374e-6]
    }
]
```

---

### REMAKE!
1. 同轴度：0.0143，拧紧A、D、E
```python
data = [
    {
        'dis_to_up_up': 40e-3,
        'readings': [375e-6, 378e-6, 378e-6, 378e-6, 375e-6, 375e-6]
    },
    {
        'dis_to_up_up': 50e-3,
        'readings': [375e-6, 375e-6, 375e-6, 375e-6, 375e-6, 375e-6]
    },
    {
        'dis_to_up_up': 60e-3,
        'readings': [379.5e-6, 380e-6, 380e-6, 380e-6, 380e-6, 379e-6]
    }
]
```
2. 同轴度：0.0060
```python
data = [
    {
        'dis_to_up_up': 40e-3,
        'readings': [382e-6, 384e-6, 384e-6, 384e-6, 383e-6, 382e-6]
    },
    {
        'dis_to_up_up': 50e-3,
        'readings': [381e-6, 381e-6, 381e-6, 381e-6, 381e-6, 381e-6]
    },
    {
        'dis_to_up_up': 60e-3,
        'readings': [378e-6, 379e-6, 379e-6, 379e-6, 379e-6, 378e-6]
    }
]
```