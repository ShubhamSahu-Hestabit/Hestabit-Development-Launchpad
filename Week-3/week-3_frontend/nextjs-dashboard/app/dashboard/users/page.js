const users = [
  {
    name: "User",
    email: "user@example.com",
    role: "User",
    created: "18/10/2024 05:27",
    updated: "18/10/2024 05:27",
  },
  {
    name: "Dr. Ray Stoltenberg",
    email: "rosalinda42@example.com",
    role: "User",
    created: "18/10/2024 05:27",
    updated: "18/10/2024 05:27",
  },
  {
    name: "Mrs. Mertie Murray MD",
    email: "ernser.susanna@example.net",
    role: "User",
    created: "18/10/2024 05:27",
    updated: "18/10/2024 05:27",
  },
  {
    name: "Gilbert Rice",
    email: "willard.walter@example.org",
    role: "User",
    created: "18/10/2024 05:27",
    updated: "18/10/2024 05:27",
  },
  {
    name: "Sydnie Rau",
    email: "doug.padberg@example.org",
    role: "User",
    created: "18/10/2024 05:27",
    updated: "18/10/2024 05:27",
  },
  {
    name: "Mr. Arvid Veum DDS",
    email: "schinner.meaghan@example.org",
    role: "User",
    created: "18/10/2024 05:27",
    updated: "18/10/2024 05:27",
  },
  {
    name: "Jayme Beier DDS",
    email: "orn.ahmed@example.com",
    role: "User",
    created: "18/10/2024 05:27",
    updated: "18/10/2024 05:27",
  },
  {
    name: "Uriah Swaniawski",
    email: "wilburn.champlin@example.org",
    role: "User",
    created: "18/10/2024 05:27",
    updated: "18/10/2024 05:27",
  },
  {
    name: "Rosanna Heaney",
    email: "boconner@example.com",
    role: "User",
    created: "18/10/2024 05:27",
    updated: "18/10/2024 05:27",
  },
  {
    name: "Adan Reichel",
    email: "mya.labadie@example.com",
    role: "User",
    created: "18/10/2024 05:27",
    updated: "18/10/2024 05:27",
  },
];

export default function UsersPage() {
  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      {/* Breadcrumb */}
      <p className="text-sm text-gray-500 mb-1">Users &gt; List</p>
      <h1 className="text-2xl font-semibold text-gray-800 mb-4">
        Users
      </h1>

      <div className="bg-white rounded-xl shadow">
        {/* Search */}
        <div className="p-4 flex justify-end">
          <div className="relative">
            <input
              type="text"
              placeholder="Search"
              className="h-10 w-64 pl-10 pr-4 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400"
            />
            <span className="absolute left-3 top-2.5 text-gray-400">
              🔍
            </span>
          </div>
        </div>

        {/* Table */}
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="border-t border-b bg-gray-50 text-gray-500">
              <tr>
                <th className="p-4 text-left">Name ↓</th>
                <th className="p-4 text-left">Email ↓</th>
                <th className="p-4 text-left">Role ↓</th>
                <th className="p-4 text-left">Created at</th>
                <th className="p-4 text-left">Updated at</th>
                <th className="p-4"></th>
              </tr>
            </thead>
            <tbody>
              {users.map((u, i) => (
                <tr
                  key={i}
                  className="border-b last:border-none hover:bg-gray-50"
                >
                  <td className="p-4">{u.name}</td>
                  <td className="p-4 text-gray-600">{u.email}</td>
                  <td className="p-4">{u.role}</td>
                  <td className="p-4">{u.created}</td>
                  <td className="p-4">{u.updated}</td>
                  <td className="p-4 text-indigo-600 text-center cursor-pointer">
                    🗑
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Footer */}
        <div className="p-4 flex items-center justify-between text-sm text-gray-500">
          <span>Showing 1 to 10 of 12 results</span>
          <div className="flex items-center gap-3">
            <span>Per page</span>
            <select className="border rounded px-2 py-1">
              <option>10</option>
            </select>
            <div className="flex gap-1">
              <button className="px-3 py-1 border rounded text-indigo-600">
                1
              </button>
              <button className="px-3 py-1 border rounded">2</button>
              <button className="px-3 py-1 border rounded">›</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
