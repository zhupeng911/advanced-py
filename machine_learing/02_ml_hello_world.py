from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 1. 加载数据（机器学习的“教材”）
X, y = load_iris(return_X_y=True)

# 2. 切分数据集（留出20%当作“模拟考卷”，训练时绝对不看）
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. 创建模型（随机森林，一个很鲁棒的算法）
model = RandomForestClassifier()

# 4. 开始学习（拟合/训练）
model.fit(X_train, y_train)

# 5. 模拟考（在没见过的数据上预测）
y_pred = model.predict(X_test)

# 6. 出成绩（计算预测准确率）
score = accuracy_score(y_test, y_pred)
print(f"模型准确率: {score:.2f}")  # 你会看到输出 1.00，即100%正确