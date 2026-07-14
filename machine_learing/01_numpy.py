# numpy(Numerical Python)：Python的科学计算库
# 应用场景：
# 做数据清洗/分析（配合 Pandas）
# 做机器学习建模（特征工程、数据预处理）
# 做图像/音频处理（图像本质就是多维数组）
# 做数值模拟或学术研究中的复杂数学计算
# 核心功能：多维数组对象（ndarray）、索引切片、广播机制（Broadcasting）和聚合统计

import numpy as np


def demo_create():
    """1. 创建数组"""
    print("=" * 50)
    print("1. 创建数组")
    print("=" * 50)

    # 从列表创建
    a1 = np.array([1, 2, 3, 4, 5])
    a2 = np.array([[1, 2, 3], [4, 5, 6]])
    print(f"一维数组: {a1}")
    print(f"二维数组:\n{a2}")

    # 指定数据类型
    a3 = np.array([1, 2, 3], dtype=np.float32)
    print(f"指定float32: {a3}, dtype={a3.dtype}")

    # 全0 / 全1
    zeros = np.zeros((2, 3))
    ones = np.ones((2, 3))
    print(f"全0 (2x3):\n{zeros}")
    print(f"全1 (2x3):\n{ones}")

    # 未初始化（速度快，内容随机）
    empty = np.empty((2, 3))
    print(f"empty (2x3):\n{empty}")

    # 单位矩阵 / 对角矩阵
    eye = np.eye(3)
    print(f"单位矩阵 (3x3):\n{eye}")

    # 等差数列
    arange = np.arange(0, 10, 2)          # start, stop, step
    linspace = np.linspace(0, 1, 5)       # start, stop, num
    print(f"arange(0,10,2): {arange}")
    print(f"linspace(0,1,5): {linspace}")

    # 全填充
    full = np.full((2, 3), 42)
    print(f"full(2x3, 42):\n{full}")


def demo_attr():
    """2. 数组属性"""
    print("=" * 50)
    print("2. 数组属性")
    print("=" * 50)

    a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    print(f"数组:\n{a}")
    print(f"shape:   {a.shape}")      # 形状
    print(f"ndim:    {a.ndim}")        # 维度数
    print(f"size:    {a.size}")         # 元素总数
    print(f"dtype:   {a.dtype}")       # 数据类型
    print(f"itemsize: {a.itemsize} bytes")  # 每个元素字节数
    print(f"nbytes:  {a.nbytes} bytes")    # 总字节数


def demo_index_slice():
    """3. 索引与切片"""
    print("=" * 50)
    print("3. 索引与切片")
    print("=" * 50)

    a = np.array([[1, 2, 3, 4],
                   [5, 6, 7, 8],
                   [9, 10, 11, 12]])
    print(f"原数组:\n{a}")

    # 基本索引
    print(f"a[0, 0] = {a[0, 0]}")
    print(f"a[1, 2] = {a[1, 2]}")

    # 切片（视图，非拷贝）
    print(f"第1行:    {a[0]}")
    print(f"第1列:    {a[:, 0]}")
    print(f"前2行前2列:\n{a[:2, :2]}")
    print(f"每隔一列: {a[:, ::2]}")

    # 花式索引（整数数组索引）
    print(f"取第0,2行:\n{a[[0, 2]]}")
    print(f"取(0,1),(1,2),(2,3)位置元素: {a[[0, 1, 2], [1, 2, 3]]}")


def demo_bool_index():
    """4. 布尔索引（条件筛选）"""
    print("=" * 50)
    print("4. 布尔索引")
    print("=" * 50)

    a = np.array([15, 8, 23, 4, 42, 16])
    print(f"原数组: {a}")

    # 条件筛选
    mask = a > 15
    print(f"a > 15 的掩码: {mask}")
    print(f"a[a > 15]: {a[a > 15]}")

    # 多条件（用 & | ~，不能用 and/or/not）
    print(f"a[(a > 10) & (a < 30)]: {a[(a > 10) & (a < 30)]}")

    # 二维布尔索引
    b = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    print(f"b:\n{b}")
    print(f"b[b > 5]: {b[b > 5]}")

    # np.where 三目运算
    result = np.where(a > 15, a, -1)
    print(f"np.where(a > 15, a, -1): {result}")


def demo_reshape():
    """5. 形状变换"""
    print("=" * 50)
    print("5. 形状变换")
    print("=" * 50)

    a = np.arange(12)
    print(f"原数组(1x12): {a}")

    # reshape
    b = a.reshape(3, 4)
    print(f"reshape(3,4):\n{b}")

    # 自动计算维度（-1）
    c = a.reshape(2, -1)
    print(f"reshape(2,-1):\n{c}")

    # 展平
    print(f"ravel(): {b.ravel()}")
    print(f"flatten(): {b.flatten()}")

    # 转置
    print(f"b.T:\n{b.T}")

    # 增加/减少维度
    d = np.array([1, 2, 3])
    print(f"原shape: {d.shape}")
    print(f"np.newaxis 列向量:\n{d[:, np.newaxis]}, shape={d[:, np.newaxis].shape}")
    print(f"expand_dims: shape={np.expand_dims(d, axis=0).shape}")

    # 拼接
    x = np.array([[1, 2], [3, 4]])
    y = np.array([[5, 6], [7, 8]])
    print(f"vstack:\n{np.vstack([x, y])}")
    print(f"hstack:\n{np.hstack([x, y])}")
    print(f"concatenate(axis=0):\n{np.concatenate([x, y], axis=0)}")
    print(f"concatenate(axis=1):\n{np.concatenate([x, y], axis=1)}")


