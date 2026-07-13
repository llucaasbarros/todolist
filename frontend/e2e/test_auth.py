from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from helpers import login_user, register_and_login, register_user


def test_register_and_login_flow(driver, base_url, unique_username):
    register_user(driver, base_url, unique_username)
    assert "/login" in driver.current_url

    login_user(driver, base_url, unique_username)

    WebDriverWait(driver, 10).until(EC.url_contains("/tasks"))
    assert "/tasks" in driver.current_url


def test_login_with_wrong_password_shows_error(driver, base_url, unique_username):
    register_user(driver, base_url, unique_username)
    login_user(driver, base_url, unique_username, password="wrong-password")

    error = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "auth-alert"))
    )
    assert "incorreta" in error.text.lower()
    assert "/login" in driver.current_url


def test_protected_route_redirects_to_login(driver, base_url):
    driver.get(base_url + "tasks")
    WebDriverWait(driver, 10).until(EC.url_contains("/login"))
    assert "/login" in driver.current_url


def test_logout_redirects_to_login(driver, base_url, unique_username):
    register_and_login(driver, base_url, unique_username)

    driver.find_element(By.XPATH, "//button[text()='Sair']").click()

    WebDriverWait(driver, 10).until(EC.url_contains("/login"))
    assert "/login" in driver.current_url
