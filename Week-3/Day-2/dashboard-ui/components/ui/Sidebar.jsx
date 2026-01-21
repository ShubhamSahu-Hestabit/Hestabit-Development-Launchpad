"use client";

import { useState } from "react";

export default function Sidebar() {
  const [active, setActive] = useState("Dashboard");

  const items = [
    { name: "Dashboard", icon: "📊" },
    { name: "Pages", icon: "📄" },
    { name: "Charts", icon: "📈" },
    { name: "Tables", icon: "📋" },
  ];

  return (
    <aside className="w-64 bg-gray-800 border-r border-gray-700 min-h-screen p-4">
      <nav className="space-y-1">
        {items.map((item) => (
          <div
            key={item.name}
            onClick={() => setActive(item.name)}
            className={`px-4 py-3 rounded cursor-pointer transition flex items-center gap-3 ${
              active === item.name
                ? "bg-blue-600 text-white"
                : "text-gray-300 hover:bg-gray-700 hover:text-white"
            }`}
          >
            <span className="text-lg">{item.icon}</span>
            <span className="font-medium">{item.name}</span>
          </div>
        ))}
      </nav>
    </aside>
  );
}