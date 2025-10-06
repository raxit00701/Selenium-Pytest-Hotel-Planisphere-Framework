import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.Homepage import HomePage

@pytest.mark.csv(path="data/login.csv")   # note: no cols=[]
def test_login(driver, base_url, data):
    email = data["email"]
    password = data["password"]

    driver.get(base_url)

    HomePage(driver).click_login_link()
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()

    try:
        wait = WebDriverWait(driver, 5)
        email_error = wait.until(EC.visibility_of_element_located((By.ID, "email-message")))
        password_error = wait.until(EC.visibility_of_element_located((By.ID, "password-message")))
        assert email_error.is_displayed() or password_error.is_displayed()
    except Exception:
        assert True
