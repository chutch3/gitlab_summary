from pydantic import BaseModel
from typing import List
from datetime import datetime


class MergeRequestData(BaseModel):
    """
    Reusing this for any user activity, though the name suggests MRs.
    You might rename to UserActivityData or separate commits vs. MRs if needed.
    """

    title: str
    description: str
    author: str
    commits: List[str]
    comments: List[str]
    weight: float = 1.0
    timestamp: datetime = None
