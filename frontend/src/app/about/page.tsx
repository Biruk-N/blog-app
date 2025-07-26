export default function AboutPage() {
  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      {/* Header */}
      <div className="text-center mb-16">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">About DevLogg</h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          A modern platform for developers to write, publish, and share technical content with the world.
        </p>
      </div>

      {/* Mission Section */}
      <div className="mb-16">
        <h2 className="text-3xl font-bold text-gray-900 mb-6">Our Mission</h2>
        <div className="bg-blue-50 rounded-lg p-8">
          <p className="text-lg text-gray-700 leading-relaxed">
            DevLogg was created with a simple mission: to provide developers with a beautiful, 
            powerful platform to share their knowledge, experiences, and insights with the 
            global developer community. We believe that knowledge sharing is the foundation 
            of innovation and growth in the tech industry.
          </p>
        </div>
      </div>

      {/* Features Grid */}
      <div className="mb-16">
        <h2 className="text-3xl font-bold text-gray-900 mb-8">What We Offer</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-100">
            <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
              <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">Rich Text Editor</h3>
            <p className="text-gray-600">
              Write beautiful articles with our powerful TipTap editor. Support for markdown, 
              code blocks, images, and more.
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-100">
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
              <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">Community Features</h3>
            <p className="text-gray-600">
              Engage with readers through comments, likes, and reactions. Build your 
              developer community and network.
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-100">
            <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
              <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 4V2a1 1 0 011-1h8a1 1 0 011 1v2m-9 0h10m-10 0a2 2 0 00-2 2v14a2 2 0 002 2h10a2 2 0 002-2V6a2 2 0 00-2-2" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">Content Organization</h3>
            <p className="text-gray-600">
              Organize your content with categories and tags. Make it easy for readers 
              to discover your articles.
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6 border border-gray-100">
            <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center mb-4">
              <svg className="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">Fast & Responsive</h3>
            <p className="text-gray-600">
              Built with Next.js and modern web technologies for lightning-fast 
              performance and mobile-first design.
            </p>
          </div>
        </div>
      </div>

      {/* Technology Stack */}
      <div className="mb-16">
        <h2 className="text-3xl font-bold text-gray-900 mb-8">Technology Stack</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div>
            <h3 className="text-xl font-bold text-gray-900 mb-4">Frontend</h3>
            <ul className="space-y-2 text-gray-600">
              <li>• Next.js 15 (App Router)</li>
              <li>• TypeScript</li>
              <li>• Tailwind CSS</li>
              <li>• TipTap Rich Text Editor</li>
              <li>• TanStack Query</li>
              <li>• React Hook Form + Zod</li>
            </ul>
          </div>
          <div>
            <h3 className="text-xl font-bold text-gray-900 mb-4">Backend</h3>
            <ul className="space-y-2 text-gray-600">
              <li>• Django 4.2+</li>
              <li>• Django REST Framework</li>
              <li>• PostgreSQL</li>
              <li>• JWT Authentication</li>
              <li>• Docker</li>
              <li>• Render Deployment</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Team Section */}
      <div className="mb-16">
        <h2 className="text-3xl font-bold text-gray-900 mb-8">The Team</h2>
        <div className="bg-gray-50 rounded-lg p-8">
          <p className="text-lg text-gray-700 mb-6">
            DevLogg is built by developers, for developers. Our team is passionate about 
            creating tools that help the developer community grow and learn together.
          </p>
          <p className="text-gray-600">
            We believe in open source, transparency, and community-driven development. 
            If you're interested in contributing or have ideas for improvement, 
            we'd love to hear from you!
          </p>
        </div>
      </div>

      {/* Contact Section */}
      <div className="text-center">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">Get in Touch</h2>
        <p className="text-lg text-gray-600 mb-8">
          Have questions, suggestions, or want to contribute? We'd love to hear from you!
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <a
            href="mailto:hello@devlogg.com"
            className="inline-flex items-center justify-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
          >
            Contact Us
          </a>
          <a
            href="https://github.com/your-repo"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center justify-center px-6 py-3 border border-gray-300 text-base font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
          >
            View on GitHub
          </a>
        </div>
      </div>
    </div>
  )
} 