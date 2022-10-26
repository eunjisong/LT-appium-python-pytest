from os import environ
import pytest
from appium import webdriver


@pytest.fixture(scope='function')
def test_setup_android(request):
    test_name = request.node.name
    build = environ.get('BUILD', "Stride-Android-dev-debug")
    capability = {
        "platformName": "android",
        "deviceName": "Galaxy S21+ 5G",
        "platformVersion": "11",
        "app": "lt://APP10160521021666811020909545",
        "devicelog": True,
        "visual": True,
        "network": True,
        "video": True,
        "project": "Android Pytest",
        "deviceOrientation": "portrait",
        "isRealMobile": True,
        "build": build,
        "name": test_name
    }

    driver = webdriver.Remote(
        command_executor="https://eunji.song:vxGnlMcez526GZMjS61iJR1LoEvChmEW1vy88jvD3R5vpMPVbL@mobile-hub.lambdatest.com/wd/hub",
        desired_capabilities=capability)  # Add LambdaTest username and accessKey here
    request.cls.driver = driver

    yield driver

    def fin():
        # browser.execute_script("lambda-status=".format(str(not request.node.rep_call.failed if "passed" else "failed").lower()))
        if request.node.rep_call.failed:
            driver.execute_script('lambda-status=failed')
        else:
            driver.execute_script('lambda-status=passed')
        driver.quit()

    request.addfinalizer(fin)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # this sets the result as a test attribute for LambdaTest reporting.
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set an report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"
    setattr(item, "rep_" + rep.when, rep)

