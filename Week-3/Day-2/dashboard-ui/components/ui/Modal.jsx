export default function Modal({ open, onClose, title, children }) {
  if (!open) return null;

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div className="bg-white rounded shadow-lg w-96 p-6">

        <h2 className="text-lg font-semibold mb-4">
          {title}
        </h2>

        <div className="text-sm text-gray-600 mb-6">
          {children}
        </div>

        <button
          onClick={onClose}
          className="text-sm text-blue-600 hover:underline"
        >
          Close
        </button>

      </div>
    </div>
  );
}