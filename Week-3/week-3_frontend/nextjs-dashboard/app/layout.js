// app/layout.js
import { Inter } from 'next/font/google' // or 'Nunito'
import './globals.css'

const inter = Inter({ 
  subsets: ['latin'],
  variable: '--font-inter', // This creates a CSS variable
})

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={inter.variable}> {/* Apply the variable here */}
      <body className={inter.className}>
        {children}
      </body>
    </html>
  )
}