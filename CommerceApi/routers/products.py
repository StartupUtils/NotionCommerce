from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from CommerceApi.utils.mongo import Mongoify

router = APIRouter(
    prefix="/product",
    tags=["product"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{target}", status_code=201)
async def get_product(target: str):
    """Find a product and return data"""
    if ":" in target:
        product_id = target.split(":")[0]
        product = await Mongoify.find_one("products", {"id": product_id})
        # Check if product has data
        if product is None:
            return JSONResponse(
                status_code=400,
                content={"message": f"No product with id {product_id}.", "ok": False, "issue_type": "not_found"},
            )
        if "_id" in product:
            del product["_id"]
        
        if product.get("display") == True:
            return JSONResponse(status_code=200, content=product)
        return JSONResponse(status_code=400, content={"message": f"Product is not enabeld for display", "ok": False, "issue_type": "not_displayed"})
    return JSONResponse(status_code=400, content={"message": f"Could not parse {target}", "ok": False, "issue_type": "id_parse"})