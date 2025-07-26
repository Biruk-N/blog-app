'use client'

import { useQuery } from '@tanstack/react-query'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'
import { Plus, Edit, Eye, Trash2, Calendar, User, BarChart3, FileText } from 'lucide-react'
import Link from 'next/link'
import api from '@/lib/api'
import { Post, User as UserType } from '@/types'
import { isAuthenticated, getUser } from '@/lib/auth'
import toast from 'react-hot-toast'

export default function DashboardPage() {
  const router = useRouter()

  // Check authentication on mount
  useEffect(() => {
    if (!isAuthenticated()) {
      router.push('/login')
      toast.error('Please login to access the dashboard')
    }
  }, [router])

  const { data: user } = useQuery<UserType>({
    queryKey: ['user'],
    queryFn: async () => {
      const response = await api.get('/users/me/')
      return response.data
    },
    enabled: isAuthenticated(),
  })

  const { data: posts, isLoading: postsLoading } = useQuery<Post[]>({
    queryKey: ['user-posts'],
    queryFn: async () => {
      const response = await api.get('/posts/')
      return response.data.results || response.data
    },
    enabled: isAuthenticated(),
  })

  const { data: stats } = useQuery({
    queryKey: ['user-stats'],
    queryFn: async () => {
      const [postsRes, commentsRes] = await Promise.all([
        api.get('/posts/my-posts/'),
        api.get('/comments/my-comments/')
      ])
      return {
        totalPosts: postsRes.data.count || postsRes.data.length || 0,
        publishedPosts: (postsRes.data.results || postsRes.data).filter((post: Post) => post.status === 'published').length,
        totalComments: commentsRes.data.count || commentsRes.data.length || 0,
      }
    },
    enabled: isAuthenticated(),
  })

  if (!isAuthenticated()) {
    return null
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Dashboard</h1>
        <p className="text-gray-600">Welcome back, {user?.first_name || user?.username}!</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 rounded-lg">
              <FileText className="w-6 h-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Posts</p>
              <p className="text-2xl font-bold text-gray-900">{stats?.totalPosts || 0}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center">
            <div className="p-2 bg-green-100 rounded-lg">
              <Eye className="w-6 h-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Published Posts</p>
              <p className="text-2xl font-bold text-gray-900">{stats?.publishedPosts || 0}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center">
            <div className="p-2 bg-purple-100 rounded-lg">
              <User className="w-6 h-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Comments</p>
              <p className="text-2xl font-bold text-gray-900">{stats?.totalComments || 0}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 mb-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h2>
        <div className="flex flex-wrap gap-4">
          <Link
            href="/write"
            className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Plus className="w-4 h-4 mr-2" />
            Write New Post
          </Link>
          <Link
            href="/profile"
            className="inline-flex items-center px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
          >
            <User className="w-4 h-4 mr-2" />
            Edit Profile
          </Link>
        </div>
      </div>

      {/* Recent Posts */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <div className="p-6 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold text-gray-900">Recent Posts</h2>
            <Link
              href="/blog"
              className="text-blue-600 hover:text-blue-700 text-sm font-medium"
            >
              View All
            </Link>
          </div>
        </div>

        <div className="p-6">
          {postsLoading ? (
            <div className="space-y-4">
              {[...Array(3)].map((_, i) => (
                <div key={i} className="animate-pulse">
                  <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                  <div className="h-3 bg-gray-200 rounded w-1/2"></div>
                </div>
              ))}
            </div>
          ) : posts && posts.length > 0 ? (
            <div className="space-y-6">
              {posts.slice(0, 5).map((post) => (
                <div key={post.id} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                  <div className="flex-1">
                    <h3 className="font-medium text-gray-900 mb-1">{post.title}</h3>
                    <div className="flex items-center text-sm text-gray-500 space-x-4">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        post.status === 'published' 
                          ? 'bg-green-100 text-green-800' 
                          : post.status === 'draft'
                          ? 'bg-yellow-100 text-yellow-800'
                          : 'bg-gray-100 text-gray-800'
                      }`}>
                        {post.status}
                      </span>
                      <span className="flex items-center">
                        <Calendar className="w-3 h-3 mr-1" />
                        {new Date(post.created_at).toLocaleDateString()}
                      </span>
                      <span className="flex items-center">
                        <Eye className="w-3 h-3 mr-1" />
                        {post.view_count} views
                      </span>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Link
                      href={`/blog/${post.id}`}
                      className="p-2 text-gray-600 hover:text-blue-600 transition-colors"
                      title="View Post"
                    >
                      <Eye className="w-4 h-4" />
                    </Link>
                    <Link
                      href={`/write?edit=${post.id}`}
                      className="p-2 text-gray-600 hover:text-green-600 transition-colors"
                      title="Edit Post"
                    >
                      <Edit className="w-4 h-4" />
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <FileText className="w-12 h-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No posts yet</h3>
              <p className="text-gray-600 mb-4">Start writing your first blog post!</p>
              <Link
                href="/write"
                className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                <Plus className="w-4 h-4 mr-2" />
                Write Your First Post
              </Link>
            </div>
          )}
        </div>
      </div>
    </div>
  )
} 