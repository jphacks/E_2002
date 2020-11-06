import datetime
from django.shortcuts import redirect, render
from django.views import generic
from .forms import BS4ScheduleForm, SimpleScheduleForm
from .models import Schedule
from . import mixins
import json
from django.views import View
from dateutil.relativedelta import relativedelta

class MonthCalendar(mixins.MonthCalendarMixin, generic.TemplateView):
    """月間カレンダーを表示するビュー"""
    template_name = 'wakeup/month.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context


class WeekCalendar(mixins.WeekCalendarMixin, generic.TemplateView):
    """週間カレンダーを表示するビュー"""
    template_name = 'wakeup/week.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_week_calendar()
        context.update(calendar_context)
        return context


class WeekWithScheduleCalendar(mixins.WeekWithScheduleMixin, generic.TemplateView):
    """スケジュール付きの週間カレンダーを表示するビュー"""
    template_name = 'wakeup/week_with_schedule.html'
    model = Schedule
    date_field = 'date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_week_calendar()
        context.update(calendar_context)
        return context


class MonthWithScheduleCalendar(mixins.MonthWithScheduleMixin, generic.TemplateView):
    """スケジュール付きの月間カレンダーを表示するビュー"""
    template_name = 'wakeup/month_with_schedule.html'
    model = Schedule
    date_field = 'date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context


class MyCalendar(mixins.MonthCalendarMixin, mixins.WeekWithScheduleMixin, generic.CreateView):
    """月間カレンダー、週間カレンダー、スケジュール登録画面のある欲張りビュー"""
    template_name = 'wakeup/mycalendar.html'
    model = Schedule
    date_field = 'date'
    form_class = BS4ScheduleForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        week_calendar_context = self.get_week_calendar()
        month_calendar_context = self.get_month_calendar()
        context.update(week_calendar_context)
        context.update(month_calendar_context)
        return context

    def form_valid(self, form):
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        if month and year and day:
            date = datetime.date(year=int(year), month=int(month), day=int(day))
        else:
            date = datetime.date.today()
        schedule = form.save(commit=False)
        schedule.date = date
        schedule.save()
        return redirect('wakeup:mycalendar', year=date.year, month=date.month, day=date.day)


class MonthWithFormsCalendar(mixins.MonthWithFormsMixin, generic.View):
    """フォーム付きの月間カレンダーを表示するビュー"""
    template_name = 'wakeup/month_with_forms.html'
    model = Schedule
    date_field = 'date'
    form_class = SimpleScheduleForm

    def get(self, request, **kwargs):
        context = self.get_month_calendar()
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        context = self.get_month_calendar()
        formset = context['month_formset']
        if formset.is_valid():
            formset.save()
            data = [[x.start_time,x.date] for x in Schedule.objects.all()]
            return redirect('wakeup:month_with_forms')

        return render(request, self.template_name, context)

