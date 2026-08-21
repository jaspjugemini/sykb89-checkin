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
        page.wait_for_timeout(3000)
        page.screenshot(path="debug_login.png")
        print("登录页截图已保存")

        # 填写账号密码（根据实际选择器调整）
        page.fill('input[name="username"], input[type="text"], input[type="email"], input[type="tel"]', username)
        page.fill('input[name="password"], input[type="password"]', password)
        page.screenshot(path="debug_filled.png")
        print("填写后截图已保存")

        # 点击登录按钮
        login_btn = page.locator('button[type="submit"], button:has-text("登录"), button:has-text("Login")')
        print(f"登录按钮数量: {login_btn.count()}")
        if login_btn.count() > 0:
            login_btn.first.click()
            page.wait_for_timeout(3000)
            # 检查是否有错误消息
            error_msg = page.locator('.v-alert, .error, .message, [class*="error"]').first
            if error_msg.count() > 0:
                print(f"错误信息: {error_msg.inner_text()}")
        else:
            print("未找到登录按钮")

        # 等待登录完成
        page.wait_for_timeout(5000)  # 等待5秒
        print(f"登录后URL: {page.url}")
        page.screenshot(path="debug_after_login.png")
        print("登录后截图已保存")

        # 2. 签到
        print("正在签到...")
        page.goto("https://www.sykb89.org/home/gift/checkIn")
        page.wait_for_timeout(5000)  # 等待5秒加载
        print(f"当前URL: {page.url}")
        print(f"按钮数量: {page.locator('button.v-btn').count()}")
        page.screenshot(path="debug.png")  # 截图保存
        print("截图已保存为 debug.png")

        # 点击签到按钮
        try:
            # 先检查是否已签到
            if page.locator('text=已签到').count() > 0:
                print("今日已签到，无需重复签到")
            else:
                # 用 JavaScript 点击签到按钮（匹配"立即签到"或"签到"，包括 disabled 按钮）
                clicked = page.evaluate('''() => {
                    const btns = document.querySelectorAll('button.v-btn');
                    for (const btn of btns) {
                        const text = btn.textContent || '';
                        if (text.includes('签到') && !text.includes('已签到')) {
                            btn.click();
                            setTimeout(() => btn.click(), 1000);
                            setTimeout(() => btn.click(), 2000);
                            return text.trim();
                        }
                    }
                    return null;
                }''')

                if clicked:
                    print(f"找到按钮: {clicked}")
                    page.wait_for_timeout(3000)
                    # 检查签到结果
                    if page.locator('text=已签到').count() > 0:
                        print("签到成功！")
                    else:
                        print("签到操作已执行，请检查结果")
                else:
                    print("未找到签到按钮")
        except Exception as e:
            print(f"签到过程出错: {e}")

        browser.close()

if __name__ == "__main__":
    checkin()
