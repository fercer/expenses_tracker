import decimal
import datetime
import secrets

import expenses
import incomes


class Account(object):
    """Class to keep track of financial movements as incomes and expenses.

    Each object represents a different account, like a chekings, savings, or
    credit card line.
    """
    last_movement_date = datetime.date(1, 1, 1)
    balance = decimal.Decimal(0)

    acc_movements = []

    def __init__(self,
                 name: str = "",
                 id: str or None = None) -> None:
        self.name = name

        if id is None:
            id = secrets.token_hex(nbytes=16)

        self.id = id

    def register_new_expense(self,
                             src_expense: expenses.Expense) -> incomes.Income:
        self.acc_movements.append(src_expense)

        amount_usd = src_expense.amount * src_expense.type_of_change
        self.balance = self.balance - amount_usd

        if self.last_movement_date < src_expense.date:
            self.last_movement_date = src_expense.date

        return incomes.Income(self.name, amount_usd, "USD", decimal.Decimal(1),
                              src_expense.date)

    def register_new_income(self,
                            src_income: incomes.Income) -> None:
        self.acc_movements.append(src_income)

        amount_usd = src_income.amount * src_income.type_of_change
        self.balance = self.balance + amount_usd

        if self.last_movement_date < src_income.date:
            self.last_movement_date = src_income.date

    def to_str(self) -> str:
        """Dump the description of this account to a string.

        This function can be used to store this into a file.

        Returns:
        --------
        acc_str: str
            A string containing the information of this account moves.
        """
        acc_str = "account"
        acc_str += ":id<str>=%s" % self.id
        acc_str += ":name<str>=%s;" % self.name

        for mov in self.acc_movements:
            acc_str += mov.to_str()

        return acc_str

    def __str__(self) -> str:
        """_summary_

        Returns:
            str: _description_
        """
        acc_str = ("[Account] %s\n"
                   "[Balance] $ %0.2f USD\n"
                   "[Last movement] %s" % (
                    self.name,
                    self.balance,
                    self.last_movement_date                    
                   ))

        return acc_str
