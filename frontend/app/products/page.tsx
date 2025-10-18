'use client'
import React, { useEffect, useState } from 'react'
import api from '../../lib/api'
import { Product } from '../../lib/types'
import ProductCard from '../../components/ProductCard'

export default function ProductsPage() {
  const [items, setItems] = useState<Product[]>([])
  useEffect(() => { (async () => { const { data } = await api.get<Product[]>('/products'); setItems(data) })() }, [])
  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold mb-2">Ostatnio zapisane</h2>
      {items.length === 0 ? <p className="text-sm text-gray-600">Brak produktów.</p> : (
        <div className="grid md:grid-cols-2 gap-4">
          {items.map(p => <ProductCard key={p.id} product={p} />)}
        </div>
      )}
    </div>
  )
}
