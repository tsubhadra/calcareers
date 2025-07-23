import re
from playwright.sync_api import Playwright, sync_playwright, expect
import time

def extract_all_jobs(page):

    job_data = []
    job_count = 0

    while True:
        # Wait until job rows are loaded
        # page.wait_for_selector("div.row")

        # Select all job rows (one div.row per job)
        job_rows = page.locator("div.row").all()

        for row in job_rows:
            def get_detail_in_row(row_element, label):
                try:
                    label_locator = row_element.locator(f"xpath=.//div[contains(@class, 'job-label') and normalize-space(text())='{label}']")
                    detail = label_locator.locator("xpath=following-sibling::div").first.inner_text().strip()
                    return detail
                except:
                    return ""

            try:
                working_title = row.locator("div.working-title span").first.inner_text().strip()
            except:
                working_title = ""

            department = get_detail_in_row(row, "Department:")
            job_control = get_detail_in_row(row, "Job Control:")
            location = get_detail_in_row(row, "Location:")
            salary = get_detail_in_row(row, "Salary Range:")
            telework = get_detail_in_row(row, "Telework:")

            try:
                filing_deadline = row.locator("div.filing-date time").first.inner_text().strip()
            except:
                filing_deadline = ""

            job_data.append({
                "Working Title": working_title,
                "Department": department,
                "Job Control": job_control,
                "Location": location,
                "Salary Range": salary,
                "Telework": telework,
                "Filing Deadline": filing_deadline
            })
            job_count += 1

        # Try clicking "Next" if available (depends on site's pagination)
        try:
            next_button = page.locator("text=Next")
            if next_button.is_enabled():
                next_button.click()
                page.wait_for_load_state("networkidle")
                time.sleep(1)  # Optional: wait for smooth transition
            else:
                break
        except:
            break

    # ✅ Print summary
    print(f"\n✅ Extracted {job_count} job(s):\n")
    for job in job_data:
        print(job)


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://calcareers.ca.gov/")
    page.get_by_text("CalHR Job Center: The CalHR Job Center, located at 1810 16th Street, Sacramento, CA 95811, will be open on the 1st and 3rd Tuesdays of the month. Our hours are 9:00 AM - 12:00 PM and 1:00 PM - 3:00 PM. A staff member will be available to assist you in navigating our CalCareer website for job opportunities. This is not a job fair event.Senior Vocational Rehabilitation Counselor,Qualified Rehabilitation Professional: The Senior Vocational Rehabilitation Counselor, Qualified Rehabilitation Professional examination will be unavailable for maintenance May 29, 2025, through July 15,").click()
    page.get_by_role("link", name=" Create Account / Log In").click()
    page.get_by_label("User I.D.").click()
    page.get_by_label("User I.D.").fill("userid")
    page.get_by_label("User I.D.").press("Tab")
    page.get_by_label("Password").fill("pwd")
    page.get_by_label("Password").press("Enter")
    page.get_by_role("link", name=" Find Jobs").click()
    page.get_by_label("Keyword:").click()
    page.get_by_label("Keyword:").fill("information technology")
    page.get_by_label("Keyword:").press("Enter")

    page.wait_for_selector("#cphMainContent_lblTotalResultCount")
    # Get the inner text (e.g., "154")
    job_count = page.inner_text("#cphMainContent_lblTotalResultCount")
    print(f"{job_count} job(s) found")

    # Wait for the select dropdown to be available
    page.wait_for_selector("#cphMainContent_ddlRowCount")
    # Select the option with value="50"
    page.select_option("#cphMainContent_ddlRowCount", value="50")
    # Optional: Wait for the page to reload after selection
    page.wait_for_load_state("networkidle")
    print("50 jobs selected in the selection list")
    extract_all_jobs(page)
    page.pause()

    page.get_by_label("INFORMATION TECHNOLOGY ASSOCIATE (481171)", exact=True).click()
    page.get_by_text("Job Posting: Information").click()
    page.locator("#lblDepartmentName").click()
    page.locator("#pnlBannerSection").get_by_text("JC-").click()
    page.get_by_text("$4,791.00 - $8,485.00 per").click()
    page.locator("#lblFinalFilingDate").click()
    page.get_by_role("button", name="Apply Now").click()
    page.get_by_text("I want to obtain eligibility").click()
    page.get_by_role("cell", name="1749").click()
    page.get_by_role("link", name="Q Logout").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
