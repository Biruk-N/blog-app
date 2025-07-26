'use client'

import { useParams } from 'next/navigation'
import BlogDetail from '@/components/BlogDetail'

export default function BlogPostPage() {
  const params = useParams()
  const id = params.slug as string

  return <BlogDetail id={id} />
} 