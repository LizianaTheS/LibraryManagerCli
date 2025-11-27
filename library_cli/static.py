import enum


class Language(str, enum.Enum):
    PERSIAN = "persian"
    ENGLISH = "english"
    GERMAN = "german"
    FRENCH = "french"
    JAPANESE = "japanese"
    CHINESE = "chinese"
    KOREAN = "korean"
    HINDI = "hindi"


class Country(str, enum.Enum):
    IRAN = "iran"
    UNITED_STATES = "united_states"
    UNITED_KINGDOM = "united_kingdom"
    GERMANY = "germany"
    FRANCE = "france"
    JAPAN = "japan"
    CHINA = "china"
    SOUTH_KOREA = "south_korea"
    INDIA = "india"


class Status(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BANNED = "banned"
    SUSPENDED = "suspended"
    PENDING = "pending"
    DELETED = "deleted"
    EXPIRED = "expired"


class Condition(str, enum.Enum):
    GOOD = "good"
    FAIR = "fair"
    DAMAGED = "damaged"
    LOST = "lost"


class Action(str, enum.Enum):
    REMOVED = "removed"
    BORROWED = "borrowed"
    FREE = "free"
    LOANED = "loaned"
