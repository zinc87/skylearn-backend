import uuid
from app import db
from app.models.user import User
from app.models.progress import XpHistory

# Threshold starts at 100 XP for level 2, then grows by level * 50 per level.
# e.g. Level 2: 100, Level 3: 250, Level 4: 450, Level 5: 700
def get_level(xp: int) -> int:
    """Calculate level from total XP."""
    level = 1
    threshold = 100
    while xp >= threshold:
        level += 1
        threshold += level * 50
    return level

def get_user_xp(user_id: str) -> int:
    """Get a user's total XP."""
    user = User.query.get(user_id)
    return user.xp if user else 0

# Note: caller is responsible for calling db.session.commit() after this function.
def award_xp(user_id: str, amount: int, source: str):
    """Award XP to a user and log it in history."""
    user = User.query.get(user_id)
    if not user:
        return
    user.xp += amount

    history = XpHistory(
        id=str(uuid.uuid4()),
        user_id=user_id,
        xp=amount,
        source=source,
    )
    db.session.add(history)
