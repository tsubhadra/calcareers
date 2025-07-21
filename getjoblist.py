from playwright.sync_api import sync_playwright

USER_ID = "tsubhadra"
PASSWORD = "#9thMay2024"

def scrape_jobs():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Go to homepage
        page.goto("https://www.calcareers.ca.gov/")

        page.on("dialog", lambda dialog: (
            print(f"Dialog message: {dialog.message}"),
            dialog.dismiss()
        ))

        # Log in
        page.get_by_role("link", name="Create Account / Log In").click()
        page.wait_for_url("https://calcareers.ca.gov/CalHRPublic/Login.aspx")
        page.fill("#cphMainContent_LogIn2_txtUserId", USER_ID)
        page.fill("#cphMainContent_LogIn2_txtPassword", PASSWORD)
        page.click("#cphMainContent_LogIn2_btnLogin")

        print("Logged in successfully.")

        # Click "Find a Job"
        page.locator("#hlCondensedFindJobs").click()

        # Fill keyword
        page.fill("#cphMainContent_txtKeyword", "INFORMATION TECHNOLOGY ASSOCIATE")
        print("Keyword entered.")

        # Click Search
        page.click("#cphMainContent_btnSearch")
        print("Search submitted.")

        # Wait for table rows
        page.wait_for_selector("table#cphMainContent_tblResults tr.ResultRow")
        print("Results loaded.")

        # Get all rows
        rows = page.query_selector_all("table#cphMainContent_tblResults tr.ResultRow")

        def cell_text(row, idx):
            cells = row.query_selector_all("td")
            return cells[idx].inner_text().strip() if idx < len(cells) else "N/A"

        for row in rows[:10]:
            job_title = row.query_selector("a").inner_text().strip()
            department = cell_text(row, 1)
            location = cell_text(row, 2)
            job_control = cell_text(row, 3)
            salary = cell_text(row, 4)
            final_filing_date = cell_text(row, 5)

            print(f"""Job: {job_title}
Department: {department}
Location: {location}
Job Control: {job_control}
Salary Range: {salary}
Filing Deadline: {final_filing_date}
""")

        browser.close()

if __name__ == "__main__":
    scrape_jobs()
