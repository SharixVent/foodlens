export type Product = {
  id: number
  barcode?: string | null
  name: string
  brand?: string | null
  ingredients_text?: string | null
  nutriscore?: string | null
  nova_group?: number | null
  nutrition?: { sugars_100g?: number; salt_100g?: number; fat_100g?: number } | null
}

export type Rules = {
  name: string
  exclude_ingredients: string[]
  max_sugars_g_per_100g?: number | null
  max_salt_g_per_100g?: number | null
}
