export interface SensorData {
  temperature: number;
  outside_temp: number;
  outside_humidity: number;
  weather_condition: string;
  ac_temp_setting: number;
  power_usage: number;
  occupancy: number;
  is_occupied: number;
  timestamp: string;
  phase: string;
}