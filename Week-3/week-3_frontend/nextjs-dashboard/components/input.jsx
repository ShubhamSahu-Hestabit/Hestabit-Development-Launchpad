export default function Input({ placeholder }) {
  return (
    <input
      placeholder={placeholder}
      className="border border-gray-300 px-3 py-2 rounded text-sm w-full focus:outline-none focus:ring-2 focus:ring-blue-500"
    />
  );
}
