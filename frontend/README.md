# DevLogg Frontend

A modern, Medium-like blog platform frontend built with Next.js 15, TypeScript, and Tailwind CSS.

## 🚀 Features

- **Modern UI/UX**: Clean, responsive design inspired by Medium
- **Rich Text Editor**: TipTap-powered editor with markdown support
- **Authentication**: JWT-based auth with automatic token refresh
- **Real-time Updates**: TanStack Query for efficient data fetching
- **Type Safety**: Full TypeScript support
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **SEO Optimized**: Next.js App Router with metadata support

## 🛠️ Tech Stack

- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Rich Text Editor**: TipTap
- **State Management**: TanStack Query
- **Forms**: React Hook Form + Zod validation
- **Icons**: Lucide React
- **HTTP Client**: Axios
- **Notifications**: React Hot Toast

## 📦 Installation

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env.local
   ```
   
   Update `.env.local` with your API URL:
   ```env
   NEXT_PUBLIC_API_BASE_URL=https://blog-app-api-jyib.onrender.com/api
   ```

3. **Run the development server**:
```bash
npm run dev
   ```

4. **Open your browser**:
   Navigate to [http://localhost:3000](http://localhost:3000)

## 🏗️ Project Structure

```
src/
├── app/                    # Next.js App Router
│   ├── login/             # Authentication pages
│   ├── register/
│   ├── dashboard/         # Protected routes
│   ├── blog/              # Blog pages
│   ├── write/             # Post editor
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/            # Reusable components
│   ├── Navbar.tsx         # Navigation
│   ├── RichTextEditor.tsx # TipTap editor
│   └── ui/               # UI components
├── lib/                  # Utilities
│   ├── api.ts           # Axios configuration
│   ├── auth.ts          # Authentication helpers
│   └── queryClient.ts   # React Query setup
└── types/               # TypeScript definitions
    └── index.ts         # API types
```

## 🔐 Authentication

The app uses JWT authentication with automatic token refresh:

- **Login**: `/login` - Sign in with email/password
- **Register**: `/register` - Create new account
- **Token Storage**: localStorage with automatic refresh
- **Protected Routes**: Automatic redirect to login

## ✍️ Rich Text Editor

The TipTap editor includes:

- **Text Formatting**: Bold, italic, headings, lists
- **Code Blocks**: Syntax highlighting
- **Links & Images**: Easy insertion
- **Markdown Support**: Keyboard shortcuts
- **Real-time Preview**: Live content updates

## 📱 Responsive Design

- **Mobile-first**: Optimized for all screen sizes
- **Touch-friendly**: Gesture support for mobile
- **Progressive Enhancement**: Works without JavaScript
- **Accessibility**: WCAG 2.1 compliant

## 🚀 Deployment

### Vercel (Recommended)

1. **Connect your repository** to Vercel
2. **Set environment variables**:
   ```
   NEXT_PUBLIC_API_BASE_URL=https://blog-app-api-jyib.onrender.com/api
   ```
3. **Deploy**: Automatic deployment on push

### Render

1. **Create a new Static Site**
2. **Connect your repository**
3. **Set build command**: `npm run build`
4. **Set publish directory**: `.next`
5. **Add environment variables**

## 🔧 Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript check

### Code Style

- **ESLint**: Configured for Next.js
- **Prettier**: Automatic code formatting
- **TypeScript**: Strict mode enabled
- **Tailwind**: Utility-first CSS

## 📊 Performance

- **Image Optimization**: Next.js Image component
- **Code Splitting**: Automatic route-based splitting
- **Caching**: TanStack Query for API responses
- **Bundle Analysis**: Built-in webpack analyzer

## 🔒 Security

- **JWT Tokens**: Secure token storage
- **CSRF Protection**: Built-in Next.js protection
- **XSS Prevention**: React's built-in escaping
- **HTTPS Only**: Production deployment

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Add tests if applicable**
5. **Submit a pull request**

## 📝 License

MIT License - see [LICENSE](../LICENSE) for details.

## 🆘 Support

- **Documentation**: Check the docs folder
- **Issues**: Create a GitHub issue
- **Discussions**: Use GitHub discussions

---

Built with ❤️ using Next.js and Tailwind CSS