# Create your views here.
class TopView(View):
    def get(self, request, *args, **kwargs):
        json_open = open('wakeup/options.json', 'r')
        json_load = json.load(json_open)
        now_date =datetime.datetime.now()
        context = self.get_context_data(now_date,json_load['absolute_or_relative'], json_load['day_week_month'])

        return render(request, 'wakeup/top.html', context)

    def post(self, request, *args, **kwargs):
        standard_date = datetime.datetime.strptime(request.POST.get('standard_date',""), '%Y--%m--%d/')
        abs_or_rela = request.POST.get('absolute_or_relative',"relative").translate(request.POST.get('absolute_or_relative',"relative").maketrans({'/': ''}))
        dwm = request.POST.get('day_week_month',"day").translate(request.POST.get('day_week_month',"day").maketrans({'/': ''}))
        #print(request.POST)
        #print('month_button' in request.POST)
        if 'absolute' in request.POST.get('ab_or_re',""):
            context = self.get_context_data(standard_date, "absolute", dwm)
        elif 'relative' in request.POST.get('ab_or_re',""):
            context = self.get_context_data(standard_date, "relative", dwm)
        if 'day_button' in request.POST:
            context = self.get_context_data(standard_date, abs_or_rela, 'day')
        elif 'week_button' in request.POST:
            context = self.get_context_data(standard_date, abs_or_rela, 'week')
        elif 'month_button' in request.POST:
            context = self.get_context_data(standard_date, abs_or_rela, 'month')
        elif 'next_button' in request.POST:
            if 'day' in request.POST.get('day_week_month',""):
                standard_date =  standard_date + relativedelta(days=10)
            elif 'week' in request.POST.get('day_week_month',""):
                standard_date =  standard_date + relativedelta(weeks=10)
            elif 'month' in request.POST.get('day_week_month',""):
                standard_date =  standard_date + relativedelta(months=10)
            context = self.get_context_data(standard_date, abs_or_rela, dwm)
        elif 'before_button' in request.POST:
            if 'day' in request.POST.get('day_week_month',""):
                standard_date =  standard_date - relativedelta(days=10)
            elif 'week' in request.POST.get('day_week_month',""):
                standard_date =  standard_date - relativedelta(weeks=10)
            elif 'month' in request.POST.get('day_week_month',""):
                standard_date =  standard_date - relativedelta(months=10)
            context = self.get_context_data(standard_date, abs_or_rela, dwm)

        #print(context)
        with open('wakeup/options.json', 'w') as f:
            json.dump(context, f, indent=4)
        #print(context)

        return render(request, 'wakeup/top.html', context)

    def get_context_data(self,standard_date,absolute_or_relative,day_week_month):
        y_data = []
        ideal_times = []
        max_score = 0
        min_score = 0
        #print(day_week_month)
        if day_week_month=='day':
            xlabel_name = [str((standard_date - datetime.timedelta(days=i)).month) + '/'
                        + str((standard_date - datetime.timedelta(days=i)).day) for i in reversed(range(10))]
            date_name = [Schedule.objects.filter(date=datetime.datetime((standard_date - datetime.timedelta(days=i)).year,\
            (standard_date - datetime.timedelta(days=i)).month,(standard_date - datetime.timedelta(days=i)).day)) for i in reversed(range(10))]
            for query_set in date_name:
                if absolute_or_relative == 'absolute':
                    if len(query_set)==0:
                        y_data.append("")
                        ideal_times.append("")
                    else:
                        #print(query_set[0].end_time)
                        try:
                            absolute_time = query_set[0].end_time.hour * 60 + query_set[0].end_time.minute
                            y_data.append(absolute_time)
                            ideal_score = query_set[0].start_time.hour * 60 + query_set[0].start_time.minute
                            ideal_times.append(ideal_score)
                            if min_score == 0:
                                min_score =absolute_time
                            if max_score < absolute_time:
                                max_score = absolute_time
                            elif min_score > absolute_time:
                                min_score = absolute_time
                            if max_score < ideal_score:
                                max_score = ideal_score
                            elif min_score > ideal_score:
                                min_score = ideal_score
                        except :
                            y_data.append("")
                            ideal_times.append("")


                else:
                    ideal_times.append(0)
                    if len(query_set)==0:
                        y_data.append("")
                    else:
                        week_score = []
                        for week_query in query_set:
                            try:
                                relative_time =int((datetime.datetime.strptime(str(week_query.end_time),"%H:%M:%S") - \
                                                    datetime.datetime.strptime(str(week_query.start_time),"%H:%M:%S")).total_seconds())
                                relative_time = int(relative_time/60)
                                week_score.append(relative_time)
                            except:
                                pass
                        if len(week_score)!=0:
                            average_score = sum(week_score)//len(week_score)
                        else:
                            average_score = 0

                        if min_score > average_score:
                            min_score = average_score
                        elif max_score < average_score:
                            max_score = average_score
                        y_data.append(average_score)


        elif day_week_month=='week':
            xlabel_name = [str((standard_date - datetime.timedelta(weeks=i)).month) + '/'  \
                        + str((standard_date - datetime.timedelta(weeks=i)).day) for i in reversed(range(10))]
            date_name = [Schedule.objects.filter(date__range=[datetime.datetime((standard_date - datetime.timedelta(days=6,weeks=i)).year,\
                        (standard_date - datetime.timedelta(days=6,weeks=i)).month,(standard_date - datetime.timedelta(days=6,weeks=i)).day),\
                        datetime.datetime((standard_date - datetime.timedelta(days=-1,weeks=i)).year,\
                        (standard_date - datetime.timedelta(days=-1,weeks=i)).month,(standard_date - datetime.timedelta(days=-1,weeks=i)).day)]) for i in reversed(range(10))]

            for query_set in date_name:
                if absolute_or_relative == 'absolute':
                    if len(query_set)==0:
                        y_data.append("")
                        ideal_times.append("")
                    else:
                        #print(query_set[0].end_time)
                        try:
                            absolute_time = query_set[0].end_time.hour * 60 + query_set[0].end_time.minute
                            y_data.append(absolute_time)
                            ideal_score = query_set[0].start_time.hour * 60 + query_set[0].start_time.minute
                            ideal_times.append(ideal_score)
                            if min_score == 0:
                                min_score =absolute_time
                            if max_score < absolute_time:
                                max_score = absolute_time
                            elif min_score > absolute_time:
                                min_score = absolute_time
                            if max_score < ideal_score:
                                max_score = ideal_score
                            elif min_score > ideal_score:
                                min_score = ideal_score
                        except:
                            y_data.append("")
                            ideal_times.append("")
                else:
                    #print(query_set)
                    ideal_times.append(0)
                    if len(query_set)==0:
                        y_data.append("")
                    else:
                        week_score = []
                        for week_query in query_set:
                            try:
                                relative_time =int((datetime.datetime.strptime(str(week_query.end_time),"%H:%M:%S") - \
                                                    datetime.datetime.strptime(str(week_query.start_time),"%H:%M:%S")).total_seconds())
                                relative_time = int(relative_time/60)
                                week_score.append(relative_time)
                            except:
                                pass
                        if len(week_score)!=0:
                            average_score = sum(week_score)//len(week_score)
                        else:
                            average_score = 0
                        if min_score > average_score:
                            min_score = average_score
                        elif max_score < average_score:
                            max_score = average_score
                        y_data.append(average_score)
        else:
            xlabel_name = [str((standard_date - relativedelta(months=i)).month) + '月' for i in reversed(range(10))]
            date_name = [Schedule.objects.filter(date__year=str((standard_date - relativedelta(months=i)).year),date__month=str((standard_date - relativedelta(months=i)).month)) for i in reversed(range(10))]
            for query_set in date_name:
                if absolute_or_relative == 'absolute':
                    if len(query_set)==0:
                        y_data.append("")
                        ideal_times.append("")
                    else:
                        try:
                            absolute_time = query_set[0].end_time.hour * 60 + query_set[0].end_time.minute
                            y_data.append(absolute_time)
                            ideal_score = query_set[0].start_time.hour * 60 + query_set[0].start_time.minute
                            ideal_times.append(ideal_score)
                            if min_score == 0:
                                min_score =absolute_time
                            if max_score < absolute_time:
                                max_score = absolute_time
                            elif min_score > absolute_time:
                                min_score = absolute_time
                            if max_score < ideal_score:
                                max_score = ideal_score
                            elif min_score > ideal_score:
                                min_score = ideal_score
                        except:
                            y_data.append("")
                            ideal_times.append("")
                else:
                    ideal_times.append(0)
                    if len(query_set)==0:
                        y_data.append("")
                    else:
                        week_score = []
                        for week_query in query_set:
                            try:
                                relative_time =int((datetime.datetime.strptime(str(week_query.end_time),"%H:%M:%S") - \
                                                    datetime.datetime.strptime(str(week_query.start_time),"%H:%M:%S")).total_seconds())
                                relative_time = int(relative_time/60)
                                week_score.append(relative_time)
                            except:
                                pass
                        if len(week_score)!=0:
                            average_score = sum(week_score)//len(week_score)
                        else:
                            average_score = 0
                        if min_score > average_score:
                            min_score = average_score
                        elif max_score < average_score:
                            max_score = average_score
                        y_data.append(average_score)

        context = {
                'xlabels': xlabel_name,
                'Y_data':y_data,
                'ideal':ideal_times,
                'max_score':max_score//10*10+60,
                'min_score':min_score//10*10-60,
                'absolute_or_relative': absolute_or_relative,
                'day_week_month':day_week_month,
                'standard_date':standard_date.strftime('%Y--%m--%d'),
        }
        return context



