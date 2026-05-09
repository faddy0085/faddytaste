import streamlit as st
import yfinance as yf
import time
import stock_f as sf
import itnetai as cai
import streamlit.components.v1 as components

# =============================================================
# 1. 缓存数据获取函数 (使用缓存，提高性能)
# =============================================================
if "str_title" not in st.session_state:
    st.session_state.str_title = ""
if 'data_report' not in st.session_state:
    st.session_state.data_report=""
if 'news_report' not in st.session_state:
    st.session_state.news_report=""
if 'ai_report' not in st.session_state:
    st.session_state.ai_report=""
if 'ai_reportP' not in st.session_state:
    st.session_state.ai_reportP=""
if 'stop_alz' not in st.session_state:
    st.session_state.stop_alz = True #人工智能按钮可用
if 'stop_save' not in st.session_state: #保存按钮禁用
    st.session_state.stop_save = True
if 'saved_form' not in st.session_state:
    st.session_state.saved_form = None
    


def btnf_alz():
    st.session_state.stop_alz=True
    st.session_state.stop_save=False
def btnf_save():
    st.session_state.stop_alz=True
    st.session_state.stop_save=True


 ####################################################   
def ipt_chang():
    strp=st.session_state.ipt_sy
    st.session_state.str_title=st.session_state.ipt_sy
    info0,info1,info2=sf.analyze_market([strp])
    st.session_state["ai_report"]=""
    st.session_state.stop_alz=False
    st.session_state.stop_save=False
    st.session_state.data_report=info0
    st.session_state.news_report=info1
    if not info2.empty:
        # 绘制收盘价折线图
        st.session_state.data_form=info2['Close']
    else:
        st.error("未获取到历史价格数据，请检查股票代码。")
    
    str_ticketp=st.session_state.str_title
    context = f"""
    {st.session_state.data_report}      
    {st.session_state.news_report}
    """
    prompt = f"作为一位资深财经分析师。基于以下数据，给出对 {str_ticketp} 的简要分析和建议：\n{context}"

    str_res=cai.ai_response(prompt)
    st.session_state["ai_report"] = str_res
    st.session_state["ai_reportp"] = str_res
    
def btn_serchf():
    strp=st.session_state.slt_stock
    st.session_state.str_title=st.session_state.slt_stock
    info0,info1,info2=sf.analyze_market([strp])
    st.session_state["ai_report"]=""
    st.session_state.stop_alz=False
    st.session_state.stop_save=False
    st.session_state.data_report=info0
    st.session_state.news_report=info1
    if not info2.empty:
        # 绘制收盘价折线图
        st.session_state.data_form=info2['Close']
    else:
        st.error("未获取到历史价格数据，请检查股票代码。")

    str_ticketp=st.session_state.str_title
    context = f"""
    {st.session_state.data_report}      
    {st.session_state.news_report}
    """
    prompt = f"你是一位资深财经分析师。基于以下数据，给出对 {str_ticketp} 的简要分析和建议：\n{context}"
    str_res=cai.ai_response(prompt)
    st.session_state["ai_report"] = str_res
    st.session_state["ai_reportp"] = str_res
####################################################

# 1. 页面配置（设置浏览器标签页标题）
st.set_page_config(page_title="AI 财经分析助手", layout="wide")

st.title("KLAUS财经")

# 2. 侧边栏：获取用户输入
st.sidebar.header("🔍 查询设置")
# 注意：这里使用 text_input，我们仍然需要判断是否为空

