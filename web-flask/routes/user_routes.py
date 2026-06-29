import psycopg
from flask import Blueprint, request

from config.db_pool import db_pool
from models.user import User
from utils.response import success, error
from utils.validators import validate_json, validate_pagination

# 创建蓝图，Blueprint是Flask的模块化组件，用于将大型应用拆分为多个模块
# 参数一：蓝图名称（必须）
# 参数二：当前模块的文件路径（必须）
# 可选：模板目录（默认 blueprints/templates）
# 可选：静态文件目录
# 可选：URL 前缀
user_bp = Blueprint('user', __name__, template_folder='templates', static_folder='static', url_prefix='/user')


# ---------- Create ----------
# 注册路由
@user_bp.route('/users', methods=['POST'])
@validate_json('name', 'email')
def create_user():
    """创建用户"""
    data = request.get_json()

    try:
        with db_pool.pool.connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO users (name, email, age)
                VALUES (%s, %s, %s) RETURNING id, name, email, age, created_at, updated_at
                """,
                (data['name'], data['email'], data.get('age'))
            )
            # 从数据库取出一条记录
            row = cursor.fetchone()
            # 提交事务
            conn.commit()
            # 创建 User 对象
            user = User.from_row(row)
            return success(data=user.to_dict(), message="用户创建成功", code=201)

    except psycopg.errors.UniqueViolation:
        return error("邮箱已存在", 409)
    except Exception as e:
        return error(f"创建用户失败: {str(e)}", 500)


# ---------- Read All (分页) ----------
@user_bp.route('/users', methods=['GET'])
@validate_pagination
def get_users(page, page_size):
    """获取用户列表（分页）"""
    offset = (page - 1) * page_size

    with db_pool.pool.connection() as conn:
        cursor = conn.cursor()

        # 查询总数
        cursor.execute("SELECT COUNT(*) FROM users")
        total = cursor.fetchone()[0]

        # 查询分页数据
        cursor.execute(
            """
            SELECT id, name, email, age, created_at, updated_at
            FROM users
            ORDER BY created_at DESC
                LIMIT %s
            OFFSET %s
            """,
            (page_size, offset)
        )
        rows = cursor.fetchall()

        users = [User.from_row(row).to_dict() for row in rows]

        return success(data={
            "users": users,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total": total,
                "total_pages": (total + page_size - 1) // page_size
            }
        })


# ---------- Read One ----------
@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """获取单个用户"""
    with db_pool.pool.connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, email, age, created_at, updated_at FROM users WHERE id = %s",
            (user_id,)
        )
        row = cursor.fetchone()

        if not row:
            return error("用户不存在", 404)

        user = User.from_row(row)
        return success(data=user.to_dict())


# ---------- Update (PUT 全量更新) ----------
@user_bp.route('/users/<int:user_id>', methods=['POST'])
@validate_json('name', 'email')
def update_user(user_id):
    """完整更新用户"""
    data = request.get_json()

    with db_pool.pool.connection() as conn:
        cursor = conn.cursor()

        # 检查用户是否存在
        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        if not cursor.fetchone():
            return error("用户不存在", 404)

        # 更新用户
        cursor.execute(
            """
            UPDATE users
            SET name       = %s,
                email      = %s,
                age        = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s RETURNING id, name, email, age, created_at, updated_at
            """,
            (data['name'], data['email'], data.get('age'), user_id)
        )
        row = cursor.fetchone()
        conn.commit()

        user = User.from_row(row)
        return success(data=user.to_dict(), message="用户更新成功")


# ---------- Update (PATCH 部分更新) ----------
@user_bp.route('/users/<int:user_id>', methods=['PATCH'])
def patch_user(user_id):
    """部分更新用户"""
    if not request.is_json:
        return error("请求必须是 JSON 格式", 400)

    data = request.get_json()
    if not data:
        return error("没有要更新的字段", 400)

    # 动态构建更新语句
    allowed_fields = ['name', 'email', 'age']
    update_fields = []
    values = []

    for field in allowed_fields:
        if field in data:
            update_fields.append(f"{field} = %s")
            values.append(data[field])

    if not update_fields:
        return error("没有有效的更新字段", 400)

    update_fields.append("updated_at = CURRENT_TIMESTAMP")
    values.append(user_id)

    with db_pool.pool.connection() as conn:
        cursor = conn.cursor()

        # 检查用户是否存在
        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        if not cursor.fetchone():
            return error("用户不存在", 404)

        sql = f"UPDATE users SET {', '.join(update_fields)} WHERE id = %s RETURNING id, name, email, age, created_at, updated_at"
        cursor.execute(sql, values)
        row = cursor.fetchone()
        conn.commit()

        user = User.from_row(row)
        return success(data=user.to_dict(), message="用户更新成功")


# ---------- Delete ----------
@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """删除用户"""
    with db_pool.pool.connection() as conn:
        cursor = conn.cursor()

        # 检查用户是否存在
        cursor.execute("SELECT id FROM users WHERE id = %s", (user_id,))
        if not cursor.fetchone():
            return error("用户不存在", 404)

        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()

        return success(message="用户删除成功")