class HowToView(View):
    def get(self, request, *args, **kwargs):
        json_open = open('wakeup/how_to_options.json', 'r')
        context = json.load(json_open)
        print(context)
        return render(request, 'wakeup/howto.html/', context)

    def post(self, request, *args, **kwargs):

        json_open = open('wakeup/how_to_options.json', 'r')
        json_load = json.load(json_open)
        context = {
            'default_alarm': request.POST.get('default_alarm',"off"),
            'all_switch':request.POST.get('all_switch','off') ,
            'all_time':request.POST.get('all_time',json_load['all_time']),
            'holiday_switch':request.POST.get('holiday_switch',"off"),
            'holiday_time':request.POST.get('holiday_time',json_load['holiday_time']),
            'weekdays_switch':request.POST.get('weekdays_switch',"off"),
            'weekdays_time':request.POST.get('weekdays_time',json_load['weekdays_time']),
            'day_of_the_week':request.POST.get('day_of_the_week',"off"),
            'sunday_switch':request.POST.get('sunday_switch',"off"),
            'sunday_time':request.POST.get('sunday_time',json_load['sunday_time']),
            'monday_switch':request.POST.get('monday_switch',"off"),
            'monday_time':request.POST.get('monday_time',json_load['monday_time']),
            'tuesday_switch':request.POST.get('tuesday_switch',"off"),
            'tuesday_time':request.POST.get('tuesday_time',json_load['tuesday_time']),
            'wednesday_switch':request.POST.get('wednesday_switch',"off"),
            'wednesday_time':request.POST.get('wednesday_time',json_load['wednesday_time']),
            'thursday_switch':request.POST.get('thursday_switch',"off"),
            'thursday_time':request.POST.get('thursday_time',json_load['thursday_time']),
            'friday_switch':request.POST.get('friday_switch',"off"),
            'friday_time':request.POST.get('friday_time',json_load['friday_time']),
            'saturday_switch':request.POST.get('saturday_switch',"off"),
            'saturday_time':request.POST.get('saturday_time',json_load['saturday_time']),
            'use_servo':request.POST.get('use_servo',"off"),
            'use_sound':request.POST.get('use_sound',"off"),
        }
        with open('wakeup/how_to_options.json', 'w') as f:
            json.dump(context, f, indent=4)
        return render(request, 'wakeup/howto.html/', context)
top = TopView.as_view()
howto = HowToView.as_view()
