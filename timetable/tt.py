from flask import Flask, render_template, request
import datetime

app = Flask(__name__)

def get_college_hours():
    start_time = request.form.get("start_time")
    end_time = request.form.get("end_time")

    try:
        start_time_obj = datetime.datetime.strptime(start_time, "%I:%M %p")
        end_time_obj = datetime.datetime.strptime(end_time, "%I:%M %p")

        if start_time_obj >= end_time_obj:
            return "End time should be after start time. Please enter valid times."

        return start_time_obj, end_time_obj
    except ValueError:
        return "Invalid input. Please enter time in HH:MM AM/PM format."
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        subjects = []
        durations = []
        tot_classes = []

        num_subjects = int(request.form['num_subjects'])

        for i in range(num_subjects):
            subjects.append(request.form[f"subject_{i+1}"])
            durations.append(int(request.form[f"duration_{i+1}"]))
            tot_classes.append(int(request.form[f"total_classes_{i+1}"]))

        start_time, end_time = get_college_hours()
        break_time = 60 * 2  # Break after every 2 hours
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

        timetable = {day: [] for day in days_of_week}

        for day in days_of_week:
            current_time = start_time
            scheduled_subjects = set()
            for i in range(num_subjects):
                if tot_classes[i] > 0 and subjects[i] not in scheduled_subjects:
                    timetable[day].append((current_time, current_time + datetime.timedelta(minutes=durations[i]), subjects[i]))
                    current_time += datetime.timedelta(minutes=durations[i])
                    scheduled_subjects.add(subjects[i])
                    tot_classes[i] -= 1

                if current_time + datetime.timedelta(minutes=break_time) <= end_time:
                    timetable[day].append((current_time, current_time + datetime.timedelta(minutes=break_time), "Break"))
                    current_time += datetime.timedelta(minutes=break_time)

        return render_template('timetable.html', timetable=timetable)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
