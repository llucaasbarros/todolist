from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DEFAULT_PASSWORD = "SenhaForte123"


def register_user(driver, base_url, username, email=None, password=DEFAULT_PASSWORD):
    email = email or f"{username}@example.com"

    driver.get(base_url + "register")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))

    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "confirmPassword").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()

    WebDriverWait(driver, 10).until(EC.url_contains("/login"))


def login_user(driver, base_url, username, password=DEFAULT_PASSWORD):
    driver.get(base_url + "login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))

    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[type=submit]").click()


def register_and_login(driver, base_url, username, password=DEFAULT_PASSWORD):
    register_user(driver, base_url, username, password=password)
    login_user(driver, base_url, username, password=password)
    WebDriverWait(driver, 10).until(EC.url_contains("/tasks"))
