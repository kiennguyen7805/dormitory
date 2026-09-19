export interface HousingApplication {
  id: string
  student_id: string
  student_name: string
  term_code: string
  preferred_room_type_id: string
  preferred_room_type_name: string
  status: 'Submitted' | 'Approved' | 'Rejected'
  rejection_reason: string | null
  created_at: string
}

export interface BedAssignment {
  id: string
  bed_id: string
  building_code: string
  room_code: string
  bed_code: string
  start_date: string
  end_date: string | null
  status: 'Active' | 'Ended'
}

export interface Contract {
  id: string
  contract_no: string
  student_id: string
  student_name: string
  application_id: string
  start_date: string
  end_date: string
  status: 'Active' | 'Terminated'
  base_rate: number
  current_assignment: BedAssignment | null
}