names = {
    # --- 指数与宏观 ---
    "^GSPC": "🇺🇸 标普500 (S&P 500)",
    "^NDX": "💻 纳指100 (Nasdaq 100)",
    "^DJI": "🏢 道琼斯 (Dow Jones)",
    "^SOX": "🔌 费城半导体指数",
    "^VIX": "😨 恐慌指数 (VIX)",

     # --- 大宗商品与债 ---
    "GLD": "✨ 黄金 ETF (Gold)",
    "SLV": "🥈 白银 ETF (Silver)",
    "BZ=F": "🛢️ 布伦特原油",
    "TLT": "📉 美债 20年+ (Treasury)",
    "UUP": "💵 美元指数 ETF",
    
    # --- 加密货币 ---
    "BTC-USD": "₿ 比特币 (Bitcoin)",
    "ETH-USD": "💎 以太坊 (Ethereum)",
    "SOL-USD": "☀️ Solana",
    "DOGE-USD": "🐕 狗狗币",

    # --- AI科技股 ---
    "NVDA": "🤖 英伟达 (NVIDIA)",
    "AAPL": "🍎 苹果 (Apple)",
    "TSLA": "⚡ 特斯拉 (Tesla)",
    "MSFT": "🖥️ 微软 (Microsoft)",
    "GOOGL": "🔍 谷歌 (Google)",
    "AMZN": "📦 亚马逊 (Amazon)",
    "META": "📱 Meta (Facebook)",
    "INTC": "🟦 英特尔 (INTEL)",
    "AMD": "🟥 超微 (AMD)",
    "ORCL": "🔴 甲骨文 (Oracle)",
    "QCOM": "🔵 高通 (Qualcomm)",
    "AVGO": "🔮 博通 (Broadcom)",
    "ARM": "📐 ARM",
    "NFLX": "🎥 奈飞 (Netflix)",
    "AMZN": "📦 亚马逊 (Amazon)",

    # --- 医药 ---
    "LLY": "🧬 礼来制药 (Lilly Pharma)",
    "NVO": "💉 诺和诺德 (Novo Nordisk)",
    "UNH": "🛡️ 联合健康 (UnitedHealth)",

    # --- 蓝筹与价值 ---
    "GE": "⚙️ 通用电气 (GE Aerospace)",
    "BRK-B": "🐂 伯克希尔 (BRK-B)",
    "JPM": "🏦 摩根大通",
    "BAC": "🔴 美国银行 (Bank of America)",
    "GS": "🏛️ 高盛 (Goldman Sachs)",
    "V": "💳 Visa",
    "KO": "🔴 可口可乐 (Coca-Cola)",
    "WMT": "🟦 沃尔玛 (Walmart)",
    "COST": "🛒 好市多 (Costco)",
    "MCD": "🟡 麦当劳 (McDonald's)",

    # --- 热门中概 ---
    "BABA": "🟠 阿里巴巴 (Alibaba)",
    "PDD": "🧧 拼多多 (Pinduoduo)",
    "TCEHY": "🎮 腾讯 (Tencent)",
    "BILI": "📺 哔哩哔哩 (Bilibili)",
    "JD": "🔴 京东 (JD.com)",
    "LI": "🚗 理想汽车",
    "NIO": "🔵 蔚来 (NIO)",
    "XPEV": "🟢 小鹏 (XPeng)",
    "LI": "🥈 理想 (Li Auto)",
    "BIDU": "🔵 百度 (Baidu)",
    "NTES": "🔴 网易 (NetEase)",
    "LKNCY": "☕ 瑞幸咖啡 (Luckin)",
    
}

# 2. 自动提取代码列表
symbols = list(names.keys())

# 3. 渲染侧边栏下拉菜单
# 注意：一定要把 selectbox 赋值给一个变量（如 selected_symbol）
selected_symbol = st.sidebar.selectbox(
    "🤖 快捷检索",
    options=symbols,
    format_func=lambda x: names.get(x, x),
    key="slt_stock"
)


#
symbol_btn = st.sidebar.button("检索",on_click=btn_serchf)
symboltxt = st.sidebar.text_input("请输入代码 (如 AAPL, TSLA, NVDA):", key="ipt_sy",on_change=ipt_chang)
analyze_btn = st.sidebar.button("深度AI分析",key="btn_alz",on_click=btnf_alz,disabled=st.session_state.stop_alz)

#############################################


if analyze_btn:
  
    str_ticketp=st.session_state.str_title
    context = f"""
    {st.session_state.data_report}      
    {st.session_state.news_report}
    """
    prompt = f"你是一位资深财经分析师。基于以下数据，给出对 {str_ticketp} 的简要分析和建议：\n{context}"
    str_res=cai.ai_Mresponse(prompt,cai.strGemini[0])
    st.session_state["ai_report"] = str_res
    st.session_state["ai_reportp"] = str_res
    

#--结果显示
try:
    col1,col2 = st.columns(2)
    with col1:
        st.write(f"📈{st.session_state.data_report}")
    with col2:
        st.write("📈价格走势")
        st.line_chart(st.session_state.data_form,height=300,width="stretch")
    if st.session_state.ai_report:
        st.divider()
        with st.container():
            st.subheader("🤖 AI综合分析")
            st.spinner()
            st.markdown(st.session_state.ai_report)
except Exception as e:
    pass
#--
import streamlit as st
import streamlit.components.v1 as components

def print_page():
    # 这个按钮点击后，通过 html 组件注入 JS
    if st.sidebar.button("🖨️ 打印",key="btn_save",on_click=btnf_save,disabled=st.session_state.stop_save):
        components.html(
            """
            <script>
                // 尝试多种路径触发打印，确保穿透沙箱
                const printWindow = window.parent || window;
                printWindow.focus();
                printWindow.print();
            </script>
            """,
            height=0,
        )
        

print_page()

def inject_print_logic():
    # 注入一段 JS 脚本，定义一个打印函数
    st.sidebar.markdown(
        """
        <style>
            .print-text-link {
                color: #ff4b4b;
                cursor: pointer;
                text-decoration: underline;
                font-weight: bold;
            }
            @media print {
                .print-text-link, [data-testid="stSidebar"] {
                    display: none !important;
                }
            }
        </style>
        

        """,
        unsafe_allow_html=True
    )
        # <!-- 使用 span 而不是 a 标签，防止触发页面跳转 -->
        # <div style="text-align: center;">
        #     <span class="print-text-link" onclick="window.parent.print()">
        #         &nbsp;
        #     </span>
        # </div>
inject_print_logic()



