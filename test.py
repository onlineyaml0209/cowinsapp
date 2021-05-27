import requests
import json

from datetime import datetime, timedelta
import time


age = 18

pinCodes = ["380006","380001","380059","380026","380005","380016","380013","380019","382445","382424","380024","380023","380004","382443","380022","382340","380061","382415","380058","382475",
"380052","382440","382480","380007","380055","382345","380015","380008","382210","380060","380021","380028","380051","382405","382330","380009","382481","380018","382350","382418","380026","380054",
"380050"]

# Print details flag
print_flag = 'Y'


numdays = 2

base = datetime.today()
date_list = [base + timedelta(days=x) for x in range(numdays)]
date_str = [x.strftime("%d-%m-%Y") for x in date_list]

while 1:

    count = 0
    msg=[]
    print("Started...")

    for pinCode in pinCodes:   
        print(pinCode) 
        for INP_DATE in date_str:
            print("\t", INP_DATE)
            URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(pinCode, INP_DATE)
            #print(URL);
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} # This is chrome, you can set whatever browser you like
            #print(headers)
            response = requests.get( URL, headers=headers )
            #print(response)
           
            if response.ok:
                resp_json = response.json()
               
                flag = False
                if resp_json["centers"]:            
                    if(print_flag=='y' or print_flag=='Y'):
                        
                        for center in resp_json["centers"]:
                            
                            #print(center)
                            for session in center["sessions"]:
                                if (session["min_age_limit"] <= age and session["available_capacity"] > 0 ) :
                                    print(pinCode)
                                    print("Available on: {}".format(INP_DATE))
                                    print("\t\t", center["name"])
                                    print("\t\t", center["block_name"])
                                    print("\t\t Price: ", center["fee_type"])
                                    print("\t\t Available Capacity: ", session["available_capacity"])
                                    if(session["vaccine"] != ''):
                                        print("\t\t Vaccine: ", session["vaccine"])
                                    print("\n")
                                    msg.append({"Date":session["date"],"CenterName":center["name"],"Pincode":center["pincode"],"Dose1️":session["available_capacity_dose1"],"Dose2️":session["available_capacity_dose2"],"VaccineType":session["vaccine"],"Price":center["fee_type"]})
                                    parse_data=json.dumps(msg)
                                    parse_data=parse_data.replace("{","")
                                    parse_data=parse_data.replace("}","\n\n")
                                    parse_data=parse_data.replace("[","")
                                    parse_data=parse_data.replace("]","")
                                    parse_data=parse_data.replace(",","\n")
                                    count = count + 1
                                    nd_url="https://api.telegram.org/bot1694634587:AAGbUbeLMUtXkVq1oKJK22YsXHyUCLFBErI/sendMessage?chat_id=-1001374032082&text="+parse_data
                                    y=requests.get(nd_url)
                                    
                                else:
                                    b = 25
                                    
                else:
                    a = 25
                   
            else:
                print("No Response")
    if(count == 0):
        print("No Vaccination center avaliable.")
    else:
        print("Sending Email")

        
    print("Completed...")
    print("..................................................")
    print("..................................................")

    dt = datetime.now() + timedelta(minutes=3)
    #dt = dt.replace(minute=1)

    while datetime.now() < dt:

        time.sleep(1)