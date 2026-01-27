export default function Modal({ open, onClose, title, children }) {
  if (!open) return null;

  return (
    <div className="fixed inset-0 flex items-center justify-center z-[9999]" style={{ backgroundColor: 'rgba(0, 0, 0, 0.8)' }}>
      
      <div className="rounded-lg shadow-2xl w-96 p-6" style={{ backgroundColor: '#ffffff' }}>

        <h2 className="text-lg font-semibold mb-4" style={{ color: '#000000' }}>
          {title}
        </h2>

        <div className="rounded-md p-4 mb-6" style={{ backgroundColor: '#e3f2fd', border: '2px solid #2196f3' }}>
          <div className="text-sm" style={{ color: '#000000' }}>
            {children}
          </div>
        </div>

        <div className="flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-md text-sm font-medium"
            style={{ backgroundColor: '#2196f3', color: '#ffffff' }}
          >
            Close
          </button>
        </div>

      </div>
    </div>
  );
}