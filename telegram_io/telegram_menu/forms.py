from aiogram.dispatcher.filters.state import State, StatesGroup


class RegisterForm(StatesGroup):
    start = State()
    first_name = State()
    last_name = State()
    phone = State()
    country = State()
    language = State()
    balance = State()
    submit = State()


class TopUpBalancePaymentForm(StatesGroup):
    amount = State()
    card_number = State()
    expire_month = State()
    expire_year = State()
    cvv = State()
    submit = State()


class WithdrawalPaymentForm(StatesGroup):
    amount = State()
    card_number = State()
    expire_month = State()
    expire_year = State()
    submit = State()


class TransactionToUserPaymentForm(StatesGroup):
    phone = State()
    amount = State()
    submit = State()

class GetTransactionsReportByCount(StatesGroup):
    count = State()


class GetTransactionsReportByDate(StatesGroup):
    date_from = State()
    date_to = State()