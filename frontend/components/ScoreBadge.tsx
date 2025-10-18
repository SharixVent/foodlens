export default function ScoreBadge({ value }: { value: number }) {
  const color = value >= 80 ? 'bg-green-500' : value >= 50 ? 'bg-yellow-500' : 'bg-red-500'
  return (
    <span className={`inline-flex items-center justify-center w-14 h-14 text-white rounded-full ${color}`}>
      {Math.round(value)}
    </span>
  )
}
