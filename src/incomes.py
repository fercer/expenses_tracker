import datetime
import decimal
import secrets


class Income(object):
    """Class to manage accounts as sources of financial resources.
    """
    def __init__(self,
                 source: str = "",
                 amount: decimal.Decimal = decimal.Decimal(0),
                 currency: str = "USD",
                 type_of_change: decimal.Decimal = decimal.Decimal(1),
                 date: str or datetime.date = datetime.date(1, 1, 1),
                 id: str or None = None) -> None:
        """Register a new income.

        Parameters:
        -----------
        income_source: str = "",
        amount: decimal.Decimal = decimal.Decimal(0),
        currency: str = "USD",
        type_of_change: decimal.Decimal = decimal.Decimal(1),
        date: str or Iterable[int, int, int] = (0, 0, 0)
        """
        self.source = source
        self.amount = amount
        self.currency = currency
        self.type_of_change = type_of_change
        self.date = date

        if id is None:
            id = secrets.token_hex(nbytes=16)

        self.id = id

    def to_str(self) -> str:
        """Dump the description of this income move to a string.

        This function can be used to store this into a file.

        Returns:
        --------
        inc_str: str
            A string containing the information of this income move.
        """
        inc_str = "income"
        inc_str += ":id<str>=%s" % self.id
        inc_str += ":source<str>=%s" % self.source
        inc_str += ":amount<decimal>=%s" % str(self.amount)
        inc_str += ":currency<str>=%s" % self.currency
        inc_str += ":type_of_change<decimal>=%s" % str(self.type_of_change)
        inc_str += ":date<date %Y%m%d>=" + "%s;" % self.date.strftime("%Y%m%d")

        return inc_str

    def __str__(self) -> str:
        """Generate a string with the information of this income.

        Returns:
        -------
        inc_strt {str}:
            A detailed description of this income.
        """
        inc_str = ("[Income] On %s of $ %0.2f %s ($ %0.2f USD)\n"
                   "[From] `%s`\n" % (
                    self.date.strftime("%A %d %B %Y"),
                    self.amount,
                    self.currency,
                    self.amount * self.type_of_change,
                    self.source))
        return inc_str
