import pytest
from appium.webdriver.common.appiumby import AppiumBy


@pytest.mark.usefixtures('test_setup_android')
class TestLink:

    def test_1(self):
        el1 = self.driver.find_elements(AppiumBy.ID, 'R.id.button_primary')
        el1.click()

    def test_2(self):
        el2 = self.driver.find_element_by_id("com.stridehealth.drive:id/button_primary")
        el2.click()




