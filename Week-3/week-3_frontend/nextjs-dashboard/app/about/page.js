import Link from 'next/link'

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <Link href="/" className="text-2xl font-bold text-gray-800">
            Start Bootstrap
          </Link>
          <div className="flex gap-6">
            <Link href="/" className="text-gray-600 hover:text-gray-900">Home</Link>
            <Link href="/about" className="text-blue-600 font-semibold">About</Link>
            <Link href="/dashboard" className="text-gray-600 hover:text-gray-900">Dashboard</Link>
          </div>
        </div>
      </nav>

      <div className="container mx-auto px-4 py-16 max-w-4xl">
        <h1 className="text-5xl font-bold text-gray-800 mb-6">About This Project</h1>
        
        <div className="bg-white rounded-lg shadow-md p-8 mb-8">
          <h2 className="text-3xl font-bold text-gray-800 mb-4">Day 3 - Next.js Routing & Layouts</h2>
          <p className="text-gray-600 text-lg mb-4">
            This project demonstrates the power of Next.js App Router with nested layouts and server/client components.
          </p>
          
          <div className="bg-blue-50 border-l-4 border-blue-500 p-4 mb-6">
            <h3 className="font-bold text-blue-800 mb-2">Key Features:</h3>
            <ul className="list-disc list-inside text-gray-700 space-y-2">
              <li>File-based routing system</li>
              <li>Nested layouts for dashboard</li>
              <li>Shared navigation components</li>
              <li>Server and Client Components</li>
              <li>Responsive sidebar with hamburger menu</li>
            </ul>
          </div>

          <h3 className="text-2xl font-bold text-gray-800 mb-3">Technologies Used</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <div className="bg-gray-100 p-4 rounded text-center">
              <p className="font-semibold">Next.js 14</p>
            </div>
            <div className="bg-gray-100 p-4 rounded text-center">
              <p className="font-semibold">React 18</p>
            </div>
            <div className="bg-gray-100 p-4 rounded text-center">
              <p className="font-semibold">Tailwind CSS</p>
            </div>
            <div className="bg-gray-100 p-4 rounded text-center">
              <p className="font-semibold">Recharts</p>
            </div>
          </div>
        </div>

        <div className="text-center">
          <Link 
            href="/dashboard"
            className="inline-block bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition"
          >
            Explore Dashboard →
          </Link>
        </div>
      </div>
    </div>
  )
}