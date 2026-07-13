from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from helpers import register_and_login

TASK_SUBMIT = ".tasks-form-card button[type=submit]"


def _create_task(driver, title):
    driver.find_element(By.ID, "task-title").send_keys(title)
    driver.find_element(By.CSS_SELECTOR, TASK_SUBMIT).click()


def _find_task_item(driver, title):
    return WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, f"//li[contains(@class,'task-item')][.//span[text()='{title}']]")
        )
    )


def test_create_task_appears_in_list(driver, base_url, unique_username):
    register_and_login(driver, base_url, unique_username)

    title = f"Tarefa E2E {unique_username}"
    _create_task(driver, title)

    task_item = _find_task_item(driver, title)
    assert task_item.is_displayed()


def test_toggle_task_completion(driver, base_url, unique_username):
    register_and_login(driver, base_url, unique_username)

    title = f"Tarefa Concluir {unique_username}"
    _create_task(driver, title)
    task_item = _find_task_item(driver, title)

    task_item.find_element(By.CSS_SELECTOR, "input[type=checkbox]").click()

    WebDriverWait(driver, 10).until(lambda d: "is-completed" in task_item.get_attribute("class"))
    assert "is-completed" in task_item.get_attribute("class")


def test_delete_task_removes_it_from_list(driver, base_url, unique_username):
    register_and_login(driver, base_url, unique_username)

    title = f"Tarefa Excluir {unique_username}"
    _create_task(driver, title)
    task_item = _find_task_item(driver, title)

    task_item.find_element(By.XPATH, ".//button[text()='Excluir']").click()
    driver.switch_to.alert.accept()

    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located(
            (By.XPATH, f"//li[contains(@class,'task-item')][.//span[text()='{title}']]")
        )
    )
