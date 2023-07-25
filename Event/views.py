from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from Event.models import Contact, Event, Timetable,TeleId
from datetime import datetime, timedelta
import pickle
from Event.task import schedule
# Create your views here.

# Home view starts here..


def Home(request):
    # Showing First 5 Reminder and Timetable
    remind = Event.objects.order_by("date").filter(username=request.user)
    tt = Timetable.objects.filter(username=request.user).first()

    if tt is not None:
        time = pickle.loads(eval(tt.time))
        topic = pickle.loads(eval(tt.topic))
        param = {"remind": remind[:5], "timetable": zip(time[:5], topic[:5])}

    else:
        param = {"remind": remind[:5]}

    return render(request, "home.html", param)

# Home view ends here..

# Signin view starts here..


def signin(request):
    if request.method == "POST":
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password1"]
        confirmpassword = request.POST["password2"]

        # Checking The conditions

        if len(username) > 15:
            messages.error(
                request, "Username is too Big,please choose a short one and try again....")
            return redirect("home")

        if User.objects.filter(username=username).exists():
            messages.error(
                request, "Username is already registered. Please try another one")
            return redirect("home")

        if User.objects.filter(email=email).exists():
            messages.error(request, "This Email is already registered")
            return redirect("home")

        if not username.isalnum():
            messages.error(
                request, "Username should only contain numbers and alphabets,you inserted a special characters,try again with alphabets and number....")
            return redirect("home")

        if password != confirmpassword:
            messages.error(
                request, "Password didn't match ,please fill correct password and try again.")
            return redirect("home")

        if len(password) < 8:
            messages.error(
                request, "Password must contain 8 or more charchter,try again with correct syntaxs.")
            return redirect("home")
        # Creating a user

        myuser = User.objects.create_user(username, email, password)
        myuser.username = username
        myuser.first_name = fname
        myuser.last_name = lname
        telegramid = TeleId(username=myuser.username)
        telegramid.save()
        myuser.save()
        messages.info(
            request, "Your account has been successfully created,Check your mail for more detail about the site working...")
        user = authenticate(username=myuser.username, password=password)
        login(request, user)
        send_mail(
            subject="Account-Created",
            message= "",
            from_email="jha.dhiraj22803@gmail.com",
            recipient_list=[f"{request.user.email}"],
            fail_silently=True,
            html_message=f"""<p>Dear {request.user.username},</p><p>We are delighted to inform you that your Timetable account has been successfully created! You can now commence creating your Reminders and Timetables on our website. Our goal is to ensure that you never miss an important event, and we will promptly remind you of your scheduled reminders at the specified times. Reminder messages will be sent to this email address.</p><p>For added convenience, if you wish to receive reminder messages on Telegram, kindly follow these simple steps:</p><ol><li>Open Telegram.</li><li>Search for MyMartian_bot.</li><li>Click on the "start" button and type your username {request.user.username}.</li><li>Create a demo reminder on our site.</li></ol><p>Once you receive a message from our bot, you are all set to go! Just Login Again and Our bot will faithfully remind you of all your scheduled reminders on time. Should you have any queries or require further assistance, please do not hesitate to contact us via our website.</p><p>We hope you enjoy using our services and find them highly beneficial.</p><p>Best regards,</p><p>Team Timetable</p><p> Click to open <a href='https://t.me/MyMartian_bot'>MyMartian_bot</a> </p>""")
        return redirect("home")

    else:
        return HttpResponse("404 - Page not Found")


def loginuser(request):

    if request.method == "POST":
        loginusername = request.POST["loginusername"]
        loginpassword = request.POST["loginpassword"]

        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            # send_mail(
            #     "Login on TimeTable",
            #     f"Dear {user.username},you are logged in on TimeTable,thanks for choosing us.You can now start using our services.\nThank you,\nTeam TimeTable.",
            #     "jha.dhiraj22803@gmail.com",
            #     [f"{user.email}"],
            #     fail_silently=True
            # )
            login(request, user)
            messages.success(request, "You are successfully logged in.")
            return redirect("home")
        else:
            messages.error(
                request, "Please enter correct Username and Password to login")
            return redirect("home")

    return HttpResponse("404 - Page not Found")


def logoutuser(request):
    # send_mail(
    #     "Logout from TimeTable",
    #     f"Dear {request.user.username},you are logged out from TimeTable,Login again to start using our services.\nThank you,\nTeam TimeTable.",
    #     "jha.dhiraj22803@gmail.com",
    #     [f"{request.user.email}"],
    #     fail_silently=True
    # )
    logout(request)
    messages.success(request, " You are successfully logged out.")
    return redirect("home")


