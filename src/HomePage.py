from selenium.webdriver.common.by import By
from config.SeleniumAction import SeleniumAction
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class HomePage:
    url = "https://www.demoblaze.com/"

    LOCATORS = {
        "category_link": "//a[text()='{category_name}']",  # Use `.format` for dynamic locators
        "product_link": "//a[text()='{product_name}']",
        "add_to_cart_button": "//a[text()='Add to cart']",
        "card_names": "//div[@class='card-block']//h4/a",
        "next_button": "//button[contains(text(), 'Next')]",
        "phones_button": "//a[contains(text(), 'Phones')]",
        "product_name": "//h2[@class='name']",
        "product_price": "//h3[@class='price-container']",
        "product_description": "//div[@id='more-information']//p",
    }

    def __init__(self, driver):
        """
        Initialize the DemoBlaze page with a WebDriver instance.
        :param driver: Selenium WebDriver instance
        """
        self.driver = driver
        self.actions = SeleniumAction(driver)  # Initialize SeleniumAction internally

    def open_home_page(self):
        self.actions.get_url(self.url)


    def select_product(self, product_name):
        """
        Select a specific product by name.
        :param product_name: Name of the product
        """
        product_xpath = self.LOCATORS["product_link"].format(product_name=product_name)
        self.actions.click_element(By.XPATH, product_xpath)

    def add_to_cart(self):
        """
        Click the 'Add to Cart' button.
        """
        self.actions.click_element(By.XPATH, self.LOCATORS["add_to_cart_button"])

    def get_card_names(self):
        """
        Get the names of all product cards displayed on the homepage.
        :return: List of product names as strings
        """
        elements = self.actions.get_elements(By.XPATH, self.LOCATORS["card_names"])
        return self.actions.get_texts_of_elements(elements)

    def get_all_card_names_with_pagination(self):
        """
        Get the names of all product cards across multiple pages with validation
        to wait until new results are loaded.
        :return: List of unique product names as strings
        """
        all_card_names = []  # Normal list to store all card names
        previous_page_names = []
        retries = 0
        max_retries = 5  # Maximum number of retries for waiting for new data

        while True:
            try:
                # Get names from the current page
                current_page_names = self.get_card_names()

                # Check if the current page data is the same as the previous page
                if current_page_names == previous_page_names:
                    retries += 1
                    if retries >= max_retries:
                        print("Max retries reached. No new content loaded.")
                        break
                    print(f"Retrying to fetch new content... Attempt {retries}/{max_retries}")
                    WebDriverWait(self.driver, 2).until(
                        lambda driver: self.get_card_names() != previous_page_names
                    )
                    continue  # Retry fetching data
                else:
                    retries = 0  # Reset retries if new data is found

                # Add new card names to the list
                all_card_names.extend(current_page_names)
                previous_page_names = current_page_names

                # Check and navigate to the next page
                if not self.go_to_next_page():
                    print("Next button not displayed. Stopping pagination.")
                    break

            except TimeoutException:
                print("Timeout while waiting for new content.")
                break
            except StaleElementReferenceException:
                print("Stale element encountered. Retrying...")
                continue

        return all_card_names


    def go_to_next_page(self):
        """
        Navigate to the next page if the 'Next' button is available.
        :return: True if navigation to the next page was successful, False otherwise
        """
        try:
            next_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, self.LOCATORS["next_button"]))
            )
            next_button.click()
            return True
        except (NoSuchElementException, TimeoutException):
            return False

    def click_phones_button(self):
        """
        Click on the 'Phones' button in the category section.
        """
        self.actions.click_element(By.XPATH, self.LOCATORS["phones_button"])


    def get_product_details(self):
        """
        Get the details of the selected product on its detail page.
        :return: Dictionary with 'name', 'price', and 'description' of the product
        """
        try:
            name = self.actions.get_text(By.XPATH, self.LOCATORS["product_name"])
            price = self.actions.get_text(By.XPATH, self.LOCATORS["product_price"])
            description = self.actions.get_text(By.XPATH, self.LOCATORS["product_description"])

            return {
                "name": name,
                "price": price,
                "description": description,
            }
        except NoSuchElementException as e:
            print("Error fetching product details:", e)
            return {}



    def navigate_category(self, category_name):
        """
        Navigate to a specific category (e.g., Laptops, Phones).
        :param category_name: Name of the category
        """
        category_xpath = self.LOCATORS["category_link"].format(category_name=category_name)
        self.actions.click_element(By.XPATH, category_xpath)
