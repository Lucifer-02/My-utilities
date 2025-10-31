import time

from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(
        headless=False,
        args=["--start-maximized"],  # Maximized window
    )
    context = browser.new_context(no_viewport=True)  # Important for max window
    page = context.new_page()
    page.goto(
        "https://xuatbanyhoc.vn/customer/login?redirect=https%3a%2f%2fxuatbanyhoc.vn%2febook%2f10784%2f0%2f48%2f"
    )
    page.get_by_role("textbox", name="Nhập email hoặc tên đăng nhập").click()
    page.get_by_role("textbox", name="Nhập email hoặc tên đăng nhập").fill(
        "nguyenleviethoang2000@gmail.com"
    )
    page.get_by_role("textbox", name="Nhập email hoặc tên đăng nhập").press("Tab")
    page.get_by_role("textbox", name="Nhập mật khẩu").click()
    page.get_by_role("textbox", name="Nhập mật khẩu").fill("EwRb-Cmi7T:SzVw")
    page.get_by_role("button", name="Đăng nhập").click()

    page.goto("https://xuatbanyhoc.vn/ebook/10784/0/2/")
    page.wait_for_load_state(state="networkidle")
    page.wait_for_load_state(state="load")
    page.wait_for_load_state(state="domcontentloaded")
    time.sleep(2)

    for page_num in range(2, 251, 2):
        left_page = page.locator(
            ".page-flip-container.z1.gradient-light.reflex-left > .page > .touch-layer > .content.vis"
        ).first
        right_page = page.locator(
            ".page-flip-container.z1.gradient-light.reflex-right > .page > .touch-layer > .content.vis"
        ).first

        left_page.wait_for(state="attached")
        right_page.wait_for(state="attached")

        left_page.screenshot(path=f"page{page_num}.jpeg")
        right_page.screenshot(path=f"page{page_num + 1}.jpeg")

        page.get_by_role("button", name="Next Page").click()
        time.sleep(0.5)

    # ---------------------
    input("Press any key to close...")
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