def contact(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        tele = request.POST["tele"]
        content = request.POST["content"]
        contact = Contact(name=name, email=email, tele=tele, content=content)
        messages.success(
            request, " Thanks for reaching us,we will soon give you a response about your issue.")
        contact.save()
        return redirect("contact")

    return render(request, "contact.html")


def timetable(request):
    times = []
    topics = []
    if request.method == "POST":
        hidden = request.POST["hidden"]
        timelist = ["time"]
        topiclist = ["topic"]
        if int(hidden) == 0:
            pass
        else:
            for i in range(1, int(hidden)+1):
                timelist.append("time"+str(i))
                topiclist.append("topic"+str(i))

        for i in range(0, len(timelist)):
            time = request.POST[timelist[i]]
            topic = request.POST[topiclist[i]]
            times.append(time)
            topics.append(topic)
        time = pickle.dumps(times)
        topic = pickle.dumps(topics)

        timetable = Timetable(username=str(request.user),
                              time=time, topic=topic)
        timetable.save()
        messages.success(request, " Your time table is successfully created")
        return redirect("home")
    username = request.user
    tt = Timetable.objects.filter(username=username).first()
    if tt is not None :
        tt_topic = eval(tt.topic)
        params = {"tt":tt_topic}
        return render(request, "timetable.html", params)
    return render(request, "timetable.html")


def reminder(request):
    if request.method == "POST":
        type = request.POST["type"]
        date = request.POST["date"]
        time = request.POST["time"]
        event = request.POST["event"]
        Events = Event(username=str(request.user), types=type,
                       date=date, time=time, event=event)
        Events.save()
        messages.success(request, " Your reminder is created..")
        val = User.objects.filter(username=request.user, id=0)
        if len(val) == 0:
            messages.info(request, " Make sure to send your username to our bot Martian on telegram to start reciving reminder messages on telegram.If you have recived the message of bot 'Your telegram id is recorded,you will recive messages of Your reminder here' you need not send again.\nThank You")
        send_notification(request, Events)
        return redirect("reminder")

    return render(request, "reminder.html")


def reminderhome(request):
    username = request.user
    current_date = datetime.today()
    event = Event.objects.filter(username=username)
    dates = []
    date_10min = []
    for i in event.iterator():
        date = datetime.combine(i.date, i.time)
        dates.append(date)
        date_10 = date + timedelta(minutes=5) # - timedelta(hours=5,minutes=35)
        date_10min.append(date_10)

    for i in range(len(dates)):
        check_date = date_10min[i]
        actual_date = dates[i]
        if current_date > check_date:
            delete = Event.objects.filter(username=username, date=str(
                (actual_date.date())), time=str(actual_date.time()))
            delete.delete()

    regular = Event.objects.order_by("date").filter(username=username, types=1)
    important = Event.objects.order_by(
        "date").filter(username=username, types=2)
    special = Event.objects.order_by("date").filter(username=username, types=3)
    parms = {"regular": regular, "important": important, "special": special}
    return render(request, "reminderhome.html", parms)


def timetablehome(request):
    username = request.user
    tt = Timetable.objects.filter(username=username).first()
    if tt is not None:
        time = pickle.loads(eval(tt.time))
        topic = pickle.loads(eval(tt.topic))
        param = {"timetable": zip(time, topic)}
        return render(request, "timetablehome.html", param)
    else:
        return render(request, "example.html")


def delete(request):
    username = request.user
    Timetable.objects.filter(username=username).delete()
    messages.success(request, "Your timetable is Sucessfully deleted!!")
    return redirect("home")


def send_notification(request, event):
    dates = event.date[2:] + " " + event.time + ":00"
    send_date_time = datetime.strptime(dates, "%y-%m-%d %H:%M:%S")
    send_date = send_date_time.date()
    send_time = send_date_time.time()
    current_date_time = datetime.now()
    current_time = current_date_time.time()
    current_date = current_date_time.date()
    datetime1 = datetime.combine(send_date, send_time) # - timedelta(hours=5,minutes=30)
    datetime2 = datetime.combine(current_date, current_time)
    times_ = datetime1 - datetime2
    num = times_.total_seconds()
    user = request.user.username
    tele_id = TeleId.objects.get(username=user)
    reciver_id = tele_id.teleid
    num_message = tele_id.num_mes
    schedule(num, user, event.event, reciver_id,num_message)

