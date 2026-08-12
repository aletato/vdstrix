import { useState, useEffect } from "react";
import { Play, Square, RefreshCw, Loader2 } from "lucide-react";

interface Scan {
  id: string;
  target: string;
  mode: string;
  status: "running" | "finished";
  pid: number;
  exit_code?: number | null;
}

interface ScanManagerProps {
  onScanSelected?: (scanId: string) => void;
}

export default function ScanManager({ onScanSelected }: ScanManagerProps) {
  const [scans, setScans] = useState<Scan[]>([]);
  const [newTarget, setNewTarget] = useState("");
  const [newMode, setNewMode] = useState("standard");
  const [isStarting, setIsStarting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchScans = async () => {
    try {
      const response = await fetch("/api/scans/list", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      });
      const data = await response.json();
      if (data.scans) {
        setScans(data.scans);
      }
    } catch (err) {
      console.error("Failed to fetch scans:", err);
    }
  };

  const startScan = async () => {
    if (!newTarget.trim()) {
      setError("Target is required");
      return;
    }

    setIsStarting(true);
    setError(null);

    try {
      const response = await fetch("/api/scans/start", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          target: newTarget.trim(),
          mode: newMode,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed to start scan");
      }

      setNewTarget("");
      setNewMode("standard");
      await fetchScans();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to start scan");
    } finally {
      setIsStarting(false);
    }
  };

  const stopScan = async (scanId: string) => {
    try {
      await fetch("/api/scans/stop", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ scan_id: scanId }),
      });
      await fetchScans();
    } catch (err) {
      console.error("Failed to stop scan:", err);
    }
  };

  useEffect(() => {
    fetchScans();
    const interval = setInterval(fetchScans, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-6">
      <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
        <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <Play className="w-5 h-5" />
          Start New Scan
        </h2>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Target</label>
            <input
              type="text"
              value={newTarget}
              onChange={(e) => setNewTarget(e.target.value)}
              placeholder="example.com or https://example.com"
              className="w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-blue-500"
              disabled={isStarting}
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Scan Mode</label>
            <select
              value={newMode}
              onChange={(e) => setNewMode(e.target.value)}
              className="w-full px-3 py-2 border rounded-md focus:ring-2 focus:ring-blue-500"
              disabled={isStarting}
            >
              <option value="standard">Standard</option>
              <option value="deep">Deep</option>
              <option value="quick">Quick</option>
            </select>
          </div>

          {error && (
            <div className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-md p-3">
              {error}
            </div>
          )}

          <button
            onClick={startScan}
            disabled={isStarting || !newTarget.trim()}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-medium py-2 px-4 rounded-md flex items-center justify-center gap-2"
          >
            {isStarting ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                Starting...
              </>
            ) : (
              <>
                <Play className="w-4 h-4" />
                Start Scan
              </>
            )}
          </button>
        </div>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold flex items-center gap-2">
            <RefreshCw className="w-5 h-5" />
            Active Scans ({scans.length})
          </h2>
          <button
            onClick={fetchScans}
            className="text-sm text-gray-600 hover:text-gray-900"
          >
            Refresh
          </button>
        </div>

        {scans.length === 0 ? (
          <p className="text-gray-500 text-center py-8">No active scans</p>
        ) : (
          <div className="space-y-3">
            {scans.map((scan) => (
              <div
                key={scan.id}
                className="border rounded-lg p-4 hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3">
                      <h3 className="font-medium">{scan.target}</h3>
                      <span className={`px-2 py-1 text-xs rounded-full ${
                        scan.status === "running"
                          ? "bg-green-100 text-green-700"
                          : "bg-gray-100 text-gray-700"
                      }`}>
                        {scan.status}
                      </span>
                      <span className="text-xs text-gray-500">{scan.mode}</span>
                    </div>
                    <p className="text-sm text-gray-500 mt-1">
                      PID: {scan.pid}
                      {scan.exit_code !== undefined && scan.exit_code !== null && (
                        <span className="ml-2">Exit: {scan.exit_code}</span>
                      )}
                    </p>
                  </div>

                  {scan.status === "running" && (
                    <button
                      onClick={() => stopScan(scan.id)}
                      className="p-2 text-red-600 hover:bg-red-50 rounded-md"
                      title="Stop scan"
                    >
                      <Square className="w-4 h-4" />
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
