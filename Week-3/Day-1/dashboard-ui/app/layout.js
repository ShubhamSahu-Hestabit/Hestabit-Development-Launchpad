import "./globals.css";
import Navbar from "../components/ui/Navbar";
import Sidebar from "../components/ui/Sidebar";

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-white text-gray-900">

        {/* TOP NAVBAR */}
        <Navbar />

        {/* BELOW NAVBAR */}
        <div className="flex min-h-[calc(100vh-64px)]">

          {/* Sidebar */}
          <Sidebar />

          {/* Main Content */}
          <main className="flex-1 bg-gray-100 p-6">
            {children}
          </main>

        </div>
      </body>
    </html>
  );
}
