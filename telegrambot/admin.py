from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import TelegramUser, TelegramBalance


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('get_formatted_info', 'user_id', 'created_at')
    list_filter = ('is_bot', 'created_at')
    search_fields = ('user_id', 'username', 'first_name', 'last_name')

    fieldsets = (
        (None, {
            'fields': ('user_id', 'is_bot', 'language_code'),
        }),
        ('User Information', {
            'fields': ('username', 'first_name', 'last_name'),
            'classes': ('collapse',),
        }),
    )

    def get_formatted_info(self, obj):
        info = (
            f"<div style='background-color: #f8f9fa; padding: 10px; border-radius: 5px; "
            f"box-shadow: 0 0 30px rgba(0, 0, 0, 0.1);'>"
        )
        info += f"<strong style='color: #000000;'>Username:</strong> {obj.username}<br>"
        info += f"<strong style='color: #000000;'>First Name:</strong> {obj.first_name}<br>"
        info += f"<strong style='color: #000000;'>Last Name:</strong> {obj.last_name}<br>"
        info += f"<strong style='color: #000000;'>Is Bot:</strong> {obj.is_bot}<br>"
        info += f"<strong style='color: #000000;'>Language Code:</strong> {obj.language_code}<br>"
        info += "</div>"
        return mark_safe(info)

    get_formatted_info.short_description = 'Информация пользователя'



@admin.register(TelegramBalance)
class TelegramBalanceAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'formatted_income', 'formatted_expenses', 'created_at', 'updated_at')
    search_fields = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Основная информация', {
            'fields': ('income', 'expenses', 'balance')
        }),
        ('Дополнительная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Расчеты по доходам', {
            'fields': ('income_month', 'income_last_3_months', 'income_last_year'),
            'classes': ('collapse',)
        }),
        ('Расчеты по расходам', {
            'fields': ('expenses_last_month', 'expenses_last_3_months', 'expenses_last_year'),
            'classes': ('collapse',)
        }),
    )

    def formatted_income(self, obj):
        return mark_safe(f"<div style='color: green;'>{obj.income}</div>")

    formatted_income.short_description = 'Доход'

    def formatted_expenses(self, obj):
        return mark_safe(f"<div style='color: red;'>{obj.expenses}</div>")

    formatted_expenses.short_description = 'Расходы'

    def income_month(self, obj):
        return obj.income_month()

    income_month.short_description = 'Доход за месяц'

    def income_last_3_months(self, obj):
        return obj.income_last_3_months()

    income_last_3_months.short_description = 'Доход за последние 3 месяца'

    def income_last_year(self, obj):
        return obj.income_last_year()

    income_last_year.short_description = 'Доход за последний год'

    def expenses_last_month(self, obj):
        return obj.expenses_last_month()

    expenses_last_month.short_description = 'Расходы за месяц'

    def expenses_last_3_months(self, obj):
        return obj.expenses_last_3_months()

    expenses_last_3_months.short_description = 'Расходы за последние 3 месяца'

    def expenses_last_year(self, obj):
        return obj.expenses_last_year()

    expenses_last_year.short_description = 'Расходы за последний год'