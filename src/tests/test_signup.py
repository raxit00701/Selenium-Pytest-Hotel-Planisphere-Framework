import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from pages.Homepage import HomePage

@pytest.mark.csv(path="data/signup.csv")
def test_signup(driver, base_url, data):
    driver.get(base_url)

    # Click signup link
    HomePage(driver).click_signup_link()


    # Fill email field
    email_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "email"))
    )
    email_field.click()
    email_field.send_keys(data['email'])

    # Fill password field
    password_field = driver.find_element(By.ID, "password")
    password_field.click()
    password_field.send_keys(data['password'])

    # Fill password confirmation field
    password_confirm = driver.find_element(By.ID, "password-confirmation")
    password_confirm.click()
    password_confirm.send_keys(data['password_confirmation'])

    # Fill username field
    username_field = driver.find_element(By.ID, "username")
    username_field.click()
    username_field.send_keys(data['username'])

    # Fill address field
    address_field = driver.find_element(By.ID, "address")
    address_field.click()
    address_field.send_keys(data['address'])

    # Fill telephone field
    tel_field = driver.find_element(By.ID, "tel")
    tel_field.click()
    tel_field.send_keys(data['tel'])

    # Select gender
    gender_select = driver.find_element(By.ID, "gender")
    gender_select.click()
    Select(gender_select).select_by_value("1")

    # Fill birthday field
    birthday_field = driver.find_element(By.ID, "birthday")
    birthday_field.click()
    birthday_field.send_keys(data['birthday'])

    # Click notification checkbox
    notification = driver.find_element(By.ID, "notification")
    notification.click()

    # Submit form
    submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    submit_button.click()

    # Check for validation errors
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//div[@class='invalid-feedback'][normalize-space()='Please fill out this field.'] | "
                "//div[normalize-space()='Please enter a non-empty email address.']"
            ))
        )
        print("signup failed")
    except:
        # Check for successful signup
        try:
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, "//h2[normalize-space()='MyPage']"))
            )
            print("signup successful")
            # Click logout
            logout_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Logout']"))
            )
            logout_button.click()
        except:
            print("signup failed")