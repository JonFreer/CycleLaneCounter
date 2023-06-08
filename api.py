import requests
import datetime
import json

class API:

    # Call and return the json from the Vivacity API
    def get_results(api_key,start_time, end_time):
        response = requests.get("https://tfwm.onl/vivacity.json?ApiKey={}&earliest={}&latest={}&Identity=40934&class=cyclist&NullDataPoints=false&to=1684840206".format(api_key,start_time,end_time))
        response.raise_for_status()
        return response.json()


    def filter_results(results: dict):

        out = {}
        records = results.get("Vivacity", {}).get("kids", {})
        
        # Iterate over values and filter out any where the Start, Centre and End values are None
        # Store the output for a given time in a dict
        for value in records.values():
            data = value["kids"]
            if not data:
                continue
            location = data.get("Location", {}).get("kids", {})
            valid_location = location and location.get("Start") is not None
            valid_location = valid_location and location.get("Centre") is not None
            valid_location = valid_location and location.get("End") is not None

            if not valid_location:
                continue

            date_string = data.get("Dates", {}).get("kids", {}).get("From")

            count = data.get("Counts", {}).get("kids", {})

            date_time = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S') # Get Unix time

            out[date_time] = count

        return out

    def aggregate_hourly(data):
        hourly_total = []
        for i in range(24):
            hourly_total.append({"In": 0, "Out": 0})

        for key, item in data.items():
            hourly_total[key.hour]["In"] = hourly_total[key.hour]["In"] + \
                int(item["In"])
            hourly_total[key.hour]["Out"] = hourly_total[key.hour]["Out"] + \
                int(item["Out"])
        return hourly_total

    def get_total(data):
        in_count, out_count = 0, 0
        for key, item in data.items():
            in_count = in_count + int(item["In"])
            out_count = out_count + int(item["Out"])
        return in_count, out_count
    
    # Output the data to json and js
    def output_data(data,date):
        with open('hourly.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        hourly_json = json.dumps(data)

        with open('hourly.js', 'w', encoding='utf-8') as f:
            f.write("hourly_data = ")
            f.write(hourly_json)
            f.write("\nday = ")
            f.write(date)



    # Get todays daily total
    def get_today(api_key):

        all_results = API.get_results(api_key,"today", "now")
        filtered_results = API.filter_results(all_results)
        hourly_total = API.aggregate_hourly(filtered_results)
     
        API.output_data(hourly_total,str(int(datetime.datetime.now().timestamp())))

        in_count, out_count = API.get_total(filtered_results)

        return in_count, out_count


    def get_yesterday(api_key):

        # Get the start time and end time as unix timestamp
        now = datetime.datetime.now()
        end = int(now.replace(hour=0, minute=0, second=0, microsecond=0).timestamp())
        start = end - (24*60*60)

        all_results = API.get_results(api_key,start, end)
        filtered_results = API.filter_results(all_results)
        hourly_total = API.aggregate_hourly(filtered_results)

        API.output_data(hourly_total,str(int(datetime.datetime.now().timestamp()) - (24*60*60)))

        in_count, out_count = API.get_total(filtered_results)

        return in_count, out_count
