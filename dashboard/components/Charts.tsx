// components/Charts.tsx
import PowerChart from './PowerChart';
import CarbonChart from './CarbonChart';

const Charts = () => (
  <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
    <PowerChart />
    <CarbonChart />
  </div>
);

export default Charts;