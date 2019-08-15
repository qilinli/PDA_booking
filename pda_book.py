from selenium import webdriver
from selenium.webdriver.support.ui import Select

# Booking info
license_number = "7281085"
license_expiry_date = "05/04/2021"
first_name = "xiangmeng"
last_name = "tang"
date_of_birth = "27/07/1991"
site = "Cannington"

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
    driver.find_element_by_xpath("//input[@value='Search Availability']").click()
    driver.find_element_by_name("searchBookingContainer:siteCode").click()
    Select(driver.find_element_by_name("searchBookingContainer:siteCode")).select_by_visible_text(site)
    driver.find_element_by_name("searchBookingContainer:search").click()
    driver.find_element_by_id("searchResultRadio0").click()
finally:
    driver.close()