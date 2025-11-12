/**
 * Komfyrvakt API Client
 */

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8080/api';

export interface StoredLog {
  id: string;
  message: string;
  level: 'debug' | 'info' | 'warning' | 'error' | 'critical';
  group?: string;
  tags: string[];
  data?: Record<string, any>;
  timestamp: string;
  source?: string;
}

export interface LogQuery {
  group?: string;
  tags?: string[];
  level?: string;
  since?: string;
  until?: string;
  source?: string;
  limit?: number;
}

export interface Stats {
  total_logs: number;
  storage: string;
  retention_hours: number;
}

async function apiRequest<T>(
  endpoint: string,
  apiKey: string,
  options: RequestInit = {}
): Promise<T> {
  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Request failed' }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  return response.json();
}

export async function fetchLogs(
  apiKey: string,
  query: LogQuery = {}
): Promise<StoredLog[]> {
  const params = new URLSearchParams();
  
  if (query.group) params.set('group', query.group);
  if (query.tags) params.set('tags', query.tags.join(','));
  if (query.level) params.set('level', query.level);
  if (query.since) params.set('since', query.since);
  if (query.until) params.set('until', query.until);
  if (query.source) params.set('source', query.source);
  if (query.limit) params.set('limit', query.limit.toString());

  const queryString = params.toString();
  const endpoint = `/logs${queryString ? `?${queryString}` : ''}`;

  return apiRequest<StoredLog[]>(endpoint, apiKey);
}

export async function fetchStats(apiKey: string): Promise<Stats> {
  const response = await apiRequest<{ status: string; stats: Stats }>(
    '/stats',
    apiKey
  );
  return response.stats;
}

export async function postLog(
  apiKey: string,
  log: Omit<StoredLog, 'id' | 'timestamp'>
): Promise<StoredLog> {
  return apiRequest<StoredLog>('/logs', apiKey, {
    method: 'POST',
    body: JSON.stringify(log),
  });
}

export async function purgeLog(
  apiKey: string,
  group?: string
): Promise<{ purged: number }> {
  const endpoint = group ? `/purge?group=${group}` : '/purge';
  const response = await apiRequest<{ status: string; result: any }>(
    endpoint,
    apiKey,
    { method: 'DELETE' }
  );
  return response.result;
}

