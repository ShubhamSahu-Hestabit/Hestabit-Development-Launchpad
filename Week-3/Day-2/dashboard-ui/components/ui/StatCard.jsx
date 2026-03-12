import Card from "./Card";

export default function StatCard({ title, value, subtitle }) {
  return (
    <Card>
      <p className="text-sm text-gray-500">{title}</p>
      <h2 className="text-2xl font-semibold mt-1">{value}</h2>
      <p className="text-xs text-gray-400 mt-1">{subtitle}</p>
    </Card>
  );
}
