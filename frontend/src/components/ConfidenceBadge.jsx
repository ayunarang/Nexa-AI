export default function ConfidenceBadge({ level }) {
  const badgeStyles = {
    high: "bg-green-200 text-green-800",
    medium: "bg-yellow-200 text-yellow-800",
    low: "bg-red-200 text-red-800",
  };

  return (
    <span
      className={`text-xs font-semibold px-2 py-0.5 rounded-full ${badgeStyles[level] || badgeStyles.low}`}
    >
      {level.toUpperCase()}
    </span>
  );
}
