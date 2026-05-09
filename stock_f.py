import yfinance as yf #雅虎财经API
import datetime
from newspaper import Article
import pandas as pd
import time
import pprint
import os

# 1. 设定你想监控的“目标”
#tickers = ["^GSPC", "^NDX", "^DJI","GLD","SLV","BZ=F","BTC-USD","ETH-USD","TLT"]
#tickers = ["^GSPC"]
#tickers = ["^GSPC", "^NDX", "^DJI"]

def analyze_market(tickers:list[str]):   #主程序

    market_data = ""    #喂给AI的市场数据字段
    market_news = ""    #喂给AI的市场新闻字段


    #--获取个股数据--
    print("正在从雅虎财经调取数据...")
    for ticker in tickers:
        stock = yf.Ticker(ticker)           #赋值个股数据

        hist = stock.history(period="1y")   #取一年的数据看趋势
        news_list = stock.news              #取最近新闻集合
        #pprint.pprint(news_list)
        #exit()
        paywall_keywords = [
            "Upgrade to read", 
            "subscription plan is required", 
            "Silver or Gold subscription",
            "access premium news"
        ]
        if hist.empty:
            print(f"{ticker}的数据无法获取！")
            continue
        else:            
            #--获取雅虎财经新闻--
          
            news_data = [] #新闻表格
            #if ticker in ["^GSPC", "BZ=F", "GLD", "BTC-USD"]:
            for item in news_list[:5]:
                news_content = item.get('content', {})
                #news_url = (news_content.get('clickThroughUrl') or {}).get('url') or news_content.get('previewUrl')
                news_title = news_content.get('title', '无标题')
                news_publisher = news_content.get('provider', {}).get('displayName', '未知来源')
                news_summary = news_content.get('summary', '')
                # 提取时间数字
                news_time = news_content.get('pubDate')
                news_time=news_time.replace('T', ' ').replace('Z', '')
                #print(f"正在获取: {news_title[:50]}...")
                #if not news_url:                 #如果没有任何url直接记录摘要
                news_data.append({
                'title': news_title,
                'publisher': news_publisher,
                'PublishTime':news_time,
                'summary': news_summary, # 自动生成的摘要
                #'keywords': article.keywords, # 提取的关键词
                #'full_text': article.text,    # 完整正文
                #'link': news_url,
                }) 

            news_dataform=pd.DataFrame(news_data) #把列表变表格
            for index, row in news_dataform.head(10).iterrows():
                market_news += f"新闻标题: {row['title']}\n \
                来源: {row['publisher']}\n \
                发布时间: {row['PublishTime']}\n \
                摘要: {row['summary']}\n \
                \n"
                #正文: {row['full_text']}\n \
                #关键字: {row['keywords']}\n \
                #链接: {row['link']}\n \
                #--


            last_20_days = hist.tail(20) #最后20日数据
            last20d_high = (last_20_days['High'].max(),last_20_days['High'].idxmax().date())
            last20d_low = (last_20_days['Low'].min(),last_20_days['Low'].idxmin().date())
            if last20d_high[1]<last20d_low[1]:
                volatility = last20d_low[0] -last20d_high[0]             #20日振幅
                pct_change = (volatility / last20d_low[0]) * 100         #20日振幅百分比
            else:
                volatility = last20d_high[0] - last20d_low[0]            #20日振幅
                pct_change = (volatility / last20d_low[0]) * 100         #20日振幅百分比
            avg20d= last_20_days['Close'].mean()                         #20日均价

            last_100_days = hist.tail(100)                      #最后100日数据
            avg100d= last_100_days['Close'].mean()              #100日均价

            high=hist['High'].max() #一年数据
            low=hist['Low'].min()
            yavg=hist['Close'].mean()    

            last_price = hist['Close'].iloc[-1]
        
        # 整理成一段人能看懂（AI能读懂）的逻辑描述
        market_data += f" {ticker}近一年的数据\n\n \
        当前价格: {last_price:.2f}\n \
        最近20日振幅值: {volatility:.2f}\n \
        最近20日振幅: {pct_change:.2f}%\n \
        最近20日收盘均价: {avg20d:.2f}\n \
        最近100日收盘均价: {avg100d:.2f}\n \
        年内最高价: {high:.2f}\n \
        年内最低价: {low:.2f}\n \
        一年每日收盘均价: {yavg:.2f}\n"

    #--

    return market_data,market_news,hist 

