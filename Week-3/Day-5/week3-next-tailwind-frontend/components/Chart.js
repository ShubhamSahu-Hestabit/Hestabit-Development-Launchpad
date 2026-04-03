'use client'

import { AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

const areaData = [
  { name: 'Mar 1', value: 10000 },
  { name: 'Mar 3', value: 30000 },
  { name: 'Mar 5', value: 20000 },
  { name: 'Mar 7', value: 32000 },
  { name: 'Mar 9', value: 35000 },
  { name: 'Mar 11', value: 27000 },
  { name: 'Mar 13', value: 40000 },
]

const barData = [
  { name: 'January', value: 4200 },
  { name: 'February', value: 5100 },
  { name: 'March', value: 6000 },
  { name: 'April', value: 8100 },
  { name: 'May', value: 10100 },
  { name: 'June', value: 14500 },
]

export function AreaChartComponent() {
  return (
    <div className="bg-white rounded shadow border border-gray-200">
      <div className="px-6 py-4 border-b border-gray-200">
        <h3 className="text-base font-semibold text-gray-900 flex items-center gap-2">
          <span>📈</span> Area Chart Example
        </h3>
      </div>
      <div className="p-6">
        <ResponsiveContainer width="100%" height={300}>
          <AreaChart data={areaData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
            <defs>
              <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#007bff" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#007bff" stopOpacity={0.05}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
            <XAxis 
              dataKey="name" 
              tick={{ fontSize: 12, fill: '#666' }}
              stroke="#ccc"
            />
            <YAxis 
              tick={{ fontSize: 12, fill: '#666' }}
              stroke="#ccc"
            />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: 'white',
                border: '1px solid #ddd',
                borderRadius: '4px',
                fontSize: '12px'
              }}
            />
            <Area 
              type="monotone" 
              dataKey="value" 
              stroke="#007bff" 
              strokeWidth={2}
              fill="url(#colorValue)" 
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}

export function BarChartComponent() {
  return (
    <div className="bg-white rounded shadow border border-gray-200">
      <div className="px-6 py-4 border-b border-gray-200">
        <h3 className="text-base font-semibold text-gray-900 flex items-center gap-2">
          <span>📊</span> Bar Chart Example
        </h3>
      </div>
      <div className="p-6">
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={barData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
            <XAxis 
              dataKey="name" 
              tick={{ fontSize: 12, fill: '#666' }}
              stroke="#ccc"
            />
            <YAxis 
              tick={{ fontSize: 12, fill: '#666' }}
              stroke="#ccc"
            />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: 'white',
                border: '1px solid #ddd',
                borderRadius: '4px',
                fontSize: '12px'
              }}
            />
            <Bar 
              dataKey="value" 
              fill="#007bff"
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}