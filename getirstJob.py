from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.calcareers.ca.gov/CalHrPublic/Jobs/JobPosting.aspx?JobControlId=483035")

    # Wait for the container to be visible
    card = page.locator("div#cphMainContent_rptResults_pnlCardContainer_0")

    # Retrieve text fields
    job_title = card.locator("a.lead").text_content().strip()
    working_title = card.locator("div.working-title span").text_content().strip()
    job_control = card.locator("div.position-number div.job-details").text_content().strip()
    salary_range = card.locator("div.salary-range div.job-details").text_content().strip()
    schedule = card.locator("div.schedule div.job-details").text_content().strip()
    department = card.locator("div.department div.job-details").text_content().strip()
    location = card.locator("div.location div.job-details").text_content().strip()
    telework = card.locator("div.telework div.job-details").text_content().strip()

    # Two publish/filing dates
    publish_date = card.locator("div.col-sm-6 div.filing-date time").text_content().strip()
    filing_deadline = card.locator("div.col-md-3 div.filing-date time").text_content().strip()

    # Get the job posting URL
    view_job_posting_url = card.locator("a.btn").get_attribute("href")

    # Print everything
    print("Job Title:", job_title)
    print("Working Title:", working_title)
    print("Job Control:", job_control)
    print("Salary Range:", salary_range)
    print("Schedule:", schedule)
    print("Department:", department)
    print("Location:", location)
    print("Telework:", telework)
    print("Publish Date:", publish_date)
    print("Filing Deadline:", filing_deadline)
    print("View Job Posting URL:", view_job_posting_url)

    browser.close()
