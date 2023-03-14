from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

from urllib.parse import urlparse
from .utils import get_cop_usd_convertion

from time import sleep
import json


def scrape_pages(log, **kwargs):

    def check_udemy_course(url):
        try:
            parsed_url = urlparse(url)
            if "udemy.com" not in parsed_url.netloc:
                return log('❌ This is not a Udemy page. Skipping...', tab=1)
            if "/course/" not in parsed_url.path:
                return log('❌ This is not a course. Skipping...', tab=1)
            found = False
            retries = 0
            max_retries = 3
            driver = Chrome()
            driver.get(url)

            while not found and retries <= max_retries:
                try:
                    sleep(0.5 + retries * 0.2)
                    title = select('h1', driver).get_attribute(
                        'textContent')
                    price_text = select('[data-purpose="sidebar-container"] div[data-purpose="price-text-container"]',
                                        driver).get_attribute('textContent')
                    try:
                        original_price = select('[data-purpose="sidebar-container"] div[data-purpose="course-old-price-text"] span:not(.ud-sr-only)',
                                                driver).get_attribute('textContent').split('\xa0')[0].replace('.', '')
                    except:
                        log('❕ This course is not discounted.', tab=1)
                        original_price = None
                    final_price = select('[data-purpose="sidebar-container"] div[data-purpose="course-price-text"] span:not(.ud-sr-only)',
                                         driver).get_attribute('textContent').split('\xa0')[0].replace('.', '')
                    try:
                        usd_price = get_cop_usd_convertion(float(final_price))
                    except:
                        usd_price = 0

                    if original_price:
                        original_price_usd = get_cop_usd_convertion(
                            float(original_price))
                    else:
                        original_price_usd = usd_price
                    is_free = ('100 % de descuento' in price_text and 'Gratis' in price_text) or (
                        '100% off' in price_text and 'Free' in price_text)
                    found = True
                    if is_free:
                        log('✅ It\'s free!', tab=1)
                    else:
                        log('❌ It\'s not free', tab=1)
                        if original_price:
                            log(
                                f'❕ Original price: {float(original_price):,.0f} COP', tab=2)
                            log(
                                f'❕ Converted original price: {original_price_usd:0.2f} USD', tab=2)
                        log(
                            f'❕ Final price: {float(final_price):,.0f} COP', tab=2)
                        log(f'❕ Converted price: {usd_price:0.2f} USD', tab=2)
                    results.append({
                        'title': title,
                        'url': url,
                        'price': f'{usd_price:0.2f}',
                        'isFree': is_free,
                        'originalPrice': f'{original_price_usd:0.2f}'
                    })
                except Exception as e:
                    # print(e)
                    retries += 1
                    log(
                        f'❌ Error checking the course\'s information. {f"Trying again... ({retries}/{max_retries})" if retries < max_retries + 1 else "Maybe the link was invalid."}', tab=1)
            return 0
        except:
            log('Invalid URL. Skipping...', tab=1)

    log('⚠️ WARNING: prices in USD may not be representative of the real value. These prices are aproximations')
    log('since the original prices are found in Colombian Pesos (COP) and they are been converted.\n')
    urls = kwargs['urls'].split('\n')
    results = []
    for url in urls:
        try:
            if len(url) == 0:
                continue
            url_string = url.replace('\r', '')
            log(f'Scraping {insert_a_tag(url_string)}...')
            check_udemy_course(url)
        except Exception as e:
            # print(e)
            continue
    log(f'[[RESULTS_READY]]{json.dumps(results)}')


def open_second_tab(driver):
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])


def close_tab_go_first_tab(driver):
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


def select(selector, driver):
    return driver.find_element(By.CSS_SELECTOR, selector)


def select_all(selector, driver):
    return driver.find_elements(By.CSS_SELECTOR, selector)


def insert_a_tag(link):
    return f'<a href="{link}" target="_blank" rel="noopener noreferrer">{link}</a>'
