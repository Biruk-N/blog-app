'use client'

import { useQuery } from '@tanstack/react-query'
import { useParams } from 'next/navigation'
import api from '@/lib/api'
import { Post, Comment } from '@/types'
import { formatDistanceToNow } from 'date-fns'
import {
  Clock,
  Eye,
  User,
  Calendar,
  Tag,
  MessageCircle,
  Heart,
  Share2,
  Bookmark,
  ArrowLeft
} from 'lucide-react'
import Link from 'next/link'
import { useState } from 'react'
import toast from 'react-hot-toast'
import CommentItem from './CommentItem'

interface BlogDetailProps {
  id: string
}

export default function BlogDetail({ id }: BlogDetailProps) {
  const [showComments, setShowComments] = useState(false)
  const [newComment, setNewComment] = useState('')

  const { data: post, isLoading, error } = useQuery<Post>({
    queryKey: ['post', id],
    queryFn: async () => {
      const response = await api.get(`/posts/${id}/`)
      return response.data
    },
    enabled: !!id,
  })

  const { data: comments, refetch: refetchComments } = useQuery<Comment[]>({
    queryKey: ['comments', id],
    queryFn: async () => {
      const response = await api.get(`/comments/for_post/?post_id=${post?.id}`)
      return response.data
    },
    enabled: !!post?.id,
  })

  const handleLike = async () => {
    if (!post) return
    try {
      await api.post('/reactions/', {
        post: post.id,
        type: 'like'
      })
      toast.success('Post liked!')
    } catch (error) {
      toast.error('Failed to like post')
    }
  }

  const handleShare = () => {
    if (navigator.share) {
      navigator.share({
        title: post?.title,
        text: post?.excerpt,
        url: window.location.href,
      })
    } else {
      navigator.clipboard.writeText(window.location.href)
      toast.success('Link copied to clipboard!')
    }
  }

  const handleComment = async () => {
    if (!post || !newComment.trim()) return
    try {
      await api.post('/comments/', {
        content: newComment,
        post_id: post.id
      })
      setNewComment('')
      refetchComments()
      toast.success('Comment added!')
    } catch (error: any) {
      console.error('Error adding comment:', error)
      const message = error.response?.data?.detail || 'Failed to add comment'
      toast.error(message)
    }
  }

  if (isLoading) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-3/4 mb-4"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2 mb-8"></div>
          <div className="h-96 bg-gray-200 rounded mb-8"></div>
          <div className="space-y-4">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="h-4 bg-gray-200 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  if (error || !post) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Post Not Found</h1>
          <p className="text-gray-600 mb-8">The post you're looking for doesn't exist.</p>
          <Link
            href="/blog"
            className="inline-flex items-center text-blue-600 hover:text-blue-700"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Blog
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {/* Back Button */}
      <Link
        href="/blog"
        className="inline-flex items-center text-gray-600 hover:text-gray-900 mb-8"
      >
        <ArrowLeft className="w-4 h-4 mr-2" />
        Back to Blog
      </Link>

      {/* Featured Image */}
      {post.featured_image && (
        <div className="mb-8">
          <img
            src={post.featured_image}
            alt={post.title}
            className="w-full h-96 object-cover rounded-lg"
          />
        </div>
      )}

      {/* Article Header */}
      <article className="mb-8">
        {/* Category and Date */}
        <div className="flex items-center text-sm text-gray-500 mb-4">
          <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-xs font-medium">
            {post.category.name}
          </span>
          <span className="mx-3">•</span>
          <div className="flex items-center">
            <Calendar className="w-4 h-4 mr-1" />
            {formatDistanceToNow(new Date(post.published_at || post.created_at), { addSuffix: true })}
          </div>
        </div>

        {/* Title */}
        <h1 className="text-4xl font-bold text-gray-900 mb-4 leading-tight">
          {post.title}
        </h1>

        {/* Excerpt */}
        {post.excerpt && (
          <p className="text-xl text-gray-600 mb-6 leading-relaxed">
            {post.excerpt}
          </p>
        )}

        {/* Author and Stats */}
        <div className="flex items-center justify-between border-b border-gray-200 pb-6 mb-8">
          <div className="flex items-center">
            <div className="w-12 h-12 bg-gray-200 rounded-full flex items-center justify-center mr-4">
              <User className="w-6 h-6 text-gray-600" />
            </div>
            <div>
              <p className="font-medium text-gray-900">
                {post.author.first_name && post.author.last_name
                  ? `${post.author.first_name} ${post.author.last_name}`
                  : post.author.username}
              </p>
              <p className="text-sm text-gray-500">Author</p>
            </div>
          </div>
          <div className="flex items-center space-x-6 text-sm text-gray-500">
            <div className="flex items-center">
              <Clock className="w-4 h-4 mr-1" />
              {post.reading_time || post.read_time || 1} min read
            </div>
            <div className="flex items-center">
              <Eye className="w-4 h-4 mr-1" />
              {post.view_count || 0} views
            </div>
          </div>
        </div>
      </article>

      {/* Article Content */}
      <div className="prose prose-lg max-w-none mb-8">
        <div dangerouslySetInnerHTML={{ __html: post.content }} />
      </div>

      {/* Tags */}
      {post.tags && post.tags.length > 0 && (
        <div className="mb-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Tags</h3>
          <div className="flex flex-wrap gap-2">
            {post.tags.map((tag) => (
              <Link
                key={tag.id}
                href={`/blog/tag/${tag.slug}`}
                className="inline-flex items-center px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm hover:bg-gray-200 transition-colors"
              >
                <Tag className="w-3 h-3 mr-1" />
                {tag.name}
              </Link>
            ))}
          </div>
        </div>
      )}

      {/* Action Buttons */}
      <div className="flex items-center justify-between border-t border-gray-200 pt-6 mb-8">
        <div className="flex items-center space-x-4">
          <button
            onClick={handleLike}
            className="flex items-center text-gray-600 hover:text-red-600 transition-colors"
          >
            <Heart className="w-5 h-5 mr-2" />
            Like
          </button>
          <button
            onClick={() => setShowComments(!showComments)}
            className="flex items-center text-gray-600 hover:text-blue-600 transition-colors"
          >
            <MessageCircle className="w-5 h-5 mr-2" />
            {comments?.length || 0} Comments
          </button>
        </div>
        <div className="flex items-center space-x-4">
          <button
            onClick={handleShare}
            className="flex items-center text-gray-600 hover:text-blue-600 transition-colors"
          >
            <Share2 className="w-5 h-5 mr-2" />
            Share
          </button>
          <button className="flex items-center text-gray-600 hover:text-blue-600 transition-colors">
            <Bookmark className="w-5 h-5 mr-2" />
            Save
          </button>
        </div>
      </div>

      {/* Comments Section */}
      {showComments && (
        <div className="border-t border-gray-200 pt-8">
          <h3 className="text-xl font-bold text-gray-900 mb-6">
            Comments ({comments?.length || 0})
          </h3>

          {/* Add Comment */}
          <div className="mb-8">
            <textarea
              value={newComment}
              onChange={(e) => setNewComment(e.target.value)}
              placeholder="Write a comment..."
              className="w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
              rows={3}
            />
            <div className="mt-2 flex justify-end">
              <button
                onClick={handleComment}
                disabled={!newComment.trim()}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Post Comment
              </button>
            </div>
          </div>

                 {/* Comments List */}
                 <div className="space-y-6">
                   {comments?.map((comment) => (
                     <CommentItem
                       key={comment.id}
                       comment={comment}
                       postId={post.id}
                       onCommentAdded={refetchComments}
                     />
                   ))}
                   {(!comments || comments.length === 0) && (
                     <p className="text-gray-500 text-center py-8">No comments yet. Be the first to comment!</p>
                   )}
                 </div>
        </div>
      )}
    </div>
  )
} 