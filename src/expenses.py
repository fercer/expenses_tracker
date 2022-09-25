from collections.abc import Iterable
import datetime
import decimal
import secrets


class Expense(object):
    """A class to represent single expeneses with all the possible details.
    """

    def __init__(self,
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
                 is_recurrent: bool = False,
                 is_transfer: bool = False,
                 id: str or None = None) -> None:
        """Register a new expense.

        Parameters:
        -----------
        amount: decimal.Decimal = decimal.Decimal(0)
        currency: str = "USD"
        type_of_change: decimal.Decimal = decimal.Decimal(1)
        date: Iterable[int, int, int] = (0, 0, 0)
        lat: decimal.Decimal = decimal.Decimal(0)
        lon: decimal.Decimal = decimal.Decimal(0)
        description: str = ""
        main_category: str = ""
        sub_category: str = ""
        keywords: Iterable[str] or None = None
        is_recurrent: bool = False
        is_transfer: bool = False
        source: str = ""
        """
        if keywords is None:
            keywords = []

        self.amount = amount
        self.currency = currency
        self.type_of_change = type_of_change
        self.date = date
        self.lat = lat
        self.lon = lon
        self.description = description
        self.main_category = main_category
        self.sub_category = sub_category
        self.keywords = keywords
        self.is_recurrent = is_recurrent
        self.is_transfer = is_transfer

        if id is None:
            id = secrets.token_hex(nbytes=16)

        self.id = id

    def to_str(self) -> str:
        """Dump the description of this expense move to a string.

        This function can be used to store this into a file.

        Returns:
        --------
        exp_str: str
            A string containing the information of this expense move.
        """
        exp_str = "expense"
        exp_str += ":id<str>=%s" % self.id
        exp_str += ":amount<decimal>=%s" % str(self.amount)
        exp_str += ":currency<str>=%s" % self.currency
        exp_str += ":type_of_change<decimal>=%s" % str(self.type_of_change)
        exp_str += ":date<date %Y%m%d>=" + "%s" % self.date.strftime("%Y%m%d")
        exp_str += ":lat<decimal>=%s" % self.lat
        exp_str += ":lon<decimal>=%s" % self.lon
        exp_str += ":description<str>=%s" % self.description
        exp_str += ":main_category<str>=%s" % self.main_category
        exp_str += ":sub_category<str>=%s" % self.sub_category
        exp_str += ":keywords<list str[,]>=%s" % ",".join(self.keywords)
        exp_str += ":is_recurrent<bool>=%i" % self.is_recurrent
        exp_str += ":is_transfer<bool>=%i;" % self.is_transfer

        return exp_str

    def __str__(self) -> str:
        """Generate a string with the information of this expense.

        Returns:
        -------
        exp_strt {str}:
            A detailed description of this expense.
        """
        exp_str = ("[Expense] On %s of $ %0.2f %s ($ %0.2f USD)\n"
                   "[Description] `%s`\n"
                   "[Category] %s (%s)\n"
                   "[Key words] %s\n"
                   "%s%s\n" % (
                    self.date.strftime("%A %d %B %Y"),
                    self.amount,
                    self.currency,
                    self.amount * self.type_of_change,
                    self.description,
                    self.main_category,
                    self.sub_category,
                    ",".join(self.keywords),
                    "\n[Recurrent]" if self.is_recurrent else "",
                    "\n[Transfer]\n" if self.is_transfer else "",
                   ))
        return exp_str
