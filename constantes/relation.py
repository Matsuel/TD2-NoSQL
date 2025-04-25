from enum import StrEnum

class RelationEnum(StrEnum):
    Friend = "FRIENDS_WITH"
    Created = "CREATED"
    HasComment = "HAS_COMMENT"
    Likes = "LIKES"