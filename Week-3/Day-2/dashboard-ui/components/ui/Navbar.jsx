export default function Navbar() {
  return (
    <header className="h-16 bg-gray-800 border-b border-gray-700 flex items-center justify-between px-6">
      {/* Logo Section */}
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 bg-blue-600 rounded flex items-center justify-center text-white font-bold text-xl">
          📈
        </div>
        <h1 className="font-semibold text-lg text-white">Hesta Analytics</h1>
      </div>

      {/* Right Section */}
      <div className="flex items-center gap-4">
        {/* Search Input */}
        <div className="relative">
          <input 
            placeholder="Search..." 
            className="bg-gray-700 text-white placeholder-gray-400 border border-gray-600 px-4 py-2 pl-10 rounded text-sm w-64 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <span className="absolute left-3 top-2.5 text-gray-400">🔍</span>
        </div>

        {/* Notification Bell */}
        <button className="text-gray-300 hover:text-white relative">
          <span className="text-xl">🔔</span>
          <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-4 h-4 flex items-center justify-center">
            3
          </span>
        </button>

        {/* User Profile */}
        <div className="flex items-center gap-2 cursor-pointer hover:opacity-80">
          <div className="w-9 h-9 bg-blue-600 rounded-full flex items-center justify-center text-white font-semibold">
            👤
          </div>
        </div>
      </div>
    </header>
  );
}