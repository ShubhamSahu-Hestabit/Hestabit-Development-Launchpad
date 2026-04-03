'use client'

import { useState } from "react"
import Card from '@/components/Card'
import Badge from '@/components/Badge'
import Button from "@/components/Button"
import Modal from "@/components/modal"
import { AreaChartComponent, BarChartComponent } from '@/components/Chart'

export default function DashboardPage() {
  const [open, setOpen] = useState(false)
  const [selectedCard, setSelectedCard] = useState(null)

  return (
    <div className="w-full max-w-full">
      {/* Page Title */}
      <h1 className="text-3xl font-bold text-gray-900 mb-2">Dashboard</h1>

      {/* Breadcrumb */}
      <div className="bg-gray-200 px-3 py-2 rounded mb-6 text-sm text-gray-600">
        Welcome to Hesta Analytics!
      </div>

      {/* Cards Row */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(4, 1fr)',
          gap: '1.5rem',
          marginBottom: '1.5rem'
        }}
      >
        <Card title="Primary Card" color="primary" />
        <Card title="Warning Card" color="warning" />
        <Card title="Success Card" color="success" />
        <Card title="Danger Card" color="danger" />
      </div>

      {/* Actions */}
      <div className="bg-white p-6 rounded-lg shadow-sm mb-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">
          Quick Actions
        </h2>

        <div className="flex flex-wrap gap-3">
          <Button
            variant="primary"
            onClick={() => {
              setSelectedCard(null)
              setOpen(true)
            }}
          >
            📊 Generate Report
          </Button>

          <Button variant="secondary">📥 Export Data</Button>
          <Button variant="secondary">⚙️ Settings</Button>
        </div>

        <div className="mt-6 flex items-center gap-3">
          <span className="text-sm text-gray-600">Status:</span>
          <Badge label="All Systems Operational" variant="success" />
          <Badge label="3 Alerts" variant="warning" />
        </div>
      </div>

      {/* Modal */}
      <Modal
        open={open}
        onClose={() => setOpen(false)}
        title={selectedCard || "Analytics Report"}
      >
        <div className="space-y-4">
          <p className="text-gray-600">
            {selectedCard
              ? `Detailed analytics for ${selectedCard} will appear here.`
              : "Your analytics report is being generated..."}
          </p>

          <div className="bg-gray-50 p-4 rounded">
            <div className="text-sm text-gray-600 space-y-2">
              <div className="flex justify-between">
                <span>Period:</span>
                <span className="font-semibold">Last 30 days</span>
              </div>
              <div className="flex justify-between">
                <span>Data Points:</span>
                <span className="font-semibold">1,234</span>
              </div>
              <div className="flex justify-between">
                <span>Last Updated:</span>
                <span className="font-semibold">2 mins ago</span>
              </div>
            </div>
          </div>

          <Button variant="primary" onClick={() => setOpen(false)}>
            Download PDF Report
          </Button>
        </div>
      </Modal>

      {/* Charts */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(2, 1fr)',
          gap: '1.5rem',
          marginBottom: '1.5rem'
        }}
      >
        <AreaChartComponent />
        <BarChartComponent />
      </div>

      {/* Datatable */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
            <span>📋</span> Datatable Example
          </h3>
        </div>

        <div className="p-6">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-4">
            <div className="flex items-center gap-2">
              <span className="text-sm text-gray-700">Show</span>
              <select className="border border-gray-300 rounded px-2 py-1 text-sm bg-white">
                <option>10</option>
                <option>25</option>
                <option>50</option>
              </select>
              <span className="text-sm text-gray-700">entries</span>
            </div>

            <div className="flex items-center gap-2">
              <label className="text-sm text-gray-700">Search:</label>
              <input
                type="text"
                className="border border-gray-300 rounded px-3 py-1 text-sm w-48"
              />
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full border-collapse">
              <thead>
                <tr className="border-t border-b border-gray-300">
                  <th className="px-4 py-3 text-left text-sm font-semibold">Name</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold">Position</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold">Office</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold">Age</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold">Start Date</th>
                  <th className="px-4 py-3 text-left text-sm font-semibold">Salary</th>
                </tr>
              </thead>

              <tbody>
                {[
                  { name: 'Tiger Nixon', position: 'System Architect', office: 'Edinburgh', age: 61, date: '2011/04/25', salary: '$320,800' },
                  { name: 'Garrett Winters', position: 'Accountant', office: 'Tokyo', age: 63, date: '2011/07/25', salary: '$170,750' },
                  { name: 'Ashton Cox', position: 'Junior Technical Author', office: 'San Francisco', age: 66, date: '2009/01/12', salary: '$86,000' },
                  { name: 'Cedric Kelly', position: 'Senior Javascript Developer', office: 'Edinburgh', age: 22, date: '2012/03/29', salary: '$433,060' },
                  { name: 'Airi Satou', position: 'Accountant', office: 'Tokyo', age: 33, date: '2008/11/28', salary: '$162,700' },
                  { name: 'Brielle Williamson', position: 'Integration Specialist', office: 'New York', age: 61, date: '2012/12/02', salary: '$372,000' },
                  { name: 'Herrod Chandler', position: 'Sales Assistant', office: 'San Francisco', age: 59, date: '2012/08/06', salary: '$137,500' },
                  { name: 'Rhona Davidson', position: 'Integration Specialist', office: 'Tokyo', age: 55, date: '2010/10/14', salary: '$327,900' },
                  { name: 'Colleen Hurst', position: 'Javascript Developer', office: 'San Francisco', age: 39, date: '2009/09/15', salary: '$205,500' },
                  { name: 'Sonya Frost', position: 'Software Engineer', office: 'Edinburgh', age: 23, date: '2008/12/13', salary: '$103,600' }
                ].map((row, i) => (
                  <tr key={i} className="border-b hover:bg-gray-50">
                    <td className="px-4 py-3 text-sm">{row.name}</td>
                    <td className="px-4 py-3 text-sm">{row.position}</td>
                    <td className="px-4 py-3 text-sm">{row.office}</td>
                    <td className="px-4 py-3 text-sm">{row.age}</td>
                    <td className="px-4 py-3 text-sm">{row.date}</td>
                    <td className="px-4 py-3 text-sm">{row.salary}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          <div className="flex flex-col md:flex-row justify-between items-center mt-4 gap-4">
            <div className="text-sm text-gray-700">
              Showing 1 to 10 of 57 entries
            </div>

            <div className="flex gap-1 flex-wrap">
              <button className="px-3 py-1.5 border rounded text-sm text-gray-500" disabled>
                Previous
              </button>
              <button className="px-3 py-1.5 bg-blue-500 text-white rounded text-sm">1</button>
              {[2,3,4,5,6].map(n => (
                <button
                  key={n}
                  className="px-3 py-1.5 border rounded text-sm text-blue-500 hover:bg-gray-50"
                >
                  {n}
                </button>
              ))}
              <button className="px-3 py-1.5 border rounded text-sm text-blue-500">
                Next
              </button>
            </div>
          </div>

        </div>
      </div>
    </div>
  )
}