def demo_operation():
    """6. 数组运算（向量化，无需写循环）"""
    print("=" * 50)
    print("6. 数组运算")
    print("=" * 50)

    a = np.array([1, 2, 3, 4])
    b = np.array([10, 20, 30, 40])

    # 逐元素运算
    print(f"a + b = {a + b}")
    print(f"a - b = {a - b}")
    print(f"a * b = {a * b}")       # 逐元素乘（不是矩阵乘法）
    print(f"a / b = {a / b}")
    print(f"a ** 2 = {a ** 2}")
    print(f"np.sqrt(a) = {np.sqrt(a)}")
    print(f"np.log(a) = {np.log(a)}")
    print(f"np.exp(a) = {np.exp(a)}")

    # 矩阵乘法
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[5, 6], [7, 8]])
    print(f"A @ B:\n{A @ B}")                           # Python 3.5+ 推荐写法
    print(f"np.dot(A, B):\n{np.dot(A, B)}")             # 等价
    print(f"np.matmul(A, B):\n{np.matmul(A, B)}")       # 等价


def demo_broadcast():
    """7. 广播机制（Broadcasting）
    不同形状的数组进行运算时，NumPy 自动扩展维度
    规则：从最后一维往前比对，维度相同或其中之一为1才可广播
    """
    print("=" * 50)
    print("7. 广播机制")
    print("=" * 50)

    # 标量与数组
    a = np.array([1, 2, 3, 4])
    print(f"a + 10 = {a + 10}")

    # 一维与二维
    b = np.array([[1, 2, 3],
                   [4, 5, 6]])
    c = np.array([10, 20, 30])
    print(f"b:\n{b}")
    print(f"c: {c}")
    print(f"b + c:\n{b + c}")

    # 列向量 + 行向量
    col = np.array([[1], [2], [3]])   # 3x1
    row = np.array([10, 20, 30])       # (3,) → 广播为 1x3
    print(f"col(3x1) + row(3,):\n{col + row}")

    # 不兼容的广播会报错
    try:
        np.array([1, 2, 3]) + np.array([1, 2])
    except ValueError as e:
        print(f"广播失败: {e}")


def demo_statistics():
    """8. 聚合统计"""
    print("=" * 50)
    print("8. 聚合统计")
    print("=" * 50)

    a = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])
    print(f"数组:\n{a}")

    # 全局统计
    print(f"sum:     {a.sum()}")
    print(f"mean:    {a.mean():.2f}")
    print(f"min:     {a.min()}")
    print(f"max:     {a.max()}")
    print(f"std:     {a.std():.2f}")
    print(f"median:  {np.median(a)}")
    print(f"percentile(50): {np.percentile(a, 50)}")

    # 按轴统计
    print(f"sum(axis=0) 按列求和: {a.sum(axis=0)}")   # (3,3) → (3,)
    print(f"sum(axis=1) 按行求和: {a.sum(axis=1)}")   # (3,3) → (3,)

    # argmax / argmin（最大/最小值的索引）
    print(f"argmax: {a.argmax()}")
    print(f"argmax(axis=0): {a.argmax(axis=0)}")


def demo_linalg():
    """9. 线性代数"""
    print("=" * 50)
    print("9. 线性代数")
    print("=" * 50)

    A = np.array([[1, 2], [3, 4]])
    v = np.array([5, 6])

    # 矩阵乘法 / 矩阵-向量乘法
    print(f"A @ v = {A @ v}")

    # 逆矩阵
    A_inv = np.linalg.inv(A)
    print(f"A 的逆矩阵:\n{A_inv}")
    print(f"A @ A_inv:\n{A @ A_inv}")

    # 行列式
    print(f"det(A) = {np.linalg.det(A):.2f}")

    # 特征值与特征向量
    eigenvalues, eigenvectors = np.linalg.eig(A)
    print(f"特征值: {eigenvalues}")
    print(f"特征向量:\n{eigenvectors}")

    # 解线性方程组 Ax = b
    b = np.array([1, 2])
    x = np.linalg.solve(A, b)
    print(f"解 Ax = b, x = {x}")
    print(f"验证 A @ x = {A @ x}")

    # SVD 分解
    U, S, Vt = np.linalg.svd(A)
    print(f"SVD - U:\n{U}")
    print(f"SVD - 奇异值: {S}")
    print(f"SVD - Vt:\n{Vt}")


