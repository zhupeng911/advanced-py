import json
from flask import Flask, jsonify, make_response, send_file

from config.db_config import Config
from routes.order_routes import order_bp
from routes.product_routes import product_bp
from routes.user_routes import user_bp


def create_app():
    """创建 Flask 应用"""
    app = Flask(__name__)
    app.config.from_object(Config)

    # 注册蓝图
    # 最终路由: /api/users, /api/users/<id>
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(order_bp, url_prefix='/api')
    app.register_blueprint(product_bp, url_prefix='/api')

    # 首页
    @app.route('/')
    def index():
        return send_file('static/index.html')

    # 健康检查
    @app.route('/health')
    def health():
        return jsonify({"status": "healthy"})

    # 全局错误处理
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"code": 404, "message": "资源不存在"}), 404

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"code": 500, "message": "服务器内部错误"}), 500

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(
        host=Config.FLASK_HOST,
        port=Config.FLASK_PORT,
        debug=Config.FLASK_DEBUG
    )
