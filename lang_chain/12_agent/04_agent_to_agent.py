from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.tools import tool

from lang_chain.config import OPENAI_API_KEY

# 基于Python + LangChain1.0实现Agent to Agent的写作案例
# 需求：
# 1.模拟携程订机票、美团订酒店、嘀嘀打车的跨平台智能协作流程
# 2.核心是让不同领域的专属Agent分工协作、完成完整的出行服务闭环
# 3.模拟用户“从北京飞上海、订浦东机场附近酒店、从机场打车到酒店的完整需求”
# 设计思路：
# 1.定义三个专属Agent（微服务）：携程机票Agent、美团酒店Agent、嘀嘀打车Agent
# 2.定义一个总控Agent（Nginx）：作为入口接收用户需求，负责将用户需求分解成子任务，并调用相应的专属Agent完成子任务

# 1.定义大模型
llm = init_chat_model(
    model="deepseek-chat",
    model_provider="deepseek",
    api_key=OPENAI_API_KEY,
    base_url="https://api.deepseek.com"
)
output_parser = StrOutputParser()


# 2.定义工具 mock返回数据
@tool("CtripBookFlight", description="预订机票唯一工具，参数说明：departure出发地、arrival目的地、date出发日期")
def ctrip_book_flight(departure: str, arrival: str, date: str) -> str:
    """携程订机票"""
    return f'【携程机票预订成功】携程订机票：从{departure}飞往{arrival}，日期：{date} 已预订 航班号：AA123(北京飞上海) 起飞时间：2023-04-01 10:00 '


@tool("MeituanBookHotel",
      description="预订酒店唯一工具，参数说明：city城市、near_by附近位置、check_in入住日期、check_out退房日期")
def meituan_book_hotel(city: str, near_by: str, check_in: str, check_out: str) -> str:
    """美团订酒店"""
    return f'【美团酒店预订成功】美团订酒店：城市：{city}，位置：{near_by}，入住日期：{check_in}，退房日期：{check_out}'


@tool("DidiCallCar", description="打车唯一工具，参数说明：start起点、end终点、time时间")
def didi_call_car(start: str, end: str, time: str) -> str:
    """嘀嘀打车"""
    return f'【嘀嘀打车成功】嘀嘀打车：从{start}到{end}，时间：{time}'


# 3.定义各专属Agent
def create_ctrip_agent(llm):
    llm_with_tools = llm.bind_tools([ctrip_book_flight])
    prompt = ChatPromptTemplate.from_messages([
        (
            "system", "你是一个专业的携程机票预订助手，只能调用CtripBookFlight工具"
                      "传入参数：departure='北京'、arrival='上海'、date='2023-04-01'"
                      "请根据用户需求，直接返回工具调用结果，不要包含额外的文本"
        ),
        ("human", "{input}")
    ])
    return prompt | llm_with_tools | output_parser


def create_meituan_agent(llm):
    llm_with_tools = llm.bind_tools([meituan_book_hotel])
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个专业的美团酒店预订助手，只能调用MeituanBookHotel工具"
                   "传入参数：city='上海'、near_by='浦东机场附近'、check_in='2023-04-01'、check_out='2023-04-02'"
                   "请根据用户需求，直接返回工具调用结果，不要包含额外的文本"),
        ("human", "{input}")
    ])
    return prompt | llm_with_tools | output_parser


def create_didi_agent(llm):
    llm_with_tools = llm.bind_tools([didi_call_car])
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个专业的嘀嘀打车助手，只能调用DidiCallCar工具"
                   "传入参数：start='浦东机场'、end='酒店'、time='2023-04-01'"
                   "请根据用户需求，直接返回工具调用结果，不要包含额外的文本"),
        ("human", "{input}")
    ])
    return prompt | llm_with_tools | output_parser


# 4.定义总控Agent【装饰器哦】
def create_travel_agent(llm, ctrip_chain, meituan_chain, didi_chain):
    """总控Agent：按顺序调用+空值兜底+打印详细测试"""

    def a2a_schedule(input_dict):
        print("开始执行A2A协作测试，依次调用各业务Agent...")
        ctrip_func = ctrip_book_flight.func  # 获取携程工具原始函数
        meituan_func = meituan_book_hotel.func  # 获取美团工具原始函数
        didi_func = didi_call_car.func

        # 调用携程Agent
        print("1.调用携程Agent...")
        try:
            ctrip_result = ctrip_chain.invoke({"input": "订机票"})
        except:
            ctrip_result = ""
        if not ctrip_result.strip():
            ctrip_result = ctrip_func("北京", "上海", "2023-04-01")  # 兜底
        print(f"携程Agent返回结果：{ctrip_result}")

        # 调用美团Agent
        print("2.调用美团Agent...")
        try:
            meituan_result = meituan_chain.invoke({"input": "订酒店"})
        except:
            meituan_result = ""
        if not meituan_result.strip():
            meituan_result = meituan_func("上海", "浦东机场附近", "2023-04-01", "2023-04-02")  # 兜底
        print(f"美团Agent返回结果：{meituan_result}")

        # 调用嘀嘀Agent
        print("3.调用嘀嘀Agent...")
        try:
            didi_result = didi_chain.invoke({"input": "打车"})
        except:
            didi_result = ""
        if not didi_result.strip():
            didi_result = didi_func("浦东机场", "酒店", "2023-04-01")  # 兜底
        print(f"嘀嘀Agent返回结果：{didi_result}")

        # 整合
        total_report = f"""
            【携程-美团-滴滴️协作测试最终报告】
            携程机票预订结果：{ctrip_result}
            美团酒店预订结果：{meituan_result}
            嘀嘀打车结果：{didi_result}
        """
        return total_report

    return RunnableLambda(a2a_schedule)


if __name__ == '__main__':
    try:
        # 初始化各agent
        print("初始化携程/美团/滴滴专属Agent...")
        ctrip_agent = create_ctrip_agent(llm)
        meituan_agent = create_meituan_agent(llm)
        didi_agent = create_didi_agent(llm)
        print("各agent初始化完成...")

        # 初始化总控Agent
        print("初始化总控Agent...")
        travel_agent = create_travel_agent(llm, ctrip_agent, meituan_agent, didi_agent)
        print("总控Agent初始化完成...")

        # 测试
        print("测试开始...")
        result = travel_agent.invoke({"input": "安排2026-02-01北京飞上海的完整行程"})
        print(result)
    except Exception as e:
        print(e)
