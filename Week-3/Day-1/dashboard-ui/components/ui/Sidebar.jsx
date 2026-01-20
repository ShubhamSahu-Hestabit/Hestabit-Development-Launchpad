export default function Sidebar() {
  return (
    <aside className="w-64 bg-slate-900 text-slate-200 min-h-screen px-4 py-6">
      
      <div className="text-xs text-slate-400 mb-4">CORE</div>
      <ul className="space-y-2 mb-6">
        <li className="hover:bg-slate-800 px-3 py-2 rounded cursor-pointer">
          Dashboard
        </li>
      </ul>

      <div className="text-xs text-slate-400 mb-4">INTERFACE</div>
      <ul className="space-y-2 mb-6">
        <li className="hover:bg-slate-800 px-3 py-2 rounded cursor-pointer">
          Layouts
        </li>
        <li className="hover:bg-slate-800 px-3 py-2 rounded cursor-pointer">
          Pages
        </li>
      </ul>

      <div className="text-xs text-slate-400 mb-4">ADDONS</div>
      <ul className="space-y-2">
        <li className="hover:bg-slate-800 px-3 py-2 rounded cursor-pointer">
          Charts
        </li>
        <li className="hover:bg-slate-800 px-3 py-2 rounded cursor-pointer">
          Tables
        </li>
      </ul>
    </aside>
  );
}
