"use client";

import Card from "../components/ui/Card";
import Badge from "../components/ui/Badge";
import Button from "../components/ui/Button";
import Modal from "../components/ui/Modal";
import { useState } from "react";

export default function Page() {
  const [open, setOpen] = useState(false);
  const [selectedCard, setSelectedCard] = useState(null);

  const handleCardClick = (cardName) => {
    setSelectedCard(cardName);
    setOpen(true);
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-semibold text-gray-800">
          Dashboard
        </h1>
        <Badge label="Live" variant="success" />
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <div onClick={() => handleCardClick("Monthly Revenue")}>
          <Card title="Monthly Revenue" variant="primary" footer="View Details">
            <div className="text-3xl font-bold mt-2">$40,000</div>
            <div className="text-sm mt-1 opacity-75">↑ 12% from last month</div>
          </Card>
        </div>

        <div onClick={() => handleCardClick("Active Users")}>
          <Card title="Active Users" variant="warning" footer="View Details">
            <div className="text-3xl font-bold mt-2">2,356</div>
            <div className="text-sm mt-1 opacity-75">↑ 8% from last month</div>
          </Card>
        </div>

        <div onClick={() => handleCardClick("Conversion Rate")}>
          <Card title="Conversion Rate" variant="success" footer="View Details">
            <div className="text-3xl font-bold mt-2">3.24%</div>
            <div className="text-sm mt-1 opacity-75">↑ 5% from last month</div>
          </Card>
        </div>

        <div onClick={() => handleCardClick("Bounce Rate")}>
          <Card title="Bounce Rate" variant="danger" footer="View Details">
            <div className="text-3xl font-bold mt-2">42.3%</div>
            <div className="text-sm mt-1 opacity-75">↓ 3% from last month</div>
          </Card>
        </div>
      </div>

      {/* Actions Section */}
      <div className="bg-white p-6 rounded-lg shadow-sm">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">Quick Actions</h2>
        
        <div className="flex flex-wrap gap-3">
          <Button variant="primary" onClick={() => setOpen(true)}>
            📊 Generate Report
          </Button>
          <Button variant="secondary">
            📥 Export Data
          </Button>
          <Button variant="secondary">
            ⚙️ Settings
          </Button>
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
              : "Your analytics report is being generated..."
            }
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
    </div>
  );
}