export interface Utility {
  id: string
  code: string
  name: string
  unit: string
}

export interface Meter {
  id: string
  utility_id: string
  utility_code: string
  utility_name: string
  room_id: string
  room_label: string
  meter_code: string
  initial_reading: string
  is_active: boolean
}

export interface TariffTier {
  tier_order: number
  from_quantity: string
  to_quantity: string | null
  unit_price: string
}

export interface UtilityTariff {
  id: string
  utility_code: string
  utility_name: string
  name: string
  effective_from: string
  effective_to: string | null
  calculation_type: string
  tiers: TariffTier[]
}

export interface MeterReading {
  id: string
  meter_code: string
  utility_code: string
  period_start: string
  period_end: string
  previous_reading: string
  current_reading: string
  consumption: string
  calculated_amount: string
  source: string
}

export interface ImportPreview {
  batch_id: string
  status: string
  total_rows: number
  valid_rows: number
  invalid_rows: number
  rows: Array<{
    row_number: number
    meter_code: string
    consumption?: string
    calculated_amount?: string
    valid: boolean
    errors: string[]
  }>
}

export interface Bill {
  id: string
  bill_no: string
  contract_id: string
  period_start: string
  period_end: string
  status: string
  total_amount: string
  balance_amount: string
  items: Array<{ id: string; description: string; amount: string }>
}
