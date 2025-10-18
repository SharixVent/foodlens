'use client'
import React, { useEffect, useState } from 'react'
import api from '../../lib/api'
import { Rules } from '../../lib/types'

export default function SettingsPage() {
  const [rules, setRules] = useState<Rules>({ name: 'default', exclude_ingredients: [], max_sugars_g_per_100g: null, max_salt_g_per_100g: null } as any)

  useEffect(()=>{ (async()=>{ const { data } = await api.get<Rules>('/analyze/rules'); setRules(data) })() }, [])

  async function save() {
    await api.post('/analyze/rules', rules)
    alert('Zapisano')
  }

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Filtry</h2>
      <div className="grid md:grid-cols-2 gap-4">
        <div>
          <label className="text-sm">Nazwa profilu</label>
          <input className="mt-1 w-full border rounded px-3 py-2" value={rules.name} onChange={e=>setRules(r=>({...r, name: e.target.value}))} />
        </div>
        <div>
          <label className="text-sm">Wykluczenia (po przecinku)</label>
          <input className="mt-1 w-full border rounded px-3 py-2" value={rules.exclude_ingredients.join(', ')} onChange={e=>setRules(r=>({...r, exclude_ingredients: e.target.value.split(',').map(s=>s.trim()).filter(Boolean)}))} />
        </div>
        <div>
          <label className="text-sm">Max cukry g/100g</label>
          <input type="number" step="0.1" className="mt-1 w-full border rounded px-3 py-2" value={rules.max_sugars_g_per_100g ?? ''} onChange={e=>setRules(r=>({...r, max_sugars_g_per_100g: e.target.value ? Number(e.target.value) : null}))} />
        </div>
        <div>
          <label className="text-sm">Max sól g/100g</label>
          <input type="number" step="0.1" className="mt-1 w-full border rounded px-3 py-2" value={rules.max_salt_g_per_100g ?? ''} onChange={e=>setRules(r=>({...r, max_salt_g_per_100g: e.target.value ? Number(e.target.value) : null}))} />
        </div>
      </div>
      <button className="px-3 py-2 rounded bg-black text-white" onClick={save}>Zapisz</button>
    </div>
  )
}
