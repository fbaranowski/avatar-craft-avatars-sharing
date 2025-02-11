from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pymongo.errors import DuplicateKeyError

from models import AvatarShare
from mongo_client import shares_collection

router = APIRouter()


@router.post("/create")
async def create_share(share: AvatarShare):
    try:
        await shares_collection.insert_one(share.dict())
        return JSONResponse(
            status_code=201,
            content={
                "message": f"Successfully shared avatar with id: {share.avatar_id} from: {share.from_user} to: {share.to_user}"
            },
        )
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="This share record already exists")


@router.get("/shares")
async def get_shares(from_user: str | None = None, to_user: str | None = None):
    query = {}

    if from_user:
        query["from_user"] = from_user
    if to_user:
        query["to_user"] = to_user

    shares = await shares_collection.find(query).to_list()

    for share in shares:
        share["_id"] = str(share["_id"])

    return jsonable_encoder(shares)


@router.delete("/delete")
async def delete_share(share: AvatarShare):
    result = await shares_collection.delete_one(
        {
            "from_user": share.from_user,
            "to_user": share.to_user,
            "avatar_id": share.avatar_id,
        }
    )

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Share not found")

    return JSONResponse(status_code=200, content={"message": "Share deleted"})
