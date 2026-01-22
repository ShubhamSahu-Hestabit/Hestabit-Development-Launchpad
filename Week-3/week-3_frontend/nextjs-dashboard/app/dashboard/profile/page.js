export default function ProfilePage() {
  return (
    <div className="container-fluid px-4">
      <h1 className="mt-4 text-2xl font-bold text-gray-800">User Profile</h1>
      <ol className="flex mb-4 text-sm text-gray-500 gap-2">
        <li className="hover:text-blue-600 cursor-pointer">Dashboard</li>
        <li>/</li>
        <li className="text-gray-400">Profile</li>
      </ol>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Left Column: Profile Picture Card */}
        <div className="lg:col-span-1">
          <div className="bg-white border border-gray-200 rounded-lg shadow-sm overflow-hidden">
            <div className="bg-gray-50 px-4 py-3 border-b border-gray-200">
              <h3 className="font-semibold text-gray-700">Profile Picture</h3>
            </div>
            <div className="p-6 text-center">
              <div className="w-32 h-32 bg-blue-600 rounded-full mx-auto flex items-center justify-center text-white text-4xl font-bold mb-4">
                👤
              </div>
              <p className="text-sm text-gray-500 mb-4">JPG or PNG no larger than 5 MB</p>
              <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded text-sm transition-colors">
                Upload New Image
              </button>
            </div>
          </div>
        </div>

        {/* Right Column: Account Details Form */}
        <div className="lg:col-span-2">
          <div className="bg-white border border-gray-200 rounded-lg shadow-sm">
            <div className="bg-gray-50 px-4 py-3 border-b border-gray-200">
              <h3 className="font-semibold text-gray-700">Account Details</h3>
            </div>
            <div className="p-6">
              <form className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">First Name</label>
                    <input type="text" defaultValue="Valerie" className="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 outline-none" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Last Name</label>
                    <input type="text" defaultValue="Luna" className="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 outline-none" />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Email address</label>
                  <input type="email" defaultValue="name@example.com" className="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 outline-none" />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Phone number</label>
                    <input type="text" defaultValue="555-123-4567" className="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 outline-none" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Birthday</label>
                    <input type="text" defaultValue="06/10/1988" className="w-full border border-gray-300 rounded px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 outline-none" />
                  </div>
                </div>

                <div className="pt-4 border-t border-gray-100 flex justify-end">
                  <button type="button" className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded text-sm font-medium transition-colors">
                    Save Changes
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>

      </div>
    </div>
  )
}