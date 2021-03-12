import os
import os.path
import datetime
import time
import json as j

from requests_async import *
import asyncio
from dotenv import load_dotenv

import dataclasses
from models import (
    Shipment,
    ShipFromAddress,
    ShipToAddress,
    Package,
    PackageWeight,
    PackageDimensions,
)

load_dotenv()

"""
This script allows for fast label creation, given identical labels.
Setup will require the following:
-Install modules listed above
-Fill out the Globals table below 
-Create a folder on your desktop, with a number of sub-folders equal to the number of threads you would like to process.
--Add folder path to downloadPdf function
--Sub-folders should be named alphabetically (A, B, C, etc) to easily work with the multiple threads.
-If you want to enable Saturday Delivery, add the following between carrier_id and ship_to: 'advanced_options':{'saturday_delivery':'true'},
-If you do not want to use return services, remove the following text from data: ,'is_return_label': true
-Set range in create label for the total number of labels you would like to produce divided by the number of threads you are running.
"""
# Globals
host = os.getenv("SHIPENGINE_BASE_URL")
# Use api-key with TEST key from your account for test processing
headers = {
    "api-key": os.getenv("SHIPENGINE_API_KEY"),
    "Content-Type": "application/json",
}
carrierId = os.getenv("CARRIER_ID")  # replace with TEST carrier_id if necessary
serviceCode = os.getenv(
    "SERVICE_CODE"
)  # Get a list of service codes by making a GET request to /v1/carriers
totalWeight = os.getenv("TOTAL_WEIGHT")
weightUnit = os.getenv("WEIGHT_UNIT")
shipToName = os.getenv("SHIP_TO_NAME")
shipToCompany = os.getenv("SHIP_TO_COMPANY")
shipToAddress1 = os.getenv("SHIP_TO_ADDRESS_1")
shipToAddress2 = os.getenv("SHIP_TO_ADDRESS_2")
shipToCity = os.getenv("SHIP_TO_CITY")
shipToState = os.getenv("SHIP_TO_STATE")
shipToZip = os.getenv("SHIP_TO_ZIP")
shipToPhone = os.getenv("SHIP_TO_PHONE")
shipFromName = os.getenv("SHIP_FROM_NAME")
shipFromCompany = os.getenv("SHIP_FROM_COMPANY")
shipFromAddress1 = os.getenv("SHIP_FROM_ADDRESS_1")
shipFromAddress2 = os.getenv("SHIP_FROM_ADDRESS_2")
shipFromCity = os.getenv("SHIP_FROM_CITY")
shipFromState = os.getenv("SHIP_FROM_STATE")
shipFromZip = os.getenv("SHIP_FROM_ZIP")
shipFromPhone = os.getenv("SHIP_FROM_PHONE")
dt = datetime.datetime.now()
CURRENT_DATE = dt.strftime("%m/%d/%Y")


async def main():
    # add createLabel calls to improve processing time.
    # Found 5 threads running in parallel best for 200 requests per minute.
    # If API limit is adjusted, add 5 threads per 200 rpm
    await asyncio.gather(
        createLabel(0, "label_thread_A/"),
        createLabel(1, "label_thread_B/"),
        createLabel(2, "label_thread_C/"),
        createLabel(3, "label_thread_D/"),
        createLabel(4, "label_thread_E/"),
        createLabel(5, "label_thread_F/"),
        createLabel(6, "label_thread_G/"),
        createLabel(7, "label_thread_H/"),
        createLabel(8, "label_thread_I/"),
        createLabel(9, "label_thread_J/"),
        createLabel(10, "label_thread_K/"),
        createLabel(11, "label_thread_L/"),
        createLabel(12, "label_thread_M/"),
        createLabel(13, "label_thread_N/"),
        createLabel(14, "label_thread_O/"),
        createLabel(15, "label_thread_P/"),
    )


async def createLabel(y, folder):
    print(f"started at {time.strftime('%X')}")
    # range should be # of threads / # of labels
    for x in range(0, int(os.getenv("HOW_MANY_LABELS_I_NEED"))):
        # Modify Globals to change shipment information
        packageDimensions = PackageDimensions()

        pacakgeWeight = PackageWeight(value=float(totalWeight), unit=weightUnit)

        packages_to_ship = Package(weight=pacakgeWeight, dimensions=packageDimensions)

        shipTo = ShipToAddress(
            name=shipToName,
            phone=shipToPhone,
            company_name=shipToCompany,
            address_line1=shipToAddress1,
            address_line2=shipToAddress2,
            city_locality=shipToCity,
            state_province=shipToState,
            postal_code=shipToZip,
            country_code="US",
        )

        shipFrom = ShipFromAddress(
            name=shipFromName,
            phone=shipFromPhone,
            company_name=shipFromCompany,
            address_line1=shipFromAddress1,
            address_line2=shipFromAddress2,
            city_locality=shipFromCity,
            state_province=shipFromState,
            postal_code=shipFromZip,
            country_code="US",
        )

        shipment = Shipment(
            carrier_id=carrierId,
            service_code=serviceCode,
            ship_date=CURRENT_DATE,
            ship_to=shipTo,
            ship_from=shipFrom,
            packages=[packages_to_ship],
        )
        new_data = j.dumps(
            {
                "is_return_label": "true",
                "charge_event": "on_carrier_acceptance",
                "shipment": dataclasses.asdict(shipment),
                "rma_number": os.getenv("RMA_NUMBER"),
            },
            indent=2,
        )
        labelUrl = host + "/v1/labels/"
        r = await post(labelUrl, headers=headers, data=new_data)
        response = r.json()
        jResponse = j.dumps(response, indent=2)
        # Uncomment the following line to print request data for quick debugging
        # print(jResponse)
        data = j.loads(jResponse, parse_int=str)
        status = r.status_code
        if status == 200:
            downloadUrl = data["label_download"]["pdf"]
            print(f"{x + 1}.) label created")
            try:
                await downloadPdf(str(x + 1), downloadUrl, folder)
            except:
                print("PDF could not be printed.")
        elif status == 429:
            sleep_seconds = 90
            print(
                f"LABEL_PROCESS_THROTTLED: Process #{x} -- waiting {sleep_seconds} seconds to retry..."
            )
            time.sleep(sleep_seconds)
        else:
            print(f"Label Number: {x + 1} failed:\n {jResponse}")


async def downloadPdf(fileName, downloadUrl, folder):
    r = await get(downloadUrl)
    filePath = "./labels/" + folder
    fileName = fileName + ".pdf"
    completeName = os.path.join(filePath, fileName)
    with open(completeName, "wb") as f:
        f.write(r.content)


asyncio.run(main())
