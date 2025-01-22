from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class WebDriverManager:
    def __init__(self, headless=False, implicit_wait_time=10):
        """
        Initialize WebDriverManager with optional headless mode and implicit wait.
        :param headless: Run browser in headless mode if True
        :param implicit_wait_time: Time (in seconds) for implicit waits
        """
        self.headless = headless
        self.implicit_wait_time = implicit_wait_time
        self.driver = None

    def create_driver(self):
        """
        Create and return a WebDriver instance with configured options.
        """
        options = Options()
        if self.headless:
            options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(self.implicit_wait_time)  # Set implicit wait
        print(f"WebDriver created with {self.implicit_wait_time} seconds implicit wait.")
        return self.driver

    def close_driver(self):
        """
        Close the WebDriver instance.
        """
        if self.driver:
            self.driver.quit()
            print("WebDriver closed.")




