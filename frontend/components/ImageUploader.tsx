'use client'
import React, { useState } from 'react'
import api from '../lib/api'

type OCRResult = { text: string; ingredients: string[] }

type Props = { onIngredients: (ingredients: string[], rawText: string) => void }

export default function ImageUploader({ onIngredients }: Props) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function onFile(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0]
    if (!file) return
    const form = new FormData()
    form.append('file', file)
    setLoading(true)
    setError(null)
    try {
      const { data } = await api.post<OCRResult>('/analyze/ocr', form, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      onIngredients(data.ingredients, data.text)
    } catch (err: any) {
      setError(err?.message || 'Błąd OCR')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="p-4 border rounded-xl bg-white shadow-sm">
      <label className="block text-sm font-medium mb-2">Wgraj zdjęcie etykiety (JPG/PNG)</label>
      <input type="file" accept="image/*" onChange={onFile} disabled={loading} />
      {loading && <p className="text-sm mt-2">Przetwarzanie OCR...</p>}
      {error && <p className="text-sm text-red-600 mt-2">{error}</p>}
    </div>
  )
}