def demo_random():
    """10. 随机数生成"""
    print("=" * 50)
    print("10. 随机数生成")
    print("=" * 50)

    # 设置随机种子（保证可复现）
    rng = np.random.default_rng(42)

    # 均匀分布 [0, 1)
    print(f"uniform [0,1): {rng.random(5)}")

    # 标准正态分布
    print(f"标准正态: {rng.standard_normal(5)}")

    # 正态分布 N(μ, σ)
    print(f"正态 N(10, 2): {rng.normal(10, 2, 5)}")

    # 随机整数
    print(f"整数 [0, 10): {rng.integers(0, 10, 10)}")

    # 随机打乱
    a = np.arange(10)
    rng.shuffle(a)
    print(f"打乱: {a}")

    # 随机抽样
    choices = rng.choice([1, 2, 3, 4, 5], size=3, replace=False)
    print(f"不放回抽样(3个): {choices}")


def demo_sort_search():
    """11. 排序与搜索"""
    print("=" * 50)
    print("11. 排序与搜索")
    print("=" * 50)

    a = np.array([3, 1, 4, 1, 5, 9, 2, 6])
    print(f"原数组: {a}")

    # 排序（返回新数组）
    print(f"np.sort(a): {np.sort(a)}")

    # 原地排序
    b = a.copy()
    b.sort()
    print(f"原地sort: {b}")

    # argsort（返回排序后的索引）
    print(f"argsort: {a.argsort()}")

    # 二维按轴排序
    c = np.array([[3, 1, 4], [1, 5, 9], [2, 6, 5]])
    print(f"二维:\n{c}")
    print(f"按行排序(axis=1):\n{np.sort(c, axis=1)}")
    print(f"按列排序(axis=0):\n{np.sort(c, axis=0)}")

    # 搜索
    arr = np.array([10, 20, 30, 40, 50])
    print(f"搜索数组: {arr}")
    print(f"30 的索引(np.where): {np.where(arr == 30)[0][0]}")

    # searchsorted（在有序数组中查找插入位置）
    print(f"25 应插入位置: {np.searchsorted(arr, 25)}")


def demo_unique_set():
    """12. 去重与集合运算"""
    print("=" * 50)
    print("12. 去重与集合运算")
    print("=" * 50)

    a = np.array([3, 1, 2, 3, 1, 4, 2, 1])

    # 去重
    unique_vals, counts = np.unique(a, return_counts=True)
    unique_idx = np.unique(a, return_index=True)[1]
    unique_inverse = np.unique(a, return_inverse=True)[1]

    print(f"原数组: {a}")
    print(f"去重值: {unique_vals}")
    print(f"出现次数: {counts}")
    print(f"首次出现索引: {unique_idx}")
    print(f"反向映射: {unique_inverse}")

    # 集合运算
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([4, 5, 6, 7, 8])
    print(f"x: {x}, y: {y}")
    print(f"交集 np.intersect1d: {np.intersect1d(x, y)}")
    print(f"并集 np.union1d: {np.union1d(x, y)}")
    print(f"差集 np.setdiff1d(x, y): {np.setdiff1d(x, y)}")


def demo_copy():
    """13. 视图与拷贝"""
    print("=" * 50)
    print("13. 视图与拷贝")
    print("=" * 50)

    a = np.array([1, 2, 3, 4, 5])

    # 视图（view）：切片返回视图，修改视图会影响原数组
    v = a[1:4]
    v[0] = 99
    print(f"a[1:4]是视图，修改后 a = {a}")  # a 也被修改

    # 浅拷贝（copy）：独立数据
    a2 = np.array([1, 2, 3, 4, 5])
    c = a2[1:4].copy()
    c[0] = 99
    print(f".copy()是拷贝，修改后 a2 = {a2}")  # a2 不变

    # 判断是否是视图
    a3 = np.array([1, 2, 3, 4, 5])
    print(f"切片是视图: {a3[1:4].base is not None}")
    print(f"copy不是视图: {a3[1:4].copy().base is not None}")


def demo_io():
    """14. 文件读写"""
    print("=" * 50)
    print("14. 文件读写")
    print("=" * 50)

    a = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])

    # 保存为 .npy（NumPy 二进制格式）
    np.save('/tmp/demo.npy', a)
    loaded = np.load('/tmp/demo.npy')
    print(f"原始:\n{a}")
    print(f"从 .npy 加载:\n{loaded}")

    # 保存为 .csv
    np.savetxt('/tmp/demo.csv', a, delimiter=',', fmt='%.1f',
               header='col1,col2,col3', comments='')
    loaded_csv = np.loadtxt('/tmp/demo.csv', delimiter=',', skiprows=1)
    print(f"从 .csv 加载:\n{loaded_csv}")

    # 多个数组保存到 .npz
    b = np.array([10, 20, 30])
    np.savez('/tmp/demo.npz', features=a, labels=b)
    data = np.load('/tmp/demo.npz')
    print(f"从 .npz 加载, keys={list(data.keys())}")
    print(f"features:\n{data['features']}")
    print(f"labels: {data['labels']}")


if __name__ == '__main__':
    demo_create()
    demo_attr()
    demo_index_slice()
    demo_bool_index()
    demo_reshape()
    demo_operation()
    demo_broadcast()
    demo_statistics()
    demo_linalg()
    demo_random()
    demo_sort_search()
    demo_unique_set()
    demo_copy()
    demo_io()
