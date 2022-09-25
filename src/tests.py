import accounts
import manager


def test_mgr():
    my_mgr = manager.AccountManager(r"C:\Users\CE Owner\Documents\FerDevStudio\expenses_tracker\examples")
    acc_id = my_mgr.new_account(accounts.Account("New Account"))
    my_mgr.register_move(from_account=None, to_account="New Account")
    my_mgr.save(overwrite=True)
    my_mgr.load()

    print(my_mgr.managed_accounts[acc_id].to_str())

if __name__ == "__main__":
    test_mgr()
