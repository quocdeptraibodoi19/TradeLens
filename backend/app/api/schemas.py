from pydantic import BaseModel


class JobResponse(BaseModel):
    job_id: str
    url: str


class SyncResponse(BaseModel):
    jobs: list[JobResponse]
