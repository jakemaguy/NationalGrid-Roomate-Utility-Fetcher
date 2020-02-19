#!/usr/bin/env python3
import argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

comcast_bill_amount = 30

def get_electric_bill_amount():
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.nationalgridus.com/SignIn')

    email = driver.find_element_by_name('txtUsername')
    email.send_keys(args.electric_username)

    password = driver.find_element_by_name('txtPassword')
    password.send_keys(args.electric_password)

    login_button = driver.find_element_by_xpath("//input[@class='button']")
    login_button.submit()

    amount_due = driver.find_element_by_xpath("//span[@class='account-amt account-balance-amount']")
    amount_due = float(amount_due.text.strip('$'))
    driver.close()
    return amount_due

def get_gas_bill_amount():
    driver = webdriver.Chrome(options=options)
    driver.get('https://online.nationalgridus.com/login/LoginActivate?applicurl=aHR0cHM6Ly9vbmxpbmUubmF0aW9uYWxncmlkdXMuY29tL2VzZXJ2aWNlX2VudS9zdGFydC5zd2U/U1dFQ21kPVN0YXJ0&auth_method=0')
    
    email = driver.find_element_by_name('uid')
    email.send_keys(args.gas_username)

    password = driver.find_element_by_name('response')
    password.send_keys(args.gas_password)

    login_button = driver.find_element_by_name('Submit')
    login_button.submit()

    driver.switch_to.frame('_sweclient')
    driver.switch_to.frame('_sweview')
    amount_due = driver.find_element_by_xpath('//*[@id="s_4_1_15_0"]')
    amount_due = float(amount_due.text.strip('$'))
    driver.close()
    return amount_due

def calculate_expected_payment():
    expected_payment = (electric_bill + gas_bill) / 2
    return expected_payment

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Arguments for username/password for National Grid Utilities')
    parser.add_argument('-E', '--electric_username', required=True, help="Username for National Grid Electric")
    parser.add_argument('-EP', '--electric_password', required=True, help="Password for National Grid Electric")
    parser.add_argument('-G', '--gas_username', required=True, help="Username for National Grid Gas")
    parser.add_argument('-GP', '--gas_password', required=True, help="Password for National Grid Gas")
    args = parser.parse_args()

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    
    electric_bill = get_electric_bill_amount()
    gas_bill = get_gas_bill_amount()
    expected_amount = calculate_expected_payment()
    final_payment = expected_amount - comcast_bill_amount

    table_data = [
        ['Electric Bill:', '${:.2f} / 2'.format(electric_bill), '${:.2f}'.format(electric_bill/2.0)],
        ['Gas Bill:','${:.2f} / 2'.format(gas_bill), '${:.2f}'.format(gas_bill/2.0)],
        ['','', '- ${}'.format(comcast_bill_amount)]
    ]

    col_width = max(len(word) for row in table_data for word in row) + 2  # padding
    for row in table_data:
        print("".join(word.ljust(col_width) for word in row))
    print('----------------------------------------')
    print('Amount Due:  ${:.2f}'.format(final_payment))
