<script lang="ts">
  import { onMount } from 'svelte';
  import { fetchLogs, type StoredLog } from '../lib/api';
  
  export let apiKey: string;
  export let group: string | undefined = undefined;
  
  let logs: StoredLog[] = [];
  let loading = true;
  let error = '';
  let autoRefresh = true;
  let refreshInterval: number;
  
  async function loadLogs() {
    try {
      loading = true;
      error = '';
      logs = await fetchLogs(apiKey, { group, limit: 100 });
    } catch (e) {
      error = e instanceof Error ? e.message : 'Failed to load logs';
    } finally {
      loading = false;
    }
  }
  
  // Reload when group changes
  $: if (group !== undefined) {
    loadLogs();
  }
  
  onMount(() => {
    loadLogs();
    
    // Auto-refresh every 5 seconds
    if (autoRefresh) {
      refreshInterval = setInterval(loadLogs, 5000);
    }
    
    return () => {
      if (refreshInterval) clearInterval(refreshInterval);
    };
  });
  
  function getLevelColor(level: string): string {
    const colors: Record<string, string> = {
      debug: 'bg-gray-100 text-gray-800',
      info: 'bg-blue-100 text-blue-800',
      warning: 'bg-yellow-100 text-yellow-800',
      error: 'bg-red-100 text-red-800',
      critical: 'bg-purple-100 text-purple-800'
    };
    return colors[level] || 'bg-gray-100 text-gray-800';
  }
  
  function formatTime(timestamp: string): string {
    return new Date(timestamp).toLocaleString();
  }
</script>

<div class="bg-white rounded-lg shadow-md">
  <!-- Header -->
  <div class="border-b border-gray-200 px-6 py-4 flex justify-between items-center">
    <h2 class="text-xl font-semibold">Recent Logs</h2>
    <div class="flex gap-2 items-center">
      <label class="flex items-center gap-2 text-sm text-gray-600">
        <input type="checkbox" bind:checked={autoRefresh} class="rounded" />
        Auto-refresh
      </label>
      <button
        on:click={loadLogs}
        class="px-3 py-1 bg-gray-100 hover:bg-gray-200 rounded text-sm"
        disabled={loading}
      >
        {loading ? 'Loading...' : 'Refresh'}
      </button>
    </div>
  </div>

  <!-- Error -->
  {#if error}
    <div class="px-6 py-4 bg-red-50 border-l-4 border-red-500">
      <p class="text-red-800">{error}</p>
    </div>
  {/if}

  <!-- Logs -->
  <div class="overflow-auto max-h-[calc(100vh-300px)]">
    {#if loading && logs.length === 0}
      <div class="px-6 py-12 text-center text-gray-500">
        Loading logs...
      </div>
    {:else if logs.length === 0}
      <div class="px-6 py-12 text-center text-gray-500">
        No logs found. Start sending logs to see them here!
      </div>
    {:else}
      {#each logs as log (log.id)}
        <div class="border-b border-gray-100 px-6 py-4 hover:bg-gray-50 transition">
          <div class="flex items-start justify-between gap-4">
            <div class="flex-1 min-w-0">
              <!-- Level & Message -->
              <div class="flex items-center gap-2 mb-1">
                <span class="px-2 py-0.5 rounded text-xs font-medium {getLevelColor(log.level)}">
                  {log.level.toUpperCase()}
                </span>
                {#if log.group}
                  <span class="text-xs text-gray-500 font-mono bg-gray-100 px-2 py-0.5 rounded">
                    {log.group}
                  </span>
                {/if}
              </div>
              
              <p class="text-gray-900 font-medium mb-1">{log.message}</p>
              
              <!-- Tags -->
              {#if log.tags && log.tags.length > 0}
                <div class="flex flex-wrap gap-1 mb-2">
                  {#each log.tags as tag}
                    <span class="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded">
                      #{tag}
                    </span>
                  {/each}
                </div>
              {/if}
              
              <!-- Data -->
              {#if log.data}
                <details class="text-sm">
                  <summary class="cursor-pointer text-gray-600 hover:text-gray-900">
                    Data
                  </summary>
                  <pre class="mt-2 p-2 bg-gray-50 rounded text-xs overflow-auto">{JSON.stringify(log.data, null, 2)}</pre>
                </details>
              {/if}
            </div>
            
            <!-- Timestamp & Source -->
            <div class="text-right flex-shrink-0">
              <p class="text-xs text-gray-500">{formatTime(log.timestamp)}</p>
              {#if log.source}
                <p class="text-xs text-gray-400 font-mono">{log.source}</p>
              {/if}
            </div>
          </div>
        </div>
      {/each}
    {/if}
  </div>
  
  <!-- Footer -->
  <div class="border-t border-gray-200 px-6 py-3 bg-gray-50">
    <p class="text-sm text-gray-600">
      Showing {logs.length} logs
    </p>
  </div>
</div>

