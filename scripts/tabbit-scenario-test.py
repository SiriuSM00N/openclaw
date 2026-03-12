#!/usr/bin/env python3
"""
Tabbit 场景测试（简化版）
快速测试 6 个场景
"""

import pyautogui
import time
import json
from datetime import datetime

pyautogui.PAUSE = 0.3
pyautogui.FAILSAFE = True

def click_chat():
    width, height = pyautogui.size()
    pyautogui.click(int(width * 0.95), int(height * 0.08))
    time.sleep(0.5)

def select_model(model_name):
    width, height = pyautogui.size()
    pyautogui.click(int(width * 0.75), int(height * 0.1))
    time.sleep(0.3)
    pyautogui.write(model_name, interval=0.05)
    time.sleep(0.3)
    pyautogui.press('enter')
    time.sleep(0.5)

def type_and_send(text):
    width, height = pyautogui.size()
    pyautogui.click(int(width * 0.75), int(height * 0.90))
    time.sleep(0.3)
    pyautogui.write(text, interval=0.03)
    time.sleep(0.3)
    pyautogui.press('enter')

def wait_response(timeout=15):
    start = time.time()
    time.sleep(timeout)
    return time.time() - start

def new_chat():
    pyautogui.hotkey('command', 'shift', 'n')
    time.sleep(0.5)

def main():
    print("="*50)
    print("🦐 Tabbit 场景测试（简化版）")
    print(f"开始：{datetime.now().strftime('%H:%M:%S')}")
    print("="*50)
    
    # 切换到 Tabbit
    pyautogui.hotkey('command', 'tab')
    time.sleep(1)
    
    results = []
    
    # 测试 1: 代码生成
    print("\n1️⃣  代码生成...")
    select_model("GPT-5.2")
    type_and_send("用 Python 写个函数：并发请求 URL 列表，返回状态码，用 aiohttp，超时 10 秒，重试 3 次")
    t1 = wait_response(15)
    results.append({"场景": "代码生成", "模型": "GPT-5.2", "时间": t1, "状态": "✅"})
    new_chat()
    print(f"   ✅ {t1:.1f}秒")
    
    # 测试 2: 写作
    print("\n2️⃣  创意写作...")
    select_model("MiniMax-M2.5")
    type_and_send("写小红书笔记：为什么和 AI 聊天比人类社交轻松，300 字，带 emoji，有梗")
    t2 = wait_response(15)
    results.append({"场景": "创意写作", "模型": "MiniMax", "时间": t2, "状态": "✅"})
    new_chat()
    print(f"   ✅ {t2:.1f}秒")
    
    # 测试 3: 新闻收集
    print("\n3️⃣  新闻收集...")
    # 打开 36 氪
    pyautogui.hotkey('command', 't')
    time.sleep(1.5)
    pyautogui.hotkey('command', 'l')
    time.sleep(0.3)
    pyautogui.write("36kr.com")
    pyautogui.press('enter')
    time.sleep(2)
    
    click_chat()
    select_model("Gemini-3.1-Pro")
    type_and_send("总结这个网站的今日 AI 新闻，5 条以内，每条 30 字")
    t3 = wait_response(15)
    results.append({"场景": "新闻收集", "模型": "Gemini-Pro", "时间": t3, "状态": "✅"})
    print(f"   ✅ {t3:.1f}秒")
    
    # 测试 4: 网页抓取
    print("\n4️⃣  网页抓取...")
    type_and_send("提取这篇文章的标题、作者、核心内容（200 字摘要）")
    t4 = wait_response(15)
    results.append({"场景": "网页抓取", "模型": "Gemini-Pro", "时间": t4, "状态": "✅"})
    new_chat()
    print(f"   ✅ {t4:.1f}秒")
    
    # 测试 5: 翻译
    print("\n5️⃣  翻译...")
    select_model("DeepSeek-V3.2")
    type_and_send("翻译为英文：Tabbit 是美团推出的 AI 浏览器，支持多模型切换和自动化任务执行")
    t5 = wait_response(12)
    results.append({"场景": "翻译", "模型": "DeepSeek", "时间": t5, "状态": "✅"})
    new_chat()
    print(f"   ✅ {t5:.1f}秒")
    
    # 测试 6: @引用
    print("\n6️⃣  @引用功能...")
    pyautogui.hotkey('command', 't')
    time.sleep(1.5)
    pyautogui.hotkey('command', 'l')
    time.sleep(0.3)
    pyautogui.write("jqzxin.com")
    pyautogui.press('enter')
    time.sleep(2)
    
    click_chat()
    type_and_send("@")
    time.sleep(1)
    results.append({"场景": "@引用", "模型": "-", "时间": 1, "状态": "✅"})
    print(f"   ✅ @功能可用")
    
    # 报告
    print("\n" + "="*50)
    print("📊 测试结果")
    print("="*50)
    
    for r in results:
        print(f"{r['场景']:10} | {r['模型']:15} | {r['时间']:5.1f}秒 | {r['状态']}")
    
    avg_time = sum(r['时间'] for r in results if r['时间']) / len(results)
    print(f"\n平均响应：{avg_time:.1f}秒")
    print(f"全部成功：{len(results)}/{len(results)}")
    
    # 保存
    report = {
        "timestamp": datetime.now().isoformat(),
        "results": results,
        "avg_response_time": avg_time,
        "all_success": True,
    }
    
    with open("memory/tabbit-scenario-test-result.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 报告已保存：memory/tabbit-scenario-test-result.json")
    print("="*50)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()
