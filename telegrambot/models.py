from django.db import models
from datetime import datetime
from datetime import timedelta
from django.utils import timezone



class TelegramUser(models.Model):
    user_id = models.BigIntegerField(
        unique=True,
        verbose_name="ID пользователя",
        help_text="Уникальный идентификатор пользователя в Telegram.",
    )
    username = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        verbose_name="Имя пользователя",
        help_text="Имя пользователя в Telegram.",
    )
    first_name = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        verbose_name="Имя",
        help_text="Имя пользователя в Telegram.",
    )
    last_name = models.CharField(
        max_length=120,
        blank=True,
        null=True,
        verbose_name="Фамилия",
        help_text="Фамилия пользователя в Telegram.",
    )
    language_code = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name="Код языка",
        help_text="Код языка, используемый пользователем в Telegram.",
    )
    is_bot = models.BooleanField(
        default=False,
        verbose_name="Бот",
        help_text="Указывает, является ли пользователь ботом.",
    )
    created_at = models.DateTimeField(
        default=datetime.now,
        verbose_name="Создан",
        help_text="Временная метка, указывающая, когда был создан пользователь.",
    )
    
    def get_name(self):
        if self.username:
            return self.username
        elif self.last_name:
            return self.last_name
        elif self.first_name:
            return self.first_name
        else:
            return "Пользователь"
        
    def __str__(self):
        return f"{self.user_id}: {self.get_name()}"
    
    class Meta:
        verbose_name = "Пользователь Telegram"
        verbose_name_plural = "Пользователи Telegram"
        ordering = ["-created_at"]
        


class TelegramChat(models.Model):
    pass


class TelegramBalance(models.Model):
    income = models.BigIntegerField(
        default=0,
        verbose_name="Доход",
        help_text="Сумма дохода на балансе."
    )
    expenses = models.BigIntegerField(
        default=0,
        verbose_name="Расходы",
        help_text="Сумма расходов на балансе."
    )
    balance = models.BigIntegerField(
        default=0,
        verbose_name="Баланс",
        help_text="Общий баланс, равный доходам минус расходы."
    )
    created_at = models.DateTimeField(
        default=datetime.now,
        verbose_name="Дата создания",
        help_text="Дата и время создания записи в балансе."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления",
        help_text="Дата и время последнего обновления записи в балансе."
    )
    
    def income_month(self):
        # Рассчитайте первый день текущего месяца
        first_day_of_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # Фильтровать транзакции за текущий месяц
        income_for_month = self.income.filter(created_at__gte=first_day_of_month)
        
        # Подведите итог доходу за месяц
        total_income_for_month = income_for_month.aggregate(models.Sum('income'))['income__sum']
        
        return total_income_for_month or 0
    
    def income_last_3_months(self):
        # Рассчитайте первый день текущего месяца
        first_day_of_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        # Рассчитайте первый день месяца 3 месяца назад
        first_day_of_last_3_months = first_day_of_month - timedelta(days=3 * 30)

        # Фильтровать транзакции за последние 3 месяца
        income_for_last_3_months = self.income.filter(created_at__gte=first_day_of_last_3_months)

        # Подведите итог доходу за последние 3 месяца
        total_income_last_3_months = income_for_last_3_months.aggregate(models.Sum('income'))['income__sum']

        return total_income_last_3_months or 0
    

    def income_last_year(self):
        # Вычислить первый день текущего месяца
        first_day_of_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        # Вычислить первый день месяца 12 месяцев назад
        first_day_of_last_year = first_day_of_month - timedelta(days=365)

        # Фильтрация транзакций за последние 12 месяцев
        income_for_last_year = self.income.filter(created_at__gte=first_day_of_last_year)

        # Суммируем доходы за последние 12 месяцев.
        total_income_last_year = income_for_last_year.aggregate(models.Sum('income'))['income__sum']

        return total_income_last_year or 0

    def expenses_last_month(self):
        # Рассчитываем первый день текущего месяца
        first_day_of_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        # Рассчитываем первый день предыдущего месяца
        first_day_of_last_month = first_day_of_month - timedelta(days=first_day_of_month.day)

        # Фильтруем транзакции за последний месяц
        expenses_for_last_month = self.expenses.filter(created_at__gte=first_day_of_last_month)

        # Суммируем расходы за последний месяц
        total_expenses_last_month = expenses_for_last_month.aggregate(models.Sum('expenses'))['expenses__sum']

        return total_expenses_last_month or 0  # Возвращаем 0, если расходов за последний месяц нет

    def expenses_last_3_months(self):
        # Рассчитываем первый день текущего месяца
        first_day_of_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        # Рассчитываем первый день месяца 3 месяца назад
        first_day_of_last_3_months = first_day_of_month - timedelta(days=3 * 30)

        # Фильтруем транзакции за последние 3 месяца
        expenses_for_last_3_months = self.expenses.filter(created_at__gte=first_day_of_last_3_months)

        # Суммируем расходы за последние 3 месяца
        total_expenses_last_3_months = expenses_for_last_3_months.aggregate(models.Sum('expenses'))['expenses__sum']

        return total_expenses_last_3_months or 0  # Возвращаем 0, если расходов за последние 3 месяца нет

    def expenses_last_year(self):
        # Рассчитываем первый день текущего месяца
        first_day_of_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        # Рассчитываем первый день месяца 12 месяцев назад
        first_day_of_last_year = first_day_of_month - timedelta(days=365)

        # Фильтруем транзакции за последний год
        expenses_for_last_year = self.expenses.filter(created_at__gte=first_day_of_last_year)

        # Суммируем расходы за последний год
        total_expenses_last_year = expenses_for_last_year.aggregate(models.Sum('expenses'))['expenses__sum']

        return total_expenses_last_year or 0  # Возвращаем 0, если расходов за последний год нет

    def __str__(self):
        return f"Баланс: {self.balance}"
    
    class Meta:
        verbose_name = "Баланс"
        verbose_name_plural = "Балансы"
        ordering = ["-created_at"]