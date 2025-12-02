def test_login_success(login_page):
    login_page.visit("/login")
    login_page.login("user", "pass")
    assert "dashboard" in login_page.driver.current_url
