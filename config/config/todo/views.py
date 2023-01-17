import time
import datetime
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import AccountForm, AddAccountForm, BS4ScheduleForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Todo, Schedule

from django.views import generic
from . import mixins

class  AccountRegistration(TemplateView):

    def __init__(self):
        self.params = {
        "AccountCreate":False,
        "account_form": AccountForm(),
        "add_account_form":AddAccountForm(),
        }

    # Get処理
    def get(self,request):
        self.params["account_form"] = AccountForm()
        self.params["add_account_form"] = AddAccountForm()
        self.params["AccountCreate"] = False
        return render(request,"todo/register.html",context=self.params)

    # Post処理
    def post(self,request):
        self.params["account_form"] = AccountForm(data=request.POST)
        self.params["add_account_form"] = AddAccountForm(data=request.POST)

        # フォーム入力の有効検証
        if self.params["account_form"].is_valid() and self.params["add_account_form"].is_valid():
            # アカウント情報をDB保存
            account = self.params["account_form"].save()
            # パスワードをハッシュ化
            account.set_password(account.password)
            # ハッシュ化パスワード更新
            account.save()

            # 下記追加情報
            # 下記操作のため、コミットなし
            add_account = self.params["add_account_form"].save(commit=False)
            # AccountForm & AddAccountForm 1vs1 紐付け
            add_account.user = account

            # 画像アップロード有無検証
            if 'account_image' in request.FILES:
                add_account.account_image = request.FILES['account_image']

            # モデル保存
            add_account.save()

            # アカウント作成情報更新
            self.params["AccountCreate"] = True

        else:
            # フォームが有効でない場合
            print(self.params["account_form"].errors)

        return render(request,"todo/register.html",context=self.params)


#ログイン
def Login(request):
    # POST
    if request.method == 'POST':
        # フォーム入力のユーザーID・パスワード取得
        ID = request.POST.get('userid')
        Pass = request.POST.get('password')

        # Djangoの認証機能
        user = authenticate(username=ID, password=Pass)

        # ユーザー認証
        if user:
            #ユーザーアクティベート判定
            if user.is_active:
                # ログイン
                login(request,user)
                # ホームページ遷移
                return HttpResponseRedirect(reverse('mycalendar'))
            else:
                # アカウント利用不可
                return HttpResponse("アカウントが有効ではありません")
        # ユーザー認証失敗
        else:
            return HttpResponse("ログインIDまたはパスワードが間違っています")
    # GET
    else:
        return render(request, 'todo/login.html')


#ログアウト
@login_required
def Logout(request):
    logout(request)
    # ログイン画面遷移
    return HttpResponseRedirect(reverse('Login'))

#ホーム
@login_required
def list(request):
    params = {"UserID":request.user,}
    return render(request, "todo/mycalendar.html",context=params)


class TodoList(LoginRequiredMixin, ListView):
    model = Todo
    context_object_name = "tasks"


class TodoDetail(LoginRequiredMixin, DetailView):
    model = Todo
    context_object_name = "task"
    

class TodoCreate(LoginRequiredMixin, CreateView):
    model = Todo
    fields = "__all__"
    success_url = reverse_lazy("list")

class TodoUpdate(LoginRequiredMixin, UpdateView):
    model = Todo
    fields = "__all__"
    success_url = reverse_lazy("list")
    
class TodoDelete(LoginRequiredMixin, DeleteView):
    model = Todo
    context_object_name = "task"
    success_url = reverse_lazy("list")



class MonthCalendar(LoginRequiredMixin, mixins.MonthCalendarMixin, generic.TemplateView):
    """月間カレンダーを表示するビュー"""
    template_name = 'todo/month.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context


class WeekCalendar(LoginRequiredMixin, mixins.WeekCalendarMixin, generic.TemplateView):
    """週間カレンダーを表示するビュー"""
    template_name = 'todo/week.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_week_calendar()
        context.update(calendar_context)
        return context



class WeekWithScheduleCalendar(LoginRequiredMixin, mixins.WeekWithScheduleMixin, generic.TemplateView):
    """スケジュール付きの週間カレンダーを表示するビュー"""
    template_name = 'todo/week_with_schedule.html'
    model = Schedule
    date_field = 'date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_week_calendar()
        context.update(calendar_context)
        return context



class MonthWithScheduleCalendar(LoginRequiredMixin, mixins.MonthWithScheduleMixin, generic.TemplateView):
    """スケジュール付きの月間カレンダーを表示するビュー"""
    template_name = 'todo/month_with_schedule.html'
    model = Schedule
    date_field = 'date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context



class MyCalendar(LoginRequiredMixin, mixins.MonthCalendarMixin, mixins.WeekWithScheduleMixin, generic.CreateView):
    """月間カレンダー、週間カレンダー、スケジュール登録画面のある欲張りビュー"""
    template_name = 'todo/mycalendar.html'
    model = Schedule
    date_field = 'date'
    form_class = BS4ScheduleForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        week_calendar_context = self.get_week_calendar()
        month_calendar_context = self.get_month_calendar()
        context.update(week_calendar_context)
        context.update(month_calendar_context)

        # 選択した日付をテンプレートファイルへ渡す
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        if month and year and day:
            date = datetime.date(year=int(year), month=int(month), day=int(day))
        else:
            date = datetime.date.today()
        context['selected_date'] = date
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
        return redirect('mycalendar', year=date.year, month=date.month, day=date.day)

    def get_form_kwargs(self):
        kwgs = super().get_form_kwargs()
        kwgs["user"] = self.request.user
        return kwgs

    # この部分を追加しました
    def get_queryset(self):
        user = self.request.user
        queryset = Schedule.objects.order_by('-date').filter(user=user)
        return queryset

    

    
class ScheduleChange(LoginRequiredMixin, generic.UpdateView):
    model = Schedule
    form_class = BS4ScheduleForm
    success_url = reverse_lazy('mycalendar')
    context_object_name = "s"


class ScheduleDetail(LoginRequiredMixin, generic.DetailView):
    model = Schedule
    context_object_name = "s"


class ScheduleDelete(LoginRequiredMixin, generic.DeleteView):
    model = Schedule
    success_url = reverse_lazy('mycalendar')
    context_object_name = "s"
    
