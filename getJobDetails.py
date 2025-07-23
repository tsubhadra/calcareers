from playwright.sync_api import sync_playwright

USER_ID = "userid"
PASSWORD = "pwd"


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set to True for headless mode
        page = browser.new_page()

        # Go to the homepage
        page.goto("https://www.calcareers.ca.gov/")

        page.on("dialog", lambda dialog: (
            print(f"Dialog message: {dialog.message}"),
            dialog.dismiss()  # or dialog.accept() if needed
        ))

        # Click the "Create Account / Log In" button in the top menu
        page.get_by_role("link", name="Create Account / Log In").click()

        # Wait for navigation to login form
        # page.wait_for_url("**/CalHRPublic/Login.aspx")
        page.wait_for_url("https://calcareers.ca.gov/CalHRPublic/Login.aspx")



        page.locator("#cphMainContent_LogIn2_txtUserId").fill(USER_ID)
        page.locator("#cphMainContent_LogIn2_txtPassword").fill(PASSWORD)

        # Click the login button
        page.locator("#cphMainContent_LogIn2_btnLogin").click()
        page.locator("#hlCondensedFindJobs").click()

        # Open the dropdown
        # Fill the input field by ID
        page.fill("#cphMainContent_txtKeyword", "INFORMATION TECHNOLOGY ASSOCIATE")

        # Click the Search button by ID
        page.click("#cphMainContent_btnSearch")

        # Wait for navigation or results to load
        page.wait_for_load_state("networkidle")


        page.pause()
        page.wait_for_selector("span.ecos-result-count.number-counter")
        # Get the job count text
        job_count = page.locator("span.ecos-result-count.number-counter").inner_text()
        print(f"{job_count} job(s) found.")

        page.wait_for_selector("select#cphMainContent_ddlRowCount")
        # Select "20 Jobs" using the value "20"
        page.select_option("select#cphMainContent_ddlRowCount", value="20")
        print("Selected: 20 Jobs")

        # Wait for job cards to load
        page.wait_for_selector("div.card-block")

        # Get all job cards
        job_cards = page.locator("div.card-block")
        count = job_cards.count()

        print(f"\nTotal job postings found: {count}\n")

        for i in range(count):
            card = job_cards.nth(i)

            title = card.locator("a.lead").text_content().strip()
            job_control_id = card.locator("div.position-number span").text_content().strip()
            department = card.locator("div.department span").text_content().strip()
            location = card.locator("div.location span").text_content().strip()
            telework = card.locator("div.telework span").text_content().strip()
            salary = card.locator("div.salary-range span").text_content().strip()
            work_type = card.locator("div.schedule span").text_content().strip()
            publish_date = card.locator("div.filing-date time").nth(0).text_content().strip()
            filing_deadline = card.locator("div.filing-date time").nth(1).text_content().strip()

            print(f"Job #{i + 1}")
            print(f"Title          : {title}")
            print(f"Job Control ID : {job_control_id}")
            print(f"Department     : {department}")
            print(f"Location       : {location}")
            print(f"Telework       : {telework}")
            print(f"Salary         : {salary}")
            print(f"Work Type      : {work_type}")
            print(f"Publish Date   : {publish_date}")
            print(f"Filing Deadline: {filing_deadline}")
            print("-" * 60)

        # Wait a moment to visually verify
        page.wait_for_timeout(3000)

if __name__ == "__main__":
    run()
