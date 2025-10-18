// frontend/app/page.tsx (Skanuj)
'use client'
import React, { useState } from 'react'
import ImageUploader from '../components/ImageUploader'
import api from '../lib/api'
import { Product, Rules } from '../lib/types'
import ProductCard from '../components/ProductCard'

export default function Page() {
  const [ingredients, setIngredients] = useState<string[]>([])
  const [raw, setRaw] = useState('')
  const [barcode, setBarcode] = useState('')
  const [product, setProduct] = useState<Product | null>(null)
  const [score, setScore] = useState<number | null>(null)
  const [rules, setRules] = useState<Rules>({ name: 'default', exclude_ingredients: [], max_sugars_g_per_100g: 12, max_salt_g_per_100g: 1.5 })

  async function fetchProduct() {
    if (!barcode) return
    const { data } = await api.get<Product>(`/products/barcode/${barcode}`)
    setProduct(data)
  }

  async function scoreIt() {
    if (!product) return
    const { data } = await api.post(`/analyze/score/${product.id}`, rules)
    setScore(data.score)
  }

  return (
    <div className="space-y-6">
      <div className="grid md:grid-cols-2 gap-6">
        <ImageUploader onIngredients={(ings, t) => { setIngredients(ings); setRaw(t) }} />
        <div className="p-4 border rounded-xl bg-white shadow-sm">
          <label className="block text-sm font-medium">EAN (opcjonalnie)</label>
          <input className="mt-1 w-full border rounded px-3 py-2" placeholder="np. 5901234123457" value={barcode} onChange={e=>setBarcode(e.target.value)} />
          <button className="mt-3 px-3 py-2 rounded bg-black text-white" onClick={fetchProduct}>Pobierz z OpenFoodFacts</button>
          {product && <div className="mt-4"><ProductCard product={product} score={score ?? undefined} /></div>}
        </div>
      </div>

      <div className="p-4 border rounded-xl bg-white shadow-sm">
        <h2 className="font-semibold mb-2">Wykryte składniki (OCR)</h2>
        {ingredients.length === 0 ? <p className="text-sm text-gray-600">Brak — wgraj zdjęcie.</p> : (
          <div className="flex flex-wrap gap-2">
            {ingredients.map((ing, i) => (
              <span key={i} className="px-2 py-1 text-sm bg-gray-100 rounded">{ing}</span>
            ))}
          </div>
        )}
        <details className="mt-3">
          <summary className="text-sm text-gray-600 cursor-pointer">Pełny tekst OCR</summary>
          <pre className="whitespace-pre-wrap text-xs mt-2">{raw}</pre>
        </details>
      </div>

      <div className="p-4 border rounded-xl bg-white shadow-sm">
        <h2 className="font-semibold mb-2">Filtry</h2>
        <div className="grid md:grid-cols-2 gap-4">
          <div>
            <label className="text-sm">Wyklucz składniki (po przecinku)</label>
            <input className="mt-1 w-full border rounded px-3 py-2" placeholder="orzechy, gluten" onChange={e=>setRules(r=>({...r, exclude_ingredients: e.target.value.split(',').map(s=>s.trim()).filter(Boolean)}))} />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-sm">Max cukry g/100g</label>
              <input type="number" step="0.1" className="mt-1 w-full border rounded px-3 py-2" defaultValue={12} onChange={e=>setRules(r=>({...r, max_sugars_g_per_100g: Number(e.target.value)}))} />
            </div>
            <div>
              <label className="text-sm">Max sól g/100g</label>
              <input type="number" step="0.1" className="mt-1 w-full border rounded px-3 py-2" defaultValue={1.5} onChange={e=>setRules(r=>({...r, max_salt_g_per_100g: Number(e.target.value)}))} />
            </div>
          </div>
        </div>
        <div className="mt-4 flex gap-3">
          <button className="px-3 py-2 rounded bg-black text-white" onClick={async()=>{await api.post('/analyze/rules', rules)}}>Zapisz filtry</button>
          <button className="px-3 py-2 rounded bg-emerald-600 text-white" onClick={scoreIt} disabled={!product}>Oceń produkt</button>
        </div>
      </div>
    </div>
  )
}
