import { Product } from '../lib/types'
import ScoreBadge from './ScoreBadge'

export default function ProductCard({ product, score }: { product: Product; score?: number }) {
  return (
    <div className="border rounded-xl p-4 bg-white shadow-sm">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="font-semibold text-lg">{product.name}</h3>
          <p className="text-sm text-gray-600">{product.brand ?? '—'}</p>
          <p className="text-xs text-gray-500 mt-1">EAN: {product.barcode ?? '—'}</p>
        </div>
        <ScoreBadge value={score ?? 0} />
      </div>
      {product.ingredients_text && (
        <p className="text-sm mt-3 line-clamp-3"><strong>Skład:</strong> {product.ingredients_text}</p>
      )}
      {product.nutrition && (
        <div className="grid grid-cols-3 gap-2 text-xs mt-3">
          <div className="p-2 bg-gray-50 rounded">Cukry/100g<br/><span className="font-semibold">{product.nutrition.sugars_100g ?? '—'}</span></div>
          <div className="p-2 bg-gray-50 rounded">Sól/100g<br/><span className="font-semibold">{product.nutrition.salt_100g ?? '—'}</span></div>
          <div className="p-2 bg-gray-50 rounded">Tłuszcz/100g<br/><span className="font-semibold">{product.nutrition.fat_100g ?? '—'}</span></div>
        </div>
      )}
    </div>
  )
}
