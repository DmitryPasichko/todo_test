import datetime

# from channels.db import database_sync_to_async
# from django.db.models import Q
#
# from RaccoonPayWebService.models.client_profile import Profile
# from RaccoonPayWebService.models.messengers import MessengerInfo
# from RaccoonPayWebService.models.operation_tariffs import TYPE_CHOICES
# from RaccoonPayWebService.models.transactions import Transaction


async def get_profile_balance_by_external_id(external_id: str):
    user = await find_user_by_external_id(external_id)
    if user:
        return user.balance.amount
    else:
        return 0.00


async def find_user_by_external_id(external_id: str):
    pass
# async def find_user_by_external_id(external_id: str) -> Profile:
#     mi = await MessengerInfo.objects.filter(external_user_id=external_id).afirst()
#     if not mi:
#         return None
#     user = Profile.objects.filter(registered_messengers=mi) | Profile.objects.filter(
#         main_messenger=mi
#     )
#     return await user.afirst()


async def find_user_by_phone_number(phone_number: str):
    pass
# async def find_user_by_phone_number(phone_number: str) -> Profile:
#     user = Profile.objects.filter(phone_number=phone_number)
#     if not user:
#         return None
#     return await user.afirst()


async def is_user_exists(external_id: str) -> bool:
    if await find_user_by_external_id(external_id):
        return True
    return False


def get_user_transaction(
    user, n_last_transactions=0, from_date=None, to_date=None
):
    pass
# def get_user_transaction(
#     user: Profile, n_last_transactions=0, from_date=None, to_date=None
# ) -> Transaction:
#     condition = Q()
#     condition.add(Q(**{"to_user": user}), Q.OR)
#     if n_last_transactions:
#         return Transaction.objects.filter(condition).order_by("-create_date")[
#             :n_last_transactions
#         ]
#     if from_date and to_date:
#         to_date = to_date + datetime.timedelta(days=1)
#         condition.add(
#             Q(**{"create_date" + "__gte": from_date, "create_date" + "__lte": to_date}),
#             Q.AND,
#         )
#         return Transaction.objects.filter(condition)

def get_report_IOBytes_from_transactions(transactions) -> str:
    pass
# @database_sync_to_async
# def get_report_IOBytes_from_transactions(transactions: Transaction) -> str:
#     import io
#     import pandas as pd
#     import pdfkit
#
#     df = pd.DataFrame(
#         transactions.values("create_date", "amount", "currency", "tx_type")
#     )
#     towrite = io.StringIO()
#     tx_type_dict = {}
#     for tup in TYPE_CHOICES:
#         tx_type_dict.update({str(tup[0]): str(tup[1])})
#     if not df.empty:
#         df["tx_type"] = df["tx_type"].astype(str)
#         df.replace({"tx_type": tx_type_dict}, inplace=True)
#         df = df.rename(
#             {
#                 "create_date": "Create Date",
#                 "amount": "Amount",
#                 "currency": "Currency",
#                 "tx_type": "Operation Type",
#             },
#             axis=1,
#         )
#     df.to_html(towrite)
#     byte_report_string = pdfkit.from_string(
#         towrite.getvalue(),
#         False,
#         options={
#             "page-size": "Letter",
#             "margin-top": "0.75in",
#             "margin-right": "0.75in",
#             "margin-bottom": "0.75in",
#             "margin-left": "0.75in",
#             "encoding": "UTF-8",
#             "no-outline": None,
#         },
#     )
#     base_report = io.BytesIO(byte_report_string)
#     base_report.seek(0)
#     return base_report


def get_current_balance_message(current_balance: float) -> str:
    return "Your current balance: {}".format(current_balance)


def get_profile_info(user) -> str:
    pass

# def get_profile_info(user: Profile) -> str:
#     return (
#         "Your Account data is:\nFirst name: {}\nLast name: {}\nPhone number: {}\nCountry: {}\nCurrency: {}"
#     ).format(
#         user.first_name,
#         user.last_name,
#         user.phone_number,
#         user.country,
#         user.balance_currency,
#     )
