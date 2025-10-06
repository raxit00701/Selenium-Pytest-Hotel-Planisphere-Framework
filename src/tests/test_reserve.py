import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from pages.Homepage import HomePage

@pytest.mark.csv(path="data/reserve.csv")
def test_reserve(driver, base_url, data):
    driver.get(base_url)
    time.sleep(1)  # Wait after navigating to base URL

    # Step 1: Click Reserve link
    HomePage(driver).click_reserve_link()
    time.sleep(1)

    # Step 2-3: Scroll to and click the 6th "Reserve room" button
    reserve_buttons = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//a[@class='btn btn-primary'][normalize-space()='Reserve room']"))
    )
    reserve_button = reserve_buttons[5]
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", reserve_button)
    time.sleep(1)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(reserve_button))
    reserve_button.click()
    time.sleep(1)

    # Step 4: Switch to new tab
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[-1])
    print("Switched to new tab")
    time.sleep(1)

    # Step 5-6: Select date
    date_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='date']"))
    )
    date_field.click()
    time.sleep(1)
    date_16 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='16']"))
    )
    date_16.click()

    # >>> OPTION A INSERTED HERE: wait for datepicker to disappear <<<
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, ".ui-datepicker, .ui-datepicker-calendar"))
    )

    # Step 7-8: Enter term
    term_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "term"))
    )
    term_field.click()
    term_field.send_keys(data.get('term', ''))

    # Step 9-10: Enter head count
    head_count_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='head-count']"))
    )
    head_count_field.click()
    head_count_field.send_keys(data.get('head_count', ''))

    # Step 11: Click sightseeing checkbox
    sightseeing_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "sightseeing"))
    )
    sightseeing_field.click()

    # Step 12-13: Enter username
    username_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='username']"))
    )
    username_field.click()
    username_field.send_keys(data.get('username', ''))

    # Step 14-15: Select contact option
    contact_select_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//select[@id='contact']"))
    )
    contact_select = Select(contact_select_element)
    contact_select.select_by_value("no")

    # Step 16-17: Enter comment
    comment_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "comment"))
    )
    comment_field.click()
    comment_field.send_keys(data.get('comment', ''))

    # Step 18-19: Scroll to and click submit button
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "submit-button"))
    )
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", submit_button)
    submit_button.click()

    # Step 20: Check for validation error
    try:
        error_message = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//div[normalize-space()='Please fill out this field.']"))
        )
        assert error_message.is_displayed(), "Expected reservation to fail, but no error message was displayed"
        return  # Test passes if error is visible, stop here
    except:
        time.sleep(0)  # Wait before continuing

    # Step 21: Click Submit Reservation button
    final_submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Submit Reservation']"))
    )
    final_submit_button.click()

    # Step 22-23: Wait for and click Close button
    close_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Close']"))
    )
    close_button.click()

    # Step 24: Verify test completion by switching back to original window
    driver.switch_to.window(window_handles[0])
    main_page_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[normalize-space()='Reserve']"))
    )
    assert main_page_element.is_displayed(), "Failed to return to main page after reservation"
