from selenium import webdriver
from datetime import date, time, timedelta
from selenium.webdriver.support.ui import Select

# User info
license_number = "00000000"
license_expiry_date = "dd/mm/yyyy"
first_name = "ERIC"
last_name = "LI"
date_of_birth = "dd/mm/yyyy"

# Booking preference
site = "Cannington"
days_min = 10   # how many days from today to start booking
days_max = 30   # how many days from today to stop booking
start_time = time(9, 0, 0)  # time to start booking 9am
end_time = time(13, 30, 0)  # time to stop booking 13:30


def date_in_range(DATE):
    today = date.today()
    start_date = today + timedelta(days=days_min)
    end_date = today + timedelta(days=days_max)
    return start_date <= DATE <= end_date


def time_in_range(TIME):
    return start_time <= TIME <= end_time


def get_date_time(date_time):
    """
    Transfer str date_time to date object, and time object of datetime lib
    :param date_time: (str)'dd/mm/yyyy at hh:mm AM'
    :return: DATE: (date object) yyyy/mm/dd
             TIME: (time object) hh:mm (24h format)
    """
    info = date_time.text
    DATE = info.split()[0]
    date_ymd = DATE.split('/')
    date_ymd.reverse()  # swich from dd/mm/yyyy to yyyy/mm/dd
    date_ymd = [int(a) for a in date_ymd]
    DATE = date(date_ymd[0], date_ymd[1], date_ymd[2])

    TIME = info.split()[2]
    hour_minute = [int(a) for a in TIME.split(':')]
    am_pm = info.split()[3]
    if am_pm == 'PM':
        hour_minute[0] += 12
    TIME = time(hour_minute[0], hour_minute[1], 0)
    return DATE, TIME


driver = webdriver.Chrome()
driver.implicitly_wait(10)  # IMPORTANT due to the delay of ajax
try:
    driver.get("https://online.transport.wa.gov.au/pdabooking/manage/?0#top")
    driver.find_element_by_name("clientDetailsPanel:licenceNumber").click()
    driver.find_element_by_name("clientDetailsPanel:licenceNumber").clear()
    driver.find_element_by_name("clientDetailsPanel:licenceNumber").send_keys(license_number)
    driver.find_element_by_id("licenceExpiryDatePicker").click()
    driver.find_element_by_id("licenceExpiryDatePicker").clear()
    driver.find_element_by_id("licenceExpiryDatePicker").send_keys(license_expiry_date)
    driver.find_element_by_name("clientDetailsPanel:firstName").click()
    driver.find_element_by_name("clientDetailsPanel:firstName").clear()
    driver.find_element_by_name("clientDetailsPanel:firstName").send_keys(first_name)
    driver.find_element_by_name("clientDetailsPanel:lastName").clear()
    driver.find_element_by_name("clientDetailsPanel:lastName").send_keys(last_name)
    driver.find_element_by_id("dateOfBirthPicker").clear()
    driver.find_element_by_id("dateOfBirthPicker").send_keys(date_of_birth)
    driver.find_element_by_id("id5").click()
    driver.find_element_by_xpath("//input[@value='Change']").click()
    driver.find_element_by_name("searchBookingContainer:siteCode").click()
    Select(driver.find_element_by_name("searchBookingContainer:siteCode")).select_by_visible_text(site)
    driver.find_element_by_name("searchBookingContainer:search").click()
    dates_times = driver.find_elements_by_xpath("//span[@id='searchResultRadioLabel']")
    index = 0
    confirmed = 0
    for date_time in dates_times:
        DATE, TIME = get_date_time(date_time)
        if date_in_range(DATE) and time_in_range(TIME):
            driver.find_element_by_id("searchResultRadio" + str(index)).click()
            driver.find_element_by_name("confirm").click()
            confirmed = 1
            break
        else:
            index += 1
finally:
    if confirmed:
        print("confirmed booking at", DATE, TIME)
    else:
        print("No booking found")
    driver.close()
