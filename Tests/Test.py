import json
import pytest
from config.WebDriverManager import WebDriverManager
from src.HomePage import HomePage
from src.ExcelReader import ExcelReader

@pytest.fixture(scope="function")
def setup_driver():
    """
    pytest fixture for WebDriver setup and teardown.
    :return: Tuple (SeleniumAction, DemoBlazePage)
    """
    manager = WebDriverManager(headless=False)
    driver = manager.create_driver()

    page = HomePage(driver)
    yield page  # Provide the DemoBlazePage instance to the test
    manager.close_driver()  # Teardown


def test_get_names_of_all_products_displayed(setup_driver):
    """
      Test to verify that the product names displayed on the website match the product names
      from the Excel sheet and check the count of products.
      """
    # Initialize ExcelReader and fetch product data
    excel_reader = ExcelReader("../resources/products.xlsx")  # Path to the Excel file
    product_data_from_excel = excel_reader.get_column_data("ProductName")  # List of product names from Excel

    # Initialize the page object
    page = setup_driver
    page.open_home_page()

    # Fetch product names displayed on the website
    print("Fetching product names from the website...")
    website_product_names = page.get_all_card_names_with_pagination()

    # Debug output
    print(f"Total products fetched from the website: {len(website_product_names)}")
    print(f"Website product names: {website_product_names}")

    # Assertions
    assert len(website_product_names) == len(product_data_from_excel), (
        f"Product count mismatch: Website ({len(website_product_names)}) vs Excel ({len(product_data_from_excel)})."
    )

    assert website_product_names == product_data_from_excel, (
        "Mismatch in product names between the website and Excel."
    )

    print("All product names match between the website and Excel.")



def test_data_of_phone(setup_driver):
    product_name = "HTC One M9"
    # Initialize the page object
    page = setup_driver
    page.open_home_page()

    #click on phones buttons
    page.click_phones_button()

    #select needed product
    page.select_product(product_name)

    # Get actual product details from the page
    actual_data = page.get_product_details()

    with open("../resources/productData.json", "r") as file:
        product_data = json.load(file)
        print(product_data)

        expected_data = product_data[product_name]
        print(expected_data)


    # Assert product details
    assert actual_data["name"] == product_name, f"Expected product name '{product_name}', but got '{actual_data['name']}'"
    assert actual_data["price"] == expected_data["price"], f"Expected price '{expected_data['price']}', but got '{actual_data['price']}'"
    assert actual_data["description"] == expected_data["description"], f"Expected description '{expected_data['description']}', but got '{actual_data['description']}'"

    # Print success message
    print(f"Product details for '{product_name}' are validated successfully.")







