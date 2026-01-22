import Link from 'next/link'

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center text-white">
          <h1 className="text-6xl font-bold mb-6">Welcome to Dashboard</h1>
          <p className="text-2xl mb-12 opacity-90">
            A modern Next.js application with routing and layouts
          </p>
          
          <div className="flex gap-6 justify-center flex-wrap">
            <Link 
              href="/dashboard"
              className="bg-white text-blue-600 px-8 py-4 rounded-lg text-xl font-semibold hover:bg-gray-100 transition-all transform hover:scale-105 shadow-lg"
            >
              Go to Dashboard
            </Link>
            
            <Link 
              href="/about"
              className="bg-transparent border-2 border-white text-white px-8 py-4 rounded-lg text-xl font-semibold hover:bg-white hover:text-blue-600 transition-all transform hover:scale-105"
            >
              About
            </Link>
          </div>

          <div className="mt-20 grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <div className="bg-white/10 backdrop-blur-lg p-8 rounded-xl">
              <h3 className="text-2xl font-bold mb-3">🚀 Fast</h3>
              <p>Built with Next.js 14 for optimal performance</p>
            </div>
            <div className="bg-white/10 backdrop-blur-lg p-8 rounded-xl">
              <h3 className="text-2xl font-bold mb-3">🎨 Beautiful</h3>
              <p>Modern UI with Tailwind CSS</p>
            </div>
            <div className="bg-white/10 backdrop-blur-lg p-8 rounded-xl">
              <h3 className="text-2xl font-bold mb-3">📱 Responsive</h3>
              <p>Works perfectly on all devices</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}