'use client'

import { useQuery } from '@tanstack/react-query'
import api from '@/lib/api'
import { Category, Post } from '@/types'
import { BookOpen, ArrowRight } from 'lucide-react'
import Link from 'next/link'

export default function CategoriesPage() {
  const { data: categories, isLoading: categoriesLoading } = useQuery<Category[]>({
    queryKey: ['categories'],
    queryFn: async () => {
      const response = await api.get('/categories/')
      return response.data.results || response.data
    },
  })

  const { data: posts, isLoading: postsLoading } = useQuery<Post[]>({
    queryKey: ['posts', 'published'],
    queryFn: async () => {
      const response = await api.get('/posts/?status=published')
      return response.data.results || response.data
    },
  })

  if (categoriesLoading || postsLoading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-8"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="h-48 bg-gray-200 rounded-lg"></div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  // Calculate post count for each category
  const getPostCount = (categoryId: string) => {
    return posts?.filter(post => post.category.id === categoryId).length || 0
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Header */}
      <div className="mb-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">Categories</h1>
        <p className="text-xl text-gray-600">
          Explore articles by topic and discover content that interests you
        </p>
      </div>

      {/* Categories Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {categories?.map((category) => {
          const postCount = getPostCount(category.id)
          return (
            <div
              key={category.id}
              className="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow border border-gray-100"
            >
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                  <BookOpen className="w-6 h-6 text-blue-600" />
                </div>
                <span className="text-sm text-gray-500">
                  {postCount} article{postCount !== 1 ? 's' : ''}
                </span>
              </div>
              
              <h3 className="text-xl font-bold text-gray-900 mb-2">
                {category.name}
              </h3>
              
              {category.description && (
                <p className="text-gray-600 mb-4 line-clamp-3">
                  {category.description}
                </p>
              )}
              
              <Link
                href={`/blog/category/${category.slug}`}
                className="inline-flex items-center text-blue-600 hover:text-blue-700 font-medium"
              >
                Browse articles
                <ArrowRight className="w-4 h-4 ml-1" />
              </Link>
            </div>
          )
        })}
      </div>

      {/* No Categories */}
      {(!categories || categories.length === 0) && (
        <div className="text-center py-12">
          <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <BookOpen className="w-8 h-8 text-gray-400" />
          </div>
          <h3 className="text-xl font-semibold text-gray-900 mb-2">No categories yet</h3>
          <p className="text-gray-600">Categories will appear here once they're created.</p>
        </div>
      )}

      {/* Stats */}
      <div className="mt-16 bg-gray-50 rounded-lg p-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
          <div>
            <div className="text-3xl font-bold text-blue-600 mb-2">
              {categories?.length || 0}
            </div>
            <div className="text-gray-600">Categories</div>
          </div>
          <div>
            <div className="text-3xl font-bold text-blue-600 mb-2">
              {posts?.length || 0}
            </div>
            <div className="text-gray-600">Total Articles</div>
          </div>
          <div>
            <div className="text-3xl font-bold text-blue-600 mb-2">
              {categories?.length ? Math.round((posts?.length || 0) / categories.length) : 0}
            </div>
            <div className="text-gray-600">Avg Articles per Category</div>
          </div>
        </div>
      </div>
    </div>
  )
} 