const API_BASE_URL = "http://localhost:8000";

export interface ExecuteCommandRequest {
  command: string;
  context?: {
    os?: string;
    current_dir?: string;
    project_type?: string;
  };
}

export interface ExecuteCommandResponse {
  task_id: string;
  steps: Array<{
    id: number;
    description: string;
    command: string;
    risk: "safe" | "moderate" | "dangerous";
    status?: "pending" | "running" | "completed" | "failed";
  }>;
  requires_confirmation: boolean;
  estimated_time?: string;
}

export interface ExecuteAllRequest {
  task_id: string;
  steps: Array<{
    id: number;
    command: string;
    description: string;
  }>;
}

export interface ExecuteAllResponse {
  task_id: string;
  results: Array<{
    step_id: number;
    status: "completed" | "failed";
    output: string;
    error: string | null;
  }>;
  overall_status: "completed" | "failed" | "partial";
}

export async function executeCommand(
  request: ExecuteCommandRequest
): Promise<ExecuteCommandResponse> {
  const response = await fetch(`${API_BASE_URL}/api/execute`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.statusText}`);
  }

  return response.json();
}

export async function executeAllSteps(
  request: ExecuteAllRequest
): Promise<ExecuteAllResponse> {
  const response = await fetch(`${API_BASE_URL}/api/execute/run`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.statusText}`);
  }

  return response.json();
}

export async function healthCheck(): Promise<{ status: string }> {
  const response = await fetch(`${API_BASE_URL}/health`);
  return response.json();
}
