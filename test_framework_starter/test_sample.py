"Test cases for learning various web interactions using Playwright"
"Author: Chris Fenton"
"Contact: fentonc2013@gmail.com"

from playwright.sync_api import sync_playwright
import time

def test_text_box_form():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # set to True if you want to hide the browser
        page = browser.new_page()
        page.goto("https://demoqa.com/text-box")

        # Fill out the form
        page.fill("#userName", "Jane Doe")
        page.fill("#userEmail", "jane@example.com")
        page.fill("#currentAddress", "123 Test Lane")
        page.fill("#permanentAddress", "456 Permanent Ave")

        # Submit the form
        page.click("#submit")

        # Validate output
        assert "Jane Doe" in page.text_content("#output")
        assert "jane@example.com" in page.text_content("#output")
        assert "123 Test Lane" in page.text_content("#output")
        assert "456 Permanent Ave" in page.text_content("#output")

        browser.close()


def test_check_box():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://demoqa.com/checkbox")

        # Expand all checkboxes
        page.click("button[title='Expand all']")

        # Click the custom checkbox labels (not input elements!)
        page.click("label:has-text('Documents')")
        page.click("label:has-text('Desktop')")

        # Validate that the result text contains the checked items
        result_text = page.text_content("#result")
        assert "documents" in result_text.lower()
        assert "desktop" in result_text.lower()

        browser.close()

def test_add_web_table_entry():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://demoqa.com/webtables")

        # Click the "Add" button
        page.get_by_role("button", name="Add").click()

        # Fill out the form using accessible names / labels
        page.get_by_placeholder("First Name").fill("Jane")
        page.get_by_placeholder("Last Name").fill("Doe")
        page.get_by_placeholder("name@example.com").fill("jane.doe@example.com")
        page.get_by_placeholder("Age").fill("35")
        page.get_by_placeholder("Salary").fill("90000")
        page.get_by_placeholder("Department").fill("Engineering")

        # Submit the form
        page.get_by_role("button", name="Submit").click()

        # Wait the print
        # time.sleep(3)

        # Confirm the new row contains the added user
        assert page.locator(".rt-td", has_text="Jane").first.is_visible()
        assert page.locator(".rt-td", has_text="Doe").first.is_visible()
        assert page.locator(".rt-td", has_text="jane.doe@example.com").first.is_visible()

        # Locate the row that contains 'Jane'
        row = page.locator(".rt-tr-group", has_text="Jane")

        # Click the edit button inside that row
        row.locator("span[id^='edit-record']").click()

        # Update the Salary field
        page.get_by_role("textbox", name="Salary").fill("95000")
        page.get_by_role("button", name="Submit").click()

        # Assert salary was updated
        assert page.locator(".rt-td", has_text="95000").first.is_visible()

        # Locate the same row again
        row = page.locator(".rt-tr-group", has_text="Jane")

        # Click the delete button (🗑) inside the row
        row.locator("span[id^='delete-record']").click()

        # Assert the record is gone
        assert not page.locator(".rt-td", has_text="Jane").first.is_visible()

        browser.close()