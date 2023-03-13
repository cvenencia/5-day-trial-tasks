from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains

from time import sleep

from langdetect import detect


driver_location = '/usr/bin/chromedriver'
binary_location = '/usr/bin/google-chrome'

chrome_options = ChromeOptions()
chrome_options.binary_location = binary_location

# chrome_options.add_argument("--disable-infobars")
# chrome_options.add_argument("--start-maximized")
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument('--window-size=1920,1080')
# chrome_options.add_argument("--headless")


# caps = DesiredCapabilities().CHROME
# caps["pageLoadStrategy"] = "eager"


def scrape_pages(**kwargs):
    urls = kwargs['urls'].split('\n')
    driver = Chrome(executable_path=driver_location,
                    options=chrome_options)
    results = []
    for url in urls:
        result = {'url': url, 'pass': True, 'notes': ""}
        driver.get(url)
        # Check index is translated
        try:
            translated = False
            retries = 0
            while not translated and retries < 3:
                retries += 1
                title = select('main > section:nth-child(1) h2',
                               driver).get_attribute('textContent')
                if detect(title) != 'hi':
                    result['pass'] = False
                    result['notes'] += "Not translated. "
                    print('Sleeping')
                    sleep(1)
                else:
                    translated = True
        except Exception as e:
            result['pass'] = False
            result['notes'] += 'Wrong page. '
            results.append(result)
            continue

        # Check high resolution image
        try:
            img = select('#learning-illus img',
                         driver)
            if img.get_attribute('data-src') is not None and "&blur=" in img.get_attribute('src'):
                result['pass'] = False
                result['notes'] += 'Images are not high resolution. '
        except Exception as e:
            print(e)

        # Hover mouse to check JS
        try:
            a = ActionChains(driver)
            button = select(
                'button[data-name="LARGE_UP_MAIN_NAV_TRIGGER"]', driver)
            a.move_to_element(button).perform()
            if 'nav-open' not in select('html', driver).get_attribute('class'):
                result['pass'] = False
                result['notes'] += 'Javascript not working. '
        except Exception as e:
            pass

        # Check if second link is translated
        try:
            new_url = select(
                'a.link-gray-underline', driver).get_attribute('href')
            open_second_tab(driver)
            driver.get(new_url)
            text = select('p.hint-card__body',
                          driver).get_attribute('textContent')
            if detect(text) != 'hi':
                result['pass'] = False
                result['notes'] += "Inner pages not translated. "
            close_tab_go_first_tab(driver)
        except Exception as e:
            close_tab_go_first_tab(driver)

        results.append(result)
    return results


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
