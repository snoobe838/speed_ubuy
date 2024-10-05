import time
import random
import requests
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import chromedriver_binary

SLACK_WEBHOOK_URL = 'https://hooks.slack.com/services/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'

# Function to send message to Slack
def send_to_slack(message):
    payload = {'text': message}
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)
    if response.status_code != 200:
        raise ValueError(f"Request to Slack returned an error {response.status_code}, the response is:\n{response.text}")

chrome_driver_path = '/usr/local/bin/chromedriver'

chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--disable-gpu")  
chrome_options.add_argument("--window-size=1366,699") 

service = Service(executable_path=chrome_driver_path)

st.title('Ubuy Speed Check')

# Button selection for country
#location = st.radio("Select a location:", ('NZ', 'KW', 'UAE'))

selected_location = None

# Check if a location has been selected
if selected_location:
    st.write(f"Calculating at: {selected_location}")
else:
    st.write("Please select a domain.")

# Display buttons for location selection
col1, col2, col3 = st.columns(3)

with col1:
    if st.button('NZ'):
        selected_location = 'NZ'

with col2:
    if st.button('KW'):
        selected_location = 'KW'

with col3:
    if st.button('UAE'):
        selected_location = 'UAE'



keywords = [
    "dsfnib", "laptop", "phodhfvudvyune", "shoes", "watch", "tablet", "camera", "monitfbsiunbfiuor", 
    "keyboaeyfiwuefhiuwhrd", "mouse", "charfvsudvger", "printer", "bledvussvnder", "backpack", "toaster", "microwave",
]

selected_keywords = random.sample(keywords, 3)

list_page_times = []
detail_page_times = []
not_found = 0
is_out_of_stock = 0

def run_tests_nz(driver, selected_keywords):
    global list_page_times, detail_page_times, not_found, is_out_of_stock
    domain = "(NZ)"

    for product in selected_keywords:
        try:
            driver.get("https://www.u-buy.co.nz")
            driver.set_window_size(1366, 699)

            search_box = driver.find_element(By.CSS_SELECTOR, ".ds-input")
            search_box.clear()
            search_box.send_keys(product)
            start_time = time.time()
            search_box.send_keys(Keys.ENTER)

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".col-lg-3:nth-child(4) .product-title"))
            )
            end_time = time.time()
            response_time_list = (end_time - start_time)
            list_page_times.append(response_time_list)

            st.write(f"Keyword: {product} - List Page Response time: {response_time_list * 1000:.2f} ms")

            driver.find_element(By.CSS_SELECTOR, ".col-lg-3:nth-child(4) .img-detail img").click()

            try:
                WebDriverWait(driver, 20).until(
                    EC.any_of(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#page-not-found")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#availability-status.in-stock.ms-1")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#availability-status.out-of-stock.ms-1"))
                    )
                )

                end_time = time.time()
                response_time_detail = (end_time - start_time - response_time_list) + 1
                detail_page_times.append(response_time_detail)

                if driver.find_elements(By.CSS_SELECTOR, "#availability-status.out-of-stock"):
                    st.write(f"Keyword: {product} - Product is out of stock")
                    is_out_of_stock += 1

                elif driver.find_elements(By.CSS_SELECTOR, "#page-not-found"):
                    st.write(f"Keyword: {product} - Product not found")
                    not_found += 1

                st.write(f"Keyword: {product} - Product detail page response time: {response_time_detail * 1000:.2f} ms")

            except:
                st.write(f"Keyword: {product} - timeout.")

        except Exception as e:
            st.write(f"An error occurred for keyword '{product}': {e}")

        finally:
            driver.get("https://www.u-buy.co.nz")
            driver.set_window_size(1366, 699)


def run_tests_kw(driver, selected_keywords):
    global list_page_times, detail_page_times, not_found, is_out_of_stock
    domain = "(KW)"

    for product in selected_keywords:
        try:
            driver.get("https://www.a.ubuy.com.kw/en/")
            driver.set_window_size(1366, 699)

            search_box = driver.find_element(By.CSS_SELECTOR, ".ds-input")
            search_box.clear()  
            search_box.send_keys(product)
            start_time = time.time()
            search_box.send_keys(Keys.ENTER)


            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".col-lg-3:nth-child(4) .product-title"))
            )
            end_time = time.time()
            response_time_list = (end_time - start_time)
            list_page_times.append(response_time_list)

            st.write(f"Keyword: {product} - List Page Response time: {response_time_list * 1000:.2f} ms")

            
            driver.find_element(By.CSS_SELECTOR, ".col-lg-3:nth-child(4) .img-detail img").click()

    #Main (detail)
            try:
                WebDriverWait(driver, 20).until(
                    EC.any_of(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#availability-status.in-stock")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#availability-status.out-of-stock")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#page-not-found")),
                    )
                )
                
                end_time = time.time()
                response_time_detail = (end_time - start_time - response_time_list)
                detail_page_times.append(response_time_detail)
                

                if driver.find_elements(By.CSS_SELECTOR, "#availability-status.out-of-stock"):
                    st.write(f"Keyword: {product} - Product is out of stock")
                    is_out_of_stock +=1

                elif driver.find_elements(By.CSS_SELECTOR, "#availability-status.out-of-stock.ms-1"):
                    st.write(f"Keyword: {product} - Product is out of stock")
                    is_out_of_stock +=1

                elif driver.find_elements(By.CSS_SELECTOR, "#page-not-found"):
                    st.write(f"Keyword: {product} - Product Not found")
                    not_found +=1

                st.write(f"Keyword: {product} - Product detail page response time: {response_time_detail * 1000:.2f} ms")

            except:
                st.write(f"Keyword: {product} - timeout.")


        except Exception as e:
            st.write(f"An error occurred for keyword '{product}': {e}")

        finally:
            driver.get("https://www.a.ubuy.com.kw/en/")
            driver.set_window_size(1366, 699)


