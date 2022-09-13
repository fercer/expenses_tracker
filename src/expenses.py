from collections.abc import Iterable
import decimal


class Expense(object):
    """A class to represent single expeneses with all the possible details.

    Parameters:
    -----------
    amount: decimal.Decimal = decimal.Decimal(0)
    currency: str = "USD"
    type_of_change: decimal.Decimal = decimal.Decimal(1)
    date: Iterable[int, int, int] = (0, 0, 0)
    place: Iterable[decimal.Decimal
                    decimal.Decimal] = (decimal.Decimal(0),
                                        decimal.Decimal(0)),
    description: str = ""
    main_category: str = ""
    sub_category: str = ""
    keywords: Iterable[str] or None = None
    is_recurrent: bool = False
    is_transfer: bool = False
    source: str = "") -> None
    """
    amount = decimal.Decimal(0)
    currency = "USD"
    type_of_change = decimal.Decimal(1)

    # Date in dd, mm, yyyy format
    date = (0, 0, 0)
    place = (decimal.Decimal(0), decimal.Decimal(0))
    description = ""
    main_category = ""
    sub_category = ""
    keywords = None
    is_recurrent = False
    is_transfer = False

    source = "Checking"

    def __init__(self,
                 amount: decimal.Decimal = decimal.Decimal(0),
                 currency: str = "USD",
                 type_of_change: decimal.Decimal = decimal.Decimal(1),
                 date: Iterable[int, int, int] = (0, 0, 0),
                 place: Iterable[decimal.Decimal,
                                 decimal.Decimal] = (decimal.Decimal(0),
                                                     decimal.Decimal(0)),
                 description: str = "",
                 main_category: str = "",
                 sub_category: str = "",
                 keywords: Iterable[str] or None = None,
                 is_recurrent: bool = False,
                 is_transfer: bool = False,
                 source: str = "") -> None:
        """Register a new expense.
        """
        assert len(date) == 3, ("Date must be in (dd, mm, yyyy) format,"
                                f" got: {date}")
        if keywords is None:
            keywords = []
        self.amount = amount
        self.currency = currency
        self.type_of_change = type_of_change
        self.date = date
        self.place = place
        self.description = description
        self.main_category = main_category
        self.sub_category = sub_category
        self.keywords = keywords
        self.is_recurrent = is_recurrent
        self.is_transfer = is_transfer
        self.source = source

    def __str__(self) -> str:
        """Generate a string with the information of this expense.

        Returns:
        -------
        exp_strt {str}:
            A detailed description of this expense.
        """
        exp_str = ("[Expense] On %02d/%02d/%04d of $ %0.2f %s ($ %0.2f USD)\n"
                   "[Description] `%s`\n"
                   "[Category] %s (%s)\n"
                   "[Key words] %s\n"
                   "[Paid from] %s"
                   "%s%s\n" % (
                    *self.date,
                    self.amount,
                    self.currency,
                    self.amount * self.type_of_change,
                    self.description,
                    self.main_category,
                    self.sub_category,
                    ",".join(self.keywords),
                    self.source,
                    "\n[Recurrent]" if self.is_recurrent else "",
                    "\n[Transfer]\n" if self.is_transfer else "",
                   ))
        return exp_str
