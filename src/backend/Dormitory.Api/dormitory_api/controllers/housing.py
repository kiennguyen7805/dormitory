from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from dormitory_application.housing import (
    BedCreate,
    BedRead,
    BedUpdate,
    BuildingCreate,
    BuildingRead,
    BuildingUpdate,
    HousingService,
    RoomCreate,
    RoomMatrixBuilding,
    RoomRead,
    RoomTypeCreate,
    RoomTypeRead,
    RoomTypeUpdate,
    RoomUpdate,
)

from dormitory_api.dependencies import admin_only, admin_or_staff, get_housing_service

router = APIRouter(prefix="/api", tags=["Housing"])


@router.get("/buildings", response_model=list[BuildingRead], dependencies=[Depends(admin_or_staff)])
def list_buildings(service: HousingService = Depends(get_housing_service)):
    return service.list_buildings()


@router.get("/buildings/{item_id}", response_model=BuildingRead, dependencies=[Depends(admin_or_staff)])
def get_building(item_id: UUID, service: HousingService = Depends(get_housing_service)):
    return service.get_building(item_id)


@router.post("/buildings", response_model=BuildingRead, status_code=201, dependencies=[Depends(admin_only)])
def create_building(payload: BuildingCreate, service: HousingService = Depends(get_housing_service)):
    return service.create_building(payload)


@router.put("/buildings/{item_id}", response_model=BuildingRead, dependencies=[Depends(admin_only)])
def update_building(item_id: UUID, payload: BuildingUpdate, service: HousingService = Depends(get_housing_service)):
    return service.update_building(item_id, payload)


@router.delete("/buildings/{item_id}", status_code=204, dependencies=[Depends(admin_only)])
def delete_building(item_id: UUID, service: HousingService = Depends(get_housing_service)):
    service.delete_building(item_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/room-types", response_model=list[RoomTypeRead], dependencies=[Depends(admin_or_staff)])
def list_room_types(service: HousingService = Depends(get_housing_service)):
    return service.list_room_types()


@router.post("/room-types", response_model=RoomTypeRead, status_code=201, dependencies=[Depends(admin_only)])
def create_room_type(payload: RoomTypeCreate, service: HousingService = Depends(get_housing_service)):
    return service.create_room_type(payload)


@router.put("/room-types/{item_id}", response_model=RoomTypeRead, dependencies=[Depends(admin_only)])
def update_room_type(item_id: UUID, payload: RoomTypeUpdate, service: HousingService = Depends(get_housing_service)):
    return service.update_room_type(item_id, payload)


@router.delete("/room-types/{item_id}", status_code=204, dependencies=[Depends(admin_only)])
def delete_room_type(item_id: UUID, service: HousingService = Depends(get_housing_service)):
    service.delete_room_type(item_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/rooms", response_model=list[RoomRead], dependencies=[Depends(admin_or_staff)])
def list_rooms(buildingId: UUID | None = None, service: HousingService = Depends(get_housing_service)):
    return service.list_rooms(buildingId)


@router.post("/rooms", response_model=RoomRead, status_code=201, dependencies=[Depends(admin_or_staff)])
def create_room(payload: RoomCreate, service: HousingService = Depends(get_housing_service)):
    return service.create_room(payload)


@router.put("/rooms/{item_id}", response_model=RoomRead, dependencies=[Depends(admin_or_staff)])
def update_room(item_id: UUID, payload: RoomUpdate, service: HousingService = Depends(get_housing_service)):
    return service.update_room(item_id, payload)


@router.delete("/rooms/{item_id}", status_code=204, dependencies=[Depends(admin_or_staff)])
def delete_room(item_id: UUID, service: HousingService = Depends(get_housing_service)):
    service.delete_room(item_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/beds", response_model=list[BedRead], dependencies=[Depends(admin_or_staff)])
def list_beds(roomId: UUID | None = None, service: HousingService = Depends(get_housing_service)):
    return service.list_beds(roomId)


@router.post("/beds", response_model=BedRead, status_code=201, dependencies=[Depends(admin_or_staff)])
def create_bed(payload: BedCreate, service: HousingService = Depends(get_housing_service)):
    return service.create_bed(payload)


@router.put("/beds/{item_id}", response_model=BedRead, dependencies=[Depends(admin_or_staff)])
def update_bed(item_id: UUID, payload: BedUpdate, service: HousingService = Depends(get_housing_service)):
    return service.update_bed(item_id, payload)


@router.delete("/beds/{item_id}", status_code=204, dependencies=[Depends(admin_or_staff)])
def delete_bed(item_id: UUID, service: HousingService = Depends(get_housing_service)):
    service.delete_bed(item_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/room-matrix", response_model=list[RoomMatrixBuilding], dependencies=[Depends(admin_or_staff)])
def room_matrix(service: HousingService = Depends(get_housing_service)):
    return service.room_matrix()