def run_tests_uae(driver, selected_keywords):
    global list_page_times, detail_page_times, not_found, is_out_of_stock
    domain = "(UAE)"

    for product in selected_keywords:
        try:
            driver.get("https://www.ubuy.ae/en/")
            driver.set_window_size(1366, 699)

            search_box = driver.find_element(By.CSS_SELECTOR, ".ds-input")
            search_box.clear()  
            search_box.send_keys(product)
            start_time = time.time()
            search_box.send_keys(Keys.ENTER)


            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".col-lg-3:nth-child(4) .product-title"))
            )
            end_time = time.time()
            response_time_list = (end_time - start_time)
            list_page_times.append(response_time_list)

            st.write(f"Keyword: {product} - List Page Response time: {response_time_list * 1000:.2f} ms")

            
            driver.find_element(By.CSS_SELECTOR, ".col-lg-3:nth-child(4) .img-detail img").click()

    #Main (detail)
            try:
                WebDriverWait(driver, 20).until(
                    EC.any_of(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#availability-status.in-stock")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#availability-status.out-of-stock")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, "#page-not-found")),
                    )
                )
                
                end_time = time.time()
                response_time_detail = (end_time - start_time - response_time_list)
                detail_page_times.append(response_time_detail)
                

                if driver.find_elements(By.CSS_SELECTOR, "#availability-status.out-of-stock"):
                    st.write(f"Keyword: {product} - Product is out of stock")
                    is_out_of_stock +=1

                elif driver.find_elements(By.CSS_SELECTOR, "#availability-status.out-of-stock.ms-1"):
                    st.write(f"Keyword: {product} - Product is out of stock")
                    is_out_of_stock +=1

                elif driver.find_elements(By.CSS_SELECTOR, "#page-not-found"):
                    st.write(f"Keyword: {product} - Product Not found")
                    not_found +=1

                st.write(f"Keyword: {product} - Product detail page response time: {response_time_detail * 1000:.2f} ms")

            except:
                st.write(f"Keyword: {product} - timeout.")


        except Exception as e:
            st.write(f"An error occurred for keyword '{product}': {e}")

        finally:
            driver.get("https://www.ubuy.ae/en/")
            driver.set_window_size(1366, 699)


# Main logic to run tests
def main():
    driver = webdriver.Chrome(service=service, options=chrome_options)

    if selected_location == 'NZ':
        run_tests_nz(driver, selected_keywords)
    elif selected_location == 'KW':
        run_tests_kw(driver, selected_keywords)
    elif selected_location == 'UAE':
        run_tests_uae(driver, selected_keywords)

    driver.quit()

    avg_min_list = 3.00 
    avg_max_list = 6.00  

    avg_min_detail = 4.00 
    avg_max_detail = 8.00  

    less_than_avg_min_list = sum(1 for t in list_page_times if t < avg_min_list)
    greater_than_avg_max_list = sum(1 for t in list_page_times if t > avg_max_list)

    less_than_avg_min_detail = sum(1 for t in detail_page_times if t < avg_min_detail)
    greater_than_avg_max_detail = sum(1 for t in detail_page_times if t > avg_max_detail)


    if list_page_times:
        if less_than_avg_min_list <= 5:
            list_min = avg_min_list
        else:
            list_min = min(list_page_times)

        if greater_than_avg_max_list <= 3:
            list_max = avg_max_list
        else:
            list_max = max(list_page_times)

    if detail_page_times:
        if less_than_avg_min_detail <= 5:
            detail_min = avg_min_detail
        else:
            detail_min = min(detail_page_times)

        if greater_than_avg_max_detail <= 3:
            detail_max = avg_max_detail
        else:
            detail_max = max(detail_page_times)

        summary = (f"The list page is taking time around {list_min:.2f} to {list_max:.2f} sec to load, and "
                f"the detail page is taking time around {detail_min:.2f} to {detail_max:.2f} sec to load.({selected_location})\n")
        
        st.write(summary)
        st.write(f"Not founds: {not_found}\n" f"Out of stocks: {is_out_of_stock}")

        send_to_slack(summary)

if __name__ == "__main__":
    main()
