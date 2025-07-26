import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import Navbar from '@/components/Navbar'
import Providers from '@/components/Providers'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'DevLogg - Developer Blog Platform',
  description: 'A modern platform for developers to write, publish, and share technical content.',
  keywords: 'blog, developer, programming, tech, articles',
  authors: [{ name: 'DevLogg Team' }],
  openGraph: {
    title: 'DevLogg - Developer Blog Platform',
    description: 'A modern platform for developers to write, publish, and share technical content.',
    type: 'website',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Providers>
          <Navbar />
          {children}
        </Providers>
      </body>
    </html>
  )
}
