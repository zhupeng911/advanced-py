# 虽然名字叫“回归”，但逻辑回归（Logistic Regression）实际上是一种用于解决二分类问题的经典线性模型。
import numpy as np
from sklearn.linear_model import LogisticRegression

# 1. 准备训练数据 (特征: [胸围, 腰围])
X = np.array([
    [82, 62],  # 女
    [79, 59],  # 女
    [81, 63],  # 女
    [72, 68],  # 男
    [73, 70],  # 男
    [74, 68]  # 男
])
Y = np.array([0, 0, 0, 1, 1, 1])

# 2. 模型训练
clf = LogisticRegression(random_state=0).fit(X, Y)

# 3. 预测新样本 (例如：胸围 76, 腰围 72)
test_sample = np.array([[76, 72]])
prediction = clf.predict(test_sample)
print(f"样本 {test_sample[0]} 的预测性别标签为: {prediction[0]} (1代表男生, 0代表女生)")

# 4. 评估模型在训练集上的准确率 (Accuracy)
score = clf.score(X, Y)
print(f"模型在训练集上的准确率: {score * 100:.1f}%")  # 输出 100.0%
