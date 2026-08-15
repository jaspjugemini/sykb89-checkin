import os
from playwright.sync_api import sync_playwright

def checkin():
    username = os.environ.get("USER")
    password = os.environ.get("PWD")

    if not username or not password:
        print("错误：未设置 USER 或 PWD 环境变量")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # 1. 登录
        print("正在登录...")
        page.goto("https://www.sykb89.org/account/login")
        page.wait_for_load_state("networkidle")
        page.screenshot(path="debug_login.png")
        print("登录页截图已保存")

        # 填写账号密码（根据实际选择器调整）
        page.fill('input[name="username"], input[type="text"], input[type="email"], input[type="tel"]', username)
        page.fill('input[name="password"], input[type="password"]', password)
        page.screenshot(path="debug_filled.png")
        print("填写后截图已保存")

        # 点击登录按钮
        page.click('button[type="submit"], button:has-text("登录"), button:has-text("Login")')

        # 等待登录完成
        page.wait_for_timeout(5000)  # 等待5秒
        page.wait_for_load_state("networkidle")
        page.screenshot(path="debug_after_login.png")
        print("登录后截图已保存")

        # 2. 签到
        print("正在签到...")
        page.goto("https://www.sykb89.org/home/gift/checkIn")
        page.wait_for_load_state("networkidle")
        page.screenshot(path="debug.png")  # 截图保存
        print("截图已保存为 debug.png")

        # 点击签到按钮（根据实际选择器调整）
        try:
            # 先检查是否已签到
            if page.locator('text=已签到').count() > 0:
                print("今日已签到，无需重复签到")
            else:
                # 尝试点击签到按钮
                sign_btn = page.locator('button:has-text("签到"):not(:has-text("已签到"))')
                if sign_btn.count() > 0:
                    sign_btn.first.click()
                    page.wait_for_timeout(1000)
                    sign_btn.first.click()  # 第二次点击
                    page.wait_for_timeout(1000)
                    sign_btn.first.click()  # 第三次点击
                    page.wait_for_timeout(2000)
                    print("签到成功！")
                else:
                    print("未找到签到按钮")
        except Exception as e:
            print(f"签到过程出错: {e}")

        browser.close()

if __name__ == "__main__":
    checkin()
