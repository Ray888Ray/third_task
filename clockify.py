import requests
import json
from datetime import datetime

workspace_id = '648b6ba2120abb5b98c51126'
api_key = 'ZWVlYzcwMGEtYmE0Zi00MjRhLTlhNDgtOGFkZDVhY2Y2ODEz'


def calculate_hours_worked(api_key, workspace_id):
    headers = {"Content-Type": "application/json", "X-Api-Key": api_key}

    rates_url = f"https://api.clockify.me/api/v1/workspaces/{workspace_id}/projects"
    rates_response = requests.get(rates_url, headers=headers)
    rates_data = json.loads(rates_response.text)

    hourly_rates = {}
    for project in rates_data:
        memberships = project["memberships"]
        for membership in memberships:
            user_id = membership["userId"]
            hourly_rate = membership["hourlyRate"]["amount"]
            hourly_rates[user_id] = hourly_rate

    API_URL = f"https://api.clockify.me/api/v1/workspaces/{workspace_id}/users"
    response = requests.get(API_URL, headers=headers)
    users = json.loads(response.text)
    start_time = (datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)).isoformat() + "Z"
    end_time = (datetime.now().replace(day=20, hour=23, minute=59, second=59, microsecond=999)).isoformat() + "Z"

    task_with_highest_time = {}
    hours_worked = {}

    for user in users:
        user_id = user["id"]
        user_name = user["name"]

        if user_id in hourly_rates:
            hourly_rate = hourly_rates[user_id]
            currency = "USD"
        else:
            hourly_rate = 50
            currency = "USD"

        API_URL = f"https://api.clockify.me/api/v1/workspaces/{workspace_id}/user/{user_id}/time-entries"
        params = {"start": start_time, "end": end_time}
        response = requests.get(API_URL, headers=headers, params=params)
        time_entries = json.loads(response.text)

        task_hours = {}
        total_hours = 0

        for entry in time_entries:
            time_interval = entry.get("timeInterval")
            if time_interval and time_interval.get("end") is not None:
                start = datetime.fromisoformat(time_interval["start"][:-1])
                end = datetime.fromisoformat(time_interval["end"][:-1])
                duration = end - start

                total_hours += duration.total_seconds() / 3600

                task_name = entry["description"]
                if task_name in task_hours:
                    task_hours[task_name] += duration.total_seconds() / 3600
                else:
                    task_hours[task_name] = duration.total_seconds() / 3600

        if task_hours:
            max_task_name = max(task_hours, key=task_hours.get)
            max_task_hours = task_hours[max_task_name]
            task_with_highest_time[user_name] = {"task_name": max_task_name, "hours": max_task_hours}
            hours_worked[user_name] = {
                "total": total_hours,
                "hourly_rate": hourly_rate,
                "currency": currency,
                "total_amount": total_hours * hourly_rate
            }

    return task_with_highest_time, hours_worked


task_with_highest_time, hours_worked = calculate_hours_worked(api_key, workspace_id)

