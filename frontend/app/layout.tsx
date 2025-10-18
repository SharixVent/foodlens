import './globals.css'
import React from 'react'

export const metadata = { title: 'FoodLens', description: 'OCR + OpenFoodFacts' }

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pl">
      <body>
        <div className="max-w-4xl mx-auto p-6">
          <header className="flex items-center justify-between mb-6">
            <h1 className="text-2xl font-bold">FoodLens</h1>
            <nav className="space-x-4 text-sm">
              <a href="/" className="hover:underline">Skanuj</a>
              <a href="/products" className="hover:underline">Produkty</a>
              <a href="/settings" className="hover:underline">Filtry</a>
            </nav>
          </header>
          {children}
        </div>
      </body>
    </html>
  )
}
