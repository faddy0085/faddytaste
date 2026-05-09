from google import genai
import os
import streamlit as st

strGemini=["gemini-2.5-flash-lite","gemini-2.0-flash","gemini-2.0-flash-lite"]
strGeminiM=["gemini-2.5-flash"]
str429="AI免费额度用完请资助作者。"
def callai():
    try:
        str_key = st.secrets["GEMINI_API_KEY"]
        client = genai.Client(api_key=str_key)
        return client     
    except Exception as e:
        print(f"Call error: {e}")

def ai_response(iptprompt):
    client=callai()
    for model_name in strGemini:
        try:
            # 尝试调用当前模型
            response = client.models.generate_content(
                model=model_name,
                contents=iptprompt
            )
            # 如果成功，直接返回结果，结束循环
            str_response=response.text
            return str_response
            
        except Exception as e:
            # 如果报错（比如 429 配额满了），打印一下提醒，然后继续循环
            print(f"模型 {model_name} 调用失败，正在尝试下一个... 错误: {e}")
            if"429" in str(e):
                str_response=f"{str429}"
            else:
                str_response=f"{e}"
            continue
    return str_response

def ai_Mresponse(iptprompt,iptmodel):
    try:
        # 1. 获取连接
        client = callai()
        
        # 2. 调用模型 (确保模型名正确)
        response = client.models.generate_content(
            model=iptmodel,
            contents=iptprompt
        )
        
        # 3. 解析结果
        if hasattr(response, 'text'):
            str_response = response.text
        else:
            # 备用方案：如果返回的是字典或其它格式
            str_response = str(response)
        return str_response    
    except Exception as e:
        error_msg = f"调用AI模型失败。错误详情: {e}"
        print(error_msg)
        if"429" in str(e):
            str_response=f"{str429}"
        else:
            str_response=f"{e}"
        return str_response
        
    