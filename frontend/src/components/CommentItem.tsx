'use client'

import { useState } from 'react'
import { User, MessageCircle, Heart, Reply, MoreVertical } from 'lucide-react'
import { formatDistanceToNow } from 'date-fns'
import { Comment } from '@/types'
import api from '@/lib/api'
import toast from 'react-hot-toast'

interface CommentItemProps {
  comment: Comment
  postId: string
  onCommentAdded: () => void
  level?: number
}

export default function CommentItem({ comment, postId, onCommentAdded, level = 0 }: CommentItemProps) {
  const [showReplyForm, setShowReplyForm] = useState(false)
  const [replyContent, setReplyContent] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleReply = async () => {
    if (!replyContent.trim()) return

    setIsSubmitting(true)
    try {
      await api.post('/comments/', {
        content: replyContent,
        post_id: postId,
        parent_id: comment.id
      })
      setReplyContent('')
      setShowReplyForm(false)
      onCommentAdded()
      toast.success('Reply added!')
    } catch (error: any) {
      console.error('Error adding reply:', error)
      const message = error.response?.data?.detail || 'Failed to add reply'
      toast.error(message)
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleLike = async () => {
    try {
      await api.post('/reactions/', {
        post: postId,
        type: 'like'
      })
      toast.success('Comment liked!')
    } catch (error) {
      toast.error('Failed to like comment')
    }
  }

  const maxLevel = 3 // Maximum nesting level
  const isMaxLevel = level >= maxLevel

  return (
    <div className={`${level > 0 ? 'ml-8 border-l-2 border-gray-100 pl-4' : ''}`}>
      <div className="border-b border-gray-100 pb-6 mb-6">
        <div className="flex items-start space-x-3">
          <div className="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center flex-shrink-0">
            <User className="w-4 h-4 text-gray-600" />
          </div>
          <div className="flex-1 min-w-0">
            <div className="flex items-center space-x-2 mb-2">
              <p className="font-medium text-gray-900">
                {comment.author.first_name && comment.author.last_name
                  ? `${comment.author.first_name} ${comment.author.last_name}`
                  : comment.author.username}
              </p>
              <span className="text-sm text-gray-500">
                {formatDistanceToNow(new Date(comment.created_at), { addSuffix: true })}
              </span>
              {comment.is_edited && (
                <span className="text-xs text-gray-400">(edited)</span>
              )}
            </div>
            <p className="text-gray-700 mb-3">{comment.content}</p>
            
            {/* Action buttons */}
            <div className="flex items-center space-x-4 text-sm">
              <button
                onClick={handleLike}
                className="flex items-center text-gray-600 hover:text-red-600 transition-colors"
              >
                <Heart className="w-4 h-4 mr-1" />
                {comment.likes_count || 0}
              </button>
              
              {!isMaxLevel && (
                <button
                  onClick={() => setShowReplyForm(!showReplyForm)}
                  className="flex items-center text-gray-600 hover:text-blue-600 transition-colors"
                >
                  <Reply className="w-4 h-4 mr-1" />
                  Reply
                </button>
              )}
              
              {(comment.reply_count || 0) > 0 && (
                <span className="text-gray-500">
                  {comment.reply_count || 0} {(comment.reply_count || 0) === 1 ? 'reply' : 'replies'}
                </span>
              )}
            </div>

            {/* Reply form */}
            {showReplyForm && !isMaxLevel && (
              <div className="mt-4">
                <textarea
                  value={replyContent}
                  onChange={(e) => setReplyContent(e.target.value)}
                  placeholder="Write a reply..."
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent focus:outline-none resize-none"
                  rows={3}
                />
                <div className="mt-2 flex justify-end space-x-2">
                  <button
                    onClick={() => setShowReplyForm(false)}
                    className="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={handleReply}
                    disabled={!replyContent.trim() || isSubmitting}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {isSubmitting ? 'Posting...' : 'Post Reply'}
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Render replies */}
      {comment.replies && comment.replies.length > 0 && (
        <div className="space-y-4">
          {comment.replies.map((reply) => (
            <CommentItem
              key={reply.id}
              comment={reply}
              postId={postId}
              onCommentAdded={onCommentAdded}
              level={level + 1}
            />
          ))}
        </div>
      )}
    </div>
  )
} 