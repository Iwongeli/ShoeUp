import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

driver = webdriver.Chrome()  # Replace with your preferred WebDriver
driver.get("https://www.reebok.eu/en-pl/shopping/men-shoes?pageindex=4")
div_elements = driver.find_elements(By.XPATH, '//*[@id="siteContent"]/div/div[2]')

# Append to an existing CSV file
csv_file = open('href_values.csv', 'a', newline='')
csv_writer = csv.writer(csv_file)

for div in div_elements:
    # Find the anchor elements within each div
    anchor_elements = div.find_elements(By.XPATH, './/a[@data-test="link-wrapper"]')
    
    # Loop through the anchor elements and extract the href values
    for anchor in anchor_elements:
        href_value = anchor.get_attribute('href')
        csv_writer.writerow([href_value])

# Close the CSV file
csv_file.close()

driver.quit()
