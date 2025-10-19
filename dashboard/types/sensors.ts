export interface SensorData {
  temperature: number | null;
  humidity: number | null;
  occupancy: number;
  power_usage: number | null;
  seat_hogged: number | null;
}

export interface SensorMessage extends SensorData {
  topic: string;
  roomId: string;
  deviceId: string;
}