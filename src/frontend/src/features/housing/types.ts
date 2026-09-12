export interface Building { id: string; code: string; name: string; address: string; floors: number; is_active: boolean }
export interface RoomType { id: string; name: string; default_monthly_rate: number; is_active: boolean }
export interface Room { id: string; building_id: string; building_code: string; room_type_id: string; room_type_name: string; code: string; floor: number; is_active: boolean }
export interface Bed { id: string; room_id: string; code: string; status: 'Available' | 'Occupied' | 'Maintenance'; is_active: boolean }
export interface MatrixRoom { id: string; code: string; floor: number; room_type: string; beds: Pick<Bed, 'id' | 'code' | 'status'>[] }
export interface MatrixBuilding { id: string; code: string; name: string; rooms: MatrixRoom[] }
