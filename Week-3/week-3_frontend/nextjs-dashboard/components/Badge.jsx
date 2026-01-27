export default function Badge({ label, variant = "default" }) {
  const styles = {
    success: { backgroundColor: '#d1fae5', color: '#065f46' },
    warning: { backgroundColor: '#fef3c7', color: '#92400e' },
    danger: { backgroundColor: '#fee2e2', color: '#991b1b' },
    default: { backgroundColor: '#e5e7eb', color: '#374151' },
  };

  return (
    <span 
      style={{
        padding: '0.25rem 0.5rem',
        fontSize: '0.75rem',
        borderRadius: '0.25rem',
        ...styles[variant]
      }}
    >
      {label}
    </span>
  );
}