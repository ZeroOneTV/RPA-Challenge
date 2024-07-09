from robocorp import workitems
from robocorp.tasks import get_output_dir, task
import logging

from src.scraper import NewsScraper
from src.utils import category_exist, verifyMonthData

logging.basicConfig(level=logging.INFO, filename='../logs/app.log', 
                    format='%(asctime)s %(levelname)s:%(message)s')

# @task
# def producer():
#     """Split Excel rows into multiple output Work Items for the next step."""
#     output = get_output_dir() or Path("output")
#     filename = "orders.xlsx"

#     for item in workitems.inputs:
#         path = item.get_file(filename, output / filename)

#         excel = Excel()
#         excel.open_workbook(path)
#         rows = excel.read_worksheet_as_table(header=True)

#         for row in rows:
#             payload = {
#                 "Name": row["Name"],
#                 "Zip": row["Zip"],
#                 "Product": row["Item"],
#             }
#             workitems.outputs.create(payload)


@task
def consumer():
    """Process all the produced input Work Items from the previous step."""
    for item in workitems.inputs:
        try:
            phrase = item.payload["phrase"]
            category = item.payload["category"]
            months = item.payload["months"]

            logging.info(f"Processing order: {phrase}, {category}, {months}")

            assert phrase, "Phrase is missing or empty"
            assert category_exist(category), "Category is missing, empty or invalid option"
            assert months, "Months is missing or empty"

            nscraper = NewsScraper(log=logging)
            convertedMonthToDateTime = verifyMonthData(months)
            itemsFromSearch = nscraper.scrape_news(phrase,category,convertedMonthToDateTime)
            logging.info(itemsFromSearch)

            item.done()
        except AssertionError as err:
            item.fail("BUSINESS", code="INVALID_ORDER", message=str(err))
        except KeyError as err:
            item.fail("APPLICATION", code="MISSING_FIELD", message=str(err))
