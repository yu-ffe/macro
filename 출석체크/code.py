from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import sys
import time
import threading


driver = webdriver.Chrome()
driver.implicitly_wait(10)
url = 'https://www.itgosu.co.kr/'
driver.get(url)
print('접속')

if driver.find_element(By.XPATH, '//*[@id="undefined-sticky-wrapper"]/nav/div[3]/div[1]/div/div/div[1]/a').is_displayed():
    element_menu_button = driver.find_element(By.XPATH, '//*[@id="undefined-sticky-wrapper"]/nav/div[3]/div[1]/div/div/div[1]/a')
    element_menu_button.click()

    element_login_button = driver.find_element(By.XPATH, '//*[@id="sidebar-content"]/div[2]/div[1]/a[1]')
    element_login_button.click()
    print('로그인 경로 1')

else:
    element_login_button = driver.find_element(By.XPATH, '//*[@id="thema_wrapper"]/aside/div/div[2]/ul/li[1]/a')
    element_login_button.click()
    print('로그인 경로 2')

def login():
    print('로그인 시도')
    tt = threading.Timer(1,login)
    tt.start()
    try:
        if driver.find_element(By.XPATH, '//*[@id="sidebar_login_form"]/div[1]/div/input').is_displayed():
            element_login_id = driver.find_element(By.XPATH, '//*[@id="sidebar_login_form"]/div[1]/div/input')
            element_login_id.click()
            element_login_id.send_keys('your_id')

            element_login_password = driver.find_element(By.XPATH, '//*[@id="sidebar_login_form"]/div[2]/div/input')
            element_login_password.send_keys('your_password')
            element_login_password.send_keys(Keys.RETURN)
            print('로그인 성공 (아이디, 비밀번호 틀려도 그대로 실행)')
            tt.cancel()
            time.sleep(1)
            sys.exit(0)
    except Exception as e:
        print(f'예외 발생: {e}')
        tt.cancel()

login()