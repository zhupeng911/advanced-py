# 线性回归（Linear Regression）是解决回归问题的最基础、最经典的统计学与机器学习模型
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# 1. 准备训练数据
# X 需要是二维数组 (样本数, 特征数)
X = np.array([[5], [10], [12], [13], [15]])
Y = np.array([20, 15, 8, 6, 4])

# 2. 初始化并训练模型（框架会自动运行优化算法如梯度下降）
reg = LinearRegression()
reg.fit(X, Y)

# 3. 输出模型学到的参数
print(f"权重 (reg.coef_): {reg.coef_[0]:.8f}")       # 输出约 -1.70689655
print(f"截距 (reg.intercept_): {reg.intercept_:.8f}") # 输出约 29.37586207

# 4. 生成预测曲线的数据
X_test = np.linspace(0, 15, 100).reshape(-1, 1)
Y_test = reg.predict(X_test)

# 5. 可视化绘制
plt.figure(figsize=(6, 4))
plt.scatter(X, Y, color='black', label='Training Data')
plt.plot(X_test, Y_test, color='blue', linewidth=3, label='Regression Line')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Linear Regression Example')
plt.legend()
plt.grid(True)
plt.show()