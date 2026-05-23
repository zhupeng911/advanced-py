from mcp.server.fastmcp import FastMCP

# 1.创建MCP实例：FastMCP类似于spring mvc
mcp = FastMCP(
    name="WeatherServerSSE",
    host="0.0.0.0",  # 模拟对外暴露服务
    port=8000
)


# 2.为MCP添加工具
@mcp.tool()
def get_weather(city: str) -> str:
    # url = "https://api.openweathermap.org/data/2.5/weather"
    # params = {
    #     "q": city,
    #     "appid": "xxx",
    #     "units": "metric",
    #     "lang": "zh_cn"
    # }
    # resp = httpx.get(url, params=params, timeout=5)
    # data = resp.json()
    # print(f'查询：{city} 的天气为:{data}')
    # return json.dumps(data, ensure_ascii=False)
    return "查询：{city} 的天气为:{{'weather': 'sunny', 'temperature': '25摄氏度'}}"


# 3.为MCP添加工具
@mcp.tool()
def get_coordinate(city: str) -> str:
    return "查询：{city} 的坐标为:{{'latitude': '39.9042', 'longitude': '116.4074'}}"


if __name__ == "__main__":
    print("启动MCP服务...")
    mcp.run(transport="sse")
