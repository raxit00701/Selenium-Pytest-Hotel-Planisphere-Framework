from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# --- Simple PageFactory descriptor ---
class Element:
    def __init__(self, locator, timeout: int = 10, when: str = "visible"):
        self.locator = locator
        self.timeout = timeout
        self.when = when  # "visible" | "clickable" | "present"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        wait = WebDriverWait(instance.driver, self.timeout)
        if self.when == "clickable":
            return wait.until(EC.element_to_be_clickable(self.locator))
        elif self.when == "visible":
            return wait.until(EC.visibility_of_element_located(self.locator))
        else:
            return wait.until(EC.presence_of_element_located(self.locator))


class HomePage:
    # Locators
    RESERVE_LINK = (By.XPATH, "//a[@href='./plans.html' and normalize-space()='Reserve']")
    SIGNUP_LINK  = (By.XPATH, "//a[normalize-space()='Sign up']")
    LOGIN_LINK   = (By.XPATH, "//a[normalize-space()='Login']")

    # PageFactory elements
    reserve_link_el = Element(RESERVE_LINK, when="clickable")
    signup_link_el  = Element(SIGNUP_LINK,  when="clickable")
    login_link_el   = Element(LOGIN_LINK,   when="clickable")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def open_home(self, base_url):
        self.driver.get(base_url)
        return self

    def click_reserve_link(self):
        self.reserve_link_el.click()
        print("Clicked on 'Reserve' link")
        sleep(10)  # Retaining sleep as per original script
        return self

    def click_signup_link(self):
        self.signup_link_el.click()
        print("📝 Clicked 'Sign up'")
        return self

    def click_login_link(self):
        self.login_link_el.click()
        print("Step 1: Clicked on Login link")
        return self

    def is_reserve_link_displayed(self):
        return self.reserve_link_el.is_displayed()
