from selenium.common import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SeleniumAction:
    def __init__(self, driver):
        self.driver = driver

    def get_url(self, url):
        self.driver.get(url)

    def find_element(self, by, value, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def click_element(self, by, value, timeout=10, retries=3):
        """
        Clicks an element on the page with retry logic to handle StaleElementReferenceException.
        :param by: Locator strategy (e.g., By.XPATH, By.ID).
        :param value: Locator value.
        :param timeout: Maximum wait time for the element to be clickable.
        :param retries: Number of retries to handle StaleElementReferenceException.
        """
        for attempt in range(retries):
            try:
                element = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable((by, value))
                )
                element.click()
                return  # Exit the function if click is successful
            except StaleElementReferenceException:
                if attempt < retries - 1:
                    print(f"Retrying click on element: {value} (Attempt {attempt + 2})")
                else:
                    raise  # Re-raise exception if all retries are exhausted

    def send_keys(self, by, value, keys, timeout=10):
        element = self.find_element(by, value, timeout)
        element.clear()
        element.send_keys(keys)

    def get_text(self, by, value, timeout=10):
        element = self.find_element(by, value, timeout)
        return element.text

    def get_elements(self, by, value, timeout=10):
        """
        Get all elements matching a locator within a timeout period.
        :param by: Locator strategy (e.g., By.ID, By.XPATH)
        :param value: Locator value
        :param timeout: Timeout for explicit wait
        :return: List of WebElements
        """
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((by, value))
        )
        return self.driver.find_elements(by, value)


    def get_texts_of_elements(self, elements):
        """
        Get the text of all WebElements in a list.
        :param elements: List of WebElements
        :return: List of text content from the elements
        """
        return [element.text for element in elements]