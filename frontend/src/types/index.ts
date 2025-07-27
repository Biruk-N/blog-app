export interface User {
  id: string;
  username: string;
  email: string;
  first_name?: string;
  last_name?: string;
  bio?: string;
  avatar?: string | null;
  website?: string;
  location?: string;
  date_of_birth?: string | null;
  is_verified?: boolean;
  is_staff?: boolean;
  is_active?: boolean;
  date_joined: string;
  last_login?: string;
}

export interface Category {
  id: string;
  name: string;
  slug: string;
  description?: string;
  created_at: string;
  updated_at: string;
}

export interface Tag {
  id: string;
  name: string;
  slug: string;
  created_at: string;
  updated_at: string;
}

export interface Post {
  id: string;
  title: string;
  slug: string;
  content: string;
  excerpt?: string;
  featured_image?: string;
  status: 'draft' | 'published' | 'archived';
  author: User;
  category: Category;
  tags: Tag[];
  read_time?: number; // Legacy field
  reading_time?: number; // New field
  view_count: number;
  unique_views_count?: number;
  word_count?: number;
  character_count?: number;
  created_at: string;
  updated_at: string;
  published_at?: string;
}

export interface Comment {
  id: string;
  content: string;
  author: User;
  post: string; // post ID
  parent?: string | null; // parent comment ID
  status: 'pending' | 'approved' | 'rejected';
  created_at: string;
  updated_at: string;
  is_edited?: boolean;
  likes_count?: number;
  replies?: Comment[];
  reply_count?: number;
}

export interface Reaction {
  id: string;
  type: 'like' | 'love' | 'laugh' | 'wow' | 'sad' | 'angry';
  user: User;
  post: string; // post ID
  created_at: string;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterCredentials {
  username: string;
  email: string;
  password: string;
  first_name?: string;
  last_name?: string;
}

export interface CreatePostData {
  title: string;
  content: string;
  excerpt?: string;
  category_id: string;
  tag_ids: string[];
  status?: 'draft' | 'published';
  featured_image?: string;
}

export interface UpdatePostData extends Partial<CreatePostData> {
  id: string;
}

export interface CreateCommentData {
  content: string;
  post_id: string;
  parent_id?: string;
}

export interface ApiResponse<T> {
  data: T;
  message?: string;
  status: 'success' | 'error';
}

export interface PaginatedResponse<T> {
  count: number;
  next?: string;
  previous?: string;
  results: T[];
} 