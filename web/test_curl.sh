#!/bin/bash
# Flask CRUD API 测试用例
# 使用方法: bash test_curl.sh

BASE_URL="http://127.0.0.1:8081/api/users"

echo "=========================================="
echo "Flask CRUD API 测试"
echo "=========================================="

# ---------- Create ----------
echo ""
echo "【1】创建用户 - POST $BASE_URL"
curl -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d '{"name": "张三", "email": "zhangsan@example.com", "age": 25}'

# ---------- Create Duplicate ----------
echo ""
echo ""
echo "【2】创建用户（重复邮箱，应返回409） - POST $BASE_URL"
curl -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d '{"name": "李四", "email": "zhangsan@example.com", "age": 30}'

# ---------- Create Missing Fields ----------
echo ""
echo ""
echo "【3】创建用户（缺少必填字段） - POST $BASE_URL"
curl -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d '{"name": "王五"}'

# ---------- Create Second User ----------
echo ""
echo ""
echo "【4】创建第二个用户 - POST $BASE_URL"
curl -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d '{"name": "李四", "email": "lisi@example.com", "age": 30}'

# ---------- Read All ----------
echo ""
echo ""
echo "【5】获取用户列表 - GET $BASE_URL"
curl -X GET "$BASE_URL"

# ---------- Read All with Pagination ----------
echo ""
echo ""
echo "【6】获取用户列表（分页 page=1, page_size=5） - GET $BASE_URL?page=1&page_size=5"
curl -X GET "$BASE_URL?page=1&page_size=5"

# ---------- Read One ----------
echo ""
echo ""
echo "【7】获取单个用户 - GET $BASE_URL/1"
curl -X GET "$BASE_URL/1"

# ---------- Read One Not Found ----------
echo ""
echo ""
echo "【8】获取单个用户（不存在） - GET $BASE_URL/999"
curl -X GET "$BASE_URL/999"

# ---------- Update (PUT) ----------
echo ""
echo ""
echo "【9】全量更新用户 - PUT $BASE_URL/1"
curl -X PUT "$BASE_URL/1" \
  -H "Content-Type: application/json" \
  -d '{"name": "张三改", "email": "zhangsan_new@example.com", "age": 28}'

# ---------- Update (PATCH) ----------
echo ""
echo ""
echo "【10】部分更新用户 - PATCH $BASE_URL/1"
curl -X PATCH "$BASE_URL/1" \
  -H "Content-Type: application/json" \
  -d '{"age": 26}'

# ---------- Update Not Found ----------
echo ""
echo ""
echo "【11】更新用户（不存在） - PUT $BASE_URL/999"
curl -X PUT "$BASE_URL/999" \
  -H "Content-Type: application/json" \
  -d '{"name": "测试", "email": "test@example.com"}'

# ---------- Delete ----------
echo ""
echo ""
echo "【12】删除用户 - DELETE $BASE_URL/2"
curl -X DELETE "$BASE_URL/2"

# ---------- Delete Not Found ----------
echo ""
echo ""
echo "【13】删除用户（不存在） - DELETE $BASE_URL/999"
curl -X DELETE "$BASE_URL/999"

# ---------- Health Check ----------
echo ""
echo ""
echo "【14】健康检查 - GET http://127.0.0.1:8081/health"
curl -X GET "http://127.0.0.1:8081/health"

echo ""
echo ""
echo "=========================================="
echo "测试完成"
echo "=========================================="
