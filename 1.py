from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import random
import string
from smsactivateru import Sms, SmsTypes, SmsService, GetBalance, GetFreeSlots, GetNumber, SetStatus, GetStatus


# ----------------------------------------------------------------------------------------------------------------------

# Генерация рег данных
# Почта
email_size = 15
reg_email = ''.join(random.choice(string.ascii_letters) for _ in range(email_size))

# Пароль
pass_size = 15
reg_pass = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(pass_size))

# ----------------------------------------------------------------------------------------------------------------------

# Рег данные
reg_email += '@dombasskiller156.com'
reg_pass += 'aA1'

# ----------------------------------------------------------------------------------------------------------------------

# Настройка браузера и смс активатора
chromedriver = 'C:\chromedriver'
chrome_options = Options()
# chrome_options.add_argument('headless')  # Раскоментировать если надо скрыть браузер
browser = webdriver.Chrome(executable_path=chromedriver, options=chrome_options)
wrapper = Sms('9841206c1633891171fb6dcA9819f5b3')  # API ключ с sms-activate.ru

# ----------------------------------------------------------------------------------------------------------------------

# Работа с DOM
# Ссылка стартовой страницы
browser.get('https://www.nike.com/ru/launch')

# Поиск рег формы
log_button = browser.find_element_by_class_name('join-log-in')
log_button.click()
time.sleep(2)
log_form = browser.find_element_by_id('nike-unite-loginForm')
log_form_footer = log_form.find_element_by_class_name('loginJoinLink')
log_form_to_reg = log_form_footer.find_element_by_tag_name('a')
log_form_to_reg.click()
time.sleep(1)

# Поиск рег полей
email_input = browser.find_element_by_name('emailAddress')
pass_input = browser.find_element_by_name('password')
first_name_input = browser.find_element_by_name('firstName')
last_name_input = browser.find_element_by_name('lastName')
date_of_birth = browser.find_element_by_name('dateOfBirth')
gender_block = browser.find_element_by_class_name('nike-unite-gender-buttons')
gender_button = gender_block.find_element_by_tag_name('li')
reg_button_block = browser.find_element_by_class_name('nike-unite-submit-button')
reg_button = reg_button_block.find_element_by_tag_name('input')

# Ввод рег данных
email_input.send_keys(reg_email)
pass_input.send_keys(reg_pass)
first_name_input.send_keys('Иван')
last_name_input.send_keys('Балеков')
date_of_birth.send_keys('14.04.2003')
gender_button.click()
time.sleep(2)
reg_button.click()
time.sleep(5)

# Входим в настройки для добовления телефона
browser.get('https://www.nike.com/ru/member/settings')
time.sleep(5)
settings_phone_block = browser.find_element_by_class_name('mex-mobile-phone')
settings_phone_add_button = settings_phone_block.find_element_by_tag_name('button')
settings_phone_add_button.click()

# Добавление телефона
phone_add_form = browser.find_element_by_id('nike-unite-progressive-profile-view')

activation = GetNumber(
    service=SmsService().Nike,
    country=SmsTypes.Country.RU
).request(wrapper)

phone_add_input = phone_add_form.find_element_by_class_name('phoneNumber')
phone_add_input.send_keys(str(activation.phone_number)[1:])
phone_add_send_code_button = phone_add_form.find_element_by_class_name('sendCodeButton')
phone_add_send_code_button.click()

# .. wait code
while True:
    time.sleep(1)
    response = GetStatus(id=activation.id).request(wrapper)
    if response['code']:
        print('Your code:{}'.format(response['code']))
        break

phone_add_code_block = phone_add_form.find_element_by_class_name('verifyCode')
phone_add_code_input = phone_add_code_block.find_element_by_tag_name('input')
phone_add_code_input.send_keys(str(response['code']))
phone_politic_checkbox = phone_add_form.find_element_by_class_name('checkbox')
phone_politic_checkbox.click()
phone_add_submit_button_block = phone_add_form.find_element_by_class_name('nike-unite-submit-button')
phone_add_submit_button = phone_add_submit_button_block.find_element_by_tag_name('input')
phone_add_submit_button.click()
time.sleep(5)

# ----------------------------------------------------------------------------------------------------------------------

# Запись данных
reg_str = reg_email + ':' + reg_pass + '\n'
reg_file = open('reg_file.txt', 'a')
reg_file.write(reg_str)
reg_file.close()

# ----------------------------------------------------------------------------------------------------------------------

# Подтверждение номра
set_as_end = SetStatus(
    id=activation.id,
    status=SmsTypes.Status.End
).request(wrapper)

# ----------------------------------------------------------------------------------------------------------------------
