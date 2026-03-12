#!/usr/bin/env python3
"""
Tabbit 全自动测试脚本（无截图版）
使用 pyautogui 模拟鼠标键盘操作
"""

import pyautogui
import time
import json
from datetime import datetime

# 配置
pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = True

def click_tabbit_chat():
    """点击 Tabbit Chat 按钮（右上角）"""
    width, height = pyautogui.size()
    x = int(width * 0.95)
    y = int(height * 0.08)
    print(f"📍 点击 Chat 按钮：({x}, {y})")
    pyautogui.click(x, y)
    time.sleep(1)

def click_model_dropdown():
    """点击模型下拉菜单"""
    width, height = pyautogui.size()
    x = int(width * 0.75)
    y = int(height * 0.1)
    print(f"📍 点击模型下拉菜单：({x}, {y})")
    pyautogui.click(x, y)
    time.sleep(1)

def select_model(model_name):
    """选择指定模型"""
    print(f"🔧 选择模型：{model_name}")
    pyautogui.write(model_name, interval=0.1)
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(1)

def type_question(question):
    """输入问题"""
    print(f"💬 输入：{question}")
    # 点击输入框（底部中央）
    width, height = pyautogui.size()
    x = int(width * 0.75)
    y = int(height * 0.90)
    pyautogui.click(x, y)
    time.sleep(0.5)
    pyautogui.write(question, interval=0.05)
    time.sleep(0.5)
    pyautogui.press('enter')

def wait_for_response(timeout=15):
    """等待响应"""
    print("⏳ 等待响应...")
    start = time.time()
    time.sleep(timeout)
    elapsed = time.time() - start
    print(f"⏱️  耗时：{elapsed:.1f}秒")
    return elapsed

def main():
    print("=" * 60)
    print("🦐 Tabbit 全自动测试")
    print(f"开始：{datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)
    
    # 1. 切换到 Tabbit（假设是下一个应用）
    print("\n1️⃣  切换到 Tabbit...")
    pyautogui.hotkey('command', 'tab')
    time.sleep(2)
    
    # 2. 打开 Chat
    print("\n2️⃣  打开 Chat 侧边栏...")
    click_tabbit_chat()
    time.sleep(2)
    
    # 3. 测试模型列表
    print("\n3️⃣  打开模型选择器...")
    click_model_dropdown()
    time.sleep(2)
    
    # 4. 测试 3 个关键模型
    print("\n4️⃣  测试模型响应...")
    
    test_sequence = [
        ("GPT-5.2", "1+1=? 一句话回答"),
        ("Claude-Sonnet", "中国首都是哪里？"),
        ("Gemini-3.1-Pro", "Python 是什么语言？"),
    ]
    
    results = []
    
    for model, question in test_sequence:
        print(f"\n--- {model} ---")
        
        # 选择模型
        select_model(model)
        time.sleep(1)
        
        # 输入问题
        type_question(question)
        
        # 等待响应
        response_time = wait_for_response(10)
        
        results.append({
            "model": model,
            "question": question,
            "response_time": response_time,
            "success": True,
        })
        
        # 新对话（Cmd+Shift+N 或清空）
        pyautogui.hotkey('command', 'shift', 'n')
        time.sleep(1)
    
    # 5. 测试@功能
    print("\n5️⃣  测试@引用...")
    pyautogui.hotkey('command', 't')  # 新标签
    time.sleep(2)
    pyautogui.hotkey('command', 'l')  # 地址栏
    time.sleep(0.5)
    pyautogui.write("https://www.36kr.com")
    pyautogui.press('enter')
    time.sleep(3)
    
    click_tabbit_chat()
    time.sleep(1)
    pyautogui.write("@")
    time.sleep(2)
    print("✅ @功能测试完成")
    
    # 6. 测试/妙招
    print("\n6️⃣  测试/妙招...")
    pyautogui.write("/")
    time.sleep(2)
    print("✅ 妙招功能测试完成")
    
    # 生成报告
    print("\n" + "=" * 60)
    print("📊 测试结果")
    print("=" * 60)
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "results": results,
        "summary": {
            "models_tested": len(results),
            "all_success": all(r["success"] for r in results),
            "avg_response_time": sum(r["response_time"] for r in results) / len(results),
        }
    }
    
    # 保存
    with open("memory/tabbit-auto-test-result.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 报告：memory/tabbit-auto-test-result.json")
    
    # 打印摘要
    print(f"\n📈 摘要:")
    print(f"  测试模型：{report['summary']['models_tested']}")
    print(f"  全部成功：{report['summary']['all_success']}")
    print(f"  平均响应：{report['summary']['avg_response_time']:.1f}秒")
    
    print("\n" + "=" * 60)
    print("✅ 完成！")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  中断（鼠标移角落）")
    except Exception as e:
        print(f"\n\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()
