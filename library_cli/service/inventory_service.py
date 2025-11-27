def log_copy_action(self, copy_id: int, member_id: int, action: str):
    """Log copy-related actions in InventoryLog."""
    pass


# ----------------- Advanced / Optional -----------------
def find_overdue_copies(self) -> List["Copy"]:
    """Return copies that are overdue based on Loan.returned_at."""
    pass


def get_copy_history(self, copy_id: int):
    """Return all InventoryLog entries for a copy."""
    pass