import {
  AlertCircle,
  CheckCircle2,
  Circle,
  Command,
  Loader2,
  Search,
  Sparkles,
  Terminal,
  X,
} from "lucide-react";
import { useState } from "react";
import {
  executeAllSteps,
  executeCommand,
  type ExecuteCommandResponse,
} from "../utils/api";

interface Step {
  id: number;
  description: string;
  command: string;
  risk: "safe" | "moderate" | "dangerous";
  status?: "pending" | "running" | "completed" | "failed";
  output?: string;
  error?: string;
}

export function Spotlight() {
  const [input, setInput] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);
  const [isExecuting, setIsExecuting] = useState(false);
  const [executionPlan, setExecutionPlan] =
    useState<ExecuteCommandResponse | null>(null);
  const [steps, setSteps] = useState<Step[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [expandedSteps, setExpandedSteps] = useState<Set<number>>(new Set());

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    setIsProcessing(true);
    setError(null);

    try {
      const response = await executeCommand({
        command: input,
        context: {
          os: navigator.platform,
          current_dir: "~",
        },
      });

      setExecutionPlan(response);
      setSteps(response.steps);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "failed to connect to backend"
      );
      console.error("execution error:", err);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleConfirm = async () => {
    if (!executionPlan) return;

    setIsExecuting(true);
    setError(null);

    // set all steps to running
    setSteps((prev) => prev.map((s) => ({ ...s, status: "running" as const })));

    try {
      const response = await executeAllSteps({
        task_id: executionPlan.task_id,
        steps: steps.map((s) => ({
          id: s.id,
          command: s.command,
          description: s.description,
        })),
      });

      // update steps with results
      setSteps((prev) =>
        prev.map((step) => {
          const result = response.results.find((r) => r.step_id === step.id);
          if (result) {
            return {
              ...step,
              status: result.status,
              output: result.output,
              error: result.error || undefined,
            };
          }
          return step;
        })
      );

      console.log("execution results:", response);
    } catch (err) {
      setError(err instanceof Error ? err.message : "execution failed");
      console.error("execution error:", err);
      // mark all running steps as failed
      setSteps((prev) =>
        prev.map((s) =>
          s.status === "running" ? { ...s, status: "failed" as const } : s
        )
      );
    } finally {
      setIsExecuting(false);
    }
  };

  const handleCancel = () => {
    setExecutionPlan(null);
    setSteps([]);
    setInput("");
    setError(null);
    setExpandedSteps(new Set());
  };

  const toggleStepExpanded = (stepId: number) => {
    setExpandedSteps((prev) => {
      const next = new Set(prev);
      if (next.has(stepId)) {
        next.delete(stepId);
      } else {
        next.add(stepId);
      }
      return next;
    });
  };

  const getRiskColor = (risk: string) => {
    switch (risk) {
      case "safe":
        return "text-emerald-400 border-emerald-500/30 bg-emerald-500/10";
      case "moderate":
        return "text-amber-400 border-amber-500/30 bg-amber-500/10";
      case "dangerous":
        return "text-red-400 border-red-500/30 bg-red-500/10";
      default:
        return "text-slate-400 border-slate-500/30 bg-slate-500/10";
    }
  };

  const getStatusIcon = (status?: string) => {
    switch (status) {
      case "completed":
        return <CheckCircle2 className="w-5 h-5 text-emerald-400" />;
      case "running":
        return <Loader2 className="w-5 h-5 text-primary-400 animate-spin" />;
      case "failed":
        return <AlertCircle className="w-5 h-5 text-red-400" />;
      default:
        return <Circle className="w-5 h-5 text-slate-600" />;
    }
  };

  return (
    <div className="fixed inset-0 bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
      {/* grid background */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#1e293b_1px,transparent_1px),linear-gradient(to_bottom,#1e293b_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_80%_50%_at_50%_0%,#000,transparent)]" />

      {/* glow effect */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[600px] h-[600px] bg-primary-500/20 rounded-full blur-[120px] pointer-events-none" />

      {/* content */}
      <div className="relative flex flex-col items-center justify-start pt-24 px-4 h-full overflow-y-auto">
        {/* logo and title */}
        <div className="mb-8 text-center">
          <div className="inline-flex items-center gap-3 mb-2">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-500 to-violet-600 flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <h1 className="text-2xl font-semibold bg-gradient-to-r from-slate-100 to-slate-400 bg-clip-text text-transparent">
              luna
            </h1>
          </div>
          <p className="text-sm text-slate-500">your local development agent</p>
        </div>

        {/* search input */}
        {!executionPlan && (
          <form onSubmit={handleSubmit} className="w-full max-w-2xl">
            <div className="relative group">
              <div className="absolute left-5 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-primary-500 transition-colors">
                <Search className="w-5 h-5" />
              </div>

              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="install chrome, setup python, check docker status..."
                disabled={isProcessing}
                className="w-full pl-14 pr-14 py-5 text-base bg-slate-800/50 backdrop-blur-xl text-slate-100 rounded-2xl border border-slate-700/50 focus:border-primary-500/50 focus:outline-none focus:ring-2 focus:ring-primary-500/20 placeholder:text-slate-500 shadow-2xl shadow-black/20 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                autoFocus
              />

              <div className="absolute right-5 top-1/2 -translate-y-1/2 flex items-center gap-1.5 text-slate-500 text-xs">
                <Command className="w-3 h-3" />
                <span>⏎</span>
              </div>
            </div>
          </form>
        )}

        {/* error state */}
        {error && (
          <div className="mt-6 w-full max-w-2xl p-4 bg-red-500/10 border border-red-500/30 rounded-xl">
            <div className="flex items-start gap-3">
              <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
              <div className="flex-1">
                <p className="text-sm text-red-400 font-medium">
                  connection error
                </p>
                <p className="text-xs text-red-300/70 mt-1">{error}</p>
                <p className="text-xs text-slate-500 mt-2">
                  make sure backend is running on localhost:8000
                </p>
              </div>
              <button
                onClick={() => setError(null)}
                className="text-red-400 hover:text-red-300"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          </div>
        )}

        {/* suggestions */}
        {!input && !executionPlan && (
          <div className="mt-6 w-full max-w-2xl">
            <p className="text-xs text-slate-500 mb-3 px-1">try these:</p>
            <div className="grid grid-cols-2 gap-2">
              {[
                "install chrome",
                "install vscode",
                "check docker status",
                "which brew",
              ].map((suggestion) => (
                <button
                  key={suggestion}
                  onClick={() => setInput(suggestion)}
                  className="px-4 py-3 text-sm text-left text-slate-400 bg-slate-800/30 hover:bg-slate-800/50 border border-slate-700/30 hover:border-slate-600/50 rounded-xl transition-all hover:text-slate-300"
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* processing state */}
        {isProcessing && (
          <div className="mt-6 w-full max-w-2xl">
            <div className="p-5 bg-slate-800/30 backdrop-blur-xl rounded-2xl border border-slate-700/30">
              <div className="flex items-center gap-3">
                <Loader2 className="w-5 h-5 text-primary-500 animate-spin" />
                <div>
                  <p className="text-sm text-slate-300">analyzing command...</p>
                  <p className="text-xs text-slate-500 mt-1">{input}</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* execution plan */}
        {executionPlan && !isProcessing && (
          <div className="mt-6 w-full max-w-2xl space-y-4 pb-24">
            {/* header */}
            <div className="p-5 bg-slate-800/30 backdrop-blur-xl rounded-2xl border border-slate-700/30">
              <div className="flex items-start justify-between mb-3">
                <div>
                  <p className="text-sm text-slate-400">execution plan</p>
                  <p className="text-slate-200 font-medium mt-1">{input}</p>
                </div>
                <span className="px-2 py-1 text-xs bg-primary-500/20 text-primary-300 border border-primary-500/30 rounded-lg">
                  {executionPlan.estimated_time}
                </span>
              </div>

              {executionPlan.requires_confirmation && (
                <div className="flex items-center gap-2 text-xs text-amber-400 bg-amber-500/10 border border-amber-500/20 rounded-lg px-3 py-2">
                  <AlertCircle className="w-4 h-4" />
                  <span>requires confirmation before execution</span>
                </div>
              )}
            </div>

            {/* steps */}
            <div className="space-y-2">
              {steps.map((step) => (
                <div
                  key={step.id}
                  className="bg-slate-800/30 backdrop-blur-xl rounded-xl border border-slate-700/30 overflow-hidden"
                >
                  <div className="p-4">
                    <div className="flex items-start gap-3">
                      <div className="mt-0.5">{getStatusIcon(step.status)}</div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-start justify-between gap-3">
                          <p className="text-sm text-slate-300">
                            {step.description}
                          </p>
                          <span
                            className={`px-2 py-0.5 text-xs border rounded ${getRiskColor(
                              step.risk
                            )} flex-shrink-0`}
                          >
                            {step.risk}
                          </span>
                        </div>
                        <button
                          onClick={() => toggleStepExpanded(step.id)}
                          className="text-xs text-slate-500 mt-2 font-mono hover:text-slate-400 transition-colors flex items-center gap-2"
                        >
                          <Terminal className="w-3 h-3" />
                          <span>$ {step.command}</span>
                        </button>
                      </div>
                    </div>
                  </div>

                  {/* output section */}
                  {expandedSteps.has(step.id) &&
                    (step.output || step.error) && (
                      <div className="px-4 pb-4">
                        <div className="p-3 bg-slate-900/50 rounded-lg border border-slate-700/30">
                          {step.output && (
                            <div className="mb-2">
                              <p className="text-xs text-slate-500 mb-1">
                                output:
                              </p>
                              <pre className="text-xs text-slate-300 font-mono whitespace-pre-wrap">
                                {step.output}
                              </pre>
                            </div>
                          )}
                          {step.error && (
                            <div>
                              <p className="text-xs text-red-400 mb-1">
                                error:
                              </p>
                              <pre className="text-xs text-red-300 font-mono whitespace-pre-wrap">
                                {step.error}
                              </pre>
                            </div>
                          )}
                        </div>
                      </div>
                    )}
                </div>
              ))}
            </div>

            {/* action buttons */}
            <div className="flex items-center gap-3">
              {!isExecuting && steps.every((s) => s.status !== "completed") && (
                <button
                  onClick={handleConfirm}
                  disabled={isExecuting}
                  className="flex-1 px-6 py-3 bg-primary-500 hover:bg-primary-600 text-white rounded-xl font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  execute {steps.length} step{steps.length > 1 ? "s" : ""}
                </button>
              )}
              {(isExecuting ||
                steps.some(
                  (s) => s.status === "completed" || s.status === "failed"
                )) && (
                <button
                  onClick={handleCancel}
                  className="flex-1 px-6 py-3 bg-slate-800/50 hover:bg-slate-800 text-slate-300 rounded-xl font-medium transition-colors border border-slate-700/50"
                >
                  {isExecuting ? "executing..." : "done"}
                </button>
              )}
            </div>
          </div>
        )}

        {/* shortcuts hint */}
        {!executionPlan && (
          <div className="absolute bottom-8 left-1/2 -translate-x-1/2 flex items-center gap-6 text-xs text-slate-600">
            <div className="flex items-center gap-2">
              <kbd className="px-2 py-1 bg-slate-800/50 border border-slate-700/50 rounded text-slate-500">
                esc
              </kbd>
              <span>clear</span>
            </div>
            <div className="flex items-center gap-2">
              <kbd className="px-2 py-1 bg-slate-800/50 border border-slate-700/50 rounded text-slate-500">
                ⌘K
              </kbd>
              <span>open</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
