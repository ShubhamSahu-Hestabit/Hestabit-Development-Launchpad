export default function Navbar() {
  return (
    <header className="h-16 flex items-center justify-between bg--200 border-b px-6">

      {/* Left: Logo + Title */}
      <div className="flex items-center gap-2 text-lg font-semibold text-gray-800">
        <span className="text-xl">📊</span>
        <span>Hesta Analytics</span>
      </div>

      {/* Right: Search + User */}
      <div className="flex items-center gap-4">

        <div className="flex">
          <input
            type="text"
            placeholder="Search for..."
            className="border border-gray-300 px-3 py-1 rounded-l-md text-sm focus:outline-none"
          />
          <button className="bg-blue-600 text-white px-3 rounded-r-md">
            🔍
          </button>
        </div>

        <div className="w-8 h-8 rounded-full bg-gray-400 flex items-center justify-center cursor-pointer">
          👤
        </div>

      </div>
    </header>
  );
}
