"""Уроки, глава 2.4"""
import os
import time
import math
from selenium import webdriver as driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ChromeDriver:
    """Объект Chrome driver."""
    def __init__(self):
        # Если были открыты - принудительно закрываю все Chrome и драйвер
        os.system("TASKKILL /F /IM chromedriver.exe")
        # Объект браузера
        self.browser = driver.Chrome(chrome_options=self.chrome_options())
        # Устанавливаю допустимое время для поиска элементов
        self.browser.implicitly_wait(15)
        # Статус выполнения задачи
        self.status = False

    def chrome_options(self):
        """Настройка Chrome browser"""
        print("Устанавливаю настройки для Chrome browser...")
        options = driver.ChromeOptions()
        # При запуске разворачивать на весь экран
        options.add_argument("--start-maximized")
        # Отключить уведомления об автоматическом режиме
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        # Отключить w3c
        options.add_experimental_option('w3c', False)
        print("Настройки для Chrome browser установлены.")
        return options

    def wait_element_by_xpath(self, element, time_wait: int=30, reraise=False) -> bool:
        """Проверяет доступен ли элемент по xpath.\n
        * time_wait - сколько ждем (30сек.)\n
        * reraise - бросать ли исключение (False)"""
        while not self.browser.find_elements_by_xpath(element) and time_wait > 0:
            time.sleep(1)
            time_wait -= 1
        # Если время ожидания не истекло до обнаружения элемента - это успех. Иначе - либо False, либо Exception.
        if time_wait:
            return True
        else:
            if not reraise:
                return False
            else:
                # Генерирую ошибку
                self.browser.find_element_by_xpath(element)

    def wait_alert(self, time_wait: int=30, reraise=False):
        """Проверяет доступно ли окно alert.\n
        * time_wait - сколько ждем (30сек.)\n
        * reraise - бросать ли исключение (False)"""
        check_flag = False
        while not check_flag and time_wait > 0:
            try:
                temp = self.browser.switch_to.alert.text
                check_flag = True
            except Exception:
                time.sleep(1)
                time_wait -= 1
        # Если время ожидания не истекло до обнаружения элемента - это успех. Иначе - либо False, либо Exception.
        if time_wait:
            return True
        else:
            if not reraise:
                return False
            else:
                # Генерирую ошибку
                raise Exception("Не удалось обнаружить окно Alert!")

    def wait_window(self, id: int, time_wait: int=30, reraise=False):
        """Проверяет доступно ли окно браузера.\n
            * id - номер искомой вкладки браузера\n
            * time_wait - сколько ждем (30сек.)\n
            * reraise - бросать ли исключение (False)"""
        check_flag = False
        while not check_flag and time_wait > 0:
            try:
                window = self.browser.window_handles[id]
                temp = self.browser.switch_to.window(window)
                check_flag = True
            except Exception:
                print("WARN - НЕУДАЧА ОБНАРУЖЕНИЯ ОКНА БРАУЗЕРА!")
                time.sleep(1)
                time_wait -= 1
        # Если время ожидания не истекло до обнаружения элемента - это успех. Иначе - либо False, либо Exception.
        if time_wait:
            return True
        else:
            if not reraise:
                return False
            else:
                # Генерирую ошибку
                raise Exception("Не удалось обнаружить окно Alert!")

    def calc(self, x):
        """Рассчитывает математическую функцию от x."""
        return str(math.log(abs(12 * math.sin(int(x)))))

    def __del__(self):
        # Закрываю браузер и драйвер
        print("Закрываю браузер и chrome драйвер...")
        try:
            self.browser.close()
            self.browser.quit()
        except Exception:
            pass
        finally:
            # Если остались открыты - принудительно закрываю все Chrome и драйвер
            os.system("TASKKILL /F /IM chromedriver.exe")
        print("Браузер и chrome драйвер закрыты.")

    def worker_1(self):
        """Первая задача"""
        # 1) Открыть страницу http://suninjuly.github.io/explicit_wait2.html
        print("Открываю страницу в браузере...")
        self.browser.get("http://suninjuly.github.io/explicit_wait2.html")
        print("Страница в браузере открыта.")
        # 2) Дождаться, когда цена дома уменьшится до $100 (ожидание нужно установить не меньше 12 секунд)
        print("Ожидаю снижения цены дома...")
        WebDriverWait(self.browser, 15).until(EC.text_to_be_present_in_element((By.ID, 'price'), '$100'))
        print("Снижения цены дома дождался.")
        # 3) Нажать на кнопку "Book"
        print("Нажимаю на кнопку 'Book'...")
        self.browser.find_element_by_xpath('//button[@id="book"]').click()
        print("На кнопку 'Book' нажал.")
        # 4) На новой странице решить капчу для роботов, чтобы получить число с ответом
        print("Решаю капчу для роботов...")
        print("Считываю значение для переменной х...")
        x = self.browser.find_element_by_xpath('//span[@id="input_value"]').text
        print(f"Значение для переменной х считано как [{x}].")
        print("Считаю математичесекую функцию от х...")
        calc = self.calc(x)
        print(f"Результат математической функции от х: [{calc}]")
        print("Ввожу ответ в текстовое поле...")
        self.browser.find_element_by_xpath('//input[@id="answer"]').send_keys(calc)
        print("Ответ в текстовое поле введен.")
        print("Нажимаю на кнопку 'Submit'...")
        self.browser.find_element_by_xpath('//button[@type="submit"]').click()
        print("На кнопку 'Submit' нажал.")
        print(f"Капча решена.")
        # Считываю текст окна с результатом
        print("Считываю текст с окна содержащего результат...")
        self.wait_alert()
        result = self.browser.switch_to.alert.text.split()[-1]
        print(f"Текст с окна содержащего результат считан как: [\033[1m\033[91m{result}\033[0m].")
        # Закрываю окно содержащее результат
        self.browser.switch_to.alert.accept()
        self.browser.close()
        self.browser.quit()


if __name__ == "__main__":
    print("===== СТАРТ =====")

    try:
        # Исполняю задачу из главы 2.4
        ChromeDriver().worker_1()
    except Exception as ex:
        print(f"Системная ошибка: [{ex}].")

    print("===== КОНЕЦ =====")