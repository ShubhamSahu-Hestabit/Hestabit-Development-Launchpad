'use client' // Required for onClick events in Next.js

export default function Button({
  children,
  variant = "primary",
  onClick
}) {
  const variants = {
    primary: "bg-blue-600 text-white hover:bg-blue-700",
    secondary: "bg-gray-200 text-gray-800 hover:bg-gray-300",
    danger: "bg-red-600 text-white hover:bg-red-700",
  };

  return (
    <button
      onClick={onClick}
      className={`px-4 py-2 rounded text-sm font-medium transition ${variants[variant]}`}
    >
      {children}
    </button>
  );
}