from collections.abc import Iterable
import datetime
import decimal

import os
import secrets
import scrypt
import getpass

import _utils as utils
import accounts
import incomes
import expenses


class AccountManager(object):
    """Manager for multiple accounts.
    """
    path = None
    managed_accounts = {}
    managed_accounts_names = {}

    def __init__(self, path: str = "."):
        assert os.path.isabs(path), ("Path must be an absolute location"
                                     f" but `{path}` was given.")

        if not path.lower().endswith(".mgr"):
            path = os.path.join(path, "my_accounts.mgr")

        self.path = path

    def save(self, overwrite: bool = False) -> None:
        # If `path`` is a directory, append a default file name to it.
        if os.path.isdir(self.path):
            new_path = os.path.join(self.path, "my_acc.mgr")
        else:
            new_path = self.path
        
        if not overwrite:
            assert not os.path.isfile(new_path), (f"File `[new_path]` already "
                                                  "exists and overwrite has been"
                                                  " set to False.")

        self.path = new_path
        
        # Generate a hash that is used to separate different accounts.
        sep_hash = secrets.token_hex(nbytes=4)
        print("Hashing accounts using separator", sep_hash)
        acc_strs = ""
        for _, acc in self.managed_accounts.items():
            acc_strs += sep_hash + acc.to_str()

        encoded_acc_strs = scrypt.encrypt(acc_strs,
                                          getpass.getpass("Password: "),
                                          0.05)

        with open(self.path, "wb") as fp:
            fp.write(encoded_acc_strs)

    def load(self):
        assert os.path.isfile(self.path), f"File `[self.path]` does not exist."

        with open(self.path, "rb") as fp:
            encoded_acc_strs = fp.read()

        acc_strs = scrypt.decrypt(encoded_acc_strs,
                                  getpass.getpass("Password: "),
                                  0.05)

        # Read the separation hash to divide the decoded string into a set of 
        # account details.
        sep_hash = acc_strs[:8]
        acc_strs = acc_strs[8:].split(sep_hash)

        self.managed_accounts = {}
        for acc_str in acc_strs:
            acc_str = acc_str.split(";")

            acc_details = acc_str[0].split(":")

            acc_details = dict([utils.parse_parameter(acc_detail)
                                for acc_detail in acc_details[1:]])

            acc_id = self.new_account(accounts.Account(**acc_details))

            for mov_str in acc_str[1:]:
                if not len(mov_str):
                    continue

                mov_details = mov_str.split(":")
                mov_type = mov_details[0]
                mov_details = dict([utils.parse_parameter(mov_detail)
                                for mov_detail in mov_details[1:]])

                if mov_type == "income":
                    self.managed_accounts[acc_id].register_new_income(
                        incomes.Income(**mov_details))
                elif mov_type == "expense":
                    self.managed_accounts[acc_id].register_new_expense(
                        expenses.Expense(**mov_details))
                else:
                    raise ValueError(f"Move type `[mov_type]` is not supported")

    def new_account(self,
                    acc_src: accounts.Account or str = "New Account") -> str:
        if isinstance(acc_src, str):
            acc_src = accounts.Account(name=acc_src)

        self.managed_accounts[acc_src.id] = acc_src
        self.managed_accounts_names[acc_src.name] = acc_src.id

        return acc_src.id

    def register_move(self,
                      from_account: str or None = None,
                      to_account: str or None = None,
                      amount: decimal.Decimal = decimal.Decimal(0),
                      currency: str = "USD",
                      type_of_change: decimal.Decimal = decimal.Decimal(1),
                      date: datetime.date = datetime.date(1, 1, 1),
                      lat: decimal.Decimal = decimal.Decimal(0),
                      lon: decimal.Decimal = decimal.Decimal(0),
                      description: str = "",
                      main_category: str = "",
                      sub_category: str = "",
                      keywords: Iterable[str] or None = None,
                      is_recurrent: bool = False):

        if from_account is None:
            from_account = ""

        if to_account is None:
            to_account = ""

        # Check if both accounts exist on this manager, or one of them is an
        # external source/destination account not managed by this.
        from_account_id = self.managed_accounts_names.get(from_account, None)
        to_account_id = self.managed_accounts_names.get(to_account, None)

        # Determine if this can be considered as a transfer between managed
        # accounts by this.
        if from_account_id is not None and to_account_id is not None:
            is_transfer = True

        if from_account_id is not None:
            new_expense = expenses.Expense(amount, currency, type_of_change,
                                           date,
                                           lat,
                                           lon,
                                           description,
                                           main_category,
                                           sub_category,
                                           keywords,
                                           is_recurrent,
                                           is_transfer)

            # Register the new expense, and in case of transfers, the generated
            # income is resistered on the destination account.
            new_income = \
                self.managed_accounts[from_account_id].register_new_expense(
                    new_expense)

        else:
            new_income = incomes.Income(from_account, amount, currency,
                                        type_of_change,
                                        date)

        if to_account_id is not None:
            self.managed_accounts[to_account_id].register_new_income(new_income)

    def __str__(self):
        mgr_str = "-" * 10
        mgr_str += " [Accounts] "
        mgr_str += "-" * 10

        for acc_key in self.managed_accounts.keys():
            mgr_str += "\n" + "-" * 32 + "\n"
            mgr_str += str(self.managed_accounts[acc_key])

        mgr_str += "\n" + "-" * 32

        return mgr_str
