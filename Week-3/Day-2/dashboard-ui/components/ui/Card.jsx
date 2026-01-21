export default function Card({ title, children, footer, variant = "default" }) {
  const variants = {
    default: "bg-white border-gray-200 text-gray-800",
    primary: "bg-blue-500 text-white border-blue-600",
    warning: "bg-yellow-500 text-white border-yellow-600",
    success: "bg-green-500 text-white border-green-600",
    danger: "bg-red-500 text-white border-red-600",
  };

  const footerVariants = {
    default: "border-gray-200 text-blue-600",
    primary: "border-blue-400 text-blue-100",
    warning: "border-yellow-400 text-yellow-100",
    success: "border-green-400 text-green-100",
    danger: "border-red-400 text-red-100",
  };

  return (
    <div className={`${variants[variant]} border rounded shadow-sm p-4`}>
      <h3 className="font-semibold mb-2">
        {title}
      </h3>

      {children && (
        <div className="text-sm opacity-90">
          {children}
        </div>
      )}

      {footer && (
        <div className={`mt-4 pt-3 border-t ${footerVariants[variant]} text-sm cursor-pointer hover:opacity-80 flex items-center justify-between`}>
          <span>{footer}</span>
          <span>→</span>
        </div>
      )}
    </div>
  );
}