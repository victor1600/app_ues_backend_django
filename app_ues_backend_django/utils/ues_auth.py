import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def authenticate_ues_student(username: str, password: str) -> dict:
    """
    Function that authenticates against https://aulacn.ues.edu.sv/login/index.php
    and to fetch data from.
    :param username: username to authenticate against.
    :param password: Password of the student
    :return: Data fetched using web scrapping
    """
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome(options=op)
    driver.get("https://aulacn.ues.edu.sv/login/index.php")

    username_input = driver.find_element(By.ID, 'username')
    username_input.send_keys(username)

    password_input = driver.find_element(By.ID, 'password')
    password_input.send_keys(password)

    login_button = driver.find_element(By.ID, 'loginbtn')
    login_button.send_keys(Keys.ENTER)

    try:
        name_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[1]/nav/ul[2]/li[2]/div/div/div/div/div/a'))
        )

        student_full_name = name_element.text.split(": ")[1]
        names = student_full_name.split(" ")
        names_len = len(names)
        first_name = ' '.join(names[:int(names_len / 2)])
        last_name = ' '.join(names[int(len(names) / 2):])

        # Getting the email
        name_element.click()
        profile_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.PARTIAL_LINK_TEXT, 'Perfil'))
        )
        profile_element.click()

        email_element = driver.find_element(By.XPATH,
                                            '/html/body/div[1]/div[2]/div/div[1]/section/div/div/div/section[1]/div/ul/li[2]/dl/dd/a')

        user_data = {
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'password': password,
            'email': email_element.text
        }

        # Store all the credentials if first time.
        return user_data

    except selenium.common.exceptions.TimeoutException:
        print('Wrong username or password')


